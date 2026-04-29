from clld.db.meta import DBSession
from clld.db.models import common
from clld.web.util import helpers
from clldutils.markup import iter_markdown_sections
from markdown import markdown

from uralic.models import Feature


def adapt_readme(text):
    res = []
    contents_level = None
    for level, header, content in iter_markdown_sections(text):
        if "How to cite" in header:
            continue

        if 'Contents' in header:
            contents_level = level
            continue

        if contents_level:
            if level > contents_level:
                continue
            if level == contents_level:
                contents_level = None

        for k, v in {
            '`sources.bib`': '[Sources](sources)',
            '`contributors.md`': '[Contributors](contributors)',
            'the `doc` folder': '[Parameters](parameters)',
        }.items():
            content = content.replace(k, v)
        res.append('#' + header)
        res.append(content)

    return markdown('\n'.join(res))


def dataset_detail_html(request=None, context=None, **kw):
    return dict(
        description=adapt_readme(context.jsondata['readme']),
        feature_count=DBSession.query(common.Parameter).count() - 1,
        language_count=DBSession.query(common.Language).count(),
        feature_count_gb=DBSession.query(Feature).join(Feature.contribution).filter(common.Contribution.id == 'GB').count(),
        feature_count_ut=DBSession.query(Feature).join(Feature.contribution).filter(common.Contribution.id == 'UT').count(),
    )


def glossed_examples(v):
    return [
        helpers.rendered_sentence(vs.sentence) for vs in
        DBSession.query(common.ValueSentence).filter(common.ValueSentence.value_pk == v.pk)]
