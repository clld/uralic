<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%! from clld_glottologfamily_plugin.models import Family %>
<%block name="title">${_('Families')}</%block>


<h2>Families</h2>

${request.get_datatable('familys', Family).render()}
