"""Musterkapitel ML: Was ist Maschinelles Lernen?

Interaktive Einführung in Supervised Learning, Modellkomplexität und
Overfitting anhand einer Polynomregression.
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

from utils.theming import FARBEN, kapitel_kopf, merkkasten, quiz

kapitel_kopf(
    "🤖",
    "Was ist Maschinelles Lernen?",
    "Lernen aus Beispielen — und warum auswendig lernen nicht reicht",
)

# ---------------------------------------------------------------- Intro
st.markdown(
    """
Klassische Programme folgen Regeln, die ein Mensch aufgeschrieben hat:
*Wenn X, dann Y.* Beim **Maschinellen Lernen (ML)** drehen wir das um —
wir geben dem Computer **Beispiele** und lassen ihn die Regeln selbst finden.

Beim **Supervised Learning** (überwachtes Lernen) besteht jedes Beispiel aus:

- **Features** $x$: das, was wir beobachten (z. B. Wohnfläche, Lage, Baujahr)
- **Label** $y$: das, was wir vorhersagen wollen (z. B. die Miete)

Das Modell sucht eine Funktion $\\hat{f}$, sodass $\\hat{f}(x) \\approx y$ —
auch für **neue** Wohnungen, die es beim Lernen nie gesehen hat. Genau dieser
letzte Halbsatz ist der Kern von allem, was jetzt kommt.
"""
)

merkkasten(
    "Definition",
    "<b>Maschinelles Lernen</b> heißt: aus Beispieldaten eine Funktion lernen, "
    "die auch auf <b>ungesehenen</b> Daten gute Vorhersagen macht. "
    "Das Ziel ist Verallgemeinerung — nicht Auswendiglernen.",
    typ="definition",
)

# ---------------------------------------------- Demo 1: Polynomregression
st.markdown("## 🎛️ Demo: Lernen heißt Kurven anpassen")
st.markdown(
    """
Unten siehst du Datenpunkte, die von einem **wahren Zusammenhang** (gestrichelte
Linie) plus Zufallsrauschen erzeugt wurden — in echten Daten kennen wir diese
Linie natürlich nie. Wir teilen die Punkte in **Trainingsdaten** (daran lernt
das Modell) und **Testdaten** (die hält das Modell nie zu Gesicht — unser
Ehrlichkeits-Check).

Deine Aufgabe: Wähle den **Polynomgrad** — also wie „biegsam“ die gelernte
Kurve sein darf — und beobachte, was mit Trainings- und Testfehler passiert.
"""
)


def wahre_funktion(x: np.ndarray) -> np.ndarray:
    return np.sin(2 * np.pi * x)


@st.cache_data
def daten_erzeugen(n: int, rauschen: float, seed: int):
    rng = np.random.default_rng(seed)
    x = np.sort(rng.uniform(0, 1, n))
    y = wahre_funktion(x) + rng.normal(0, rauschen, n)
    return x, y


if "ml_seed" not in st.session_state:
    st.session_state.ml_seed = 2026

regler_grad, regler_n, regler_rauschen, knopf = st.columns([2, 2, 2, 1])
grad = regler_grad.slider("Polynomgrad (Biegsamkeit)", 1, 15, 1)
n = regler_n.slider("Anzahl Datenpunkte", 20, 300, 60, step=20)
rauschen = regler_rauschen.slider("Rauschen", 0.05, 1.0, 0.3, step=0.05)
with knopf:
    st.markdown("&nbsp;")
    if st.button("🎲 Neue Daten"):
        st.session_state.ml_seed += 1

x, y = daten_erzeugen(n, rauschen, st.session_state.ml_seed)
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=0
)

modell = make_pipeline(PolynomialFeatures(grad), LinearRegression())
modell.fit(x_train.reshape(-1, 1), y_train)

raster = np.linspace(0, 1, 300)
vorhersage = modell.predict(raster.reshape(-1, 1))
mse_train = mean_squared_error(y_train, modell.predict(x_train.reshape(-1, 1)))
mse_test = mean_squared_error(y_test, modell.predict(x_test.reshape(-1, 1)))

fig = go.Figure()
fig.add_scatter(
    x=x_train, y=y_train, mode="markers", name="Trainingsdaten",
    marker=dict(color=FARBEN["gletscher"], size=8, opacity=0.8),
)
fig.add_scatter(
    x=x_test, y=y_test, mode="markers", name="Testdaten",
    marker=dict(color=FARBEN["sonne"], size=8, symbol="diamond", opacity=0.9),
)
fig.add_scatter(
    x=raster, y=wahre_funktion(raster), mode="lines", name="Wahrer Zusammenhang",
    line=dict(color=FARBEN["schiefer"], dash="dash", width=2),
)
fig.add_scatter(
    x=raster, y=vorhersage, mode="lines", name=f"Gelerntes Modell (Grad {grad})",
    line=dict(color=FARBEN["nacht"], width=3),
)
fig.update_layout(
    yaxis=dict(range=[-2.5, 2.5]), xaxis_title="Feature x", yaxis_title="Label y",
    height=440,
)
st.plotly_chart(fig, use_container_width=True)

metrik_train, metrik_test = st.columns(2)
metrik_train.metric("Fehler auf Trainingsdaten (MSE)", f"{mse_train:.3f}")
metrik_test.metric("Fehler auf Testdaten (MSE)", f"{mse_test:.3f}")

if grad <= 2:
    st.info(
        "**Underfitting:** Die Kurve ist zu starr, um den wahren Zusammenhang "
        "zu treffen — beide Fehler bleiben hoch. Probier einen höheren Grad!"
    )
elif grad >= 9:
    st.warning(
        "**Overfitting:** Die Kurve schlängelt sich durch jeden Trainingspunkt — "
        "sie lernt das Rauschen auswendig. Trainingsfehler winzig, Testfehler "
        "explodiert. Drück auch mal auf „🎲 Neue Daten“: die gelernte Kurve "
        "ändert sich drastisch, obwohl der wahre Zusammenhang gleich bleibt."
    )

# ------------------------------------- Demo 2: Fehler über alle Grade
st.markdown("## 📉 Der ganze Verlauf: Trainings- vs. Testfehler")
st.markdown(
    """
