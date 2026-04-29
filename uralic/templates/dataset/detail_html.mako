<%inherit file="../home_comp.mako"/>

<%block name="header">
    <div id="header">
        <a href="${request.resource_url(request.dataset)}">
            <img src="${request.static_url('uralic:static/URHIA_banner-scaled.jpg')}"/>
        </a>
        <div class="banner-text"><h1>Uralic Areal Typology Online</h1></div>
    </div>
</%block>

<%block name="head">
    <style>
        #header {
            position: relative;
            text-align: center;
            color: white;
            font-size: larger;
            text-shadow: -1px -1px 0 darkolivegreen, 1px -1px 0 darkolivegreen, -1px 1px 0 darkolivegreen, 1px 1px 0 darkolivegreen;
        }
        .banner-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
    </style>
</%block>

<%def name="sidebar()">
    <div class="well">
        <h3>How to cite UraTyp 2.0 datasets</h3>
        <blockquote>
            <p>${ctx.jsondata['citation']}</p>
            <a href="https://doi.org/10.5281/zenodo.5236365">
                <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.5236365.svg" alt="DOI: 10.5281/zenodo.5236365"></a>
        </blockquote>
    </div>
</%def>

${description|n}
