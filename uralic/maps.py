from clld.interfaces import ILanguage, IIndex
from clld.web.adapters.geojson import GeoJson
from clld.web.maps import ParameterMap, Layer


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


def includeme(config):
    config.register_adapter(GeoJsonAreas, ILanguage, IIndex)
    config.register_map('parameter', FeatureMap)
