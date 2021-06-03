<%inherit file="../resource_rdf.mako"/>
<%block name="properties">
    <rdf:type rdf:resource="${str(h.rdf.NAMESPACES['skos']['Concept'])}"/>
    % for lang in ctx.languages:
    <skos:narrower rdf:resource="${request.resource_url(lang)}"/>
    % endfor
</%block>
