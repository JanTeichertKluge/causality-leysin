"""Startseite: Hero, Kurzvorstellung, Einstieg in die drei Bereiche."""

import streamlit as st

from utils.theming import merkkasten

st.markdown(
    """
<div class="hero">
  <h1>Künstliche Intelligenz und das „Warum“</h1>
  <div class="untertitel">
    Eine Einführung in Maschinelles Lernen und Kausalität.
    Begleitwebsite zur Arbeitsgruppe der Sommerakademie Leysin.
  </div>
  <div class="hero-badges">
    <span>18.–27. August 2026</span>
    <span>Leysin, Schweiz</span>
    <span>Studienstiftung des deutschen Volkes</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("## Worum geht es hier?")
st.markdown(
    """
Moderne KI-Systeme sind erstaunlich gut darin, **Muster zu erkennen und
vorherzusagen**, aber Muster sind nicht dasselbe wie Ursachen. Wer aus Daten
Entscheidungen ableiten will („Hilft dieses Medikament?“, „Bringt diese
Werbekampagne etwas?“), braucht mehr als Korrelationen: eine Antwort auf die
Frage nach dem **Warum**. Auf dieser Website kannst du Modelle und kausale
Annahmen selbst ausprobieren: Verändere Parameter, ziehe neue Stichproben und
beobachte, wie sich Schlussfolgerungen verändern.
"""
)

spalte_ml, spalte_kausal, spalte_projekte = st.columns(3)

with spalte_ml, st.container(border=True):
    st.markdown("### 🤖 Maschinelles Lernen")
    st.markdown(
        "Starte bei Trainings- und Testdaten und arbeite dich von linearer "
        "Regression bis zu Trees, neuronalen Netzen und LLMs vor."
    )
    st.page_link("views/ml/grundlagen.py", label="Mit ML starten", icon="▶️")

with spalte_kausal, st.container(border=True):
    st.markdown("### 🔀 Kausalität")
    st.markdown(
        "Untersuche, wann ein Zusammenhang kausal gedeutet werden darf und "
        "welche Annahmen hinter DAGs, Potential Outcomes und kausalem ML stehen."
    )
    st.page_link("views/kausalitaet/korrelation.py", label="Mit Kausalität starten", icon="▶️")

with spalte_projekte, st.container(border=True):
    st.markdown("### 🚀 Gruppenprojekte")
    st.markdown(
        "Wählt euren Track, steigt mit den empfohlenen Quellen ein und entwickelt "
        "vor Ort eine interaktive Analyse zu eurer eigenen Fragestellung."
    )
    st.page_link("views/projekte/themen.py", label="Tracks ansehen", icon="▶️")

merkkasten(
    "Gut zu wissen",
    "Du kannst alle Materialien während und nach der Akademie frei nutzen. "
    "Die ausführlichen Kapitel im Appendix sind optional: Für den gemeinsamen "
    "Einstieg brauchst du sie nicht vollständig durchzuarbeiten.",
    typ="definition",
)

st.page_link("views/ueber.py", label="Über uns", icon="ℹ️")
