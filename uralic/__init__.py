import functools
import collections

from pyramid.config import Configurator

from clld_glottologfamily_plugin import util

from clld.interfaces import IMapMarker, IValueSet, IValue, IDomainElement
from clldutils.svg import pie, icon, data_url

from clld.web.app import menu_item

# we must make sure custom models are known at database initialization!
from uralic import models


class LanguageByFamilyMapMarker(util.LanguageByFamilyMapMarker):
    def __call__(self, ctx, req):

        if IValueSet.providedBy(ctx):
            c = [(v.frequency if v.frequency is not None else 1, v.domainelement.jsondata['color'])
                 for v in ctx.values]
            c.sort(key=lambda i: i[1])
            return data_url(pie([i[0] for i in c], [i[1] for i in c], **dict(stroke_circle=True)))
        if IDomainElement.providedBy(ctx):
            return data_url(icon(ctx.jsondata['color'].replace('#', 'c')))
        if IValue.providedBy(ctx):
            return data_url(icon(ctx.domainelement.jsondata['color'].replace('#', 'c')))

        return super(LanguageByFamilyMapMarker, self).__call__(ctx, req)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')

    config.include('clldmpg')

    # this customize the order of each page
    config.register_menu(
        ('dataset', functools.partial(menu_item, 'dataset', label='Uralic Areal Typology')),
        ('languages', functools.partial(menu_item, 'languages')),
        ('parameters', functools.partial(menu_item, 'parameters')),
        # ('StructureDataset', lambda ctx, req: (req.route_url(
        #     'contribution', id='StructureDataset'), 'Features')),
        # ('Wordlist', lambda ctx, req: (req.route_url('contribution', id='Wordlist'), 'Wordlist')),
        ('sources', functools.partial(menu_item, 'sources')),
        # ('about', lambda c, r: (r.route_url('about'), 'About')),
    )

    config.registry.registerUtility(LanguageByFamilyMapMarker(), IMapMarker)

    return config.make_wsgi_app()
