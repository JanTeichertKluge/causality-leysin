"""Katalogübersicht der neun Gruppenprojekte."""

import streamlit as st

from utils.theming import kapitel_kopf
from utils.topics import load_topics

kapitel_kopf(
    "🧭",
    "Neun Projekt-Tracks",
    "Findet den Track, in den ihr gemeinsam einsteigen möchtet",
)

st.markdown(
    """
Lest zuerst die Kurzbeschreibungen und öffnet die Tracks, die euch
interessieren. Dort findet ihr zwei Einstiegsquellen, eine optionale
Vertiefung und den Arbeitsbereich für eure Gruppe. Ihr müsst das Thema an
dieser Stelle noch nicht vollständig beherrschen – sucht zunächst eine
Richtung, über die ihr mehr herausfinden möchtet.
"""
)

topics = load_topics()
page_map = st.session_state.get("themen_seiten", {})
for row_start in range(0, len(topics), 3):
    columns = st.columns(3)
    for column, topic in zip(columns, topics[row_start : row_start + 3]):
        with column, st.container(border=True):
            st.markdown(f"### {topic.emoji} {topic.title}")
            st.markdown(topic.abstract)
            page = page_map.get(topic.slug)
            if page is not None:
                st.page_link(page, label="Thema und Quellen öffnen", icon="▶️")

st.page_link(
    "views/projekte/uebersicht.py",
    label="So arbeitet ihr an eurem Projekt",
    icon="🛠️",
)
