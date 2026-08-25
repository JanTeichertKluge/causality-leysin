import numpy as np
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

st.title("Randomized Controlled Trials")

#Einführung
st.header("Einführung in Randomisierte Kontrollierte Studien (RCTs)")
st.markdown("Bei einer randomisierten kontrollierten Studie (RCT) handelt es sich um eine Forschungsmethode, mit der untersucht wird, ob eine bestimmte Intervention ein bestimmtes Ergebnis bewirkt. ")
st.markdown("Bei einer RCT werden die Teilnehmer:innen nach dem Zufallsprinzip einer Behandlungs- oder einer Kontrollgruppe zugeordnet. Die Behandlungsgruppe erhält beispielsweise ein neues Medikament, während die Kontrollgruppe dieses nicht erhält oder die übliche Behandlung erhält. Anschließend vergleichen die Forscher die gesundheitlichen Ergebnisse beider Gruppen, um die Wirkung des Medikaments abzuschätzen. ")
st.markdown("Die zufällige Zuordnung ist wichtig, da sie jedem Teilnehmer die gleiche Chance gibt, in eine der beiden Gruppen eingeteilt zu werden. Dadurch sind die Gruppen zu Beginn der Studie in der Regel ähnlich, auch hinsichtlich Merkmalen, die die Forscher möglicherweise nicht gemessen haben. Daher können Unterschiede in den Ergebnissen mit größerer Sicherheit der Intervention und nicht anderen Faktoren zugeschrieben werden. ")
st.markdown("Allerdings hält sich nicht jeder Teilnehmer wie geplant an die zugewiesene Behandlung. So vergessen manche Personen in der Behandlungsgruppe möglicherweise, das Medikament einzunehmen, brechen die Einnahme aufgrund von Nebenwirkungen ab oder nehmen nur einen Teil der verschriebenen Dosis ein. Dieses Verhalten wird als non-compliance bezeichnet. Die Nichtbefolgung stellt eine Herausforderung dar, da die Gruppen die Behandlung, die die Teilnehmer tatsächlich erhalten haben, möglicherweise nicht mehr widerspiegeln. ")
st.markdown("Die Hauptfrage lautet daher nicht: **Wirkt das Medikament, wenn alle es korrekt einnehmen?** Sondern auch: **Wie wirkt sich die Zuweisung des Medikaments aus, wenn einige Teilnehmer den Behandlungsplan nicht einhalten?**")


#Non-Complience
st.header("Umgang mit Non-Compliance")

#Anwendung
st.subheader("Demo: Intention-To-Treat, Per-Protocol, Local-Average-Treatment-Effect")

n_regler = st.select_slider("Stichprobengröße", options=[50, 100, 200, 500, 1000, 5000], value=200)

np.random.seed(42)
n = n_regler

age = np.random.normal(loc=35, scale=10, size=n)
health = np.random.normal(loc=50, scale=15, size=n)
gender = np.random.choice(["m","w"], size=n)

treatment = np.random.choice([0,1], size=n)

actual_treatment_random = np.zeros(n, dtype=int)
actual_treatment_age = np.zeros(n, dtype=int)
p_comply_random = 0.8
p_comply_age = 0.9 - 0.01*age
idx_treated = treatment == 1
actual_treatment_random[idx_treated] = np.random.choice([1,0], size=idx_treated.sum(), p=[p_comply_random, 1-p_comply_random])

p_age_treated = p_comply_age[idx_treated]
actual_treatment_age[idx_treated] = (
    np.random.random(idx_treated.sum()) < p_age_treated
).astype(int)



error = np.random.normal(loc=0, scale=4, size=n)
outcome_random = 10*actual_treatment_random - 0.01*age + 0.01*health + error
outcome_age = 10*actual_treatment_age - 0.01*age + 0.01*health + error

df_random = pd.DataFrame({"age":age, "health":health, "gender":gender, "intended treatment":treatment, "actual treatment":actual_treatment_random, "outcome":outcome_random})
complient_random = df_random[df_random["actual treatment"] == 1]

