"""Startseite: Hero, Kurzvorstellung, Einstieg in die drei Bereiche."""

import streamlit as st

from utils.theming import merkkasten

st.markdown(
    """
<div class="hero">
  <h1>Künstliche Intelligenz und das „Warum“</h1>
  <div class="untertitel">
    Eine Einführung in Maschinelles Lernen und Kausalität —
    Begleitwebsite zur Arbeitsgruppe der Sommerakademie Leysin.
  </div>
  <div class="hero-badges">
    <span>📅 18.–27. August 2026</span>
    <span>📍 Leysin, Schweiz</span>
    <span>🎓 Studienstiftung des deutschen Volkes</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("## Worum geht es hier?")
st.markdown(
    """
Moderne KI-Systeme sind erstaunlich gut darin, **Muster zu erkennen und
vorherzusagen** — aber Muster sind nicht dasselbe wie Ursachen. Wer aus Daten
Entscheidungen ableiten will („Hilft dieses Medikament?“, „Bringt diese
Werbekampagne etwas?“), braucht mehr als Korrelationen: eine Antwort auf die
Frage nach dem **Warum**.

Auf dieser Website lernst du beides: wie Maschinelles Lernen funktioniert —
und wie man mit Daten sauber über **Kausalität** nachdenkt. Alle Kapitel
enthalten interaktive Demos: Regler bewegen, Daten würfeln, selbst sehen,
was passiert.
"""
)

spalte_ml, spalte_kausal, spalte_projekte = st.columns(3)

with spalte_ml, st.container(border=True):
    st.markdown("### 🤖 Maschinelles Lernen")
    st.markdown(
        "Wie lernen Maschinen aus Beispielen? Von linearer Regression über "
        "Entscheidungsbäume bis zu neuronalen Netzen und LLMs."
    )
    st.page_link("views/ml/grundlagen.py", label="Kapitel 1 starten", icon="▶️")

with spalte_kausal, st.container(border=True):
    st.markdown("### 🔀 Kausalität")
    st.markdown(
        "Warum Korrelation nicht Kausalität ist — und wie man mit DAGs, "
        "Potential Outcomes und kausalem ML echte Effekte aus Daten holt."
    )
    st.page_link("views/kausalitaet/korrelation.py", label="Kapitel 1 starten", icon="▶️")

with spalte_projekte, st.container(border=True):
    st.markdown("### 🚀 Gruppenprojekte")
    st.markdown(
        "Während der Akademie erkunden Gruppen eigene Themen in Python — "
        "ihre Ergebnisse erscheinen hier auf der Website."
    )
    st.page_link("views/projekte/uebersicht.py", label="Zu den Projekten", icon="▶️")

st.markdown("## Wie du diese Seite nutzt")
st.markdown(
    """
1. **Vor der Akademie:** Schnupper in die ersten Kapitel — Vorwissen brauchst
   du keins, Grundkenntnisse in Statistik helfen.
2. **Während der Akademie:** Die Kapitel begleiten die Sitzungen; dein
   Gruppenprojekt bekommt eine eigene Seite.
3. **Danach:** Alles bleibt online — zum Nachschlagen, Teilen und Weiterlernen.
"""
)

merkkasten(
    "Gut zu wissen",
    "Diese Website bleibt nach der Akademie dauerhaft öffentlich. "
    "Alle Materialien und Gruppenprojekte sind frei zugänglich.",
    typ="definition",
)

st.page_link("views/ueber.py", label="Mehr über die Akademie", icon="ℹ️")
