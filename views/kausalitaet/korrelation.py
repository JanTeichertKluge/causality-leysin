"""Musterkapitel Kausalität: Korrelation ≠ Kausalität.

Interaktive Einführung: Scheinkorrelation durch Confounder und das
Simpson-Paradox.
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.theming import FARBEN, kapitel_kopf, merkkasten, quiz

kapitel_kopf(
    "🔀",
    "Korrelation ≠ Kausalität",
    "Warum Muster in Daten noch keine Ursachen sind",
)

# ---------------------------------------------------------------- Intro
st.markdown(
    """
Ein paar Zusammenhänge, die sich in echten Daten finden lassen:

- In Regionen mit mehr **Störchen** werden mehr **Kinder** geboren.
- An Tagen mit hohem **Eisverkauf** gibt es mehr **Sonnenbrände**.
- Menschen, die **Rotwein** trinken, sind im Schnitt gesünder.

Kaufen wir also Eis, um Sonnenbrand zu verursachen? Natürlich nicht. Alle drei
Korrelationen sind echt — aber keine davon ist ein kausaler Effekt. Hinter
jeder steckt eine **dritte Variable**: Ländlichkeit, Sonnenstunden, Einkommen.
Solche Variablen heißen **Confounder** (Störfaktoren).
"""
)

merkkasten(
    "Definition",
    "<b>Korrelation:</b> Zwei Größen bewegen sich systematisch gemeinsam. "
    "<b>Kausalität:</b> Ein Eingriff in die eine Größe <i>verändert</i> die "
    "andere. Ein Confounder Z, der beide beeinflusst, erzeugt Korrelation "
    "ganz ohne Kausalität.",
    typ="definition",
)

# ------------------------------------------ Demo 1: Confounder-Simulator
st.markdown("## 🎛️ Demo: Der Confounder-Simulator")
st.markdown(
    """
Wir bauen uns die Eis-Sonnenbrand-Welt selbst: Die **Sonnenstunden** $Z$
beeinflussen den **Eisverkauf** $X$ (Pfeil $a$) und die **Sonnenbrände** $Y$
(Pfeil $b$). Ob Eis *wirklich* Sonnenbrand verursacht, steuerst du mit dem
Pfeil $c$ — stell ihn auf 0 und schau, was eine naive Auswertung trotzdem
behauptet.
"""
)

regler_a, regler_b, regler_c = st.columns(3)
effekt_zx = regler_a.slider("a: Sonne → Eisverkauf", 0.0, 2.0, 1.2, step=0.1)
effekt_zy = regler_b.slider("b: Sonne → Sonnenbrände", 0.0, 2.0, 1.2, step=0.1)
effekt_xy = regler_c.slider(
    "c: Eisverkauf → Sonnenbrände (wahrer kausaler Effekt)",
    -1.0, 1.0, 0.0, step=0.1,
)


@st.cache_data
def confounder_daten(a: float, b: float, c: float, n: int = 400, seed: int = 2026):
    rng = np.random.default_rng(seed)
    z = rng.normal(0, 1, n)
    x = a * z + rng.normal(0, 1, n)
    y = c * x + b * z + rng.normal(0, 1, n)
    return z, x, y


z, x, y = confounder_daten(effekt_zx, effekt_zy, effekt_xy)

# Naive Schätzung: einfache Regression y ~ x (ignoriert Z)
naiv = np.polyfit(x, y, 1)[0]
# Adjustierte Schätzung: Regression y ~ x + z, Koeffizient auf x
design = np.column_stack([x, z, np.ones_like(x)])
adjustiert = np.linalg.lstsq(design, y, rcond=None)[0][0]

spalte_dag, spalte_streu = st.columns([2, 3])

with spalte_dag:
    st.graphviz_chart(
        f"""
