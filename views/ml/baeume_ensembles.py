"""Kapitel ML: Bäume & Ensembles.

Entscheidungsbäume interaktiv, Random Forests und Feature Importance —
Grundlage für die Gruppenthemen Explainable ML und Causal ML.
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from utils.ml_demos import entscheidungsgrenze, monde_daten
from utils.theming import FARBEN, kapitel_kopf, merkkasten, quiz

kapitel_kopf(
    "🌲",
    "Bäume & Ensembles",
    "Vorhersagen als Wenn-dann-Regeln — und die Weisheit der vielen Bäume",
)

# ---------------------------------------------------------------- Intro
st.markdown(
    """
Ein **Entscheidungsbaum** stellt Fragen an die Daten, eine nach der anderen:
*Ist das Einkommen über 3 000 €? Ist die Person jünger als 30?* Jede Frage
teilt die Daten in zwei Gruppen — am Ende jedes Astes steht eine Vorhersage.
"""
)

st.graphviz_chart(
    """
digraph {
    bgcolor="transparent";
    node [shape=box, style="rounded,filled", fillcolor="#EEF3FA",
          color="#3E6DB5", fontname="sans-serif"];
    edge [fontname="sans-serif", color="#5C6470", fontsize=11];
    A [label="Einkommen > 3 000 €?"];
    B [label="Schuldenquote < 40 %?"];
    C [label="Bürgschaft vorhanden?"];
    D [label="✅ Kredit", fillcolor="#EDF6F0", color="#4C956C"];
    E [label="❌ kein Kredit", fillcolor="#FCF1E9", color="#E8804C"];
    F [label="✅ Kredit", fillcolor="#EDF6F0", color="#4C956C"];
    G [label="❌ kein Kredit", fillcolor="#FCF1E9", color="#E8804C"];
    A -> B [label="ja"];
    A -> C [label="nein"];
    B -> D [label="ja"];
    B -> E [label="nein"];
    C -> F [label="ja"];
    C -> G [label="nein"];
}
""",
    use_container_width=True,
)

st.markdown(
    """
Der Lernalgorithmus sucht automatisch die Fragen (Splits), die die Klassen am
saubersten trennen. Das macht Bäume herrlich **interpretierbar** — man kann
jede Vorhersage als Regelkette vorlesen. Aber sie haben eine Schwäche, die
dir aus dem Kapitel „Was ist Maschinelles Lernen?“ bekannt vorkommen wird …
"""
)

# --------------------------------------- Demo 1: Baumtiefe & Overfitting
st.markdown("## 🎛️ Demo: Wie tief darf der Baum fragen?")
st.markdown(
    """
Die **Tiefe** eines Baums ist seine Biegsamkeit: Jede zusätzliche Frageebene
erlaubt feinere Aufteilungen. Unten trennt ein Baum zwei verschränkte
Punktwolken („Monde“). Spiel mit der Tiefe und beobachte die
**Entscheidungsgrenze** — und die Lücke zwischen Trainings- und Testgenauigkeit.
"""
)

X, y = monde_daten(n=400, rauschen=0.3)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

tiefe = st.slider("Maximale Baumtiefe", 1, 15, 2)

baum = DecisionTreeClassifier(max_depth=tiefe, random_state=0)
baum.fit(X_train, y_train)

fig_baum = entscheidungsgrenze(baum, X_train, y_train, titel=f"Entscheidungsbaum, Tiefe {tiefe}")
st.plotly_chart(fig_baum, use_container_width=True)

acc_train = baum.score(X_train, y_train)
acc_test = baum.score(X_test, y_test)
metrik_train, metrik_test = st.columns(2)
metrik_train.metric("Genauigkeit Training", f"{acc_train:.1%}")
metrik_test.metric("Genauigkeit Test", f"{acc_test:.1%}")

if tiefe <= 2:
    st.info(
        "**Underfitting:** Wenige kantige Schnitte — die Mondform ist so nicht "
        "zu fassen. Gib dem Baum mehr Tiefe."
    )
elif tiefe >= 8:
    st.warning(
        "**Overfitting:** Der Baum schnitzt Mini-Rechtecke um einzelne "
        "Rausch-Punkte. Trainingsgenauigkeit nahe 100 %, Testgenauigkeit fällt "
        "zurück — dasselbe U-Kurven-Drama wie bei der Polynomregression."
    )

# ---------------------------------------------- Demo 2: Random Forest
st.markdown("## 🌲🌲🌲 Demo: Der Wald ist schlauer als der Baum")
st.markdown(
    """
