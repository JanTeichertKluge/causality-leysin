"""Einstiegspunkt der App „KI und das Warum“ — Sommerakademie Leysin 2026.

Baut die Navigation (statische Kapitel + dynamisch entdeckte
Gruppenprojekte) und lädt Theme/CSS. Gestartet wird mit:

    streamlit run streamlit_app.py
"""

import streamlit as st

from utils import theming
from utils.projects import lade_projekte, projekt_seiten

st.set_page_config(
    page_title="KI und das Warum — Sommerakademie Leysin",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "**KI und das „Warum“** — Begleitwebsite zur Arbeitsgruppe "
            "„Eine Einführung in Maschinelles Lernen und Kausalität“ der "
            "Sommerakademie Leysin 2026 (Studienstiftung des deutschen Volkes)."
        ),
    },
)

theming.register_plotly_template()
theming.inject_css()

start = st.Page("views/start.py", title="Start", icon="🏔️", default=True)
ueber = st.Page("views/ueber.py", title="Über die Akademie", icon="ℹ️")

ml_seiten = [
    st.Page("views/ml/grundlagen.py", title="Was ist Maschinelles Lernen?", icon="🤖"),
    st.Page("views/ml/baeume_ensembles.py", title="Bäume & Ensembles", icon="🌲"),
    st.Page("views/ml/neuronale_netze.py", title="Neuronale Netze", icon="🧠"),
    st.Page("views/ml/llms_kausalitaet.py", title="LLMs & kausales Denken", icon="💬"),
]

kausal_seiten = [
    st.Page("views/kausalitaet/korrelation.py", title="Korrelation ≠ Kausalität", icon="🔀"),
    st.Page("views/kausalitaet/dags_confounding.py", title="DAGs & Confounding", icon="🕸️"),
    st.Page("views/kausalitaet/potential_outcomes.py", title="Potential Outcomes", icon="⚖️"),
    st.Page("views/kausalitaet/kausales_ml.py", title="Kausales Machine Learning", icon="🎯"),
]

uebersicht = st.Page("views/projekte/uebersicht.py", title="Alle Projekte", icon="🗂️")

# Gruppenprojekte dynamisch aus content/projekte/ einsammeln. Die Map wird
# in den Session State gelegt, damit die Projektübersicht per st.page_link
# auf die registrierten Seiten verlinken kann.
projekte = lade_projekte()
seiten_map = projekt_seiten(projekte)
st.session_state["projekt_seiten"] = seiten_map

navigation = st.navigation(
    {
        "": [start, ueber],
        "Maschinelles Lernen": ml_seiten,
        "Kausalität": kausal_seiten,
        "Gruppenprojekte": [uebersicht, *seiten_map.values()],
    }
)

with st.sidebar:
    st.markdown(
        '<div class="sidebar-fuss">Sommerakademie Leysin 2026<br>'
        "Studienstiftung des deutschen Volkes<br>"
        "Oliver Schacht &amp; Jan Teichert-Kluge</div>",
        unsafe_allow_html=True,
    )

navigation.run()
