"""Gemeinsame Bausteine für die ML-Demos: Datensätze und Decision-Boundary-Plots.

Wird von den Kapiteln Bäume & Ensembles, Neuronale Netze und Explainable ML
geteilt, damit alle Klassifikations-Demos gleich aussehen.
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from sklearn.datasets import make_moons

from utils.theming import FARBEN


@st.cache_data
def monde_daten(n: int = 300, rauschen: float = 0.25, seed: int = 2026):
    """Zwei ineinander verschränkte Halbmonde — der Klassiker für nichtlineare
    Klassifikation."""
    X, y = make_moons(n_samples=n, noise=rauschen, random_state=seed)
    return X, y


def entscheidungsgrenze(
    modell, X: np.ndarray, y: np.ndarray, titel: str = "", aufloesung: int = 120
) -> go.Figure:
    """Zeichnet die Entscheidungsgrenze eines 2D-Klassifikators als Kontur
    plus die Datenpunkte."""
    x_min, x_max = X[:, 0].min() - 0.7, X[:, 0].max() + 0.7
    y_min, y_max = X[:, 1].min() - 0.7, X[:, 1].max() + 0.7
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, aufloesung), np.linspace(y_min, y_max, aufloesung)
    )
    gitter = np.c_[xx.ravel(), yy.ravel()]
    if hasattr(modell, "predict_proba"):
        z = modell.predict_proba(gitter)[:, 1]
    else:
        z = modell.predict(gitter).astype(float)

    fig = go.Figure()
    fig.add_contour(
        x=np.linspace(x_min, x_max, aufloesung),
        y=np.linspace(y_min, y_max, aufloesung),
        z=z.reshape(xx.shape),
        colorscale=[[0.0, "#DCE7F5"], [0.5, "#FFFFFF"], [1.0, "#FADFCE"]],
        zmin=0,
        zmax=1,
        showscale=False,
        contours=dict(showlines=False),
        hoverinfo="skip",
    )
    for klasse, farbe, name in (
        (0, FARBEN["gletscher"], "Klasse 0"),
        (1, FARBEN["sonne"], "Klasse 1"),
    ):
        maske = y == klasse
        fig.add_scatter(
            x=X[maske, 0],
            y=X[maske, 1],
            mode="markers",
            name=name,
            marker=dict(color=farbe, size=7, line=dict(width=0.5, color="white")),
        )
    fig.update_layout(
        title=titel,
        height=420,
        xaxis_title="Feature 1",
        yaxis_title="Feature 2",
    )
    return fig
