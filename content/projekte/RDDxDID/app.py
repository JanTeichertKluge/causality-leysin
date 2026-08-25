
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import statsmodels.formula.api as smf

st.markdown("**Quasi-Experimente: DiD und RDD**")
st.caption("Team: die Blondinen (Noah R., Helena S.)")

st.markdown("Die grundlegende Idee des Differences-in-Differences (DD) Schätzverfahrens besteht darin, die unterschiedliche Entwicklung zweier ursprünglich vergleichbarer Gruppen nach einem, für eine der Gruppen, disruptiven Ereignis zu vergleichen. Unser Ziel ist es den Effekt des disruptiven Ereignisses zu isolieren. Die zweite, unbetroffene Gruppe dient uns als Kontrolle. Nicht jede beliebige Gruppe kann als Kontrolle verwendet werden, um uns sinnvolle Informationen über die kontrafaktische Entwicklung liefern zu können, müssen wir davon ausgehen, dass sich beide Gruppen parallel entwickeln. Diese sogenannte Parallel-Trends-Assumption ist zentral für die Identifikation des kausalen Effekts, nur im Fall paralleler Trends können wir davon ausgehen dass die Unterschiede in den Entwicklungen der Gruppen ausschließlich auf das disruptive Ereignis zurückgehen.")
st.markdown("Im Folgenden ist die Treated Group die Gruppe, auf die das disruptive Ereignis wirkt, und die Untreated Group die Vergleichsgruppe.")
# Falls ihr Dateien aus eurem Ordner ladet:
florida = pd.read_csv(Path(__file__).parent / "SeriesReport-20260821045422_221c9b.csv")
georgia = pd.read_csv(Path(__file__).parent / "SeriesReport-20260821045510_c5cb8f.csv")
generiert = pd.read_csv(Path(__file__).parent / "hurricane_did_two_counties.csv")


CUTOFF=0
#Hole nötige Daten für die vier Regressionen (maybe untreated noch zusammenfassen)
links_untreated_time = generiert.loc[(generiert["treated"]==0) & (generiert["post"]==0), "event_time"]
links_treated_time = generiert.loc[(generiert["treated"]==1) & (generiert["post"]==0), "event_time"]
rechts_untreated_time = generiert.loc[(generiert["treated"]==0) & (generiert["post"]==1), "event_time"]
rechts_treated_time = generiert.loc[(generiert["treated"]==1) & (generiert["post"]==1), "event_time"]
links_untreated_rate = generiert.loc[(generiert["treated"]==0) & (generiert["post"]==0), "unemployment_rate"]
links_treated_rate = generiert.loc[(generiert["treated"]==1) & (generiert["post"]==0), "unemployment_rate"]
rechts_untreated_rate = generiert.loc[(generiert["treated"]==0) & (generiert["post"]==1), "unemployment_rate"]
rechts_treated_rate = generiert.loc[(generiert["treated"]==1) & (generiert["post"]==1), "unemployment_rate"]
# Finde Regression durch Polynominterpolation
fit_links_u = np.polyfit(links_untreated_time, links_untreated_rate, 1)
fit_rechts_u = np.polyfit(rechts_untreated_time, rechts_untreated_rate, 1)
fit_links_t = np.polyfit(links_treated_time, links_treated_rate, 1)
fit_rechts_t = np.polyfit(rechts_treated_time, rechts_treated_rate, 1)
#Unterscheide Bereiche
raster_links=np.linspace(-12, 0, 20)
raster_rechts=np.linspace(0, 12, 20)

fig2 = go.Figure()
for contestant, group in generiert.groupby("county"):
    fig2.add_scatter(x=group["event_time"], y=group["unemployment_rate"], name=contestant,
      hovertemplate="County=%s<br>event_time=%%{x}<br>unemployment_rate=%%{y}<extra></extra>"% contestant, mode="markers")
