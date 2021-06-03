from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from clld.db.meta import Base
from clld.db.models.common import IdNameDescriptionMixin

from clld_glottologfamily_plugin.interfaces import IFamily


@implementer(IFamily)
class Family(Base, IdNameDescriptionMixin):
    @property
    def url(self):
        return self.description


class HasFamilyMixin(object):
    macroarea = Column(Unicode)

    @declared_attr
    def family_pk(cls):
        return Column(Integer, ForeignKey('family.pk'))

    @declared_attr
    def family(cls):
        return relationship(Family, backref='languages')