df_age = pd.DataFrame({"age":age, "health":health, "gender":gender, "intended treatment":treatment, "actual treatment":actual_treatment_age, "outcome":outcome_age})
complient_age = df_age[df_age["actual treatment"] == 1]

intended_to_treat_random = df_random[df_random["intended treatment"] == 1]
intended_to_treat_age = df_age[df_age["intended treatment"] == 1]

idx_actual_treated_random = actual_treatment_random == 1
idx_actual_treated_age = actual_treatment_age == 1

control = df_random[df_random["intended treatment"] == 0]
control_mean = control["outcome"].mean()

itt_mean_random = intended_to_treat_random["outcome"].mean()
itt_effect_random = itt_mean_random - control_mean

pp_mean_random = complient_random["outcome"].mean()
pp_effect_random = pp_mean_random - control_mean

anteil_compliers_random = idx_actual_treated_random.sum() / idx_treated.sum()
late_mean_random = (itt_mean_random - control_mean) / anteil_compliers_random

itt_mean_age = intended_to_treat_age["outcome"].mean()
itt_effect_age = itt_mean_age - control_mean

pp_mean_age = complient_age["outcome"].mean()
pp_effect_age = pp_mean_age - control_mean

anteil_compliers_age = idx_actual_treated_age.sum() / idx_treated.sum()
late_mean_age = (itt_mean_age - control_mean) / anteil_compliers_age

methode = st.radio("**Methode**",["Intention-To-Treat", "Per-Protocol", "Local-Average-Treatment-Effect"], horizontal=True)

if methode.startswith("Intention"):
     st.markdown("**Intention-To-Treat**")
     st.markdown("In der Regel beginnen Forscher mit einer Intention-to-Treat-Analyse (ITT). Dabei werden die Teilnehmer entsprechend ihrer ursprünglichen Zufallszuordnung verglichen, unabhängig davon, ob sie den Behandlungsplan befolgt haben oder nicht. Die ITT-Analyse bewahrt den Nutzen der Randomisierung und schätzt die Wirkung der Verabreichung oder Zuweisung des Medikaments unter realen Bedingungen. ")
elif methode.startswith("Per"):
     st.markdown("**Per-Protocol**")
     st.markdown("Forscher können auch eine Per-Protocol-Analyse vorlegen, die nur Teilnehmer einbezieht, die den Behandlungsplan befolgt haben. Dies kann dabei helfen, die Wirkung bei Personen abzuschätzen, die sich an die Vorgaben halten. Zu beachten ist jedoch, dass diese Teilnehmer sich in wichtigen Punkten von denjenigen unterscheiden können, die sich nicht an die Vorgaben halten, wodurch die Analyse verzerrt sein kann.")
