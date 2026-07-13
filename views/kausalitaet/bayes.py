"""Kapitel Kausalität: Bayesian Methods.

Prior → Daten → Posterior am Beta-Binomial-Modell, sequentielles Lernen
und die Brücke zu kausalen Fragen.
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

from utils.theming import FARBEN, kapitel_kopf, merkkasten, quiz

kapitel_kopf(
    "🎲",
    "Bayesian Methods",
    "Wissen als Wahrscheinlichkeit: Vorwissen einbauen, mit Daten aktualisieren",
)

# ---------------------------------------------------------------- Intro
st.markdown(
    r"""
Bisher haben wir Wahrscheinlichkeit als **Häufigkeit** benutzt (wie oft
passiert etwas bei vielen Wiederholungen?). Die **bayesianische** Sichtweise
liest sie als **Grad der Überzeugung** und macht damit Sätze möglich wie:
*„Mit 90 % Wahrscheinlichkeit liegt die Wirksamkeit über 50 %.“*

Das Rezept ist immer dasselbe (Satz von Bayes):

$$
\underbrace{p(\theta \mid \text{Daten})}_{\text{Posterior}} \;\propto\;
\underbrace{p(\text{Daten} \mid \theta)}_{\text{Likelihood}} \times
\underbrace{p(\theta)}_{\text{Prior}}
$$

**Vorwissen** (Prior) trifft auf **Daten** (Likelihood) und wird zu
**aktualisiertem Wissen** (Posterior). Kein einzelner Schätzwert, sondern
eine ganze Verteilung dessen, was du glauben darfst.
"""
)

# ------------------------------------------ Demo 1: Beta-Binomial
st.markdown("## Demo: Wie wirksam ist die Behandlung?")
st.markdown(
    r"""
Eine neue Therapie hat eine unbekannte Erfolgswahrscheinlichkeit $\theta$.
Als **Prior** wählen wir eine Beta-Verteilung, die Studiendaten ($k$ Erfolge
bei $n$ Behandelten) folgen einer Binomialverteilung. Diese Kombination ist
**konjugiert**: Der Posterior ist wieder eine Beta-Verteilung und lässt sich
geschlossen angeben:

$$
\theta \sim \mathrm{Beta}(\alpha, \beta), \quad
k \mid \theta \sim \mathrm{Bin}(n, \theta)
\;\;\Longrightarrow\;\;
\theta \mid k \sim \mathrm{Beta}(\alpha + k,\; \beta + n - k).
$$

Die Prior-Parameter lassen sich als „gedachte frühere Beobachtungen“ lesen:
$\alpha$ frühere Erfolge, $\beta$ frühere Misserfolge. Das Posterior-Mittel
ist ein **gewichtetes Mittel** aus Prior-Mittel und beobachteter
Erfolgsquote,

$$
E[\theta \mid k]
= \frac{\alpha + k}{\alpha + \beta + n}
= w\,\frac{\alpha}{\alpha + \beta} + (1 - w)\,\frac{k}{n},
\qquad w = \frac{\alpha + \beta}{\alpha + \beta + n},
$$

