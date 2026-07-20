"""Einführender Brückenschlag zwischen flexiblem ML und Kausalinferenz."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from sklearn.ensemble import RandomForestRegressor

from utils.theming import (
    FARBEN,
    einfuehrung_hinweis,
    kapitel_kopf,
    lehrpfad_kontext,
    merkkasten,
)

kapitel_kopf(
    "🎯",
    "Kausales Machine Learning",
    "Was flexibles ML nach der Identifikation leisten kann – und was nicht",
)

einfuehrung_hinweis("25–35 Minuten", [
    "Prediction, Confounder-Adjustierung und Effektschätzung auseinanderhalten",
    "flexible Residualisierung als Grundidee von Double Machine Learning einordnen",
])

lehrpfad_kontext(
    "Welche Rolle kann flexibles ML spielen, nachdem der kausale Estimand identifiziert ist?",
    "Verbinde das Partialling-Out aus der linearen Regression mit der Confounder-Adjustierung aus dem Kausalitätsteil.",
    "Nimm die Residualisierung als Grundidee mit. DML-Theorie, Learner-Wahl, Inferenz und heterogene Effekte kannst du im Gruppenprojekt untersuchen.",
)

st.markdown(
    r"""
In den bisherigen Kapiteln kamen zwei Aufgaben getrennt vor: Machine Learning
lernt flexible Vorhersagefunktionen; Kausalinferenz definiert einen Estimand
und begründet, unter welchen Annahmen er identifiziert ist. **Kausales Machine
Learning** verbindet beide Aufgaben, ersetzt aber die Identifikationsannahmen
nicht durch einen Algorithmus.

Angenommen, $D$ ist ein Treatment, $Y$ das Outcome und $X$ eine möglicherweise
große Menge beobachteter Confounder. Ein partiell lineares Modell schreibt

$$Y = \tau D + g(X) + \varepsilon.$$

Der Zielparameter ist $\tau$; die unbekannte Funktion $g(X)$ ist nur eine
Stör- oder **Nuisance-Funktion**. Flexible Modelle können diese Funktion
lernen. Der kausale Gehalt kommt dagegen aus der Annahme, dass nach Kontrolle
von $X$ kein relevantes Confounding verbleibt.
"""
)

merkkasten(
    "Reihenfolge der Argumente",
    "Zuerst kommen <b>Fragestellung, Estimand und Identifikation</b>. Erst "
    "danach entscheidet man, ob ML bei der Schätzung unbekannter Funktionen "
    "hilft. Gute Vorhersagegüte kann fehlende Confounder nicht reparieren.",
    typ="achtung",
)

st.markdown("## Simulation: lineare oder flexible Adjustierung?")
st.markdown(
    """
In den simulierten Daten beeinflussen fünf Variablen sowohl Treatment als
auch Outcome – teilweise nichtlinear. Verglichen werden ein naiver
Treatment-Vergleich, eine lineare Adjustierung und eine flexible
Residualisierung. Letztere ist eine **Vorschau** auf Double Machine Learning,
kein vollständiges Rezept.
"""
)

tau_column, confounding_column, sample_column = st.columns([2, 2, 1])
tau = tau_column.slider("Wahrer Effekt τ", 0.0, 2.0, 1.0, step=0.1)
gamma = confounding_column.slider("Stärke des Confoundings γ", 0.0, 2.0, 1.0, step=0.1)
with sample_column:
    st.markdown("&nbsp;")
    if st.button("Neue Stichprobe"):
        st.session_state["causal_ml_seed"] = st.session_state.get("causal_ml_seed", 0) + 1
seed = st.session_state.get("causal_ml_seed", 0)


@st.cache_data
def estimator_comparison(tau: float, gamma: float, seed: int, n: int = 1200):
    rng = np.random.default_rng(seed)
    features = rng.uniform(-2, 2, size=(n, 5))
    confounding = (
        2 * np.sin(features[:, 0]) + 0.5 * features[:, 1] ** 2 + features[:, 2]
    )
    treatment = gamma * confounding + rng.normal(0, 1, n)
    outcome = tau * treatment + gamma * confounding + rng.normal(0, 1, n)

    naive = np.polyfit(treatment, outcome, 1)[0]
    linear_design = np.column_stack([treatment, features, np.ones(n)])
    linear = np.linalg.lstsq(linear_design, outcome, rcond=None)[0][0]

    half = n // 2
    folds = [
        (np.arange(half), np.arange(half, n)),
        (np.arange(half, n), np.arange(half)),
    ]
    residual_outcome = np.zeros(n)
    residual_treatment = np.zeros(n)
    for train, test in folds:
        outcome_model = RandomForestRegressor(
            n_estimators=160, max_depth=8, random_state=0
        )
        treatment_model = RandomForestRegressor(
            n_estimators=160, max_depth=8, random_state=0
        )
        outcome_model.fit(features[train], outcome[train])
        treatment_model.fit(features[train], treatment[train])
        residual_outcome[test] = outcome[test] - outcome_model.predict(features[test])
        residual_treatment[test] = treatment[test] - treatment_model.predict(features[test])
    flexible = np.polyfit(residual_treatment, residual_outcome, 1)[0]
    return naive, linear, flexible


naive, linear, flexible = estimator_comparison(tau, gamma, seed)
figure = go.Figure()
figure.add_bar(
    x=["Naiv", "Linear adjustiert", "Flexibel residualisiert"],
    y=[naive, linear, flexible],
    marker_color=[FARBEN["beere"], FARBEN["sonne"], FARBEN["wiese"]],
    text=[f"{naive:.2f}", f"{linear:.2f}", f"{flexible:.2f}"],
    textposition="outside",
)
figure.add_hline(
    y=tau,
    line_dash="dash",
    line_color=FARBEN["schiefer"],
    annotation_text=f"wahrer Effekt τ = {tau:.1f}",
)
figure.update_layout(yaxis_title="geschätzter Effekt", height=410)
st.plotly_chart(figure, use_container_width=True)

st.markdown(
    """
Die Simulation illustriert eine begrenzte Aussage: Wenn Confounding
nichtlinear von beobachteten Merkmalen abhängt, kann eine flexible
Störfunktionsschätzung weniger Modellmissspezifikation aufweisen als eine rein
lineare. Daraus folgt noch keine allgemeine Überlegenheit. Das Ergebnis hängt
von Stichprobengröße, Overfitting, Learner-Wahl, Cross-Fitting und den
Identifikationsannahmen ab.
"""
)

st.markdown("## Was das Gruppenprojekt selbst entscheiden muss")
st.markdown(
    """
- Welches DML- oder Meta-Learner-Framework passt zum Estimand?
- Wie werden Learner und Hyperparameter gewählt, ohne die Effektschätzung zu verzerren?
- Wie entstehen gültige Standardfehler und Konfidenzintervalle?
- Soll ein Durchschnittseffekt oder Treatment-Effect-Heterogenität untersucht werden?
- Welche Sensitivitätsanalyse adressiert verbleibendes unbeobachtetes Confounding?
"""
)

team_page = st.session_state.get("themen_seiten", {}).get("causal-inference-with-ml")
if team_page is not None:
    st.page_link(team_page, label="Zum Projekttrack Causal Inference with ML", icon="🎯")

st.markdown("## Weiterführende Literatur")
st.markdown(
    """
- V. Chernozhukov et al. (2018), *Double/Debiased Machine Learning for Treatment and Structural Parameters*
- P. Bach et al. (2022), *DoubleML: An Object-Oriented Implementation of Double Machine Learning in Python*
- M. Huber (2023), *Causal Analysis*
"""
)
