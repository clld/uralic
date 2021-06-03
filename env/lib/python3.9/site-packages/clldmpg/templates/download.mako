<%inherit file="home_comp.mako"/>
<%namespace name="mpg" file="clldmpg_util.mako"/>

<%block name="head">
    <style>
        a.accordion-toggle {font-weight: bold;}
    </style>
</%block>


<h3>Downloads</h3>

${mpg.downloads(request)}

<%def name="sidebar()">
    <div class="well well-small">
        ${mpg.downloads_legend()}
    </div>
</%def>
