import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import doubleml as dml
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from utils.theming import FARBEN, gruppen_aufgabe, kapitel_kopf, merkkasten, vertiefung
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

kapitel_kopf(
    "↔️",      #noch ändern
    "Causal Inference",
    "Double ML in Verwendung gegen durch Confounder gebiaste Datensätze",
)

#--------------------------------------------------------- Intro
merkkasten(
    "Standard Predictive ML",
    r"""
    
$\text{Features } (X) \xrightarrow{\quad \text{(Korrelationen)} \quad} \text{Outcome } (Y)$

„Wie hoch ist die Wahrscheinlichkeit von (Y) gegeben (X)?“

Identifiziert reine Korrelationen zwischen den Variablen.

""",
    typ="definition",
)

merkkasten(
    "Causal Inference",
    r"""

$\text{Features } (X) + \text{Treatment } (D) \xrightarrow{\quad \text{(Kausaler Effekt)} \quad} \text{Outcome } (Y)$

„Was ist die spezifische Änderung des Ergebnisses (Y), die ausschließlich durch die Anwendung von Maßnahme (D) auf eine Einheit mit den Merkmalen (X) verursacht wird?“

Identifiziert den Effekt des Treatments (D) auf das Outcome (Y).
""",
    typ="definition",
)

st.markdown(
    r'''
    Beispiel: Untersucht wird der Effekt von Impfungen (D) auf die prognistizierte Anzahl der Tage,
    welche eine Person in einem Krankenhaus verbringen muss (Y). Nicht nur die Impfung (D), sondern auch andere Confounder
    wie zum Beispiel das Alter, Vorerkrankungen und Lebensweise beeinflussen die Aufenthaltsdauer. Zur Vereifachung beschränken wir uns ausschließlich auf das Alter (X).
'''
)

st.markdown("## Naives Modell")
st.markdown(
    r'''
    Es wird der Zusammenhang des Impfens mit der Anzahl der Tage im Krankenaushaus beobachtet.
    Ein Impfgegner würde direkt sagen: Ich habe es gewusst, Impfungen machen Menschen krank! 
    Folglich tut sich die Frage auf: Existiert ein kausaler Zusammenhang oder lediglich eine Korrelation?
'''
)


regler_confounder_effect, regler_treatment_effect = st.columns(2)
confounder_effect = regler_confounder_effect.slider("Confounder-Effekt Stärke", min_value= 0.0, max_value=1.0, value=0.35, step=0.01)
treatment_effect = regler_treatment_effect.slider("Treatment-Effekt Stärke", min_value=-10.0, max_value=0.0, value=-2.7, step=0.1)

@st.cache_data
def dgp_demo(n=500, seed=42, confounding_effect = 0.35, treatment_effect = 2.7):
    np.random.seed(seed)

    # 1. Alter (Confounder X)
    alter = np.random.normal(loc=50, scale=12, size=n)
    alter = np.clip(alter, 20, 80)

    # 2. Impfwahrscheinlichkeit
    p_vacc = 1 / (1 + np.exp(-0.15 * (alter - 50)))
    vacc = np.random.binomial(n=1, p=p_vacc, size=n)

    # 3. Kausales Modell
    tage_in_h = (
        5.0                                                                   #(Sockelwert): Die Basis-Aufenthaltsdauer in Tagen für einen jungen, ungeimpften Patienten (Alter 20).
        + confounding_effect * (alter - 20)                                   #(Alterseffekt / Confounder): Jedes Lebensjahr über 20 erhöht die erwartete Krankenhauseffektdauer um 0,18 Tage. Ein 70-Jähriger bekommt dadurch automatisch $+9$ Tage ($0.18 \times 50$) aufgerechnet.
        + treatment_effect * vacc                                             #(Wahrer kausaler Impfeffekt): Eine Impfung ($vacc = 1$) verkürzt den Aufenthalt direkt um 2.72 Tage.
        + np.random.normal(loc=0, scale=1.5, size=n)                          #(Individuelles Rauschen): Zufällige biologische Schwankungen um den Mittelwert $0$ mit einer Standardabweichung von 1,5 Tagen (z. B. Vorerkrankungen, Immunsystem).
    )

    return pd.DataFrame(
        {"Alter": alter, "Geimpft": vacc, "Tage_in_Hospital": tage_in_h}
    )

df_sample = dgp_demo(500, confounding_effect=confounder_effect, treatment_effect=treatment_effect)


#Werte ein kleines bisschen streuen lassen
rng = np.random.default_rng(42)
x_jitter = df_sample["Geimpft"] + rng.uniform(-0.06, 0.06, size=len(df_sample))

#lineare Regression
naiv_fit = np.polyfit(df_sample["Geimpft"], df_sample["Tage_in_Hospital"], 1)
x_linie = np.array([0.0, 1.0])
y_linie = np.polyval(naiv_fit, x_linie)

#Farben für die Punkte
farben = np.where(df_sample["Geimpft"] == 1, "orange", "blue")

