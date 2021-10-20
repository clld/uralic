from clld.interfaces import ILanguage, IIndex, IParameter
from clld.web.adapters.geojson import GeoJson, GeoJsonParameter
from clld.web.maps import ParameterMap, Layer, LanguageMap, Legend
from clld.web.util.htmllib import HTML
from clld.web.util import helpers
from clld.db.meta import DBSession
from clld.db.models import common
from clldutils.misc import nfilter
from clldutils.color import _to_rgb

from uralic.models import SUBFAMILIES


class GeoJsonFeature(GeoJsonParameter):
    def feature_properties(self, ctx, req, valueset):
        return {
            'values': list(valueset.values),
            'label': ', '.join(nfilter(v.name for v in valueset.values))
            if valueset.parameter.id != 'adm' else self.get_language(ctx, req, valueset).name}


class GeoJsonAreas(GeoJson):
    extension = 'areas.geojson'

    def featurecollection_properties(self, ctx, req):
        return {'name': "Speaker Areas"}

    def get_features(self, ctx, req):
        for lang in ctx.get_query():
            polygon = lang.jsondata['feature']
            yield {
                'type': 'Feature',
                'properties': {
                        'id': lang.id,
                        'label': '%s %s' % (lang.id, lang.name),
                        'subfamily': lang.subfamily,
                        'color': lang.color,
                        # 'language': {'id': lang.id},
                        # 'latlng': [lang.latitude, lang.longitude],
                },
                'geometry': polygon['geometry'],
            }


class FeatureMap(ParameterMap):
    def get_layers(self):
        yield Layer(
            'areas',
            'Speaker Areas',
            self.req.route_url('languages_alt', ext='areas.geojson'))

        for layer in ParameterMap.get_layers(self):
            yield layer

    def get_legends(self):
        items = []

        for layer in self.layers:
            if layer.id == 'areas':
                continue
            items.append([
                HTML.label(
                    HTML.input(
                        class_="stay-open",
                        type="checkbox",
                        checked="checked",
                        onclick=helpers.JS_CLLD.mapToggleLayer(
                            self.eid, layer.id, helpers.JS("this"))),
                    getattr(layer, 'marker', ''),
                    layer.name,
                    class_="checkbox inline stay-open",
                    style="margin-left: 5px; margin-right: 5px;",
                ),
            ])
        yield Legend(
            self,
            'layers',
            items,
            label=self.ctx.name,
            stay_open=True,
            item_attrs=dict(style='clear: right'))
        items = [
            (
                ' ',
                HTML.span(' ', style="display: inline-block; height: 1em; width: 1em; outline: 1px solid {}; background-color: rgba({}, {}, {}, 0.5);".format(
                    c, *_to_rgb(c)
                )),
                ' ',
                sf,
            ) for sf, c in SUBFAMILIES.items()
        ]
        yield Legend(
            self,
            'areas',
            items,
            label='Speaker areas',
            stay_open=True,
            item_attrs=dict(style='clear: right'))

        for legend in ParameterMap.get_legends(self):
            if legend.name != 'layers':
                yield legend


class AdmixtureMap(FeatureMap):
    def __init__(self, ctx, req, **kw):
        ctx = DBSession.query(common.Parameter).filter(common.Parameter.id == 'adm').one()
        super(AdmixtureMap, self).__init__(ctx, req, **kw)


class VarietyMap(LanguageMap):

    """Map showing a single language."""

    def get_layers(self):
        yield Layer(
            'areas',
            'Speakeer Area',
            dict(type='FeatureCollection', features=[self.ctx.jsondata['feature']]))
        for la in LanguageMap.get_layers(self):
            yield la


def includeme(config):
    #config.register_adapter(GeoJsonAreas, ILanguage, IIndex)
    config.register_map('parameter', FeatureMap)
    #config.register_map('languages', AdmixtureMap)
    config.register_map('language', VarietyMap)
    config.register_adapter(GeoJsonFeature, IParameter, name=GeoJson.mimetype)
