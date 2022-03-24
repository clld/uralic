import itertools

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

from clld_phylogeny_plugin.interfaces import IPhylogeny
from clld_phylogeny_plugin.models import Phylogeny

SUBFAMILIES = {
    'Finnic': '#31688E',  # dark blue
    'Mari': '#443A83',  # dark purple
    'Mordvin': '#80c9ac',
    'Permic': '#440154',  # purple
    'Saami': '#35B779',  # green
    'Samoyed': '#FDE725',  # yellow
    'Ugric': '#21908C',  # light green
}


@implementer(interfaces.ILanguage)
class Variety(CustomModelMixin, common.Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    glottocode = Column(String)
    subfamily = Column(String)

    @property
    def color(self):
        return SUBFAMILIES[self.subfamily]

    def iter_grouped_experts(self):
        for cid, ex in itertools.groupby(
            sorted(self.experts, key=lambda e: (e.contribution.id, e.ord)),
            lambda e: e.contribution.id
        ):
            yield cid, list(ex)


class LanguageExpert(Base):
    __table_args__ = (UniqueConstraint('language_pk', 'contributor_pk', 'contribution_pk'),)

    language_pk = Column(Integer, ForeignKey('language.pk'), nullable=False)
    contributor_pk = Column(Integer, ForeignKey('contributor.pk'), nullable=False)
    contribution_pk = Column(Integer, ForeignKey('contribution.pk'), nullable=False)
    ord = Column(Integer)
    language = relationship(common.Language, backref='experts')
    contributor = relationship(common.Contributor, backref='experts')
    contribution = relationship(common.Contribution, backref='experts')


@implementer(interfaces.IParameter)
class Feature(CustomModelMixin, common.Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    # sortkey = Column(Unicode)
    # concepticon_id = Column(Unicode)
    category = Column(Unicode)
    contribution_pk = Column(Integer, ForeignKey('contribution.pk'))
    contribution = relationship(common.Contribution, backref='parameters')