fig2.add_scatter(x=raster_links, y=np.polyval(fit_links_u, raster_links), mode="lines", name="Lineare Regression Untreated Group vor Treatment")
fig2.add_scatter(x=raster_links, y=np.polyval(fit_links_t, raster_links), mode="lines", name="Lineare Regression Treated Group vor Treatment")
fig2.add_scatter(x=raster_rechts, y=np.polyval(fit_rechts_u, raster_rechts), mode="lines", name="Lineare Regression Untreated Group nach Treatment")
fig2.add_scatter(x=raster_rechts, y=np.polyval(fit_rechts_t, raster_rechts), mode="lines", name="Lineare Regression Treated Group nach Treatment")
fig2.add_scatter(x=raster_rechts, y=np.polyval(fit_rechts_t, raster_rechts)-np.polyval(fit_rechts_u, raster_rechts), mode="lines", name="Differenz Untreated und Treated Group nach Treatment")
fig2.add_scatter(x=raster_links, y=np.polyval(fit_links_t, raster_links)-np.polyval(fit_links_u, raster_links), mode="lines", name="Differenz Untreated und Treated Group vor Treatment")
fig2.add_vline(x=CUTOFF, line_dash="dot", name="Hurricane")
        
fig2.update_layout(legend_title_text = "County")
fig2.update_xaxes(title_text="Time")
fig2.update_yaxes(title_text="Unemployment Rate")
st.plotly_chart(fig2, use_container_width=True)
rdd=np.polyval(fit_rechts_t, 0)-np.polyval(fit_links_t, 0)
did=np.polyval(fit_rechts_t, 0)-np.polyval(fit_rechts_u, 0)-np.polyval(fit_links_t, 0)+np.polyval(fit_links_u, 0)
st.markdown("Der Difference-in-Differences dieser Daten ist " + str(round(did,2)) + ". Der RDD-Wert ist " + str(round(rdd,2)) + ".")

st.markdown("Es macht einen Unterschied, wie viele Daten man in die Regression einrechnet, besonders, wenn danach ein weiteres disruptives Ereignis stattfindet. Man kann dieses Problem auch umgehen, indem man die verschiedenen Werte abhängig von der Zeit nach dem betrachteten Ereignis gewichtet. Wir werden die späteren Werte allerdings einfach ignorieren. Beides verhindert die Betrachtung von Spätfolgen.")

st.html("<html><center><a title='NOAA&#039;s GOES 16 Satellite, Public domain, via Wikimedia Commons' href='https://commons.wikimedia.org/wiki/File:Irma_2017-09-06_1230Z.jpg'><img width='250' alt='Irma 2017-09-06 1230Z' src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Irma_2017-09-06_1230Z.jpg/250px-Irma_2017-09-06_1230Z.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=thumbnail'></a></center></html>")
st.markdown("Betrachten wir dieses Problem nun am Beispiel des Hurricanes Irma, der 2017 auf Florida traf, Georgia allerdings verschonte. Irma traf am 10. September mit 285km/h auf die Küste Floridas und war mit 914 mbar Luftdruck der viertstärkste Hurricane in den USA.")
st.markdown("Da wir die Veränderungen im Arbeitsmarkt betrachten wollen, müssen wir besonders die Corona-Pandemie ab 2020 beachten. Hierfür können wir die Anzahl betrachteter Monate nach dem Hurricane verändern.")

regler_def, regler_2 = st.columns(2)
ente = regler_def.slider("Betrachtete Zeit nach disruptivem Ereignis (hier: Hurricane Irma)", 1.0, 20.0, 63.0, step=1.0)
links_georgia_time = georgia.loc[(georgia["event_time"]<=0), "event_time"]
links_florida_time = florida.loc[(florida["event_time"]<=0), "event_time"]
rechts_georgia_time = georgia.loc[(georgia["event_time"]>=1) & (georgia["event_time"]<=ente), "event_time"]
rechts_florida_time = florida.loc[(florida["event_time"]>=1) & (florida["event_time"]<=ente), "event_time"]
links_georgia_rate = georgia.loc[(georgia["event_time"]<=0), "unemployment rate"]
links_florida_rate = florida.loc[(florida["event_time"]<=0), "unemployment rate"]
rechts_georgia_rate = georgia.loc[(georgia["event_time"]>=1) & (georgia["event_time"]<=ente), "unemployment rate"]
rechts_florida_rate = florida.loc[(florida["event_time"]>=1) & (florida["event_time"]<=ente), "unemployment rate"]