Statt einzelne Grade durchzuprobieren, zeichnen wir beide Fehler für **alle**
Grade von 1 bis 15. Es entsteht das wohl wichtigste Bild des Maschinellen
Lernens: Der Trainingsfehler sinkt immer weiter — der Testfehler bildet ein
**U**. Links Underfitting, rechts Overfitting, dazwischen der Sweet Spot.
"""
)


@st.cache_data
def fehlerkurven(x_tr, y_tr, x_te, y_te, max_grad: int = 15):
    grade = list(range(1, max_grad + 1))
    train_fehler, test_fehler = [], []
    for g in grade:
        m = make_pipeline(PolynomialFeatures(g), LinearRegression())
        m.fit(x_tr.reshape(-1, 1), y_tr)
        train_fehler.append(mean_squared_error(y_tr, m.predict(x_tr.reshape(-1, 1))))
        test_fehler.append(mean_squared_error(y_te, m.predict(x_te.reshape(-1, 1))))
    return grade, train_fehler, test_fehler


grade, train_fehler, test_fehler = fehlerkurven(x_train, y_train, x_test, y_test)
bester_grad = grade[int(np.argmin(test_fehler))]

fig_fehler = go.Figure()
fig_fehler.add_scatter(
    x=grade, y=train_fehler, mode="lines+markers", name="Trainingsfehler",
    line=dict(color=FARBEN["gletscher"], width=3),
)
fig_fehler.add_scatter(
    x=grade, y=test_fehler, mode="lines+markers", name="Testfehler",
    line=dict(color=FARBEN["sonne"], width=3),
)
fig_fehler.add_vline(
    x=grad, line_dash="dot", line_color=FARBEN["schiefer"],
    annotation_text="dein Grad", annotation_position="top",
)
fig_fehler.add_vline(
    x=bester_grad, line_dash="dash", line_color=FARBEN["wiese"],
    annotation_text="bester Testfehler", annotation_position="top right",
)
fig_fehler.update_layout(
    xaxis_title="Polynomgrad", yaxis_title="MSE (log-Skala)",
    yaxis_type="log", height=400,
)
st.plotly_chart(fig_fehler, use_container_width=True)

merkkasten(
    "Merke",
    "Ein Modell ist so gut wie sein Fehler auf <b>ungesehenen</b> Daten. "
    "Mehr Flexibilität senkt den Trainingsfehler immer — den Testfehler nur "
    "bis zu einem Punkt. Danach lernt das Modell Rauschen statt Struktur "
    "(<b>Bias-Variance-Tradeoff</b>).",
    typ="merke",
)

# ------------------------------------------------------------------ Quiz
quiz(
    "Ein Modell erreicht fast null Fehler auf den Trainingsdaten, aber einen "
    "riesigen Fehler auf den Testdaten. Was liegt vor?",
    [
        "Underfitting — das Modell ist zu simpel",
        "Overfitting — das Modell hat das Rauschen auswendig gelernt",
        "Perfektes Modell — Trainingsfehler null ist das Ziel",
        "Datenfehler — so etwas kann bei sauberen Daten nicht passieren",
    ],
    richtig=1,
    erklaerung=(
        "Null Trainingsfehler bei hohem Testfehler ist das Markenzeichen von "
        "Overfitting: Das Modell verallgemeinert nicht, es erinnert sich nur."
    ),
    key="quiz_ml_grundlagen",
)

# -------------------------------------------------------------- Ausblick
st.markdown("## Wie geht's weiter?")
st.markdown(
    """
Polynome von Hand wählen ist nur der Anfang. In den nächsten Kapiteln lernst
du Modelle kennen, die ihre Flexibilität cleverer einsetzen — und am Ende die
Frage, die dieses ganze Projekt antreibt: Ein Modell, das perfekt
**vorhersagt**, weiß noch lange nicht, **warum** etwas passiert.
"""
)
weiter_ml, weiter_kausal = st.columns(2)
with weiter_ml:
    st.page_link(
        "views/ml/baeume_ensembles.py", label="Weiter: Bäume & Ensembles", icon="🌲"
    )
with weiter_kausal:
    st.page_link(
        "views/kausalitaet/korrelation.py",
        label="Oder direkt: Korrelation ≠ Kausalität",
        icon="🔀",
    )
