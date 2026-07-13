"""Kapitel ML: Neural Networks.

Vom Neuron zum Netz, interaktives MLP-Training auf 2D-Daten, Brücke zu
Deep Learning und LLMs.
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from utils.ml_demos import entscheidungsgrenze, monde_daten
from utils.theming import FARBEN, kapitel_kopf, merkkasten, quiz

kapitel_kopf(
    "🧠",
    "Neural Networks",
    "Vom einzelnen Neuron zur flexibelsten Modellfamilie des Machine Learning",
)

# ---------------------------------------------------------------- Intro
st.markdown(
    r"""
Ein künstliches **Neuron** ist mathematisch unspektakulär. Es bildet eine
gewichtete Summe seiner Eingaben und wendet darauf eine
**Activation Function** $\sigma$ an:

$$
\text{Ausgabe} = \sigma(w_1 x_1 + w_2 x_2 + \dots + w_k x_k + b).
$$

Ohne $\sigma$ bliebe dies eine lineare Funktion. Erst die Aktivierung, etwa
die **ReLU**, die negative Werte auf null setzt, führt die entscheidende
Nichtlinearität ein. Schaltet man viele Neuronen in **Layern**
hintereinander, kann das Netz nahezu beliebig komplexe Funktionen
zusammensetzen, dieses Resultat ist als *Universal Approximation Theorem*
bekannt. Beim Training stellt die **Backpropagation** die Gewichte $w$ so
ein, dass der Vorhersagefehler sinkt. Es ist dasselbe Prinzip der
Fehlerminimierung wie in Kapitel 1, nur mit Millionen, bei großen
Sprachmodellen sogar Milliarden von Parametern gleichzeitig.
"""
)

# ------------------------------------------------ Demo: MLP interaktiv
st.markdown("## Demo: Architektur und Decision Boundary")
st.markdown(
    """
In dieser Demo trainiert ein kleines **Multi-Layer Perceptron (MLP)** live
auf den Mond-Daten aus dem Trees-Kapitel. Wähle Architektur und Activation
Function und beobachte, welche Formen die Decision Boundary annehmen kann
und wie die **Loss Curve**, also der Fehler pro Trainingsepoche, verläuft.
"""
)

regler_schichten, regler_neuronen, regler_aktivierung = st.columns(3)
schichten = regler_schichten.slider("Hidden Layers", 1, 3, 1)
neuronen = regler_neuronen.select_slider(
    "Neuronen pro Layer", options=[2, 4, 8, 16, 32, 64], value=4
)
aktivierung = regler_aktivierung.selectbox(
    "Activation Function", ["relu", "tanh", "logistic"], index=0
)

X, y = monde_daten(n=400, rauschen=0.3)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)


@st.cache_data
def netz_trainieren(schichten: int, neuronen: int, aktivierung: str, X_tr, y_tr):
    netz = MLPClassifier(
        hidden_layer_sizes=(neuronen,) * schichten,
        activation=aktivierung,
        max_iter=1500,
        random_state=0,
    )
    netz.fit(X_tr, y_tr)
    return netz


netz = netz_trainieren(schichten, neuronen, aktivierung, X_train, y_train)

spalte_grenze, spalte_verlust = st.columns(2)
with spalte_grenze:
    architektur = " × ".join([str(neuronen)] * schichten)
    st.plotly_chart(
        entscheidungsgrenze(netz, X_train, y_train, titel=f"MLP ({architektur}, {aktivierung})"),
        use_container_width=True,
    )
with spalte_verlust:
    fig_verlust = go.Figure()
    fig_verlust.add_scatter(
        y=netz.loss_curve_, mode="lines", name="Trainingsverlust",
        line=dict(color=FARBEN["beere"], width=3),
    )
    fig_verlust.update_layout(
        title="Loss Curve: Verlust pro Trainingsepoche",
        xaxis_title="Epoche", yaxis_title="Verlust", height=420,
    )
    st.plotly_chart(fig_verlust, use_container_width=True)

metrik_train, metrik_test = st.columns(2)
metrik_train.metric("Genauigkeit Training", f"{netz.score(X_train, y_train):.1%}")
metrik_test.metric("Genauigkeit Test", f"{netz.score(X_test, y_test):.1%}")

if schichten == 1 and neuronen <= 4:
    st.info(
        "**Geringe Kapazität:** Wenige Neuronen erzeugen nur wenige Knicke in "
        "der Decision Boundary, sie bleibt entsprechend grob (Underfitting). "
        "Erhöhe die Kapazität des Netzes."
    )
elif schichten >= 2 and neuronen >= 32:
    st.warning(
        "**Hohe Kapazität:** Das Netz kann die Monde vollständig umschließen "
        "und hat zugleich genug Spielraum, das Rauschen mitzulernen. Der "
        "Vergleich von Trainings- und Testgenauigkeit zeigt die aus Kapitel 1 "
        "bekannte Signatur des Overfittings."
    )

st.markdown(
    """