fit_links_f = np.polyfit(links_florida_time, links_florida_rate, 1)
fit_rechts_f = np.polyfit(rechts_florida_time, rechts_florida_rate, 1)
fit_links_g = np.polyfit(links_georgia_time, links_georgia_rate, 1)
fit_rechts_g = np.polyfit(rechts_georgia_time, rechts_georgia_rate, 1)
raster_links=np.linspace(-68, 0, 200)
raster_rechts=np.linspace(0, ente, 200)

fig_real = go.Figure()
fig_real.add_scatter(x=links_georgia_time, y=links_georgia_rate, name="Georgia vor Hurricane")
fig_real.add_scatter(x=rechts_georgia_time, y=rechts_georgia_rate, name="Georgia nach Hurricane")
fig_real.add_scatter(x=links_florida_time, y=links_florida_rate, name="Florida vor Hurricane")
fig_real.add_scatter(x=rechts_florida_time, y=rechts_florida_rate, name="Florida nach Hurricane")
fig_real.add_scatter(x=raster_links, y=np.polyval(fit_links_g, raster_links), mode="lines", name="Lineare Regression Georgia vor Hurricane")
fig_real.add_scatter(x=raster_links, y=np.polyval(fit_links_f, raster_links), mode="lines", name="Lineare Regression Florida vor Hurricane")
fig_real.add_scatter(x=raster_rechts, y=np.polyval(fit_rechts_g, raster_rechts), mode="lines", name="Lineare Regression Georgia nach Hurricane")
fig_real.add_scatter(x=raster_rechts, y=np.polyval(fit_rechts_f, raster_rechts), mode="lines", name="Lineare Regression Florida nach Hurricane")
fig_real.add_scatter(x=raster_rechts, y=np.polyval(fit_rechts_f, raster_rechts)-np.polyval(fit_rechts_g, raster_rechts), mode="lines", name="Differenz Georgia und Florida nach Hurricane")
fig_real.add_scatter(x=raster_links, y=np.polyval(fit_links_f, raster_links)-np.polyval(fit_links_g, raster_links), mode="lines", name="Differenz Georgia und Florida vor Hurricane")
fig_real.add_vline(x=0, line_dash="dot", name="Hurricane")

fig_real.update_layout(legend_title_text="County")
fig_real.update_xaxes(title_text="Time")
fig_real.update_yaxes(title_text="Unemployment Rate")
st.plotly_chart(fig_real, use_container_width=True)

rdd = np.polyval(fit_rechts_f, 0) - np.polyval(fit_links_f, 0)
did = np.polyval(fit_rechts_f, 0) - np.polyval(fit_rechts_g, 0) - np.polyval(fit_links_f, 0) + np.polyval(fit_links_g, 0)

st.markdown("Der Difference-in-Differences dieser Daten ist " + str(round(did, 2)) + ". Der RDD-Wert ist " + str(round(rdd, 2)) + ".")

st.markdown("Wie können wir aber nun herausfinden, ob unsere Parallel-Trends-Annahme erfüllt ist?")
st.markdown("\n\nUnser erster Weg führt uns über die quadrierte Summe der Residuen, sprich den Distanzen zwischen wahren und geschätzten Werten. Je geringer diese Differenz ist, desto besser beschreibt die geschätzte Regression die wahren Werte der Parameter. Nehmen wir parallele Trends an, unterscheiden sich die linearen Regressionen beider Gruppen nur in ihren Intercepts, ihre Slopes sollten sehr ähnlich verlaufen. Diese Eigenschaften können wir für die Prüfung unserer Annahme nutzen: korrigieren wir für die Intercepts und nutzen die Regressionsgleichung der einen Gruppe, um Werte der anderen Gruppe zu schätzen, sollten sich die vorhergesagten Werte mit beiden Slope-Parametern wenig bis gar nicht unterscheiden. Verwenden wir nun das Ergebnis dieser “umgetauschten” Regression für die Berechnung der Residuen, bzw. deren quadrierter Summe, könnten wir überprüfen, ob es signifikante Unterschiede zwischen der Original- und getauschten Regression gibt. Bei parallelen Trends sollten nur geringe Unterschiede zwischen den verschiedenen quadrierten Summen der Residuen bestehen.")

