from sqlalchemy.orm import joinedload
from clld.db.models.common import Parameter, ValueSet
from clld.db.meta import DBSession
from clld_phylogeny_plugin.interfaces import ITree
from clld_phylogeny_plugin.tree import Tree


class FeatureTree(Tree):
    def __init__(self, ctx, req, pid, eid='tree'):
        Tree.__init__(self, ctx, req, eid=eid)

        self._parameters = DBSession.query(Parameter) \
            .filter(Parameter.id.in_([pid])) \
            .options(
            joinedload(Parameter.valuesets).joinedload(ValueSet.values),
            joinedload(Parameter.domain)) \
            .all()

    @property
    def parameters(self):
        return self._parameters

    def get_marker(self, valueset):
        return 'c', valueset.values[0].domainelement.jsondata['color']


def includeme(config):
    config.registry.registerUtility(FeatureTree, ITree)
