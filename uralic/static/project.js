URALIC = {};

URALIC.style = function(feature) {
    return {
            'color': '#000',
            'weight': 1,
            'opacity': 0.2,
            'fillOpacity': 0.3,
            'fillColor': feature.properties.color
    }
};

CLLD.LayerOptions.areas = {
    style: URALIC.style
}