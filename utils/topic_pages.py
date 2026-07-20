"""Generierte Übersichts- und Unterseiten des zentralen Themenkatalogs."""

from __future__ import annotations

import re
from collections.abc import Callable

import streamlit as st

from utils.projects import Projekt, render_markdown_projekt, render_streamlit_projekt
from utils.theming import kapitel_kopf
from utils.topics import Source, Topic

PROJECT_BRIEF = (
    "Verschafft euch mithilfe der Quellen einen wissenschaftlich fundierten "
    "Überblick über das Thema und entwickelt daraus eine klar abgegrenzte "
    "Fragestellung. Vor Ort setzt ihr eine interaktive Streamlit-Anwendung um, "
    "die eine zentrale Methode, Annahme, Anwendung oder Grenze des Themenfeldes "
    "nachvollziehbar untersucht. Die App soll keine vollständige "
    "Lehrbuchdarstellung liefern, sondern ein präzises wissenschaftliches "
    "Argument anhand von Daten, Simulationen oder einer Fallstudie sichtbar machen."
)


def _render_source(source: Source, number: int | None = None) -> None:
    prefix = f"{number}. " if number is not None else ""
    st.markdown(
        f"{prefix}**[{source.title}]({source.url})**  \n"
        f"{source.authors} · {source.description}"
    )


def render_topic(topic: Topic) -> None:
    """Rendert genau den schlanken, kataloggestützten Rahmen eines Tracks."""
    kapitel_kopf(topic.emoji, topic.title, "Euer Einstieg in das Gruppenprojekt")
    if topic.group_members:
        st.caption("Team: " + ", ".join(topic.group_members))
    else:
        st.caption("Euer Team wird vor Ort ergänzt.")

    st.markdown(topic.abstract)
    st.markdown("## Damit könnt ihr starten")
    for number, source in enumerate(topic.required_sources, start=1):
        _render_source(source, number)
    st.markdown("### Wenn ihr noch tiefer einsteigen möchtet")
    _render_source(topic.optional_source)

    st.info(f"**Euer Projekt:** {PROJECT_BRIEF}")
    st.markdown("## Eure interaktive Analyse")

    folder = topic.absolute_project_path
    app_path = folder / "app.py"
    markdown_path = folder / "projekt.md"
    project = Projekt(
        slug=topic.slug,
        titel=topic.title,
        emoji=topic.emoji,
        mitglieder=list(topic.group_members),
        md_datei=markdown_path if markdown_path.exists() else None,
        app_datei=app_path if app_path.exists() else None,
    )
    if project.app_datei is not None:
        render_streamlit_projekt(project)
    elif project.md_datei is not None:
        st.info(
            "Ihr seht momentan eure Markdown-Notizen. Sobald ihr eine `app.py` "
            "anlegt, erscheint hier eure interaktive Analyse."
        )
        render_markdown_projekt(project, show_header=False)
    else:
        st.info(
            "Hier ist Platz für eure Streamlit-App. Kopiert das Team-Template "
            "in den folgenden Arbeitsordner und beginnt mit eurer Fragestellung."
        )
        st.code(topic.project_path, language=None)

    if topic.deepening:
        with st.expander("Passende Vertiefung auf dieser Website"):
            page_map = st.session_state.get("vertiefung_seiten", {})
            for link in topic.deepening:
                st.page_link(page_map.get(link.path, link.path), label=link.label)


def topic_page(topic: Topic) -> Callable[[], None]:
    """Erzeugt eine benannte Render-Funktion für ``st.Page``."""
    def page() -> None:
        render_topic(topic)

    page.__name__ = "thema_" + re.sub(r"\W", "_", topic.slug)
    return page