regler0, regler1 = st.columns(2)
slope0 = regler0.slider("Slope Treated Group", -1.0, 1.0, 0.0, step=0.01)
slope1 = regler1.slider("Slope Untreated Group", -1.0, 1.0, 0.0, step=0.01)
# Finde Regression durch Polynominterpolation
fit_links_u = np.polyfit(links_untreated_time, links_untreated_rate, 1)
fit_rechts_u = np.polyfit(rechts_untreated_time, rechts_untreated_rate, 1)
fit_links_t = np.polyfit(links_treated_time, links_treated_rate, 1)
fit_rechts_t = np.polyfit(rechts_treated_time, rechts_treated_rate, 1)
#Unterscheide Bereiche
raster_links=np.linspace(-12, 0, 20)
raster_rechts=np.linspace(0, 12, 20)
slope_t, intercept_t = np.polyfit(links_treated_time, links_treated_rate, 1)
slope_u, intercept_u = np.polyfit(links_untreated_time, links_untreated_rate, 1)

fig= go.Figure()
for contestant, group in generiert.groupby("county"):
    fig.add_scatter(x=group["event_time"], y=group["unemployment_rate"], name=contestant,
      hovertemplate="County=%s<br>event_time=%%{x}<br>unemployment_rate=%%{y}<extra></extra>"% contestant, mode="markers")
fig.add_scatter(x=raster_links, y=slope_u*raster_links+intercept_t, mode="lines", name="Untreated Slope auf Treated")
fig.add_scatter(x=raster_links, y=slope_t*raster_links+intercept_u, mode="lines", name="Treated Slope auf Untreated")
fig.add_scatter(x=raster_links, y=slope0*raster_links+intercept_t, mode="lines", name="Slope auf Treated Group")
fig.add_scatter(x=raster_links, y=slope1*raster_links+intercept_u, mode="lines", name="Slope auf Untreated Group")
fig.add_vline(x=CUTOFF, line_dash="dot", name="Hurricane")
        
fig.update_layout(legend_title_text = "County")
fig.update_xaxes(title_text="Time")
fig.update_yaxes(title_text="Unemployment Rate")
st.plotly_chart(fig, use_container_width=True)
lut=links_untreated_time.to_numpy()
lur=links_untreated_rate.to_numpy()
ltt=links_treated_time.to_numpy()
ltr=links_treated_rate.to_numpy()
res_u_u=0
res_u_t=0
res_t_u=0
res_t_t=0
res_s_u=0 #User slope untreated
res_s_t=0 #User slope treated
for i in range(0, lut.size):
    res_u_u+=(lur[i]-slope_u*lut[i]-intercept_u)**2
    res_t_u+=(lur[i]-slope_t*lut[i]-intercept_u)**2
    res_s_u+=(lur[i]-slope1*lut[i]-intercept_u)**2

for i in range(0, ltt.size):
    res_u_t+=(ltr[i]-slope_u*ltt[i]-intercept_t)**2
    res_t_t+=(ltr[i]-slope_t*ltt[i]-intercept_t)**2
    res_s_t+=(ltr[i]-slope0*ltt[i]-intercept_t)**2

summen_matrix = pd.DataFrame({
    "Untreated Group": [res_u_u, res_t_u, res_s_u],
    "Treated Group": [res_u_t, res_t_t, res_s_t]
}, index=["Untreated Slope", "Treated Slope", "dein Slope"])
st.table(summen_matrix)


