<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Family')} ${ctx.name}</%block>

<ul class="inline codes pull-right" style="margin-top: 10px;">
    <li>
        <span class="large label label-info">
            ${h.models.IdentifierType.glottolog.description}:
            ${h.external_link(ctx.description, label=ctx.id, inverted=True, style="color: white;")}
        </span>
    </li>
</ul>

<h2>Family ${ctx.name}</h2>

${request.map.render()}

<h3>${_('Languages')}</h3>
<div id="list-container" class="row-fluid">
    % for languages in h.partitioned(ctx.languages):
    <div class="span4">
        <table class="table table-condensed table-nonfluid">
            <tbody>
                % for language in languages:
                <tr>
                    <td>${h.link_to_map(language)}</td>
                    <td>${h.link(request, language)}</td>
                </tr>
                % endfor
            </tbody>
        </table>
    </div>
    % endfor
</div>