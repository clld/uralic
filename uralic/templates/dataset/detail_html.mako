<%inherit file="../home_comp.mako"/>

<%def name="sidebar()">
    <div class="well">
        <h3>How to cite UraTyp datasets</h3>
        <p>Please cite the submitted manuscript</p>
        <blockquote>
            Miina Norvik, Yingqi Jing, Michael Dunn, Robert Forkel, Terhi Honkola, Gerson Klumpp, Richard Kowalik, Helle
            Metslang, Karl Pajusalu, Minerva Piha, Eva Saar, Sirkka Saarinen and Outi Vesakoski: Uralic typology in the
            light of new comprehensive data sets (submitted ms to Journal of Uralic Linguistics)
        </blockquote>
        <p>as well as the datasets</p>
        <blockquote>
            <a href="https://doi.org/10.5281/zenodo.5236365">
                <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.5236365.svg" alt="DOI: 10.5281/zenodo.5236365"></a>
        </blockquote>
    </div>
</%def>

<h2>Welcome to the Uralic Typological database – UraTyp</h2>

<p>
    The UraTyp database contains
    ${feature_count}
    features mainly on morphology, syntax, and phonology collected from
    ${language_count}
    Uralic languages/language varieties. The database grew out from the cooperation with
    the ${h.external_link('https://glottobank.org', label='Grambank team')} who set out to collect data from about
    half of the world’s languages.
    The goal of building the UraTyp database was to create a family-specific database.
</p>

<p>
    The UraTyp database contains information collected with two separate questionnaires.
    ${feature_count_gb}
    features in UraTyp
    originate from the questionnaire developed by the Grambank team (hereinafter GB questionnaire), whereas the
    author team of the UraTyp database created
    ${feature_count_ut}
    features (hereinafter UT). As features in both questionnaires
    were formed as binary questions designed to be answered with “yes, this function/feature is present in the language”
    or “no, this function/feature is not present in the language” the two datasets could be easily joined to form a
    single coherent database.
</p>

<p>
    The UraTyp database is the first comprehensive database that presents comparative structural data on the
    Uralic language family from all its branches.
</p>

<p>
    We hope that the database proves to be a useful tool in research and teaching for typologists, Uralists, as well
    as everyone else interested in the Uralic languages.
</p>

<h3>How to use UraTyp</h3>
<p>
    The database can be explored in several ways. One option is to browse the interactive database at
    https://uralic.clld.org according to languages.
    Clicking on <a href="${req.route_url('languages')}">“Languages”</a> on the navigation bar and then selecting a
    language enables one to see all the answers provided for the respective language. Another option is to search
    according to <a href="${req.route_url('parameters')}">“Parameters”</a> and study the general picture parameter
    by parameter. In the "Id" column, <em>GB</em> stands for the features collected with the GB questionnaire,
    whereas <em>UT</em> represents the features collected with the UT questionnaire. Clicking on the name of the
    parameter takes to the general description and map. The box “values” gives a possibility to recieve a quick
    overview of the general distribution of absence/presence of features. It is also possible to explore the
    <a href="${req.route_url('sources')}">“Sources”</a> that were used for giving linguistic examples for UT questions.
    To a large extent, both questionnaires were filled out by involving language experts. The names of the
    language experts are listed in the section <a href="${req.route_url('contributors')}">“Contributors”</a>.
</p>


<h3>Funders and supporters</h3>
<p>
    Kipot ja kielet (‘Pots and languages’) project, funded by the University of Turku (2018–2020), the URKO (Uralilainen Kolmio = ‘Uralic Triangle’) project, funded by the Academy of Finland (2020–2022); The Collegium for Transdisciplinary Studies in Archeology, Genetics and Linguistics, University of Tartu (2018–)
</p>

<h3>Terms of use</h3>

<p>
    This dataset is licensed under a CC-BY-4.0 license
</p>
