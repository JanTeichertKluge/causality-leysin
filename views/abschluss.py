"""Abschlussfolien der Arbeitsgruppe."""

import streamlit as st

from utils.theming import kapitel_kopf

kapitel_kopf(
    "🎓",
    "Rückblick auf die Akademie",
    "Unser gemeinsamer Weg von den Grundlagen zu den Gruppenprojekten",
)

st.markdown(
    """
Das Deck fasst die Grundlagen, den Weg von kontrollierten Experimenten über
Quasi-Experimente zu Beobachtungsstudien und die Gruppenprojekte zusammen.
"""
)

st.link_button("Reveal.js-Folien öffnen", "slides/abschluss.html", type="primary")