Die geniale Idee der **Ensembles**: Trainiere viele *unterschiedliche* Bäume
(jeder sieht eine zufällige Stichprobe der Daten und der Features) und lass
sie **abstimmen**. Einzelne Bäume irren wild in verschiedene Richtungen —
im Mittel heben sich die Irrtümer weg. Das ist der **Random Forest**.
"""
)

anzahl_baeume = st.select_slider(
    "Anzahl Bäume im Wald", options=[1, 2, 5, 10, 25, 50, 100, 200], value=1
)


@st.cache_data
def wald_trainieren(n_baeume: int, X_tr, y_tr):
    wald = RandomForestClassifier(n_estimators=n_baeume, random_state=0)
    wald.fit(X_tr, y_tr)
    return wald


@st.cache_data
def wald_lernkurve(X_tr, y_tr, X_te, y_te):
    stufen = [1, 2, 5, 10, 25, 50, 100, 200]
    return stufen, [
        RandomForestClassifier(n_estimators=s, random_state=0)
        .fit(X_tr, y_tr)
        .score(X_te, y_te)
        for s in stufen
    ]


wald = wald_trainieren(anzahl_baeume, X_train, y_train)

spalte_grenze, spalte_kurve = st.columns(2)
with spalte_grenze:
    st.plotly_chart(
        entscheidungsgrenze(
            wald, X_train, y_train, titel=f"Random Forest, {anzahl_baeume} Bäume"
        ),
        use_container_width=True,
    )
with spalte_kurve:
    stufen, genauigkeiten = wald_lernkurve(X_train, y_train, X_test, y_test)
    fig_kurve = go.Figure()
    fig_kurve.add_scatter(
        x=stufen, y=genauigkeiten, mode="lines+markers", name="Testgenauigkeit",
        line=dict(color=FARBEN["wiese"], width=3),
    )
    fig_kurve.add_vline(x=anzahl_baeume, line_dash="dot", line_color=FARBEN["schiefer"])
    fig_kurve.update_layout(
        title="Testgenauigkeit vs. Waldgröße",
        xaxis_title="Anzahl Bäume (log)", xaxis_type="log",
        yaxis_title="Genauigkeit", height=420,
    )
    st.plotly_chart(fig_kurve, use_container_width=True)

st.markdown(
    """
Mit einem Baum: zackige, nervöse Grenze. Mit vielen: **glatt und stabil** —
und die Testgenauigkeit steigt, obwohl jeder Einzelbaum tief (also
overfitting-anfällig) ist. Mittelung senkt **Varianz**, ohne den Bias zu
erhöhen. Verwandte Idee mit anderem Dreh: **Gradient Boosting** baut Bäume
nacheinander, wobei jeder die Fehler des bisherigen Ensembles korrigiert
(XGBoost, LightGBM — die Arbeitspferde auf Tabellendaten).
"""
)

# ------------------------------------------ Demo 3: Feature Importance
st.markdown("## 📊 Demo: Welche Features zählen?")
st.markdown(
    """
Ein Wald aus 200 Bäumen ist keine vorlesbare Regelkette mehr — dafür kann er
verraten, **welche Features seine Vorhersagen am stärksten beeinflussen**
(Feature Importance): Wie oft und wie gewinnbringend wurde über ein Feature
gesplittet? Hier für ein fiktives Kreditausfall-Modell:
"""
)


@st.cache_data
def kredit_importances(seed: int = 5):
    namen = ["Einkommen", "Schuldenquote", "Alter", "Anzahl Kredite", "Kontostand"]
    X_k, y_k = make_classification(
        n_samples=800, n_features=5, n_informative=3, n_redundant=1,
        random_state=seed, shuffle=False,
    )
    wald_k = RandomForestClassifier(n_estimators=200, random_state=0)
    wald_k.fit(X_k, y_k)
    return namen, wald_k.feature_importances_


namen, wichtigkeiten = kredit_importances()
reihenfolge = np.argsort(wichtigkeiten)
fig_imp = go.Figure(
    go.Bar(
        x=wichtigkeiten[reihenfolge],
        y=[namen[i] for i in reihenfolge],
        orientation="h",
        marker_color=FARBEN["gletscher"],
    )
)
fig_imp.update_layout(
    xaxis_title="Feature Importance", height=320, margin=dict(t=20)
)
st.plotly_chart(fig_imp, use_container_width=True)

merkkasten(
    "Achtung — wichtig ≠ ursächlich",
    "Feature Importance sagt: <i>Das Modell nutzt dieses Feature stark für "
    "Vorhersagen.</i> Sie sagt <b>nicht</b>: <i>Dieses Feature verursacht das "
    "Ergebnis.</i> Ein Confounder oder ein bloßes Korrelat kann ganz oben "
    "stehen. Diese Unterscheidung wird im Kapitel Explainable ML und in der "
    "ganzen Kausalitäts-Sektion zentral.",
    typ="achtung",
)

# ------------------------------------------------------------------ Quiz
quiz(
    "Warum overfittet ein Random Forest weniger als ein einzelner tiefer Baum?",
    [
        "Weil jeder Baum im Wald flacher ist als ein Einzelbaum",
        "Weil die Mittelung vieler unterschiedlich irrender Bäume die Varianz senkt",
        "Weil der Wald weniger Features benutzt",
        "Er overfittet nicht weniger — er ist nur schneller",
    ],
    richtig=1,
    erklaerung=(
        "Die Bäume sind einzeln tief und wackelig (hohe Varianz), aber ihre "
        "Fehler sind teils unkorreliert — beim Abstimmen mitteln sie sich weg."
    ),
    key="quiz_ml_baeume",
)

# -------------------------------------------------------------- Ausblick
st.markdown("## Wie geht's weiter?")
weiter_xai, weiter_nn = st.columns(2)
with weiter_xai:
    st.page_link(
        "views/ml/explainable_ml.py",
        label="Weiter: Explainable ML — Black Boxes öffnen",
        icon="🔍",
    )
with weiter_nn:
    st.page_link(
        "views/ml/neuronale_netze.py", label="Oder: Neuronale Netze", icon="🧠"
    )