st.markdown("Schauen wir uns dies nun wieder am realen Beispiel von Florida und Georgia vor dem Hurricane Irma an.")


regler0, regler1 = st.columns(2)

slope0 = regler0.slider("Slope Florida", -1.0, 1.0, 0.0, step=0.01)
slope1 = regler0.slider("Slope Georgia", -1.0, 1.0, 0.0, step=0.01)

# Finde Regression durch Polynominterpolation
fit_links_georgia = np.polyfit(links_georgia_time, links_georgia_rate, 1)
fit_rechts_georgia = np.polyfit(rechts_georgia_time, rechts_georgia_rate, 1)
fit_links_florida = np.polyfit(links_florida_time, links_florida_rate, 1)
fit_rechts_florida = np.polyfit(rechts_florida_time, rechts_florida_rate, 1)

# Unterscheide Bereiche
raster_links = np.linspace(-68, 0, 200)
raster_rechts = np.linspace(0, 63, 200)

slope_florida, intercept_florida = np.polyfit(
    links_florida_time, links_florida_rate, 1
)
slope_georgia, intercept_georgia = np.polyfit(
    links_georgia_time, links_georgia_rate, 1
)

fig_real_2 = go.Figure()

fig_real_2.add_scatter(x=links_georgia_time, y=links_georgia_rate, name="Georgia vor Hurricane", mode="markers")
fig_real_2.add_scatter(x=rechts_georgia_time, y=rechts_georgia_rate, name="Georgia nach Hurricane", mode="markers")
fig_real_2.add_scatter(x=links_florida_time, y=links_florida_rate, name="Florida vor Hurricane", mode="markers")
fig_real_2.add_scatter(x=rechts_florida_time, y=rechts_florida_rate, name="Florida nach Hurricane", mode="markers")
fig_real_2.add_scatter(
    x=raster_links,
    y=slope_georgia * raster_links + intercept_florida,
    mode="lines",
    name="Georgias Slope auf Florida"
)

fig_real_2.add_scatter(
    x=raster_links,
    y=slope_florida * raster_links + intercept_georgia,
    mode="lines",
    name="Floridas Slope auf Georgia"
)

fig_real_2.add_scatter(
    x=raster_links,
    y=slope0 * raster_links + intercept_florida,
    mode="lines",
    name="Slope auf Florida Group"
)

fig_real_2.add_scatter(
    x=raster_links,
    y=slope1 * raster_links + intercept_georgia,
    mode="lines",
    name="Slope auf Georgia Group"
)

fig_real_2.add_vline(
    x=CUTOFF,
    line_dash="dot",
    name="Hurricane"
)

fig_real_2.update_layout(legend_title_text="County")
fig_real_2.update_xaxes(title_text="Time")
fig_real_2.update_yaxes(title_text="Unemployment Rate")

st.plotly_chart(fig_real_2, use_container_width=True)


lut = links_georgia_time.to_numpy()
lur = links_georgia_rate.to_numpy()
ltt = links_florida_time.to_numpy()
ltr = links_florida_rate.to_numpy()

res_georgia_georgia = 0
res_georgia_florida = 0
res_florida_georgia = 0
res_florida_florida = 0
res_s_georgia = 0  # User slope Georgia
res_s_florida = 0  # User slope Florida

for i in range(0, lut.size):
    res_georgia_georgia += (
        lur[i] - slope_georgia * lut[i] - intercept_georgia
    ) ** 2

    res_florida_georgia += (
        lur[i] - slope_florida * lut[i] - intercept_georgia
    ) ** 2

    res_s_georgia += (
        lur[i] - slope1 * lut[i] - intercept_georgia
    ) ** 2

for i in range(0, ltt.size):
    res_georgia_florida += (
        ltr[i] - slope_georgia * ltt[i] - intercept_florida
    ) ** 2

    res_florida_florida += (
        ltr[i] - slope_florida * ltt[i] - intercept_florida
    ) ** 2

    res_s_florida += (
        ltr[i] - slope0 * ltt[i] - intercept_florida
    ) ** 2