wobei das Gewicht $w$ des Vorwissens mit wachsendem $n$ gegen null geht.
"""
)

regler_prior, regler_daten = st.columns(2)
with regler_prior:
    st.markdown("**Prior: Was glaubst du vorher?**")
    alpha = st.slider("α (gedachte frühere Erfolge)", 0.5, 30.0, 1.0, step=0.5)
    beta = st.slider("β (gedachte frühere Misserfolge)", 0.5, 30.0, 1.0, step=0.5)
    st.caption(
        "α = β = 1: flach/ahnungslos · α klein, β groß: skeptisch · "
        "α groß, β klein: optimistisch"
    )
with regler_daten:
    st.markdown("**Daten: Was zeigt die Studie?**")
    n_patienten = st.slider("Patient:innen behandelt", 0, 200, 20)
    k_erfolge = st.slider("davon Erfolge", 0, max(n_patienten, 1), min(14, n_patienten))

theta = np.linspace(0.001, 0.999, 400)
prior = stats.beta.pdf(theta, alpha, beta)
posterior = stats.beta.pdf(theta, alpha + k_erfolge, beta + n_patienten - k_erfolge)

fig = go.Figure()
fig.add_scatter(
    x=theta, y=prior, mode="lines", name="Prior",
    line=dict(color=FARBEN["himmel"], width=2, dash="dash"),
)
if n_patienten > 0:
    likelihood = stats.binom.pmf(k_erfolge, n_patienten, theta)
    likelihood = likelihood / likelihood.max() * posterior.max() * 0.8
    fig.add_scatter(
        x=theta, y=likelihood, mode="lines", name="Likelihood (skaliert)",
        line=dict(color=FARBEN["sonne"], width=2, dash="dot"),
    )
fig.add_scatter(
    x=theta, y=posterior, mode="lines", name="Posterior",
    line=dict(color=FARBEN["nacht"], width=4), fill="tozeroy",
    fillcolor="rgba(30, 58, 95, 0.12)",
)
fig.update_layout(
    xaxis_title="Erfolgswahrscheinlichkeit θ", yaxis_title="Dichte", height=430,
)
st.plotly_chart(fig, use_container_width=True)

post = stats.beta(alpha + k_erfolge, beta + n_patienten - k_erfolge)
metrik_mittel, metrik_ki, metrik_p50 = st.columns(3)
metrik_mittel.metric("Posterior-Mittel", f"{post.mean():.1%}")
metrik_ki.metric(
    "95 %-Credible-Interval", f"{post.ppf(0.025):.0%} – {post.ppf(0.975):.0%}"
)
metrik_p50.metric("P(θ > 50 %)", f"{1 - post.cdf(0.5):.1%}")

st.markdown(
    """
Drei Beobachtungen lohnen das Ausprobieren. Erstens dominiert bei wenigen
Daten der Prior, während bei vielen Daten die Likelihood übernimmt, nahezu
unabhängig vom Vorwissen. Zweitens verlangt ein skeptischer Prior (etwa
α = 2, β = 8) mehr Evidenz, bevor er von der Therapie überzeugt ist, ganz
wie eine sorgfältige Gutachterin. Drittens darf man das **Credible
Interval** wörtlich nehmen: θ liegt mit 95 % Wahrscheinlichkeit in diesem
Bereich. Das ist genau der Satz, den viele beim frequentistischen
Konfidenzintervall aussprechen möchten, dort aber nicht dürfen.
"""
)

# ------------------------------------------ Demo 2: Sequentiell lernen
st.markdown("## Demo: Sequentielles Lernen")
st.markdown(
    """
Der Posterior von heute ist der Prior von morgen. Zieh den Regler und sieh
zu, wie die Verteilung mit jedem Patientenschub wandert und schärfer wird
(wahre Wirksamkeit in der Simulation: **70 %**).
"""
)

WAHRES_THETA = 0.7


@st.cache_data
def patienten_sequenz(n_max: int = 150, seed: int = 9):
    rng = np.random.default_rng(seed)
    return rng.binomial(1, WAHRES_THETA, n_max)


gesehen = st.slider("Bisher behandelte Patient:innen", 0, 150, 0, step=10)
ausgaenge = patienten_sequenz()[:gesehen]
erfolge_seq = int(ausgaenge.sum())

fig_seq = go.Figure()
for m, deckkraft in [(0, 0.25), (gesehen // 2, 0.5), (gesehen, 1.0)]:
    if m == 0 and gesehen > 0:
        name = "Start (Prior, flach)"
    elif m == gesehen:
        name = f"nach {gesehen} Patient:innen"
    else:
        name = f"nach {m} Patient:innen"
    teil = patienten_sequenz()[:m]
    fig_seq.add_scatter(
        x=theta,
        y=stats.beta.pdf(theta, 1 + teil.sum(), 1 + m - teil.sum()),
        mode="lines", name=name, opacity=deckkraft,
        line=dict(color=FARBEN["nacht"], width=3),
    )
fig_seq.add_vline(
    x=WAHRES_THETA, line_dash="dash", line_color=FARBEN["wiese"],
    annotation_text="wahres θ = 0,7",
)
fig_seq.update_layout(
    xaxis_title="Erfolgswahrscheinlichkeit θ", yaxis_title="Dichte", height=400,
)
st.plotly_chart(fig_seq, use_container_width=True)

if gesehen > 0:
    st.caption(
        f"Stand: {erfolge_seq} Erfolge bei {gesehen} Behandelten "
        f"({erfolge_seq / gesehen:.0%})."
    )

# ---------------------------------------------------- Bezug zur Kausalität
st.markdown("## Bezug zur Kausalinferenz")
st.markdown(
    """
