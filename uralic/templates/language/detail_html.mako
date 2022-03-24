<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    ${util.codes()}
    <div style="clear: right;"> </div>
    <%util:well title="Language experts">
        <dl>
            % for cid, experts in ctx.iter_grouped_experts():
                <dt>${cid}</dt>
                <dd>${', '.join([e.contributor.name for e in experts])}</dd>
            % endfor
        </dl>
    </%util:well>
    % if ctx.latitude is not None:
    <%util:well>
        ${request.map.render()}
        ${h.format_coordinates(ctx)}
    </%util:well>
    % endif
    <%util:well title="Sources">
        ${util.sources_list(sorted(list(ctx.sources), key=lambda s: s.name))}
    </%util:well>
</%def>
