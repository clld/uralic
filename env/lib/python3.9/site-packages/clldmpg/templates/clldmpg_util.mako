<%namespace name="util" file="util.mako"/>
<%! from clldmpg import cdstar %>

<%def name="downloads(request)">
    <div class="accordion" id="downloads" style="margin-top: 1em; clear: right;">
        % for version, links in reversed(list(cdstar.downloads(request))):
            % if loop.first:
                <%util:accordion_group eid="acc-${version.replace('.', '-')}" parent="downloads" title="Version ${version}" open="True">
                    <ul>
                        % for link in links:
                            <li>${link|n}</li>
                        % endfor
                    </ul>
                </%util:accordion_group>
            % else:
                <%util:accordion_group eid="acc-${version.replace('.', '-')}" parent="downloads" title="Version ${version}">
                    <ul>
                        % for link in links:
                            <li>${link|n}</li>
                        % endfor
                    </ul>
                </%util:accordion_group>
            % endif
        % endfor
    </div>
</%def>

<%def name="downloads_legend()">
    <h4>File types</h4>
    <dl>
    % for model, dls in h.get_downloads(request):
        % for dl in dls:
            % if getattr(dl, 'description'):
                <dt><strong>${dl.url(req).split('/')[-1].replace('-', '_')}</strong></dt>
                <dd>${dl.description}</dd>
            % endif
        % endfor
    % endfor
    </dl>
</%def>