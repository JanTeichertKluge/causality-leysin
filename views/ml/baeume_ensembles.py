"""Kapitel ML: Trees & Ensembles.

Decision Trees interaktiv, Random Forests und Feature Importance als
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
    "Trees & Ensembles",
    "Vorhersagen als Wenn-dann-Regeln und die Stärke der Aggregation",
)

# ---------------------------------------------------------------- Intro
st.markdown(
    """
Ein **Decision Tree** stellt nacheinander Fragen an die Daten: Liegt das
Einkommen über 3 000 €? Ist die Person jünger als 30? Jede Frage teilt die
Daten in zwei Gruppen, und am Ende jedes Astes steht eine Vorhersage. Je
nach Zielgröße spricht man von **Classification Trees** (kategoriales Label)
oder **Regression Trees** (stetiges Label).
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
    D [label="Kredit", fillcolor="#EDF6F0", color="#4C956C"];
    E [label="kein Kredit", fillcolor="#FCF1E9", color="#E8804C"];
    F [label="Kredit", fillcolor="#EDF6F0", color="#4C956C"];
    G [label="kein Kredit", fillcolor="#FCF1E9", color="#E8804C"];
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
Der Lernalgorithmus wählt die Splits automatisch: In jedem Knoten sucht er
die Frage, die die Klassen am besten trennt (gemessen etwa an der
Gini-Impurity), und unterteilt rekursiv weiter. Das macht Decision Trees
außerordentlich **interpretierbar**, denn jede Vorhersage lässt sich als
Regelkette vorlesen. Zugleich haben sie eine Schwäche, die dir aus dem
Kapitel „Was ist Maschinelles Lernen?“ vertraut vorkommen dürfte.
"""
)

# --------------------------------------- Demo 1: Baumtiefe & Overfitting
st.markdown("## Demo: Tiefe des Trees und Overfitting")
st.markdown(
    """
Die maximale **Tiefe** eines Decision Trees bestimmt seine Flexibilität,
denn jede zusätzliche Frageebene erlaubt feinere Aufteilungen des
Feature-Raums. In der Abbildung trennt ein Classification Tree zwei
ineinander verschränkte Punktwolken. Variiere die Tiefe und beobachte
sowohl die **Decision Boundary** als auch die Lücke zwischen Trainings- und
Testgenauigkeit.
"""
)

X, y = monde_daten(n=400, rauschen=0.3)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

tiefe = st.slider("Maximale Tiefe (max_depth)", 1, 15, 2)

baum = DecisionTreeClassifier(max_depth=tiefe, random_state=0)
baum.fit(X_train, y_train)

fig_baum = entscheidungsgrenze(baum, X_train, y_train, titel=f"Decision Tree, Tiefe {tiefe}")
st.plotly_chart(fig_baum, use_container_width=True)

acc_train = baum.score(X_train, y_train)
acc_test = baum.score(X_test, y_test)
metrik_train, metrik_test = st.columns(2)
metrik_train.metric("Genauigkeit Training", f"{acc_train:.1%}")
metrik_test.metric("Genauigkeit Test", f"{acc_test:.1%}")

if tiefe <= 2:
    st.info(
        "**Underfitting:** Wenige achsenparallele Schnitte können die "
        "Mondform nicht abbilden. Erhöhe die Tiefe des Trees."
    )
elif tiefe >= 8:
    st.warning(
        "**Overfitting:** Der Tree bildet kleinste Regionen um einzelne "
        "Rauschpunkte. Die Trainingsgenauigkeit nähert sich 100 %, während "
        "die Testgenauigkeit zurückfällt. Es ist dieselbe Systematik wie bei "
        "der Polynomregression."
    )

# ---------------------------------------------- Demo 2: Random Forest
st.markdown("## Demo: Vom Tree zum Random Forest")
st.markdown(
    r"""
Die zentrale Idee der **Ensembles** besteht darin, viele *unterschiedliche*
Trees zu trainieren, jeden auf einer Bootstrap-Stichprobe der Daten und mit
zufälliger Feature-Auswahl je Split, und ihre Vorhersagen per
Mehrheitsentscheid zu aggregieren. Das Ergebnis ist der **Random Forest**.
Warum die Aggregation hilft, zeigt eine kurze Rechnung. Für $B$ Schätzer mit
Varianz $\sigma^2$ und paarweiser Korrelation $\rho$ gilt

