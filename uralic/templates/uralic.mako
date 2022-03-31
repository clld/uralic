<%inherit file="app.mako"/>

<%block name="header">
##<div id="header">
##    <a href="${request.resource_url(request.dataset)}">
##        <img src="${request.static_url('uralic:static/URHIA_banner-scaled.jpg')}"/>
##    </a>
##</div>
</%block>

${next.body()}
