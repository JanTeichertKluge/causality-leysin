"""Analysefunktionen für das Beispielprojekt (Project STAR).

Bewusst ohne Streamlit-Import: Hier steht *nur* die Analyse, das UI liegt in
`app.py`. Diese Trennung ist Absicht und Teil der Vorlage: So lassen sich
die Ergebnisse testen (siehe `tests/test_beispielprojekt.py`), ohne die App
zu starten, und ihr könnt dieselben Funktionen in einem Notebook benutzen.

"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import plotly.express as px


def plot_accuracy(data):
    df = pd.DataFrame(data)

    accuracy = (
        df.groupby(["x", "y", "z", "a"])["success"]
        .mean()
        .reset_index()
    )

    # Prüfen, ob z bzw. a im gesamten übergebenen Datensatz
    # irgendwo einen Wert ungleich 0 haben
    z_used = df["z"].ne(0).any()
    a_used = df["a"].ne(0).any()

    # Beschriftung der Kombination erzeugen
    def make_combination(row):
        parts = [
            f"x={row['x']}",
            f"y={row['y']}"
        ]

        if z_used:
            parts.append(f"z={row['z']}")

        if a_used:
            parts.append(f"a={row['a']}")

        return ", ".join(parts)

    accuracy["combination"] = accuracy.apply(
        make_combination,
        axis=1
    )

    fig = px.bar(
        accuracy,
        x="combination",
        y="success",
        range_y=[0, 1],
        labels={
            "combination": "Kombinationen",
            "success": "Richtigkeitswahrscheinlichkeit"
        },
        title="Richtigkeitswahrscheinlichkeit"
    )

    fig.update_layout(
        yaxis_tickformat=".0%",
        xaxis_tickangle=-45
    )

    return fig






def create_accuracy_heatmap(data_sets):
    """
    Erstellt eine 3x3 Heatmap mit fließendem Farbübergang.
    """
    # Matrix für die Genauigkeiten erstellen
    accuracy_matrix = np.zeros((3, 3))
    
    for difficulty in range(3):
        for extra in range(3):
            data = data_sets[difficulty][extra]
            if data and len(data) > 0:
                df = pd.DataFrame(data)
                accuracy = df['success'].mean()
                accuracy_matrix[difficulty][extra] = accuracy
            else:
                accuracy_matrix[difficulty][extra] = np.nan
    
    # DataFrame für Plotly erstellen
    df_heatmap = pd.DataFrame(
        accuracy_matrix,
        index=['Einfach (0)', 'Mittel (1)', 'Schwer (2)'],
        columns=['Keine (0)', 'Etwas (1)', 'Viele (2)']
    )
    
    # Heatmap mit fließendem Farbverlauf
    fig = px.imshow(
        df_heatmap,
        text_auto='.0%',
        color_continuous_scale=[
            [0.0, 'darkred'],    # 0%   - dunkelrot
            [0.3, 'red'],        # 30%  - rot
            [0.5, 'orange'],     # 50%  - orange
            [0.7, 'yellow'],     # 70%  - gelb
            [0.8, 'lightgreen'], # 80%  - hellgrün
            [0.9, 'green'],      # 90%  - grün
            [1.0, 'darkgreen']   # 100% - dunkelgrün
        ],
        range_color=[0, 1],
        aspect="auto",
        title="Genauigkeit nach Schwierigkeit und Zusatzinformationen",
        labels=dict(
            x="Zusatzinformationen",
            y="Schwierigkeit",
            color="Genauigkeit"
        )
    )
    
    # Layout-Anpassungen
    fig.update_layout(
        height=450,
        width=500,
        xaxis_side='top',
        coloraxis_colorbar=dict(
            title="Genauigkeit",
            tickformat='.0%',
            tickvals=[0, 0.25, 0.5, 0.75, 1],
            ticktext=['0%', '25%', '50%', '75%', '100%']
        ),
        font=dict(size=14)
    )
    
    # Werte mit Prozentsatz formatieren und Schrift anpassen
    fig.update_traces(
        texttemplate='%{text:.0%}',
        textfont=dict(
            color='white',  # Weiße Schrift für bessere Lesbarkeit
            size=18,
            family="Arial Black"
        ),
        hovertemplate='<b>Schwierigkeit:</b> %{y}<br>' +
                      '<b>Zusatzinfo:</b> %{x}<br>' +
                      '<b>Genauigkeit:</b> %{z:.1%}<br>' +
                      '<extra></extra>'
    )
    
    return fig


