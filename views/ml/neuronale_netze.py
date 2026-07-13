"""Kapitel ML: Neuronale Netze.

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
    "Neuronale Netze",
    "Vom einzelnen Neuron zur flexibelsten Modellfamilie der Welt",
)

# ---------------------------------------------------------------- Intro
st.markdown(
    r"""
Ein künstliches **Neuron** ist unspektakulär: Es bildet eine gewichtete Summe
seiner Eingaben und jagt sie durch eine **Aktivierungsfunktion** $\sigma$:

$$
\text{Ausgabe} = \sigma(w_1 x_1 + w_2 x_2 + \dots + w_k x_k + b)
$$

Ohne $\sigma$ wäre das nur eine lineare Funktion — die Aktivierung (z. B.
ReLU: „negative Werte auf null kappen“) bringt den **Knick**, aus dem alles
Weitere folgt. Denn: Schaltet man viele Neuronen in **Schichten**
hintereinander, kann das Netz beliebig komplizierte Funktionen zusammensetzen
(*Universalapproximation*). Beim **Training** stellt Backpropagation die
Gewichte $w$ so ein, dass der Vorhersagefehler sinkt — dasselbe Prinzip
„Fehler minimieren“ wie in Kapitel 1, nur mit Millionen (bei LLMs:
Milliarden) Stellschrauben gleichzeitig.
"""
)

# ------------------------------------------------ Demo: MLP interaktiv
st.markdown("## 🎛️ Demo: Bau dir ein Netz")
st.markdown(
    """
Unten trainiert live ein kleines Netz (Multi-Layer Perceptron) auf den
Mond-Daten aus dem Bäume-Kapitel. Stell **Architektur** und **Aktivierung**
ein und sieh, welche Formen die Entscheidungsgrenze annehmen kann — und wie
die **Lernkurve** (Fehler pro Trainingsrunde) aussieht.
"""
)

regler_schichten, regler_neuronen, regler_aktivierung = st.columns(3)
schichten = regler_schichten.slider("Verborgene Schichten", 1, 3, 1)
neuronen = regler_neuronen.select_slider(
    "Neuronen pro Schicht", options=[2, 4, 8, 16, 32, 64], value=4
)
aktivierung = regler_aktivierung.selectbox(
    "Aktivierungsfunktion", ["relu", "tanh", "logistic"], index=0
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
        title="Lernkurve: Verlust pro Trainingsrunde",
        xaxis_title="Trainingsrunde (Epoche)", yaxis_title="Verlust", height=420,
    )
    st.plotly_chart(fig_verlust, use_container_width=True)

metrik_train, metrik_test = st.columns(2)
metrik_train.metric("Genauigkeit Training", f"{netz.score(X_train, y_train):.1%}")
metrik_test.metric("Genauigkeit Test", f"{netz.score(X_test, y_test):.1%}")

if schichten == 1 and neuronen <= 4:
    st.info(
        "**Klein und ehrlich:** Wenige Neuronen können nur wenige „Knicke“ "
        "bauen — die Grenze bleibt grob. Gib dem Netz mehr Kapazität."
    )
elif schichten >= 2 and neuronen >= 32:
    st.warning(
        "**Viel Kapazität:** Das Netz kann die Monde perfekt umschlingen — "
        "und hat genug Spielraum, auch Rauschen mitzulernen. Vergleiche "
        "Trainings- und Testgenauigkeit: Bekannte Melodie?"
    )

st.markdown(
    """
**Warum Tiefe?** Eine breite flache Schicht *kann* theoretisch alles — aber
tiefe Netze bauen **Hierarchien**: frühe Schichten lernen einfache Muster
(Kanten, Silben), spätere kombinieren sie zu abstrakten Konzepten (Gesichter,
Grammatik). Genau diese Hierarchie plus riesige Datenmengen plus GPUs machte
**Deep Learning** ab ca. 2012 zum Durchbruch — und ist die Grundlage der
**Transformer**-Architektur, aus der LLMs wie GPT gebaut sind.
"""
)

merkkasten(
    "Merke",
    "Neuronale Netze sind extrem flexible Funktionsapproximatoren: Aktivierungs-"
    "Knicke + Schichten = beliebige Formen. Der Preis: Sie brauchen viele Daten, "
    "und niemand kann die Millionen Gewichte direkt <i>lesen</i> — sie sind die "
    "namensgebende <b>Black Box</b> des Explainable-ML-Themas.",
    typ="merke",
)

# ------------------------------------------------------------------ Quiz
quiz(
    "Was passiert, wenn man in einem tiefen Netz alle Aktivierungsfunktionen "
    "durch die Identität (also „keine Aktivierung“) ersetzt?",
    [
        "Nichts — die Tiefe liefert trotzdem Flexibilität",
        "Das Netz kollabiert mathematisch zu einem einzigen linearen Modell",
        "Das Netz kann dann nur noch Klassifikation, keine Regression",
        "Das Training wird unmöglich",
    ],
    richtig=1,
    erklaerung=(
        "Verkettete lineare Funktionen sind wieder linear — egal wie viele "
        "Schichten. Erst die Nichtlinearität der Aktivierung macht aus Tiefe "
        "echte Ausdruckskraft."
    ),
    key="quiz_ml_netze",
)

# -------------------------------------------------------------- Ausblick
st.markdown("## Wie geht's weiter?")
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
        label="Oder: Explainable ML — Black Boxes öffnen",
        icon="🔍",
    )
