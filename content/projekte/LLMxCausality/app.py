"""Beispielprojekt: Bringen kleinere Schulklassen bessere Leistungen?

Vorlage für die Gruppenprojekte. Die sechs Tabs entsprechen genau den sechs
Abschnitten, die wir von einer Projektarbeit erwarten:

    Frage → Daten → Naive Analyse → Identifikation → Ergebnis → Limitationen

Wichtigste technische Regel: KEIN st.set_page_config() aufrufen, das erledigt
die Haupt-App.
"""

import sys
from pathlib import Path

import streamlit as st

ORDNER = Path(__file__).parent
if str(ORDNER) not in sys.path:
    sys.path.insert(0, str(ORDNER))

from LLMxCausanalyse import *
from daten import *

from utils.theming import FARBEN, merkkasten

st.markdown("# Können LLMs kausal denken, oder lernen sie lediglich auswendig?")
st.caption(
    "Projekt der Sommerakademie Leysin von Clemens, Baki, Jacob"
)

merkkasten(
    "Ziel des Projektes",
    "Ziel dieses Projektes ist es, die Fähigkeit von LLMs zu testen in Bezug auf kausales Denken. Wir erstellen " \
    "Fragen in unterschiedlichen Schwierigkeitsstufen und mit einem unterschiedlichen Gehalt an unnötigen Zusatzinformationen " \
    "und ermitteln dann, wie gut diese beantwortet werden und wie sehr die Wahl unserer Parameter eine Rolle spielt. " \
    "Unser Ziel ist es Hinweise darauf zu erlangen, ob LLMs wirklich logisch denken können, oder ob ihre Ausgaben lediglich " \
    "Ergebnis von gelernten Beispielen sind.",
    typ="merke",
)

st.markdown("# Einführung zu LLMs und Kausalität")
st.markdown("Eine detailierte Einführung in die Kausalität findet ihr hier: ")
st.page_link("views/kausalitaet/korrelation.py", label="Zur Kausalität", icon="🗂️")
st.markdown("Eine detailierte Einführung in LLMs findet ihr hier: ")
st.page_link("views/ml/llms_kausalitaet.py", label="Zu den LLMs", icon="🗂️")




st.divider()

st.markdown("# Unser Experiment")

