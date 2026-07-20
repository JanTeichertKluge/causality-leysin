"""Struktur- und Regressionstests für das Academy-Redesign."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from utils.topics import ROOT, load_topics


EXPECTED_TITLES = [
    "Kausale Effekte in randomisierten Experimenten",
    "Explainable ML / AI",
    "Causality and LLMs",
    "DAGs / SEMs / Causal Discovery",
    "Causal Inference with ML",
    "Natürliche Experimente: RDD / DiD",
    "Bayesian Methods",
    "Sensitivitätsanalysen / Robustheitsprüfungen",
    "Case Study / Eigenes Forschungsprojekt",
]


def test_themenkatalog_hat_neun_vollstaendige_tracks():
    topics = load_topics()
    assert [topic.title for topic in topics] == EXPECTED_TITLES
    assert len({topic.slug for topic in topics}) == 9
    for topic in topics:
        assert len(topic.required_sources) == 2
        assert topic.optional_source.url.startswith("https://")
        assert topic.project_path.startswith("content/projekte/")
        assert topic.abstract


def test_navigation_hat_einfuehrung_gruppen_und_appendix():
    source = (ROOT / "streamlit_app.py").read_text(encoding="utf-8")
    assert '"Für alle · Einführung"' not in source
    assert '"Einführung · Maschinelles Lernen"' in source
    assert '"Einführung · Kausalität"' in source
    assert '"Gruppenprojekte"' in source
    assert '"Appendix"' in source


def test_nur_vier_kapitel_sind_appendix():
    appendix = [
        ROOT / "views/ml/explainable_ml.py",
        ROOT / "views/kausalitaet/quasi_experimente.py",
        ROOT / "views/kausalitaet/bayes.py",
        ROOT / "views/kausalitaet/sem_surveys.py",
    ]
    introduction = [
        ROOT / "views/ml/grundlagen.py",
        ROOT / "views/ml/lineare_regression.py",
        ROOT / "views/ml/regularisierung.py",
        ROOT / "views/ml/baeume_ensembles.py",
        ROOT / "views/ml/neuronale_netze.py",
        ROOT / "views/ml/llms_kausalitaet.py",
        ROOT / "views/kausalitaet/korrelation.py",
        ROOT / "views/kausalitaet/dags_confounding.py",
        ROOT / "views/kausalitaet/potential_outcomes.py",
        ROOT / "views/kausalitaet/kausales_ml.py",
    ]
    assert all("vertiefung_hinweis(" in path.read_text(encoding="utf-8") for path in appendix)
    assert all("einfuehrung_hinweis(" in path.read_text(encoding="utf-8") for path in introduction)
    assert all("vertiefung_hinweis(" not in path.read_text(encoding="utf-8") for path in introduction)


@pytest.mark.parametrize("slug", [topic.slug for topic in load_topics()])
def test_generierte_track_seite_rendert(slug: str):
    def page(topic_slug: str, root: str) -> None:
        import sys
        from pathlib import Path

        import streamlit as st

        if root not in sys.path:
            sys.path.insert(0, root)
        from utils.topic_pages import topic_page
        from utils.topics import load_topics

        topic = next(item for item in load_topics() if item.slug == topic_slug)
        track_page = st.Page(topic_page(topic), title=topic.title, default=True)
        reference_page_map = {
            link.path: st.Page(str(Path(root) / link.path), title=link.label)
            for link in topic.deepening
        }
        reference_pages = list(reference_page_map.values())
        st.session_state["vertiefung_seiten"] = reference_page_map
        sections = {"Track": [track_page]}
        if reference_pages:
            sections["Vertiefung"] = reference_pages
        st.navigation(sections).run()

    at = AppTest.from_function(page, args=(slug, str(ROOT)), default_timeout=30)
    at.run()
    assert not at.exception
    title = next(topic.title for topic in load_topics() if topic.slug == slug)
    assert any(title in block.value for block in at.markdown)


def test_keine_quiz_ui_in_kapiteln_oder_navigation():
    paths = [ROOT / "streamlit_app.py", *sorted((ROOT / "views").rglob("*.py"))]
    source = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert "quiz(" not in source
    assert "Verständnisfrage" not in source


def test_streamlit_template_hat_wissenschaftliche_minimalstruktur():
    template = (ROOT / "content" / "projekte" / "_vorlage" / "app.py").read_text(
        encoding="utf-8"
    )
    for section in (
        "Fragestellung",
        "Wissenschaftlicher Hintergrund",
        "Kausale Annahmen oder Identifikationsproblem",
        "Interaktive Analyse",
        "Ergebnisse",
        "Grenzen",
        "Literatur",
    ):
        assert section in template
    assert "st.set_page_config(" not in template


def test_fehlerhafte_team_app_bleibt_isoliert(tmp_path: Path):
    broken_app = tmp_path / "app.py"
    broken_app.write_text("raise RuntimeError('absichtlicher Teamfehler')", encoding="utf-8")

    def page(app_path: str, root: str) -> None:
        import sys
        from pathlib import Path

        if root not in sys.path:
            sys.path.insert(0, root)
        from utils.projects import Projekt, render_streamlit_projekt

        render_streamlit_projekt(
            Projekt(slug="kaputt", titel="Kaputtes Team", app_datei=Path(app_path))
        )

    at = AppTest.from_function(page, args=(str(broken_app), str(ROOT)))
    at.run()
    assert not at.exception
    assert at.error
