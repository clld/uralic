<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%! from clld_phylogeny_plugin.tree import Tree %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>

<%block name="head">
    ${Tree.head(req)|n}
    <style>
        blockquote p {
            font-size: inherit !important;
            line-height: inherit !important;
        }
    </style>
</%block>

<ul class="nav nav-pills" style="float: right">
    <li class="">
        <a href="#map-container">
            <img src="${req.static_url('uralic:static/Map_Icon.png')}"
                 width="35">
            Map
        </a>
    </li>
    <li class="">
        <a href="#table-container">
            <img src="${req.static_url('uralic:static/Table_Icon.png')}"
                 width="35">
            Table
        </a>
    </li>
    <li class="">
        <a href="#tree-container">
            <img src="${req.static_url('uralic:static/Tree_Icon.png')}"
                 width="35">
            Tree
        </a>
    </li>
</ul>

<div class="span4" style="float: right; margin-top: 1em; clear: right">
    <%util:well title="Values">
        <table class="table table-condensed">
            % for de in ctx.domain:
            <tr>
                <td>${h.map_marker_img(req, de)}</td>
                <td>${de.name}</td>
                <td>${de.description}</td>
                <td class="right">${len(de.values)}</td>
            </tr>
            % endfor
        </table>
    </%util:well>
</div>


<h2>${ctx.name}</h2>

% if ctx.markup_description:
<div>${ctx.markup_description|n}</div>
% endif

<div style="clear: both"/>
<div id="map-container">
    ${(map_ or request.map).render()}
</div>

<div id="table-container">
${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
</div>


<div id="tree-container">
${tree.render()|n}
</div>

##${h.get_adapter(h.interfaces.IRepresentation, ctx, req, ext='valuetable.html').render(ctx, req)|n}