digraph {{
    rankdir=LR;
    bgcolor="transparent";
    node [shape=box, style="rounded,filled", fillcolor="#EEF3FA",
          color="#3E6DB5", fontname="sans-serif"];
    edge [fontname="sans-serif", color="#5C6470"];
    Z [label="☀️ Sonnenstunden (Z)"];
    X [label="🍦 Eisverkauf (X)"];
    Y [label="🔥 Sonnenbrände (Y)"];
    Z -> X [label="a = {effekt_zx:.1f}"];
    Z -> Y [label="b = {effekt_zy:.1f}"];
    X -> Y [label="c = {effekt_xy:.1f}", color="#E8804C", fontcolor="#B05A2B",
            penwidth=2];
}}
""",
        use_container_width=True,
    )

with spalte_streu:
    raster = np.linspace(x.min(), x.max(), 50)
    fig = go.Figure()
    fig.add_scatter(
        x=x, y=y, mode="markers", name="Tage",
        marker=dict(
            color=z, colorscale=[[0, "#D9E4F2"], [1, FARBEN["nacht"]]],
            size=7, opacity=0.75,
            colorbar=dict(title="Sonnenstunden Z", thickness=12),
        ),
    )
    fig.add_scatter(
        x=raster, y=np.polyval(np.polyfit(x, y, 1), raster), mode="lines",
        name=f"Naive Regressionsgerade (Steigung {naiv:.2f})",
        line=dict(color=FARBEN["sonne"], width=3),
    )
    fig.update_layout(
        xaxis_title="Eisverkauf X", yaxis_title="Sonnenbrände Y", height=380,
    )
    st.plotly_chart(fig, use_container_width=True)

metrik_wahr, metrik_naiv, metrik_adj = st.columns(3)
metrik_wahr.metric("Wahrer Effekt c", f"{effekt_xy:.2f}")
metrik_naiv.metric(
    "Naive Schätzung (y ~ x)", f"{naiv:.2f}", delta=f"{naiv - effekt_xy:+.2f} verzerrt",
    delta_color="inverse",
)
metrik_adj.metric(
    "Adjustiert für Z (y ~ x + z)", f"{adjustiert:.2f}",
    delta=f"{adjustiert - effekt_xy:+.2f}", delta_color="inverse",
)

if abs(effekt_xy) < 0.05 and abs(naiv) > 0.3:
    merkkasten(
        "Scheinkorrelation!",
        f"Der wahre Effekt ist <b>{effekt_xy:.1f}</b> — Eis verursacht hier "
        f"keinen Sonnenbrand. Trotzdem meldet die naive Auswertung eine "
        f"Steigung von <b>{naiv:.2f}</b>. Der gemeinsame Treiber Z gaukelt "
        "einen Zusammenhang vor. Die Regression, die Z berücksichtigt, "
        "findet dagegen fast null.",
        typ="achtung",
    )

st.markdown(
    """
Beachte die Färbung der Punkte: Sonnige Tage (dunkel) liegen rechts oben,
trübe Tage (hell) links unten. Die naive Gerade verbindet in Wahrheit
**Wettertypen**, nicht Wirkung von Eis. Sobald wir Z in die Regression
aufnehmen („für Z adjustieren“), verschwindet der Spuk — der geschätzte
Effekt landet nahe beim wahren $c$.
"""
)

# --------------------------------------------- Demo 2: Simpson-Paradox
st.markdown("## 🙃 Demo: Das Simpson-Paradox")
st.markdown(
    """
