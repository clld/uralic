URALIC = {};

URALIC.subfamilies = {
    'Finnic': '#99afb6',
    'Mari': '#80bdb0',
    'Mordvin': '#80c9ac',
    'Permic': '#89d1a6',
    'Saami': '#aadf93',
    'Samoyed': '#f9ed77',
    'Ugric': '#87a8b1',
}

URALIC.style = function(feature) {
    return {
            'color': '#000',
            'weight': 1,
            'opacity': 0.2,
            'fillOpacity': 0.3,
            'fillColor': URALIC.subfamilies[feature.properties.subfamily]
    }
};

CLLD.LayerOptions.areas = {
    style: URALIC.style
}