summen_matrix = pd.DataFrame({
    "Georgia": [res_georgia_georgia, res_florida_georgia, res_s_georgia],
    "Florida": [res_georgia_florida, res_florida_florida, res_s_florida]
}, index=["Georgias Slope", "Floridas Slope", "dein Slope"])
st.table(summen_matrix)
st.markdown("Man könnte natürlich auch die Steigungen der Regressionen vergleichen. Um einen Vergleichbaren Wert zu haben, normieren wir die Differenz der Steigungen mit der Steigung der Treated Group. Dieser sollte bei Parallelität annähernd 0 sein.")
st.markdown("In diesem Beispiel hat die Regression durch Georgia die Steigung " + str(round(slope_georgia, 4)) + "und die Regression durch Florida die Steigung " + str(round(slope_florida, 4)) + ". Also ist unser normierter Wert für die Steigungsdifferenz " + str(round((slope_florida-slope_georgia)/slope_florida, 4)) + ".")
st.markdown("Der zweite Weg die Annahme zu überprüfen nutzt eine zweite DD-Schätzung vor unserem eigentlich betrachteten disruptiven Ereignis. Wir verkürzen damit iterativ den Zeitraum für den wir parallele Trends annehmen, indem wir immer frühere Zeiten für das künstliche disruptive Ereignis wählen, und testen gleichzeitig, ob es zu einem der vorangegangenen Zeitpunkte ein Ereignis gab, dass zu einer signifikant unterschiedlichen Entwicklung der Trends führt. An dem Punkt an dem wir einen signifikanten DD-Effekt vor dem eigentlichen disruptiven Ereignis finden brechen wir den Prozess ab und können die Hypothese paralleler Trends ablehnen oder müssen einen kürzeren Zeitraum betrachten. ")



regler, regler2 = st.columns(2)
CUTOFF = regler.slider("Testzeitpunkt Parallelität", -10.0, -1.0, -5.0, step=0.01)

JAHRE = np.arange(-12, 12)
REFORM = 0

links_untreated_time = generiert.loc[(generiert["treated"]==0) & (generiert["event_time"]<CUTOFF)&(generiert["event_time"]<REFORM), "event_time"]
links_treated_time = generiert.loc[(generiert["treated"]==1) & (generiert["event_time"]<CUTOFF)&(generiert["event_time"]<REFORM), "event_time"]
rechts_untreated_time = generiert.loc[(generiert["treated"]==0) & (generiert["event_time"]>=CUTOFF)&(generiert["event_time"]<REFORM), "event_time"]
rechts_treated_time = generiert.loc[(generiert["treated"]==1) & (generiert["event_time"]>=CUTOFF)&(generiert["event_time"]<REFORM), "event_time"]
links_untreated_rate = generiert.loc[(generiert["treated"]==0) & (generiert["event_time"]<CUTOFF)&(generiert["event_time"]<REFORM), "unemployment_rate"]
links_treated_rate = generiert.loc[(generiert["treated"]==1) & (generiert["event_time"]<CUTOFF)&(generiert["event_time"]<REFORM), "unemployment_rate"]
rechts_untreated_rate = generiert.loc[(generiert["treated"]==0) & (generiert["event_time"]>=CUTOFF)&(generiert["event_time"]<REFORM), "unemployment_rate"]
rechts_treated_rate = generiert.loc[(generiert["treated"]==1) & (generiert["event_time"]>=CUTOFF)&(generiert["event_time"]<REFORM), "unemployment_rate"]
# Finde Regression durch Polynominterpolation
fit_links_u = np.polyfit(links_untreated_time, links_untreated_rate, 1)
fit_rechts_u = np.polyfit(rechts_untreated_time, rechts_untreated_rate, 1)
fit_links_t = np.polyfit(links_treated_time, links_treated_rate, 1)
fit_rechts_t = np.polyfit(rechts_treated_time, rechts_treated_rate, 1)
#Unterscheide Bereiche
raster_links=np.linspace(-12, CUTOFF, 20)
raster_rechts=np.linspace(CUTOFF, 0, 20)

