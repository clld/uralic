from clld_phylogeny_plugin.models import Phylogeny

from uralic.adapters import FeatureTree


def parameter_detail_html(request=None, context=None, **kw):
    return dict(tree=FeatureTree(Phylogeny.get('p'), request, context.id))
