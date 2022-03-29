<%inherit file="home_comp.mako"/>
<%namespace name="mpg" file="clldmpg_util.mako"/>

<h3>${_('Downloads')}</h3>

<div class="alert alert-info">
    <p>
        This web application serves the latest
        ${h.external_link('https://github.com/cldf-datasets/uratyp/releases', label=_('released version'))}
        of data curated at
        ${h.external_link('https://github.com/cldf-datasets/uratyp', label='cldf-datasets/uratyp')}.
        All released versions are accessible via<br/>
        <a href="https://doi.org/10.5281/zenodo.5236365">
            <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.5236365.svg" alt="DOI">
        </a>
        <br/>
        on ZENODO as well.
    </p>
    <p>
        For a list of errata, see
        ${h.external_link('https://github.com/cldf-datasets/uratyp/issues?q=is%3Aissue+is%3Aopen+label%3Aerratum', label='the issues at GitHub')}.
    </p>
</div>