#Plot
fig_2 = go.Figure()
for contestant, group in generiert.groupby("county"):
#    fig.add_trace(go.Bar(x=group["event_time"], y=group["unemployment_rate"], name=contestant,
#     hovertemplate="County=%s<br>event_time=%%{x}<br>unemployment_rate=%%{y}<extra></extra>"% contestant))
    fig_2.add_scatter(x=group["event_time"], y=group["unemployment_rate"], name=contestant,
      hovertemplate="County=%s<br>event_time=%%{x}<br>unemployment_rate=%%{y}<extra></extra>"% contestant, mode="markers")
fig_2.add_scatter(x=raster_links, y=np.polyval(fit_links_u, raster_links), mode="lines", name="Lineare Regression Untreated Group.")
fig_2.add_scatter(x=raster_links, y=np.polyval(fit_links_t, raster_links), mode="lines", name="Lineare Regression Treated Group vor Treatment")
fig_2.add_scatter(x=raster_rechts, y=np.polyval(fit_rechts_u, raster_rechts), mode="lines", name="Lineare Regression Untreated Group")
fig_2.add_scatter(x=raster_rechts, y=np.polyval(fit_rechts_t, raster_rechts), mode="lines", name="Lineare Regression Treated Group nach Treatment")
fig_2.add_scatter(x=raster_rechts, y=np.polyval(fit_rechts_t, raster_rechts)-np.polyval(fit_rechts_u, raster_rechts), mode="lines", name="Differenz Untreated und Treated Group nach Treatment")
fig_2.add_scatter(x=raster_links, y=np.polyval(fit_links_t, raster_links)-np.polyval(fit_links_u, raster_links), mode="lines", name="Differenz Untreated und Treated Group vor Treatment")
fig_2.add_vline(x=REFORM, line_dash="dot", name="Hurricane")
fig_2.add_vline(x=CUTOFF, line_dash="dot", name="Parallelität Testzeit")
fig_2.update_layout(legend_title_text = "County")
fig_2.update_xaxes(title_text="Time")
fig_2.update_yaxes(title_text="Unemployment Rate")
st.plotly_chart(fig_2, use_container_width=True)
rdd=np.polyval(fit_rechts_t, 0)-np.polyval(fit_links_t, 0)
did=np.polyval(fit_rechts_t, raster_rechts).mean()-np.polyval(fit_rechts_u, raster_rechts).mean()-np.polyval(fit_links_t, raster_links).mean()+np.polyval(fit_links_u, raster_links).mean()
st.markdown("Der Difference-in-Differences dieser Daten an unserem künstlichen Ereignis ist " + str(round(did,2)) + ".")

st.markdown("Da in diesem Beispiel sehr wenig Messwerte vorliegen, ist diese Methode hier nicht wirklich effektiv. Daher lohnt es sich, noch einmal unser Beispiel mit dem Hurricane zu betrachten.")

regler, regler2 = st.columns(2)
CUTOFF = regler.slider("Testzeitpunkt Parallelität", -62.0, -1.0, -20.0, step=0.01)

JAHRE = np.arange(-63, 20)
REFORM = 0

links_georgia_time = georgia.loc[
    (georgia["event_time"] < CUTOFF)
    & (georgia["event_time"] < REFORM),
    "event_time"
]

links_florida_time = florida.loc[
    (florida["event_time"] < CUTOFF)
    & (florida["event_time"] < REFORM),
    "event_time"
]

rechts_georgia_time = georgia.loc[
    (georgia["event_time"] >= CUTOFF)
    & (georgia["event_time"] < REFORM),
    "event_time"
]

rechts_florida_time = florida.loc[
    (florida["event_time"] >= CUTOFF)
    & (florida["event_time"] < REFORM),
    "event_time"
]

links_georgia_rate = georgia.loc[
    (georgia["event_time"] < CUTOFF)
    & (georgia["event_time"] < REFORM),
    "unemployment rate"
]

