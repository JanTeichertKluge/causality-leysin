"""Themen der Gruppenarbeiten: 9 Themen mit Abstracts und Vorbereitungs-Links."""

import streamlit as st

from utils.theming import kapitel_kopf, merkkasten

kapitel_kopf(
    "🧭",
    "Themen der Gruppenarbeiten",
    "Neun Richtungen und die Kapitel, die dich darauf vorbereiten",
)

st.markdown(
    """
Während der Akademie bearbeitet ihr in Gruppen eines dieser Themen in Python.
Zu jedem Thema findest du hier den Abstract und die Kapitel dieser Website,
die dich am besten darauf vorbereiten. Alle Wege führen über die beiden
Grundlagenkapitel, danach kannst du gezielt vertiefen.
"""
)

THEMEN = [
    {
        "emoji": "🏥",
        "titel": "Randomisierte Experimente / Medizin",
        "abstract": (
            "Design und Analyse randomisierter kontrollierter Studien (RCTs) "
            "mit Fokus auf den klinischen Kontext, den methodischen Umgang "
            "mit Non-Compliance und die Auswertung experimenteller Daten in "
            "der medizinischen Forschung."
        ),
        "links": [
            ("views/kausalitaet/potential_outcomes.py", "Potential Outcomes & RCTs", "⚖️"),
            ("views/kausalitaet/korrelation.py", "Korrelation ≠ Kausalität", "🔀"),
        ],
    },
    {
        "emoji": "🔍",
        "titel": "Explainable ML / AI",
        "abstract": (
            "Methoden zur Interpretation komplexer „Black-Box“-Modelle "
            "(z. B. SHAP, LIME) und die Analyse des grundlegenden Trade-offs "
            "zwischen prädiktiver Performanz und algorithmischer Transparenz."
        ),
        "links": [
            ("views/ml/explainable_ml.py", "Explainable ML", "🔍"),
            ("views/ml/baeume_ensembles.py", "Trees & Ensembles", "🌲"),
        ],
    },
    {
        "emoji": "💬",
        "titel": "Causality and LLMs",
        "abstract": (
            "Die Schnittstelle von generativer KI und Kausalität: "
            "Einsatzmöglichkeiten von LLMs für Causal Reasoning, Causal "
            "Discovery oder die Kontrolle von Confounding in unstrukturierten "
            "Textdaten."
        ),
        "links": [
            ("views/ml/llms_kausalitaet.py", "LLMs & kausales Denken", "💬"),
            ("views/kausalitaet/dags_confounding.py", "DAGs & Confounding", "🕸️"),
        ],
    },
    {
        "emoji": "🕸️",
        "titel": "DAGs / Causal Discovery",
        "abstract": (
            "Grafische Modelle (Directed Acyclic Graphs) und algorithmische "
            "Verfahren zur datengetriebenen Identifikation zugrundeliegender "
            "kausaler Strukturen und valider Kausalpfade direkt aus "
            "Beobachtungsdaten."
        ),
        "links": [
            ("views/kausalitaet/dags_confounding.py", "DAGs & Confounding", "🕸️"),
            ("views/kausalitaet/korrelation.py", "Korrelation ≠ Kausalität", "🔀"),
        ],
    },
    {
        "emoji": "🎯",
        "titel": "Causal Inference with ML",
        "abstract": (
            "Nutzung flexibler Machine-Learning-Algorithmen zur Schätzung "
            "kausaler Effekte in hochdimensionalen Settings, einschließlich "
            "Frameworks wie Double/Debiased Machine Learning."
        ),
        "links": [
            ("views/kausalitaet/kausales_ml.py", "Kausales Machine Learning", "🎯"),
            ("views/ml/baeume_ensembles.py", "Trees & Ensembles", "🌲"),
        ],
    },
    {
        "emoji": "📐",
        "titel": "Tools: RDD / DiD",
        "abstract": (
            "Quasi-experimentelle ökonometrische Designs wie "
            "Difference-in-Differences und Regression Discontinuity Design "
            "zur Schätzung valider kausaler Effekte aus Paneldaten oder bei "
            "exogenen Schwellenwerten (Policy Cutoffs)."
        ),
        "links": [
            ("views/kausalitaet/quasi_experimente.py", "Quasi-Experimente: DiD & RDD", "📐"),
            ("views/kausalitaet/potential_outcomes.py", "Potential Outcomes & RCTs", "⚖️"),
        ],
    },
    {
        "emoji": "🎲",
        "titel": "Bayesian Methods",
        "abstract": (
            "Probabilistische Inferenzansätze zur Integration von Vorwissen "
            "(Priors), zur Aktualisierung von Wahrscheinlichkeiten über "
            "Posteriori-Verteilungen und zur Anwendung bayesianischer "
            "Konzepte auf kausale Modellierungen."
        ),
        "links": [
            ("views/kausalitaet/bayes.py", "Bayesian Methods", "🎲"),
            ("views/kausalitaet/potential_outcomes.py", "Potential Outcomes & RCTs", "⚖️"),
        ],
    },
    {
        "emoji": "📚",
        "titel": "Examples / Case Studies",
        "abstract": (
            "Angewandte, praxisnahe Replikation und kritische methodische "
            "Analyse prominenter Paper im Bereich Causal Inference sowie die "
            "Übertragung theoretischer Ansätze auf reale Datensätze."
        ),
        "links": [
            ("views/kausalitaet/korrelation.py", "Korrelation ≠ Kausalität", "🔀"),
            ("views/kausalitaet/quasi_experimente.py", "Quasi-Experimente: DiD & RDD", "📐"),
            ("views/kausalitaet/potential_outcomes.py", "Potential Outcomes & RCTs", "⚖️"),
        ],
    },
    {
        "emoji": "📝",
        "titel": "SEMs / Eigene Experimente & Surveys",
        "abstract": (
            "Formulierung von Strukturgleichungsmodellen (SEMs) zur "
            "Evaluierung komplexer multivariater Zusammenhänge, kombiniert "
            "mit dem praktischen Design, der Implementierung und der "
            "Auswertung eigener Survey-Experimente."
        ),
        "links": [
            ("views/kausalitaet/sem_surveys.py", "SEMs & Survey Experiments", "📋"),
            ("views/kausalitaet/dags_confounding.py", "DAGs & Confounding", "🕸️"),
        ],
    },
]

for zeile_start in range(0, len(THEMEN), 2):
    spalten = st.columns(2)
    for spalte, thema in zip(spalten, THEMEN[zeile_start : zeile_start + 2]):
        with spalte, st.container(border=True):
            st.markdown(f"### {thema['emoji']} {thema['titel']}")
            st.markdown(thema["abstract"])
            st.markdown("**Zur Vorbereitung:**")
            for pfad, label, icon in thema["links"]:
                st.page_link(pfad, label=label, icon=icon)

merkkasten(
    "Und dann?",
    "Sobald eure Gruppe loslegt, bekommt ihr eine eigene Seite auf dieser "
    "Website. Wie das geht, steht in der Projektübersicht.",
    typ="definition",
)

st.page_link("views/projekte/uebersicht.py", label="Zur Projektübersicht", icon="🗂️")
