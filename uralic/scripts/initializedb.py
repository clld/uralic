import csv
import itertools
import collections
import pathlib

from nexus import NexusReader
from markdown import markdown
from pycldf import Sources, Dataset
from clldutils.misc import nfilter
from clldutils.color import qualitative_colors
from clld.cliutil import Data, bibtex2source, add_language_codes
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from csvw.dsv import reader
from clld_phylogeny_plugin.models import Phylogeny, LanguageTreeLabel, TreeLabel

import uralic
# inherited from models.py
from uralic import models

csv.field_size_limit(1000000)


def render_description(s):
    s = markdown(s)
    return s


def get_tree():
    nex = NexusReader(pathlib.Path(uralic.__file__).parent.parent.parent / 'Uralic_MCC.nex')
    nex.trees.detranslate()
    return nex.trees.trees[0]


def get_admixture():
    admix_dic = reader(
        pathlib.Path(uralic.__file__).parent.parent.parent / 'admixture_coef.csv', dicts=True)
    return admix_dic


def main(args):
    geo = Dataset.from_metadata(args.cldf.directory.parent.parent /
                                'rantanenurageo' / 'cldf' / 'Generic-metadata.json')
    langs = {r['id']: r['glottocode'] or r['id']
             for r in geo.iter_rows('LanguageTable', 'id', 'glottocode')}
    areas = {langs[r['languageReference']]: r['SpeakerArea']
             for r in geo.iter_rows('areas.csv', 'languageReference')}
    data = Data()
    data.add(
        common.Dataset,
        uralic.__name__,
        id=uralic.__name__,
        name='UraTyp',
        description="Uralic Areal Typology",
        domain='uralic.clld.org',
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'},

    )

    for row in args.cldf.iter_rows('ContributionTable', 'id', 'name'):
        data.add(
            common.Contribution,
            row['id'],
            id=row['id'],
            name=row['name'],
        )

    for rec in bibtex.Database.from_file(args.cldf.bibpath, lowercase=True):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    n2l, n2v = {}, {}
    for lang in args.cldf.iter_rows(
            'LanguageTable', 'id', 'glottocode', 'name', 'latitude', 'longitude', 'source'):
        n2l[lang['name'].replace(' ', '_').replace('-', '_')] = lang['id']
        lang['glottocode'] = {
            'Hill_Mari': 'kozy1238',
        }.get(lang['name'], lang['glottocode'])
        assert lang['glottocode'] or lang['name'] == 'East_Mansi'
        v = data.add(
            models.Variety,
            lang['id'],
            id=lang['id'],
            name=lang['name'],
            latitude=lang['latitude'],
            longitude=lang['longitude'],
            glottocode=lang['glottocode'],
            # edit the models.py by adding a subfamily
            subfamily=lang['Subfamily'],
            jsondata=dict(feature=areas[lang['glottocode'] or 'EastMansi'])
        )
        n2v[v.name] = v
        if lang['glottocode']:
            add_language_codes(data, v, lang['ISO639P3code'], glottocode=lang['glottocode'])
        DBSession.flush()
        for src in lang['source']:
            DBSession.add(common.LanguageSource(language_pk=v.pk, source_pk=data['Source'][src].pk))

    tree = get_tree().newick_tree
    phylo = Phylogeny(id='p', name='Uralic languages')

    def rename(n):
        if n.name:
            #name = n.name
            #n.name = n2l[name]
            LanguageTreeLabel(
                language=n2v[n.name], treelabel=TreeLabel(id=n.name, name=n.name, phylogeny=phylo))

    tree.visit(rename)
    phylo.newick = tree.newick + ';'
    DBSession.add(phylo)

    refs = collections.defaultdict(list)

    for param in args.cldf.iter_rows('ParameterTable', 'id', 'name', 'contributionReference'):
        description = args.cldf.directory.parent.joinpath('doc', '{}.md'.format(param['id']))
        if description.exists():
            description = description.read_text(encoding='utf8')
        else:
            description = None
        data.add(
            models.Feature,
            param['id'],
            id=param['id'],
            name='{}'.format(param['name']),
            markup_description=render_description(description) if description else None,
            category=param['Area'],
            contribution=data['Contribution'][param['contributionReference']],
    )
    data.add(
        models.Feature,
        'adm',
        id='adm',
        name="Admixture component",
    )
    for ccid, cid, color in [
        ('C1', 'Finnic ancestry', '#e79e3f'),
        ('C2', 'Ob-Ugric ancestry', '#7783c5'),
        ('C3', 'Volgaic ancestry', '#b44094'),
        ('C4', 'Saami ancestry', '#7d9f64'),
    ]:
        data.add(
            common.DomainElement,
            ccid,
            id=ccid,
            name=cid,
            parameter=data['Feature']['adm'],
            jsondata=dict(color=color),
        )
    for pid, codes in itertools.groupby(
            sorted(
                args.cldf.iter_rows('CodeTable', 'id', 'name', 'description', 'parameterReference'),
            key=lambda v: (v['parameterReference'], v['id'])),
        lambda v: v['parameterReference'],
    ):
        codes = list(codes)
        colors = qualitative_colors(len(codes))
        for code, color in zip(codes, colors):
            data.add(
                common.DomainElement,
                code['id'],
                id=code['id'],
                name=code['name'],
                description=code['description'],
                parameter=data['Feature'][code['parameterReference']],
                jsondata=dict(color=color),
            )
        data.add(
            common.DomainElement,
            '{}-?'.format(pid),
            id='{}-NA'.format(pid),
            name='?',
            description='missing value',
            parameter=data['Feature'][pid],
            jsondata=dict(color='#f00'),
        )
    for ex in args.cldf.iter_rows('ExampleTable', 'id', 'languageReference'):
        data.add(
            common.Sentence,
            ex['id'],
            id=ex['id'],
            language=data['Variety'][ex['languageReference']],
            name=ex['Primary_Text'],
            analyzed='\t'.join(ex['Analyzed_Word']),
            original_script='\t'.join(ex['Analyzed_Word_IPA']),
            gloss='\t'.join(ex['Gloss']),
            description=ex['Translated_Text'],
        )
    for val in args.cldf.iter_rows(
            'ValueTable',
            'id', 'value', 'languageReference', 'parameterReference', 'codeReference',
            'exampleReference',
            'source'):
        vsid = (val['languageReference'], val['parameterReference'])
        vs = data['ValueSet'].get(vsid)
        if not vs:
            vs = data.add(
                common.ValueSet,
                vsid,
                id='-'.join(vsid),
                language=data['Variety'][val['languageReference']],
                parameter=data['Feature'][val['parameterReference']],
                contribution=data['Contribution'][val['parameterReference'][:2]],
            )
        for ref in val.get('source', []):
            sid, pages = Sources.parse(ref)
            refs[(vsid, sid)].append(pages)
        v = data.add(
            common.Value,
            val['id'],
            id=val['id'],
            name=val['value'],
            description=val['Comment'],
            valueset=vs,
            domainelement=data['DomainElement'][val['codeReference'] if val['value'] else '{}-?'.format(val['parameterReference'])],
        )
        if val['exampleReference']:
            DBSession.add(common.ValueSentence(value=v, sentence=data['Sentence'][val['exampleReference']]))

    for row in get_admixture():
        lid = n2l[row['lang']]
        vs = data.add(
            common.ValueSet,
            '{}-adm'.format(lid),
            id='{}-adm'.format(lid),
            language=data['Variety'][lid],
            parameter=data['Feature']['adm'],
            contribution=data['Contribution']['UT'],
        )
        for k in ['C1', 'C2', 'C3', 'C4']:#['Finnic ancestry', 'Ob-Ugric ancestry', 'Volgaic ancestry', 'Saami ancestry']:
            v = round(float(row[k]), 3)
            data.add(
                common.Value,
                '{}-{}-{}'.format(lid, 'adm', k),
                id='{}-{}-{}'.format(lid, 'adm', k),
                name=str(v),
                frequency=100 * v,  # admixture proportions
                valueset=vs,
                domainelement=data['DomainElement'][k],
            )

    for (vsid, sid), pages in refs.items():
        DBSession.add(common.ValueSetReference(
            valueset=data['ValueSet'][vsid],
            source=data['Source'][sid],
            description='; '.join(nfilter(pages))
        ))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
