from clld.db.meta import DBSession
from clld.db.models import common
from clld.web.util import helpers

from clld_phylogeny_plugin.models import Phylogeny

from uralic.adapters import FeatureTree


def parameter_detail_html(request=None, context=None, **kw):
    return dict(tree=FeatureTree(Phylogeny.get('p'), request, context.id))


def glossed_examples(v):
    return [
        helpers.rendered_sentence(vs.sentence) for vs in
        DBSession.query(common.ValueSentence).filter(common.ValueSentence.value_pk == v.pk)]