elif methode.startswith("Local"):
     st.markdown("**Local-Average-Treatment-Effect**")
     st.markdown("Um die Einschränkungen der ITT- und der Per-Protocol-Analyse zu überwinden, können Forscher die LATE-Methode nutzen (auch als Complier Average Causal Effect bekannt). Sie schätzt die kausale Wirkung der Behandlung gezielt für die Gruppe der sogenannten Compliers – also derjenigen Teilnehmer, die sich tatsächlich an die ihnen zugewiesene Regel halten.  ")
     st.markdown("Der LATE basiert methodisch auf einer sogenannten Instrumentenvariablen-Schätzung. Bei einer einseitigen Non-Compliance – wenn also nur Personen aus der Behandlungsgruppe die Einnahme verweigern (sog. Never-Takers), während die Kontrollgruppe garantiert unbehandelt bleibt – lässt sich der Effekt sehr anschaulich berechnen:  ")
     st.markdown(rf"""$LATE = \frac{{{"ITT"}}}{{{"Anteil Compliers"}}}$""")
     st.markdown("*ITT (Intention-to-Treat)*: Zunächst wird der Gesamteffekt der ursprünglichen Zuweisung über die gesamte Gruppe gemessen (z. B. der Unterschied im durchschnittlichen Gesundheitszustand.") 
     st.markdown("*Anteil Compliers*: Dieser Wert gibt an, wie viel Prozent der Teilnehmer in der Behandlungsgruppe das Medikament tatsächlich wie vorgesehen eingenommen haben.")
     st.markdown("**Annahme (Exclusion Restriction)**: Für diese Berechnung wird vorausgesetzt, dass die reine Zuweisung zur Behandlunggruppe keinen Einfluss auf das Ergebnis hat, sondern einzig und allein die tatsächliche Einnahme des Medikaments. Da Personen, die die Einnahme verweigern (Never-Takers), in beiden Gruppen unbehandelt bleiben, verändert die Zuweisung bei ihnen nichts. Der gesamte gemessene ITT-Effekt lässt sich somit vollständig auf die Gruppe der Compliers zurückführen. " \
     "Der LATE fällt bei vorhandener Non-Compliance immer höher aus als der ITT-Effekt, da er die Auswirkung der Behandlung nicht durch diejenigen verwässert, die sie gar nicht erst eingenommen haben.  ")
     st.markdown("(Hinweis: Neben der einseitigen Non-Compliance existiert theoretisch auch eine zweiseitige Non-Compliance, bei der zusätzlich Personen aus der Kontrollgruppe die Behandlung auf eigene Faust erhalten.) ")


compliance = st.radio("**Compliance**",["Random", "Age"], horizontal=True)

if compliance.startswith("Random"):
     st.markdown("Bei der Methode „Random“ werden 80% der Personen in der Treatment-Gruppe zufällig ausgewählt. Diese Personen wenden das Treatment wie vorgesehen an. Die übrigen 10% werden als Non-Compliance-Personen eingestuft und halten sich nicht an die vorgegebene Behandlung. " \
     "Bei dieser Methode hängt Non-Compliance ausschließlich vom Zufall ab. Merkmale wie Alter, Gesundheitszustand oder Motivation haben keinen Einfluss darauf, ob eine Person das Treatment einhält. ")
elif compliance.startswith("Age"):
     st.markdown("Bei der Methode „Age“ beeinflusst das Alter die Wahrscheinlichkeit für Non-Compliance. Es wird angenommen, dass ältere Personen mit höherer Wahrscheinlichkeit Schwierigkeiten haben, das Treatment wie vorgesehen anzuwenden. " \
     "Mögliche Gründe dafür sind beispielsweise ein erhöhtes Demenzrisiko, die gleichzeitige Einnahme mehrerer Medikamente und damit verbundene Übersichtsschwierigkeiten oder eine geringere Therapietreue. Diese Annahme ist jedoch eine Vereinfachung und sollte nicht als allgemeine Aussage über ältere Menschen verstanden werden. ")
st.space("small")

success = "Das Medikament erreicht die benötigte Wirksamkeit. Dabei wurde jedoch nicht berücksichtigt, dass unter realen Bedingungen Medikamente nicht ausschließlich vorschriftsgemäß eingenommen werden."
error = "Das Medikament erreicht die benötigte Wirksamkeit nicht. In der Realität ist der ITT-Wert Behörden zur Zulassung vorzulegen, da dieser die Wirksamkeit eines Medikaments unter Realbedingungen abbildet"

st.markdown(rf""" Mittelwert Kontrollgruppe: ${control_mean}$""")
st.markdown(rf""" Angenommen, unser Medikament gilt ab einem Effekt von $+8,5$ als wirksam.""")