fig1 = go.Figure()

#Datenpunkte
fig1.add_scatter(
    x=x_jitter,
    y=df_sample["Tage_in_Hospital"],
    mode="markers",
    marker=dict(color=farben, size=8, opacity=0.8),
    showlegend=False,
)

#Fit
fig1.add_scatter(
    x=x_linie,
    y=y_linie,
    mode="lines",
    line=dict(color="red", width=3),
    showlegend=False,
)

#Plot Layout
fig1.update_layout(
    xaxis=dict(
        title="Impfstatus",
        tickvals=[0, 1],                #Nur 0 und 1 anzeigen
        ticktext=[
            "0 (Ungeimpft)",
            "1 (Geimpft)",
        ], 
        range=[-0.3, 1.3],               #seitlicher Abstand
        showgrid=True,
        gridcolor="#E2E8F0",
        zeroline=False,
    ),
    yaxis=dict(title="Tage im Krankenhaus", showgrid=True, gridcolor="#E2E8F0")
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown(
    r'''
    Die **Confounder-Effekt Stärke** beschreibt den Einfluss des Alters (X) auf die Krankenhausaufenthautsdauer (Y) und kann mit dem linken Schieberegler angepasst werden. 
    Die **Treatment-Effekt Stärke** ($\tau$) beschreibt den Einfluss der Impfung (D) auf die Krankenhausaufenthautsdauer (Y) und kann mit dem rechten Schieberegler angepasst werden. 
    Wird die Treatment-Effekt Stärke auf -10 gesetzt, so muss ein Patient 10 Tage kürzer im Krankenhaus bleiben, als wenn er nicht geimpft worden wäre. 
'''
)
#fig1.show()

st.markdown("## Alter als Confounder ")
st.markdown(
    r'''
    Die Anzahl der Tage im Krankenhaus wird über das Alter aufgetragen. Das Alter korreliert in dem Modell linear mit der Anzahl der Tage im Krankenhaus,
    wobei die Confounder-Effekt Stärke der Proportionalitätsfaktor ist.
    Einfach gesagt: Ältere Menschen verbringen wegen ihrer schlechteren körperlichen Verfassung im Durchschnitt eine längere Zeit im Krankenhaus. 
    Außerdem sind die Impfungen nicht gleichverteilt. Ältere Menschen sind aufgrund von Impfempfehlungen tendentiell öfter geimpft.
'''
)


#Farben für die Punkte
farben = np.where(df_sample["Geimpft"] == 1, "orange", "blue")

#lineare Regression
fit_alter = np.polyfit(df_sample["Alter"], df_sample["Tage_in_Hospital"], 1)
x_linie_alter = np.array([df_sample["Alter"].min(), df_sample["Alter"].max()])
y_linie_alter = np.polyval(fit_alter, x_linie_alter)

fig2 = go.Figure()

#Datenpunkte
fig2.add_scatter(
    x=df_sample["Alter"],
    y=df_sample["Tage_in_Hospital"],
    mode="markers",
    marker=dict(color=farben, size=8, opacity=0.8),
    showlegend=False,
)

#Fit
fig2.add_scatter(
    x=x_linie_alter,
    y=y_linie_alter,
    mode="lines",
    line=dict(color="red", width=3),
    showlegend=False,
)

#Plot Layout
fig2.update_layout(
    xaxis=dict(
        title="Alter (Jahre)",
        range=[15, 85],  # Angenehmer seitlicher Abstand für Altersbereiche
        showgrid=True,
        gridcolor="#E2E8F0",
    ),
    yaxis=dict(
        title="Tage im Krankenhaus", showgrid=True, gridcolor="#E2E8F0"
    ),
)

st.plotly_chart(fig2, use_container_width=True)
#fig2.show()

st.markdown(
    """
    <style>
    a {
        color: black !important;
        text-decoration: none !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown("## Double ML")
st.markdown(
    r'''
    Double ML basiert auf dem [**Frisch-Waugh-Lovell Theorem**](/kausales_ml#das-modell-partially-linear-regression). 
$$
\begin{array}{rll}
\tilde{Y} = Y - \hat Y & : & \hat Y \text{ Vorhersage des Outcomes berechnet durch ein ML-Modell} \\
\tilde{D} = D - \hat D & : & \hat D \text{ Vorhersage des Treatments berechnet durch ein ML-Modell}
\end{array}
$$
'''
)

st.markdown(
    r'''
    Durch diese sogenannte Resisualisierung wird der Effekt der Confounder (Alter) rausgerechnet und es bleibt
    nur noch der wahre Effekt des Treatments (Impfung) auf das Outcome (Aufenthaltsdauer) übrig. Die Regression des
    Residuums des Outcomes $\tilde{Y}$ auf des Residuum des Treatments $\tilde{D}$ liefert eine Vorhersage
    für den wahren Treatmenteffekt $\hat \tau$.
'''
)
#nachher link

st.markdown("## Der wahre Effekt des Impfens")
st.markdown(
    r'''
    Die Vorhersagen $\hat Y$ und $\hat D$ für das Residualisieren können mit verscheidenen ML-Modellen getroffen werden. In dem unteren Dropdownmenü 
    können ein lineares Modell, ein RandomForest Modell und ein Neuronales Netzwerk ausgewählt werden. 
'''
)

model_options_m = {
    "OLS ML": LogisticRegression(),
    "Random Forest ML": RandomForestClassifier(n_estimators=100, random_state=42)
}

model_options_l = {
    "OLS ML": LinearRegression(),
    "Random Forest ML": RandomForestRegressor(n_estimators=100, random_state=42)
}

regler_model_m, regler_model_l = st.columns(2)

selected_label_m = regler_model_m.selectbox(
    "Modell zur Berechnung von $\hat D$", ["OLS ML", "Random Forest ML", "Neuronales ML"], index=0
)
selected_label_l = regler_model_l.selectbox(
    "Modell zur Berechnung von $\hat Y$ ", ["OLS ML", "Random Forest ML", "Neuronales ML"], index=0
)

if selected_label_m == "Neuronales ML":
    regler_schichten_m, regler_neuronen_m = st.columns(2)
    schichten_m = regler_schichten_m.slider("Hidden Layers D", 1, 3, 1)
    neuronen_m = regler_neuronen_m.select_slider(
        "Neuronen pro Layer D", options=[2, 4, 8, 16, 32, 64], value=4
    )
    used_model_m = make_pipeline(
        StandardScaler(),
        MLPClassifier(hidden_layer_sizes=(neuronen_m,) * schichten_m, solver="lbfgs", activation="tanh", max_iter=2000, random_state=42)
    )
else:
    used_model_m = model_options_m[selected_label_m]


if selected_label_l == "Neuronales ML":
    regler_schichten_l, regler_neuronen_l = st.columns(2)
    schichten_l = regler_schichten_l.slider("Hidden Layers Y", 1, 3, 1)
    neuronen_l = regler_neuronen_l.select_slider(
        "Neuronen pro Layer Y", options=[2, 4, 8, 16, 32, 64], value=4
    )
    used_model_l = make_pipeline(
        StandardScaler(),
        MLPRegressor(hidden_layer_sizes=(neuronen_l,) * schichten_l, solver="lbfgs", activation="tanh",max_iter=2000, random_state=42)
    )
else:
    used_model_l = model_options_l[selected_label_l]

dml_data = dml.DoubleMLData(
    df_sample, y_col="Tage_in_Hospital", d_cols="Geimpft", x_cols=["Alter"]
)

#Modell initialisieren (ml_l für Y, ml_m für D)
dml_plr = dml.DoubleMLPLR(
    dml_data,
    ml_l=used_model_l,
    ml_m=used_model_m,
    score="partialling out",
)

#Modell fitten
dml_plr.fit()

#Residuen aus dem Modell extrahierem
hat_g = dml_plr.predictions["ml_l"].reshape(-1)
hat_m = dml_plr.predictions["ml_m"].reshape(-1)

residuum_krankenhaustage = dml_data.y.reshape(-1) - hat_g
residuum_impfen = dml_data.d.reshape(-1) - hat_m

#Fit durch die Residuen
dml_fit = np.polyfit(residuum_impfen, residuum_krankenhaustage, 1)
x_linie_dml = np.array([residuum_impfen.min(), residuum_impfen.max()])
y_linie_dml = np.polyval(dml_fit, x_linie_dml)
steigung = dml_fit[0]

farben = np.where(df_sample["Geimpft"] == 1, "orange", "blue")

fig3 = go.Figure()

#Datenpunkte
fig3.add_scatter(
    x=residuum_impfen,
    y=residuum_krankenhaustage,
    mode="markers",
    marker=dict(color=farben, size=8, opacity=0.8),
    showlegend=False,
)

#Fit
fig3.add_scatter(
    x=x_linie_dml,
    y=y_linie_dml,
    mode="lines",
    line=dict(color="red", width=3),
    showlegend=False,
)

#Layout
fig3.update_layout(
    xaxis=dict(
        title=r"Residualisierter Impfstatus (D̃)",
        showgrid=True,
        gridcolor="#E2E8F0",
        zeroline=False,
    ),
    yaxis=dict(
        title=r"Residualisierte Tage im Krankenhaus (Ỹ)",
        showgrid=True,
        gridcolor="#E2E8F0",
        zeroline=False,
    ),
)

st.plotly_chart(fig3, use_container_width=True)

metrik_wahr, metrik_berechnet = st.columns(2)

with metrik_wahr:
    st.markdown("Wahrer Treatment-Effekt $\\tau$:")
    st.metric(label="Wahr", value=f"{treatment_effect:.1f}", label_visibility="collapsed")

with metrik_berechnet:
    st.markdown("Vorhergesagter Effekt $\\hat{\\tau}$:")
    st.metric(label="Berechnet", value=f"{steigung:.1f}", label_visibility="collapsed")
#fig3.show()