st.markdown("Im Folgenden könnt ihr interaktiv die Schwierigkeit sowie die Menge an unnützen Information einstellen für die Fragen, die " \
" wir an Gemini Flash 3.7 stellen. Interessant ist neben der Performance bei wechselnder Schwierigkeit auch, wie sich die Qualität der " \
" Antwort bei unterschiedlichen Parametern, aber der gleichen Fragen verhält.")

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.markdown("**Schwierigkeit**")
    difficulty = st.slider(
        "Difficulty",
        0,
        2,
        width="stretch",
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("**Ausmaß an zusätzlicher, unnötiger Information**")
    random_bullshit = st.slider(
        "Extra Information",
        0,
        2,
        width="stretch",
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.write(
        f"**Difficulty:** {difficulty}  |  "
        f"**Extra:** {random_bullshit}"
    )


    fig = plot_accuracy(data_sets[difficulty][random_bullshit])
    st.plotly_chart(fig, width="stretch")


    st.subheader("Frage: ")
    st.markdown(fragen[difficulty][random_bullshit])

    st.subheader("Korrekte Antwort: ")
    st.markdown(["y - 1", "y + z - 1" , "y - 1 + a - 4"][difficulty])

st.divider()

st.markdown("## Beobachtungen: ")

st.markdown("Sofort fällt auf, dass bei gleicher Frage für verschiedene Parameter deutlich unterschiedliche Ergebnisse " \
"erzeugt werden. So scheint neben der Wahl der Schwierigkeit und der Menge an unnützen Informationen auch die Wahl der " \
"Parameter, wenngleich diese die kausalen Zusammenhänge nicht beeinflussen, ausschlaggebend zu sein.")

# 3x3 Grid mit fließendem Farbverlauf anzeigen
st.markdown("### Übersicht über alle Kombinationen")
#st.markdown("*Die Farbe zeigt die Genauigkeit: von rot (0%) über gelb (50%) bis grün (100%)*")

fig = create_accuracy_heatmap(data_sets)
st.plotly_chart(fig, use_container_width=True)

merkkasten(
    "Wir stellen fest:",
    "Tatsächlich sind die Ergebnisse nicht so, wie man vielleicht auf den ersten Blick vermuten würde. Zwar konnten alle" \
    " einfachen Fragen mit hoher Präzision gelöst werden, ungeachtet dem Gehalt an zusätzlichen, redundanten Informationen, " \
    "wir können aber auch feststellen, dass die Güte der Antwort nicht parallel zu der Komplexität der Fragen sinkt, sondern offenbar " \
    "an anderen, unbekannten Faktoren hängt. \nZudem ist sehr interessant, dass entgegen unseren Vermutungen mit zusätzlichen, redundanten " \
    "und teilweise sogar verwirrenden Informationen, die Qualität der Antworten zu steigen scheint.",
    typ="merke",
)

st.divider()

st.markdown("# Fazit")
st.markdown("Es ist zwar bekannt, dass moderne LLMs Matheklausuren und Benchmarktests auf höchstem Niveau lösen können, doch stellen " \
"wir fest, dass die gleichen Modelle an solchen, für Menschen recht simplen Fragen, an ihre Grenzen stoßen. \n" \
"Kann hier eine kausale Fähigkeit der Sprachmodelle angenommen werden, wenn die Antwortgüte scheinbar neben den gewählten " \
"Parametern auch von der Menge unnötiger Informationen abhängt und zumindest nur teilweise an der Komplexität des kausalen Zusammenhangs hängt?")
st.markdown("Die Vermutung, dass den LLMs die Fähigkeit fehlt kausale Zusammenhänge tiefgründig zu verstehen liegt nahe. " \
"Wir können annehmen, dass LLMs nicht vermögen tiefgründig kausale Zusammenhänge zu erkennen. Die Qualität der Antworten ist somit " \
"auf andere Faktoren, wie ähnliche Vorkommen in Trainingsdaten zurückzuführen. Eine plausible Erklärung für die Varianz der Qualität " \
"der Antworten bei gleicher Frage, aber anderen Parametern, ist somit auch gegeben, denn in Trainingsdaten sind mit Sicherheit ähnliche " \
"Beispiele zu finden, aber eben nur mit manchen Parameterkombinationen. ")
st.markdown("Deutlich verwunderlicher als diese Erkenntnis ist, dass mit zusätzlicher unnötiger Information die Qualität der Antworten " \
"steigt. Wir gehen davon aus, dass zusätzliche Informationen den Prompt verlängern und dass die Architektur des Modells daraus eine " \
"längere Reasoningzeit produziert, mit der verständlicherweise eine Verbesserung des Ergebnisses einhergeht.")
st.markdown("Zusammenfassend kann man also sagen, dass wir zum Schluss gekommen sind, dass LLMs wenn überhaupt nur im begrenzten Rahmen " \
"kausale Zusammenhänge erschließen können und dass der Begriff 'Causal Parrot' durchaus seine Berechtigung hat." )

merkkasten(
    "Disclaimer:",
    "Die Daten wurden mit Gemini Flash 3.7 erhoben, einem durchaus starken LLM, aber allerdings nicht auf dem gleichen Stand der " \
    "aktuell stärksten Modelle auf dem Markt. Unsere Beispiele sind auf dieses Modell angepasst, ähnliche Ergebnisse, mit allerdings etwas schwächerem Effekt, " \
    "konnten von uns aber auch mit mächtigeren Modellen wie Claude-Opus erzeugt werden.",
    typ="achtung",
)


st.divider()

st.page_link("views/projekte/uebersicht.py", label="Zur Projektübersicht", icon="🗂️")