$$
\mathrm{Var}\!\left(\frac{1}{B}\sum_{b=1}^{B} \hat{f}_b(x)\right)
= \rho\,\sigma^2 + \frac{1-\rho}{B}\,\sigma^2 .
$$

Der zweite Term verschwindet mit wachsender Ensemblegröße $B$, übrig bleibt
allein der korrelierte Anteil $\rho\,\sigma^2$. Genau deshalb dekorreliert
der Random Forest seine Trees durch doppelte Zufälligkeit in Daten *und*
Features: Je kleiner $\rho$, desto stärker die Varianzreduktion, und das bei
unverändertem Bias.
"""
)

anzahl_baeume = st.select_slider(
    "Anzahl Trees (n_estimators)", options=[1, 2, 5, 10, 25, 50, 100, 200], value=1
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
            wald, X_train, y_train, titel=f"Random Forest, {anzahl_baeume} Trees"
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
        title="Testgenauigkeit über die Anzahl Trees",
        xaxis_title="Anzahl Trees (log)", xaxis_type="log",
        yaxis_title="Genauigkeit", height=420,
    )
    st.plotly_chart(fig_kurve, use_container_width=True)

st.markdown(
    """
Mit einem einzelnen Tree ist die Decision Boundary zerklüftet und instabil.
Mit vielen Trees wird sie glatt, und die Testgenauigkeit steigt, obwohl
jeder einzelne Tree tief und damit anfällig für Overfitting ist. Eine
verwandte Ensemble-Strategie ist das **Gradient Boosting**: Dort werden
Trees sequenziell trainiert, wobei jeder die Residuen des bisherigen
Ensembles korrigiert. Die bekanntesten Implementierungen, XGBoost und
LightGBM, gelten auf tabellarischen Daten häufig als Stand der Technik.
"""
)

# ------------------------------------------ Demo 3: Feature Importance
st.markdown("## Demo: Feature Importance")
st.markdown(
    """
Ein Random Forest aus 200 Trees ist keine vorlesbare Regelkette mehr. Er
kann jedoch ausweisen, welche Features seine Vorhersagen am stärksten
beeinflussen (**Feature Importance**): Wie oft und mit welchem Gewinn an
Trennschärfe wurde über ein Feature gesplittet? Die folgende Abbildung
zeigt dies für ein fiktives Kreditausfall-Modell.
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
    "Achtung: wichtig ist nicht ursächlich",
    "Feature Importance besagt, dass das Modell ein Feature stark für seine "
    "Vorhersagen nutzt. Sie besagt <b>nicht</b>, dass dieses Feature das "
    "Ergebnis verursacht. Ein Confounder oder ein bloßes Korrelat kann an "
    "erster Stelle stehen. Diese Unterscheidung wird im Kapitel Explainable "
    "ML und in der gesamten Kausalitäts-Sektion zentral sein.",
    typ="achtung",
)

# ------------------------------------------------------------------ Quiz
quiz(
    "Warum overfittet ein Random Forest weniger als ein einzelner tiefer "
    "Decision Tree?",
    [
        "Weil jeder Tree im Forest flacher ist als ein Einzelbaum",
        "Weil die Mittelung vieler unterschiedlich irrender Trees die Varianz senkt",
        "Weil der Forest weniger Features benutzt",
        "Er overfittet nicht weniger, er ist nur schneller",
    ],
    richtig=1,
    erklaerung=(
        "Die Trees sind einzeln tief und instabil, haben also hohe Varianz. "
        "Ihre Fehler sind jedoch teilweise unkorreliert und mitteln sich bei "
        "der Aggregation heraus."
    ),
    key="quiz_ml_baeume",
)

# -------------------------------------------------------------- Ausblick
st.markdown("## Weiterführende Literatur")
st.markdown(
    """
- G. James, D. Witten, T. Hastie & R. Tibshirani (2021), *An Introduction to Statistical Learning*, 2. Aufl., Springer, Kap. 8 (frei online)
- T. Hastie, R. Tibshirani & J. Friedman (2009), *The Elements of Statistical Learning*, 2. Aufl., Springer, Kap. 9, 10 und 15 (frei online)
"""
)

st.markdown("## Wie geht es weiter?")
weiter_xai, weiter_nn = st.columns(2)
with weiter_xai:
    st.page_link(
        "views/ml/explainable_ml.py",
        label="Weiter: Explainable ML",
        icon="🔍",
    )
with weiter_nn:
    st.page_link(
        "views/ml/neuronale_netze.py", label="Oder: Neural Networks", icon="🧠"
    )
