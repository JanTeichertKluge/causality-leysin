"""Organisatorische Übersicht für die Arbeit an den Team-Apps."""

import streamlit as st

from utils.theming import kapitel_kopf, merkkasten

kapitel_kopf(
    "🗂️",
    "Euer Gruppenprojekt",
    "Von einer klaren Frage zu einer interaktiven wissenschaftlichen Analyse",
)

st.markdown(
    """
Auf eurer Track-Seite findet ihr die Quellen für den ersten Einstieg. Nutzt
sie, um zentrale Begriffe, Methoden und offene Fragen zu sammeln. Vor Ort
grenzt ihr daraus eine eigene Fragestellung ab und setzt sie als interaktive
**Streamlit-App** um. Eure App soll nicht das gesamte Themenfeld erklären,
sondern eine wissenschaftliche Aussage anhand von Daten, einer Simulation
oder einer Fallstudie nachvollziehbar machen.
"""
)

st.markdown("## Daran könnt ihr euch orientieren")
st.markdown(
    """
1. Fragestellung
2. wissenschaftlicher Hintergrund
3. kausale Annahmen oder Identifikationsproblem
4. interaktive Analyse
5. Ergebnisse
6. Grenzen
7. Literatur
"""
)

with st.expander("So startet ihr eure Streamlit-App", expanded=True):
    st.markdown(
        """
1. Sucht auf eurer Track-Seite den angegebenen Arbeitsordner und kopiert
   `content/projekte/_vorlage/` dorthin.
2. Öffnet `app.py` und ersetzt die Beispieltexte und -grafik schrittweise
   durch eure Analyse.
3. Ruft in eurer Datei kein `st.set_page_config()` auf. Verwendet nur Pakete aus
   `requirements.txt` und ladet Dateien über `Path(__file__).parent`.
4. Startet die Website lokal mit `streamlit run streamlit_app.py` und prüft
   eure Änderungen direkt auf der Track-Seite.
"""
    )

with st.expander("Falls ihr zunächst nur mit Markdown arbeiten möchtet"):
    st.markdown(
        """
Ihr könnt eure Inhalte vorübergehend in `projekt.md` festhalten. Sobald eine
`app.py` in eurem Arbeitsordner liegt, wird die interaktive Version angezeigt.
Am Ende präsentiert ihr eure Ergebnisse gemeinsam als Streamlit-App.
"""
    )

merkkasten(
    "Keine Sorge vor Fehlern",
    "Wenn eure App einmal nicht läuft, bleiben alle anderen Seiten erreichbar. "
    "Auf eurer Track-Seite seht ihr die Fehlermeldung und könnt sie gemeinsam "
    "mit uns Schritt für Schritt beheben.",
    typ="merke",
)

st.page_link("views/projekte/themen.py", label="Track auswählen", icon="🧭")
example_page = st.session_state.get("projekt_seiten", {}).get("beispielprojekt")
if example_page is not None:
    st.page_link(example_page, label="So kann eine kleine Streamlit-App aussehen", icon="🎲")
