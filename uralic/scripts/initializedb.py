import csv
import itertools
import collections
import pathlib

from markdown import markdown
from pycldf import Sources, Dataset
from clldutils.misc import nfilter
from clldutils.color import qualitative_colors
from clld.cliutil import Data, bibtex2source, add_language_codes
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from csvw.dsv import reader

import uralic
# inherited from models.py
from uralic import models

csv.field_size_limit(1000000)


def render_description(s):
    s = markdown(s)
    return s


def main(args):
    geo = Dataset.from_metadata(args.cldf.directory.parent.parent / 'rantanenurageo' / 'cldf' / 'Generic-metadata.json')
    langs = {r['id']: r['glottocode'] or r['id'] for r in geo.iter_rows('LanguageTable', 'id', 'glottocode')}
    areas = {langs[r['languageReference']]: r['SpeakerArea'] for r in geo.iter_rows('areas.csv', 'languageReference')}
    assert args.glottolog, 'The --glottolog option is required!'
    data = Data()
    data.add(
        common.Dataset,
        uralic.__name__,
        id=uralic.__name__,
        name="Uralic Languages",
        domain='uralic.clld.org',
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'},

    )

    contrib = data.add(
        common.Contribution,
        None,
        id='cldf',
        name=args.cldf.properties.get('dc:title'),
        description=args.cldf.properties.get('dc:bibliographicCitation'),
    )

    n2l = {}
    for lang in args.cldf.iter_rows('LanguageTable', 'id', 'glottocode', 'name', 'latitude', 'longitude'):
        n2l[lang['name'].replace(' ', '_').replace('-', '_')] = lang['id']
        lang['glottocode'] = {
            'Hill_Mari': 'kozy1238',
            'South_Selkup': 'kety1234',
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
        if lang['glottocode']:
            add_language_codes(data, v, lang['ISO639P3code'], glottocode=lang['glottocode'])

    for rec in bibtex.Database.from_file(args.cldf.bibpath, lowercase=True):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    refs = collections.defaultdict(list)

    for param in args.cldf.iter_rows('ParameterTable', 'id', 'name'):
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
    )
    data.add(
        models.Feature,
        'adm',
        id='adm',
        name="Admixture coefficients",
    )
    for cid, color in [
        ('c1', '#e79e3f'),
        ('c2', '#7783c5'),
        ('c3', '#b44094'),
        ('c4', '#7d9f64'),
    ]:
        data.add(
            common.DomainElement,
            cid,
            id=cid,
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
    for val in args.cldf.iter_rows(
            'ValueTable',
            'id', 'value', 'languageReference', 'parameterReference', 'codeReference', 'source'):
        if val['value'] is None:  # Missing values are ignored.
            continue
        vsid = (val['languageReference'], val['parameterReference'])
        vs = data['ValueSet'].get(vsid)
        if not vs:
            vs = data.add(
                common.ValueSet,
                vsid,
                id='-'.join(vsid),
                language=data['Variety'][val['languageReference']],
                parameter=data['Feature'][val['parameterReference']],
                contribution=contrib,
            )
        for ref in val.get('source', []):
            sid, pages = Sources.parse(ref)
            refs[(vsid, sid)].append(pages)
        data.add(
            common.Value,
            val['id'],
            id=val['id'],
            name=val['value'],
            valueset=vs,
            domainelement=data['DomainElement'][val['codeReference']],
        )

    for row in reader(pathlib.Path(uralic.__file__).parent.parent.parent / 'admixture_coef.csv', dicts=True):
        lid = n2l[row['lang']]
        vs = data.add(
            common.ValueSet,
            '{}-adm'.format(lid),
            id='{}-adm'.format(lid),
            language=data['Variety'][lid],
            parameter=data['Feature']['adm'],
            contribution=contrib,
        )
        for k in ['C1', 'C2', 'C3', 'C4']:
            v = float(row[k])
            data.add(
                common.Value,
                '{}-{}-{}'.format(lid, 'adm', k),
                id='{}-{}-{}'.format(lid, 'adm', k),
                name=str(v),
                frequency=100 * v,
                valueset=vs,
                domainelement=data['DomainElement'][k.lower()],
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