Bayesianische Ideen tauchen in der Kausalinferenz überall auf:

- **Priors über Effektstärken:** Wundereffekte sind selten. Ein skeptischer
  Prior schützt vor der Überinterpretation kleiner Studien und ist die
  formale Version des Grundsatzes, dass außergewöhnliche Behauptungen
  außergewöhnliche Evidenz erfordern.
- **Bayesianische A/B-Tests und adaptive Studien:** Statt eines starren
  Stichprobenplans wird laufend die Posterior-Wahrscheinlichkeit berechnet,
  dass Variante A besser ist, und Studien dürfen früher gestoppt werden.
- **Sensitivity Analysis:** Wie stark müsste ein unbeobachteter Confounder
  sein, um den Effekt wegzuerklären? Priors machen solche
  Was-wäre-wenn-Fragen quantifizierbar.
- **Werkzeuge:** `PyMC` (Python) und `Stan` schätzen beliebige
  Wahrscheinlichkeitsmodelle, einschließlich kompletter Kausal- und
  Mehrebenenmodelle.
"""
)

merkkasten(
    "Merke",
    "Bayes = Prior × Likelihood → Posterior. Vorwissen ist kein Schmuggel, "
    "sondern <b>explizit gemachte Annahme</b>, und bei wachsender Datenmenge "
    "verliert es automatisch an Gewicht. Credible Intervals sagen direkt, "
    "was man wissen will: die Wahrscheinlichkeit einer Hypothese gegeben "
    "die Daten.",
    typ="merke",
)

# ------------------------------------------------------------------ Quiz
quiz(
    "Ein 95 %-Credible-Interval für θ ist [0,55; 0,80]. Welche Aussage ist "
    "korrekt?",
    [
        "In 95 % aller Wiederholungen der Studie läge das Intervall um das wahre θ",
        "Gegeben Daten und Prior liegt θ mit 95 % Wahrscheinlichkeit zwischen 0,55 und 0,80",
        "95 % der Patient:innen sprechen auf die Therapie an",
        "Das wahre θ ist sicher größer als 0,5",
    ],
    richtig=1,
    erklaerung=(
        "Genau das ist der Charme des bayesianischen Intervalls: eine direkte "
        "Wahrscheinlichkeitsaussage über den Parameter. Das frequentistische "
        "Konfidenzintervall macht dagegen die Aussage aus Option A, also über das "
        "Verfahren, nicht über θ."
    ),
    key="quiz_kausal_bayes",
)

# -------------------------------------------------------------- Ausblick
st.markdown("## Weiterführende Literatur")
st.markdown(
    """
- R. McElreath (2020), *Statistical Rethinking*, 2. Aufl., CRC Press
- A. Gelman, J. B. Carlin, H. S. Stern, D. B. Dunson, A. Vehtari & D. B. Rubin (2013), *Bayesian Data Analysis*, 3. Aufl., CRC Press (frei online)
- A. B. Downey (2021), *Think Bayes*, 2. Aufl., O'Reilly (frei online)
"""
)

st.markdown("## Wie geht es weiter?")
weiter_sem, weiter_po = st.columns(2)
with weiter_sem:
    st.page_link(
        "views/kausalitaet/sem_surveys.py",
        label="Weiter: SEMs & Survey Experiments",
        icon="📋",
    )
with weiter_po:
    st.page_link(
        "views/kausalitaet/potential_outcomes.py",
        label="Zurück: Potential Outcomes & RCTs",
        icon="⚖️",
    )
