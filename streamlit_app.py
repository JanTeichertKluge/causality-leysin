"""Einstiegspunkt der App „KI und das Warum“ (Sommerakademie Leysin 2026).

Baut die Navigation (statische Kapitel + dynamisch entdeckte
Gruppenprojekte) und lädt Theme/CSS. Gestartet wird mit:

    streamlit run streamlit_app.py
"""

from pathlib import Path

import streamlit as st

from utils import theming
from utils.projects import lade_projekte, projekt_seiten
from utils.topic_pages import topic_page
from utils.topics import load_topics

APP_ICON = Path(__file__).parent / "assets" / "icon.png"

st.set_page_config(
    page_title="KI und das Warum | Sommerakademie Leysin",
    page_icon=str(APP_ICON),
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "**KI und das „Warum“**: Begleitwebsite zur Arbeitsgruppe "
            "„Eine Einführung in Maschinelles Lernen und Kausalität“ der "
            "Sommerakademie Leysin 2026 (Studienstiftung des deutschen Volkes)."
        ),
    },
)

theming.register_plotly_template()
theming.inject_css()

start = st.Page("views/start.py", title="Start", icon="🏔️", default=True)
ueber = st.Page("views/ueber.py", title="Über uns", icon="ℹ️")
referenzen = st.Page("views/referenzen.py", title="Referenzen & Quellen", icon="📚")

ml_seiten = [
    st.Page("views/ml/grundlagen.py", title="Was ist Maschinelles Lernen?", icon="🤖"),
    st.Page("views/ml/lineare_regression.py", title="Lineare Regression", icon="📈"),
    st.Page("views/ml/regularisierung.py", title="Lasso & Ridge", icon="🎚️"),
    st.Page("views/ml/baeume_ensembles.py", title="Trees & Ensembles", icon="🌲"),
    st.Page("views/ml/neuronale_netze.py", title="Neural Networks", icon="🧠"),
    st.Page("views/ml/llms_kausalitaet.py", title="LLMs & kausales Denken", icon="💬"),
]

kausal_seiten = [
    st.Page("views/kausalitaet/korrelation.py", title="Korrelation ≠ Kausalität", icon="🔀"),
    st.Page("views/kausalitaet/dags_confounding.py", title="DAGs & Confounding", icon="🕸️"),
    st.Page("views/kausalitaet/potential_outcomes.py", title="Potential Outcomes & RCTs", icon="⚖️"),
    st.Page("views/kausalitaet/kausales_ml.py", title="Kausales Machine Learning", icon="🎯"),
]

appendix_seiten = [
    st.Page("views/ml/explainable_ml.py", title="Explainable AI", icon="🔍"),
    st.Page("views/kausalitaet/quasi_experimente.py", title="Quasi-Experimente: DiD & RDD", icon="📐"),
    st.Page("views/kausalitaet/bayes.py", title="Bayesian Methods", icon="🎲"),
    st.Page("views/kausalitaet/sem_surveys.py", title="SEMs & Survey Experiments", icon="📋"),
]

vertiefung_seiten = dict(
    zip(
        [
            "views/ml/grundlagen.py",
            "views/ml/lineare_regression.py",
            "views/ml/regularisierung.py",
            "views/ml/baeume_ensembles.py",
            "views/ml/neuronale_netze.py",
            "views/ml/explainable_ml.py",
            "views/ml/llms_kausalitaet.py",
            "views/kausalitaet/korrelation.py",
            "views/kausalitaet/dags_confounding.py",
            "views/kausalitaet/potential_outcomes.py",
            "views/kausalitaet/quasi_experimente.py",
            "views/kausalitaet/kausales_ml.py",
            "views/kausalitaet/bayes.py",
            "views/kausalitaet/sem_surveys.py",
        ],
        [
            *ml_seiten[:5],
            appendix_seiten[0],
            ml_seiten[5],
            *kausal_seiten[:3],
            appendix_seiten[1],
            kausal_seiten[3],
            *appendix_seiten[2:],
        ],
        strict=True,
    )
)
st.session_state["vertiefung_seiten"] = vertiefung_seiten

themen = st.Page("views/projekte/themen.py", title="Eure Projekt-Tracks", icon="🧭")
uebersicht = st.Page("views/projekte/uebersicht.py", title="So arbeitet ihr", icon="🗂️")
template = st.Page("views/projekte/template.py", title="Vorlage für eure App", icon="🛠️")

topics = load_topics()
themen_seiten = {
    topic.slug: st.Page(
        topic_page(topic),
        title=f"{topic.emoji} {topic.title}",
        url_path=f"thema-{topic.slug}",
    )
    for topic in topics
}
st.session_state["themen_seiten"] = themen_seiten

# Gruppenprojekte dynamisch aus content/projekte/ einsammeln. Die Map wird
# in den Session State gelegt, damit die Projektübersicht per st.page_link
# auf die registrierten Seiten verlinken kann.
projekte = [projekt for projekt in lade_projekte() if projekt.slug == "beispielprojekt"]
seiten_map = projekt_seiten(projekte)
st.session_state["projekt_seiten"] = seiten_map

navigation = st.navigation(
    {
        "": [start, ueber],
        "Einführung · Maschinelles Lernen": ml_seiten,
        "Einführung · Kausalität": kausal_seiten,
        "Gruppenprojekte": [themen, *themen_seiten.values(), uebersicht, template],
        "Appendix": appendix_seiten,
        "Material & Quellen": [referenzen, *seiten_map.values()],
    }
)

with st.sidebar:
    st.markdown(
        '<div class="sidebar-fuss">Sommerakademie Leysin 2026<br>'
        "Studienstiftung des deutschen Volkes<br>"
        "Dr. Oliver Schacht &amp; Jan Teichert-Kluge</div>",
        unsafe_allow_html=True,
    )

navigation.run()