if compliance.startswith("Random"):
    if methode.startswith("Intention"):
        st.dataframe(df_random)
        st.markdown(rf""" Mittelwert: ${itt_mean_random}$""")
        if control_mean > 0:
            st.markdown(rf""" Effekt: ${itt_mean_random} - {control_mean} = {itt_effect_random}$ """)
        else:
            st.markdown(rf""" Effekt: ${itt_mean_random} + {-control_mean} = {itt_effect_random}$ """)
        st.error(error)
    elif methode.startswith("Per"):
        st.dataframe(complient_random)
        st.markdown(rf""" Mittellwert: ${pp_mean_random}$""")
        if control_mean > 0:
            st.markdown(rf""" Effekt: ${pp_mean_random} - {control_mean} = {pp_effect_random}$ """)
        else:
             st.markdown(rf""" Effekt: ${pp_mean_random} + {-control_mean} = {pp_effect_random}$ """)
        st.success(success)
    elif methode.startswith("Local"):
        st.dataframe(df_random)
        if control_mean > 0:
            st.markdown(rf""" Effekt: $\frac{{{"Mittelwert(ITT) - Mittelwert(Kontrolle)"}}}{{{"Anteil Compliers"}}} = \frac{{{itt_mean_random-control_mean}}}{{{anteil_compliers_random}}} = {late_mean_random}$ """)
        else:
             st.markdown(rf""" Effekt: $\frac{{{"Mittelwert(ITT) + Mittelwert(Kontrolle)"}}}{{{"Anteil Compliers"}}} = \frac{{{itt_mean_random-control_mean}}}{{{anteil_compliers_random}}} = {late_mean_random}$ """)
        st.success(success)
elif compliance.startswith("Age"):
    if methode.startswith("Intention"):
            st.dataframe(df_age)
            st.markdown(rf""" Mittelwert: ${itt_mean_age}$ """)
            if control_mean > 0:
                st.markdown(rf""" Effekt: ${itt_mean_age} - {control_mean} = {itt_effect_age}$ """)
            else:
                st.markdown(rf""" Effekt: ${itt_mean_age} + {-control_mean} = {itt_effect_age}$ """)
            st.error(error)
    elif methode.startswith("Per"):
            st.dataframe(complient_age)
            st.markdown(rf""" Mittellwert: ${pp_mean_age}$ """)
            if control_mean > 0:
                st.markdown(rf""" Effekt: ${pp_mean_age} - {control_mean} = {pp_effect_age}$ """)
            else:
                st.markdown(rf""" Effekt: ${pp_mean_age} + {-control_mean} = {pp_effect_age}$ """)
            st.success(success)
    elif methode.startswith("Local"):
            st.dataframe(df_age)
            if control_mean > 0:
                st.markdown(rf""" Effekt: $\frac{{{"Mittelwert(ITT) - Mittelwert(Kontrolle)"}}}{{{"Anteil Compliers"}}} = \frac{{{itt_mean_age-control_mean}}}{{{anteil_compliers_age}}} = {late_mean_age}$ """)
            else:
                st.markdown(rf""" Effekt: $\frac{{{"Mittelwert(ITT) + Mittelwert(Kontrolle)"}}}{{{"Anteil Compliers"}}} = \frac{{{itt_mean_age-control_mean}}}{{{anteil_compliers_age}}} = {late_mean_age}$ """)
            st.success(success)


#Grenzen 
st.header("Grenzen eines RCT")
st.markdown("Trotz ihrer Vorteile sind RCTs nicht immer problemlos oder vollständig realisierbar. Besonders in der Medizin können ethische und praktische Gründe die Durchführung einschränken. Es wäre beispielsweise nicht vertretbar, "
    "Patientinnen und Patienten eine notwendige Behandlung vorzuenthalten oder ihnen absichtlich eine möglicherweise schädliche Behandlung zu geben. Außerdem können hohe Kosten, lange Studiendauern, eine geringe Teilnehmendenzahl, Nebenwirkungen "
    "oder Abbrüche die Ergebnisse beeinflussen. Auch die strengen Auswahlkriterien einer Studie können dazu führen, dass die Ergebnisse nicht vollständig auf alle Patientinnen und Patienten übertragbar sind. RCTs liefern daher wichtige Informationen "
    "über die Wirkung einer Behandlung, sollten aber immer gemeinsam mit klinischer Erfahrung, weiteren Studien und den individuellen Bedürfnissen der Patientinnen und Patienten betrachtet werden. ")