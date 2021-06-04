from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models import common

from clld_glottologfamily_plugin.models import HasFamilyMixin


# -----------------------------------------------------------------------------
# specialized common mapper classes
# -----------------------------------------------------------------------------

@implementer(interfaces.ILanguage)
class Variety(CustomModelMixin, common.Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    glottocode = Column(String)
    subfamily = Column(String)


@implementer(interfaces.IParameter)
class Feature(CustomModelMixin, common.Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    # sortkey = Column(Unicode)
    # concepticon_id = Column(Unicode)
    # category = Column(Unicode)
    # contribution_pk = Column(Integer, ForeignKey('cldfdataset.pk'))
    # contribution = relationship(CLDFDataset, backref='parameters')
