from clld.interfaces import ILanguage, IIndex, IParameter
from clld.web.adapters.geojson import GeoJson, GeoJsonParameter
from clld.web.maps import ParameterMap, Layer
from clld.db.meta import DBSession
from clld.db.models import common
from clldutils.misc import nfilter

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
                        #'language': {'id': lang.id},
                        #'latlng': [lang.latitude, lang.longitude],
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


class AdmixtureMap(FeatureMap):
    def __init__(self, ctx, req, **kw):
        ctx = DBSession.query(common.Parameter).filter(common.Parameter.id == 'adm').one()
        super(AdmixtureMap, self).__init__(ctx, req, **kw)


def includeme(config):
    config.register_adapter(GeoJsonAreas, ILanguage, IIndex)
    config.register_map('parameter', FeatureMap)
    config.register_map('languages', AdmixtureMap)
    config.register_adapter(GeoJsonFeature, IParameter, name=GeoJson.mimetype)
