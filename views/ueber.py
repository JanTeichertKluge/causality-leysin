"""Über die Akademie: Programm, Ort, Dozenten, Hintergrund."""

import streamlit as st

from utils.theming import kapitel_kopf, merkkasten

kapitel_kopf(
    "ℹ️",
    "Über die Akademie",
    "Künstliche Intelligenz und das „Warum“ — Sommerakademie Leysin 2026",
)

spalte_wann, spalte_wo, spalte_wer = st.columns(3)
spalte_wann.metric("Wann", "18.–27. Aug 2026")
spalte_wo.metric("Wo", "Leysin, Schweiz")
spalte_wer.metric("Träger", "Studienstiftung")

st.markdown("## Die Arbeitsgruppe")
st.markdown(
    """
Die Arbeitsgruppe **„Eine Einführung in Maschinelles Lernen und Kausalität“**
ist Teil der Sommerakademie Leysin der Studienstiftung des deutschen Volkes.
Sie verbindet Statistik, Informatik und Ökonomie zu einer Frage, die
datengetriebene Forschung überall beschäftigt: **Wann dürfen wir aus Daten auf
Ursache und Wirkung schließen?**

KI-Systeme, die Korrelationen mit kausalen Zusammenhängen verwechseln, können
zu schlechten — teils schädlichen — Entscheidungen führen. Wir schauen uns an,
wie solche Verzerrungen entstehen, wie man sie erkennt und mit welchen
Strategien man kausale Parameter aus Daten schätzt. Dazu gehören auch aktuelle
Themen wie die Frage, wie es bei **Large Language Models** um kausales und
logisches Denken steht.
"""
)

st.markdown("## Dozenten")
spalte_os, spalte_jtk = st.columns(2)

with spalte_os, st.container(border=True):
    st.markdown("### Oliver Schacht")
    st.markdown(
        "Universität Hamburg, Lehrstuhl für Statistik mit "
        "wirtschaftswissenschaftlichen Anwendungen."
    )

with spalte_jtk, st.container(border=True):
    st.markdown("### Jan Teichert-Kluge")
    st.markdown(
        "Universität Hamburg, Lehrstuhl für Statistik mit "
        "wirtschaftswissenschaftlichen Anwendungen."
    )

st.markdown("## Voraussetzungen")
st.markdown(
    """
- Interesse an quantitativer Forschung und Datenanalyse
- Grundkenntnisse in Statistik sind hilfreich
- Python-Kenntnisse sind **keine** Voraussetzung — was wir brauchen, lernen wir gemeinsam
"""
)

merkkasten(
    "Offizielle Programminfo",
    'Details zur Akademie gibt es auf der Seite der '
    '<a href="https://www.studienstiftung.de/kalender/programmlinien/detail/26011102" '
    'target="_blank">Studienstiftung des deutschen Volkes</a>.',
    typ="beispiel",
)