**Warum Tiefe?** Eine einzelne breite Schicht kann theoretisch jede Funktion
approximieren. Tiefe Netze bauen jedoch **Hierarchien** auf: Frühe Layer
lernen einfache Muster wie Kanten oder Silben, spätere kombinieren sie zu
abstrakten Konzepten wie Gesichtern oder Grammatik. Diese Hierarchiebildung,
verbunden mit großen Datenmengen und leistungsfähigen GPUs, machte
**Deep Learning** ab etwa 2012 zum Durchbruch. Sie ist auch die Grundlage
der **Transformer**-Architektur, auf der moderne Large Language Models
aufbauen.
"""
)

merkkasten(
    "Merke",
    "Neural Networks sind außerordentlich flexible Funktionsapproximatoren: "
    "Nichtlineare Aktivierungen und gestapelte Layer erzeugen nahezu "
    "beliebige Formen. Der Preis dafür: Sie benötigen viele Daten, und "
    "niemand kann die Millionen Gewichte direkt <i>lesen</i>. Sie sind die "
    "namensgebende <b>Black Box</b> des Explainable-ML-Themas.",
    typ="merke",
)

# ------------------------------------------------------------------ Quiz
quiz(
    "Was passiert, wenn man in einem tiefen Netz alle Activation Functions "
    "durch die Identität ersetzt, also auf Aktivierung verzichtet?",
    [
        "Nichts, die Tiefe liefert weiterhin Flexibilität",
        "Das Netz kollabiert mathematisch zu einem einzigen linearen Modell",
        "Das Netz kann dann nur noch Klassifikation, keine Regression",
        "Das Training wird unmöglich",
    ],
    richtig=1,
    erklaerung=(
        "Verkettete lineare Funktionen sind wieder linear, unabhängig von der "
        "Anzahl der Layer. Erst die Nichtlinearität der Aktivierung verleiht "
        "der Tiefe echte Ausdruckskraft."
    ),
    key="quiz_ml_netze",
)

# -------------------------------------------------------------- Ausblick
st.markdown("## Weiterführende Literatur")
st.markdown(
    """
- I. Goodfellow, Y. Bengio & A. Courville (2016), *Deep Learning*, MIT Press, Kap. 6 (frei online)
- M. Nielsen (2015), *Neural Networks and Deep Learning*, Online-Buch (frei online)
"""
)

st.markdown("## Wie geht es weiter?")
weiter_llm, weiter_xai = st.columns(2)
with weiter_llm:
    st.page_link(
        "views/ml/llms_kausalitaet.py",
        label="Weiter: LLMs & kausales Denken",
        icon="💬",
    )
with weiter_xai:
    st.page_link(
        "views/ml/explainable_ml.py",
        label="Oder: Explainable ML",
        icon="🔍",
    )
