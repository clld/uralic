from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol

from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.datatables import FamilyCol


from uralic import models


class Languages(datatables.Languages):
    def base_query(self, query):
        return query.join(Family).options(joinedload(models.Variety.family)).distinct()

    def col_defs(self):
        print(models.Variety)
        return [
            LinkCol(self, 'name'),
            # FamilyCol(self, 'Family', models.Variety),
            Col(self, "Subfamily", model_col=models.Variety.subfamily),
            Col(self,
                'latitude',
                sDescription='<small>The geographic latitude</small>'),
            Col(self,
                'longitude',
                sDescription='<small>The geographic longitude</small>'),
            LinkToMapCol(self, 'm'),
        ]


def includeme(config):
    """register custom datatables"""

    config.register_datatable('languages', Languages)
