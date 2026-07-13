"""Beispielprojekt (Weg 2): eine eigene interaktive Streamlit-Seite.

Für Gruppen als Vorlage gedacht. Wichtigste Regel: KEIN
st.set_page_config() aufrufen — das erledigt die Haupt-App.
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.markdown("# 🎲 Beispielprojekt: Würfeln mit dem Zufall")
st.caption("Team: Das Dozenten-Team — Vorlage für eine interaktive Projektseite")

st.markdown(
    """
So kann eine Projektseite mit eigenen Widgets aussehen. Als Mini-Demo: der
**Zentrale Grenzwertsatz**. Wir würfeln pro Wurf mehrere Würfel und notieren
den **Mittelwert**. Ein einzelner Würfel ist gleichverteilt — aber je mehr
Würfel wir mitteln, desto mehr sieht die Verteilung wie eine Glockenkurve aus.
"""
)

anzahl_wuerfel = st.slider("Würfel pro Wurf", 1, 50, 1)
anzahl_wuerfe = st.slider("Anzahl Würfe", 500, 20000, 5000, step=500)

rng = np.random.default_rng(42)
mittelwerte = rng.integers(1, 7, size=(anzahl_wuerfe, anzahl_wuerfel)).mean(axis=1)

fig = go.Figure(go.Histogram(x=mittelwerte, nbinsx=60, name="Mittelwerte"))
fig.update_layout(
    xaxis_title="Mittelwert der Augenzahlen",
    yaxis_title="Häufigkeit",
    height=420,
    xaxis=dict(range=[1, 6]),
)
st.plotly_chart(fig, use_container_width=True)

if anzahl_wuerfel == 1:
    st.info("Ein Würfel: alle Augenzahlen gleich häufig — flach wie ein Brett.")
elif anzahl_wuerfel >= 20:
    st.success(
        "Viele Würfel: Die Mittelwerte drängeln sich glockenförmig um 3,5 — "
        "der Zentrale Grenzwertsatz in Aktion."
    )