links_florida_rate = florida.loc[
    (florida["event_time"] < CUTOFF)
    & (florida["event_time"] < REFORM),
    "unemployment rate"
]

rechts_georgia_rate = georgia.loc[
    (georgia["event_time"] >= CUTOFF)
    & (georgia["event_time"] < REFORM),
    "unemployment rate"
]

rechts_florida_rate = florida.loc[
    (florida["event_time"] >= CUTOFF)
    & (florida["event_time"] < REFORM),
    "unemployment rate"
]

# Finde Regression durch Polynominterpolation
fit_links_georgia = np.polyfit(
    links_georgia_time,
    links_georgia_rate,
    1
)

fit_rechts_georgia = np.polyfit(
    rechts_georgia_time,
    rechts_georgia_rate,
    1
)

fit_links_florida = np.polyfit(
    links_florida_time,
    links_florida_rate,
    1
)

fit_rechts_florida = np.polyfit(
    rechts_florida_time,
    rechts_florida_rate,
    1
)

# Unterscheide Bereiche
raster_links = np.linspace(-63, CUTOFF, 200)
raster_rechts = np.linspace(CUTOFF, 0, 200)

# Plot
fig_real_2 = go.Figure()

fig_real_2.add_scatter(
    x=georgia["event_time"],
    y=georgia["unemployment rate"],
    name="Georgia",
    mode="lines"
)

fig_real_2.add_scatter(
    x=florida["event_time"],
    y=florida["unemployment rate"],
    name="Florida",
    mode="lines"
)

fig_real_2.add_scatter(
    x=raster_links,
    y=np.polyval(fit_links_georgia, raster_links),
    mode="lines",
    name="Lineare Regression Georgia Group"
)

fig_real_2.add_scatter(
    x=raster_links,
    y=np.polyval(fit_links_florida, raster_links),
    mode="lines",
    name="Lineare Regression Florida Group vor imaginärem Treatment"
)

fig_real_2.add_scatter(
    x=raster_rechts,
    y=np.polyval(fit_rechts_georgia, raster_rechts),
    mode="lines",
    name="Lineare Regression Georgia Group"
)

fig_real_2.add_scatter(
    x=raster_rechts,
    y=np.polyval(fit_rechts_florida, raster_rechts),
    mode="lines",
    name="Lineare Regression Florida Group nach imaginärem Treatment"
)

fig_real_2.add_scatter(
    x=raster_rechts,
    y=(
        np.polyval(fit_rechts_florida, raster_rechts)
        - np.polyval(fit_rechts_georgia, raster_rechts)
    ),
    mode="lines",
    name="Differenz Georgia und Florida Group nach imaginärem Treatment"
)

fig_real_2.add_scatter(
    x=raster_links,
    y=(
        np.polyval(fit_links_florida, raster_links)
        - np.polyval(fit_links_georgia, raster_links)
    ),
    mode="lines",
    name="Differenz Georgia und Florida Group vor imaginärem Treatment"
)

fig_real_2.add_vline(
    x=REFORM,
    line_dash="dot",
    name="Hurricane"
)

fig_real_2.add_vline(
    x=CUTOFF,
    line_dash="dot",
    name="Parallelität Testzeit"
)

fig_real_2.update_layout(
    legend_title_text="County"
)

fig_real_2.update_xaxes(
    title_text="Time"
)

fig_real_2.update_yaxes(
    title_text="Unemployment_rate"
)

st.plotly_chart(
    fig_real_2,
    use_container_width=True
)

did = (
    np.polyval(fit_rechts_florida, raster_rechts).mean()
    - np.polyval(fit_rechts_georgia, raster_rechts).mean()
    - np.polyval(fit_links_florida, raster_links).mean()
    + np.polyval(fit_links_georgia, raster_links).mean()
)

st.markdown(
    "Der Difference-in-Differences zu unserem imaginärem Ereignis ist "
    + str(round(did,3))
    + "."
)