Confounder können mehr als Zusammenhänge vortäuschen — sie können sie sogar
**umdrehen**. Ein Klassiker: In einer Studie scheint mehr **Sport** mit
*höherem* **Cholesterin** einherzugehen. Skandal? Schalte die Aufschlüsselung
nach **Altersgruppen** ein und sieh selbst.
"""
)


@st.cache_data
def simpson_daten(seed: int = 7):
    rng = np.random.default_rng(seed)
    gruppen = {
        "20–35 Jahre": (2.0, 195.0),
        "40–55 Jahre": (5.0, 215.0),
        "60–75 Jahre": (8.0, 235.0),
    }
    frames = []
    for name, (sport_mitte, chol_mitte) in gruppen.items():
        n = 60
        sport = np.clip(rng.normal(sport_mitte, 1.2, n), 0, None)
        # Innerhalb jeder Altersgruppe senkt Sport das Cholesterin.
        chol = chol_mitte - 4.0 * (sport - sport_mitte) + rng.normal(0, 8, n)
        frames.append((name, sport, chol))
    return frames


frames = simpson_daten()
alle_sport = np.concatenate([f[1] for f in frames])
alle_chol = np.concatenate([f[2] for f in frames])
gesamt_steigung = np.polyfit(alle_sport, alle_chol, 1)[0]

aufschluesseln = st.toggle("🔍 Nach Altersgruppen aufschlüsseln")

fig_simpson = go.Figure()
gruppen_farben = [FARBEN["gletscher"], FARBEN["sonne"], FARBEN["wiese"]]

if not aufschluesseln:
    fig_simpson.add_scatter(
        x=alle_sport, y=alle_chol, mode="markers", name="Alle Personen",
        marker=dict(color=FARBEN["schiefer"], size=7, opacity=0.6),
    )
    raster = np.linspace(alle_sport.min(), alle_sport.max(), 50)
    fig_simpson.add_scatter(
        x=raster, y=np.polyval(np.polyfit(alle_sport, alle_chol, 1), raster),
        mode="lines", name=f"Gesamttrend (Steigung {gesamt_steigung:+.1f})",
        line=dict(color=FARBEN["beere"], width=4),
    )
else:
    for (name, sport, chol), farbe in zip(frames, gruppen_farben):
        steigung = np.polyfit(sport, chol, 1)[0]
        fig_simpson.add_scatter(
            x=sport, y=chol, mode="markers", name=f"{name}",
            marker=dict(color=farbe, size=7, opacity=0.7),
        )
        raster = np.linspace(sport.min(), sport.max(), 20)
        fig_simpson.add_scatter(
            x=raster, y=np.polyval(np.polyfit(sport, chol, 1), raster),
            mode="lines", name=f"{name}: Steigung {steigung:+.1f}",
            line=dict(color=farbe, width=3),
        )

fig_simpson.update_layout(
    xaxis_title="Sport (Stunden pro Woche)",
    yaxis_title="Cholesterin (mg/dl)",
    height=440,
)
st.plotly_chart(fig_simpson, use_container_width=True)

if aufschluesseln:
    st.success(
        "**Auflösung:** Innerhalb *jeder* Altersgruppe senkt Sport das "
        "Cholesterin (negative Steigungen). Der positive Gesamttrend entsteht "
        "nur, weil Ältere sowohl mehr Sport treiben als auch höheres "
        "Cholesterin haben — das **Alter** ist der Confounder."
    )
else:
    st.info(
        f"Der Gesamttrend hat Steigung **{gesamt_steigung:+.1f}**: mehr Sport, "
        "mehr Cholesterin?! Schalte die Aufschlüsselung ein, bevor du dem "
        "Ergebnis glaubst."
    )

merkkasten(
    "Merke",
    "Ob ein Zusammenhang erscheint, verschwindet oder sich umkehrt, kann "
    "davon abhängen, welche Gruppen man betrachtet (<b>Simpson-Paradox</b>). "
    "Welche Aufteilung die <i>richtige</i> ist, sagen dir die Daten allein "
    "nicht — dafür brauchst du Annahmen über die Kausalstruktur.",
    typ="merke",
)

# ------------------------------------------------------------------ Quiz
quiz(
    "Eine Studie findet: Wer viel Rotwein trinkt, ist gesünder. Was ist die "
    "vorsichtigste Interpretation?",
    [
        "Rotwein macht gesund — der Zusammenhang ist ja statistisch signifikant",
        "Gesundheit führt zu Rotweinkonsum",
        "Ein Confounder (z. B. Einkommen oder Lebensstil) könnte beide Größen treiben",
        "Der Zusammenhang muss ein Messfehler sein",
    ],
    richtig=2,
    erklaerung=(
        "Signifikanz schützt nicht vor Confounding. Ohne Experiment oder "
        "Adjustierung bleibt offen, ob Rotwein, umgekehrte Kausalität oder "
        "eine dritte Variable den Zusammenhang erzeugt."
    ),
    key="quiz_kausal_korrelation",
)

# -------------------------------------------------------------- Ausblick
st.markdown("## Wie geht's weiter?")
st.markdown(
    """
„Für Z adjustieren“ hat im Simulator funktioniert — aber woher weiß man,
**welche** Variablen man adjustieren muss (und welche man besser in Ruhe
lässt)? Dafür gibt es eine wunderbar klare Sprache: **kausale Graphen (DAGs)**.
"""
)
st.page_link(
    "views/kausalitaet/dags_confounding.py",
    label="Weiter: DAGs & Confounding",
    icon="🕸️",
)
