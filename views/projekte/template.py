"""Dokumentierte Vorschau des gemeinsamen Team-Templates."""

import streamlit as st

from utils.theming import kapitel_kopf

kapitel_kopf(
    "🛠️",
    "Team-Template",
    "Euer Ausgangspunkt für die gemeinsame Streamlit-App",
)

st.markdown(
    """
Kopiert den Ordner `content/projekte/_vorlage/` in euren Arbeitsordner. In
`app.py` findet ihr sieben Abschnitte, die euch vom Formulieren der Frage bis
zu Literatur und Grenzen führen. Ersetzt die Beispieltexte und die kleine
Demo nach und nach durch eure eigene Analyse – ihr müsst nicht alles auf
einmal fertigstellen.
"""
)

st.code(
    """content/projekte/_vorlage/
├── app.py       # hier entwickelt ihr eure interaktive Analyse
└── projekt.md   # hier könnt ihr Inhalte zunächst in Markdown sammeln""",
    language=None,
)

st.markdown("## Bevor ihr eure App präsentiert")
st.markdown(
    """
- Könnt ihr eure Fragestellung in einem Satz formulieren?
- Ist klar, welche Population, welches Treatment, welches Outcome und welcher
  Estimand euch interessieren?
- Benennt Identifikationsannahmen und Grenzen explizit.
- Erklärt bei jedem Widget, welche wissenschaftliche Aussage ihr damit
  untersuchen möchtet.
- Trennt Ergebnisse von Interpretation und vermeidet kausale Aussagen, die
  das Design nicht trägt.
- Prüft, ob eure App nach einem Neustart noch läuft und alle Daten findet.
"""
)
