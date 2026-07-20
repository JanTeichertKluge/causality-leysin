"""Team-Template: kopieren, fokussieren und mit eigener Analyse ersetzen.

Keine eigene Seitenkonfiguration aufrufen; das übernimmt die Hauptanwendung.
Dateien immer relativ zu ``BASE_DIR`` laden.
"""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st

BASE_DIR = Path(__file__).parent
RNG = np.random.default_rng(2026)

st.markdown("# Projekttitel")
st.caption("Team: Namen ergänzen")

st.markdown("## 1. Fragestellung")
st.markdown("Formuliert eine präzise, empirisch untersuchbare Frage.")

st.markdown("## 2. Wissenschaftlicher Hintergrund")
st.markdown("Ordnet die Frage knapp in die Einstiegsliteratur ein.")

st.markdown("## 3. Kausale Annahmen oder Identifikationsproblem")
st.warning(
    "Benennt Population, Treatment, Outcome und Estimand sowie die Annahmen, "
    "unter denen eure Analyse kausal interpretiert werden darf."
)

st.markdown("## 4. Interaktive Analyse")
assumption_strength = st.slider(
    "Beispielparameter – durch einen wissenschaftlich relevanten Regler ersetzen",
    0.0,
    1.0,
    0.5,
)
x = np.linspace(0, 1, 100)
y = assumption_strength * x
figure = go.Figure(go.Scatter(x=x, y=y, mode="lines"))
figure.update_layout(xaxis_title="x", yaxis_title="simuliertes Ergebnis")
st.plotly_chart(figure, use_container_width=True)
st.caption("Erklärt direkt am Widget, welche wissenschaftliche Aussage es illustriert.")

st.markdown("## 5. Ergebnisse")
st.markdown("Berichtet zentrale Resultate, inklusive relevanter Unsicherheit.")

st.markdown("## 6. Grenzen")
st.markdown("Trennt Daten-, Modell- und Identifikationsgrenzen.")

st.markdown("## 7. Literatur")
st.markdown("- Vollständige, überprüfbare Literaturangaben ergänzen.")
