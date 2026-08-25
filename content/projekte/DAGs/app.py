
# %%
import os
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import streamlit as st

from causallearn.graph.Endpoint import Endpoint
from causallearn.search.ConstraintBased.PC import pc
from causallearn.utils.cit import fisherz

DATA_DIR = Path(__file__).resolve().parent / "datasets"

# ============================================================
# PAGE CONFIG
# ============================================================

# ============================================================
# EINFÜHRUNG
# ============================================================

st.title("☕ Causal Discovery: Kaffeekonsum und Lebenserwartung")

st.markdown(
    """
### Forschungsfrage

**Hat Kaffeekonsum einen kausalen Effekt auf die Lebenserwartung?**

Wir verwenden fünf simulierte Datensätze, die unterschiedliche angenommene kausale
Strukturen zwischen folgenden Variablen repräsentieren:

- Coffee consumption
- Socioeconomic status (SES)
- Diet
- Baseline health
- Life expectancy

Ziel ist es zu untersuchen, inwieweit der **PC-Algorithmus** die zugrunde liegende kausale Struktur allein anhand der beobachteten Daten rekonstrukieren kann.
"""
)

st.info(""" **Causal Discovery:** Der Prozess aus Daten auf kausale Zusammenhänge zwischen den zugrunde liegenden Variablen zu schließen""") 

st.success("""### **DAGs Recap!** 

* Ein DAG (Directed Acyclic Graph) stellt angenommene kausale Beziehungen zwischen Variablen dar. Knoten (Nodes) sind Variablen, gerichtete Kanten (Edges) zeigen die angenommene kausale Richtung: X → Y. Acyclic bedeutet, dass es keine gerichteten Kreisläufe gibt.
* Bei X → Y ist X ein Parent von Y und Y ein Child von X.
* Ein Confounder ist eine gemeinsame Ursache zweier Variablen: X ← Z → Y. Dadurch kann eine Assoziation zwischen X und Y entstehen, obwohl diese nicht (vollständig) auf einem kausalen Effekt von X auf Y beruht.
* Ein Mediator liegt auf einem kausalen Pfad zwischen zwei Variablen: X → M → Y. Er beschreibt einen Mechanismus, über den X auf Y wirkt.
* Ein Collider ist eine gemeinsame Wirkung zweier Variablen: X → C ← Y. Anders als bei Confoundern sollte auf Collider typischerweise nicht konditioniert werden, da dadurch eine zuvor geschlossene Verbindung zwischen X und Y geöffnet werden kann.
* Conditioning bedeutet, eine Variable bei der Analyse konstant zu halten bzw. Informationen über ihren Wert zu berücksichtigen (z. B. durch Kontrolle in einem statistischen Modell). Je nach Position einer Variable im DAG kann Conditioning Pfade blockieren oder öffnen.

→ Causal Discovery kehrt die übliche Perspektive auf DAGs gewissermaßen um: Statt von einer angenommenen kausalen Struktur auf beobachtbare Zusammenhänge zu schließen, versucht man, aus Mustern von (Conditional) Independencies mögliche kausale Strukturen zu rekonstruieren.
""")
 
# D-SEPARATION

st.header("d-separation in DAGs")

st.markdown("""path zwischen Variablen X und Y **blocked** durch ein conditioning set Z (darf auch leer sein), wenn gilt:
1. path enthält eine Variable W mit ->W-> oder ->W<- mit W in Z
2. path enthält einen collider W und W, sowie seine descendants sind nicht in Z

X, Y **d-seperated** durch Z, wenn alle paths zwischen ihnen blocked (durch Z)sind
""")

st.markdown(
    "<small style='color: gray;'>"
    "Quelle: <a href='https://www.youtube.com/watch?v=yIwTzdwVz0Q' "
    "target='_blank'>Brady Neil</a>"
    "</small>",
    unsafe_allow_html=True,
)

d_separation_image_path = Path(__file__).parent / "Illustration_d-seperation-Beispiel.jpeg"
st.image(str(d_separation_image_path), caption="Erstellt mit Gemini AI")

st.header("PC-Algorithm - Theorie")

st.subheader("Annahmen")
st.markdown("""
- Acyclity
- Causal sufficiency: Es gibt keine nicht beobachtete Variable, die gemeinsame Ursache (parent) von zwei oder mehr beobachteten Varibalen ist
- Faithfulness: alle bedingten Unabhängigkeiten implizieren d-seperation im Graphen 
- Causal Markov condition: Jede Variable ist bedingt auf ihre parents unabhängig von allen anderen Variablen, die nicht Nachkommen sind
""")

st.markdown(
    "<small style='color: gray;'>"
    "Quelle: <a href='https://docs.actable.ai/causal_discovery.html' "
    "target='_blank'>Actable AI</a>"
    "</small>",
    unsafe_allow_html=True,
)

st.subheader("Struktur")
illustration_path = Path(__file__).parent / "Illustration_PC-Algo.png"
st.image(str(illustration_path), caption="Quelle: Shaw Talebi")
st.markdown(
    "<small style='color: gray;'>"
    "<a href='https://www.youtube.com/watch?v=tufdEUSjmNI&t=190s' "
    "target='_blank'>Zum Video von Shaw Talebi</a>"
    "</small>",
    unsafe_allow_html=True,
)


st.subheader("Wie orientieren wir Kanten?")
st.markdown("""Wir erinnern an die besondere Rolle von Collidern. Finden wir V Strukturen der Form X-M-Y (wobei X, Y unabhänigig sind, also die Kante entfernt wurde), so prüfen wir ob X⊥Y∣M gilt. Wenn nicht dann handelt es sich bei M um einen Collider, und wir orientieren die Kante von X nach M und von Y nach M. Andernfalls erhalten wir zwar den Erkenntnisgewinn, dass M kein Collider ist, aber wir können die Kanten nicht orientieren (es könnte X->M->Y, X<-M<-Y oder X<-M->Y gelten).""")
st.markdown("""Unter der (notwendigen) Annahme der Azyklizität können wir eventuell noch weitere Kanten orientieren. In der Regel schaffen wir es aber nicht einen eindeutigen DAG zu erhalten.""")

st.markdown("""**Output: ein CPDAG** ist formal eine Markov-Äquivalenzklasse von DAGs, die wie folgt definiert ist: Zwei DAGs G,H sind äquivalent gdw alle d-seperation Bedingungen gleich sind:""")
st.latex(r"\forall A,B,Z \subseteq V:\quad (A \perp B \mid Z) \text{ in } G \Longleftrightarrow (A \perp B \mid Z) \text{ in } H")
st.markdown("""Für unsere Zwecke reicht es aber einen CPDAG als eine Graphen zu verstehen, der sowohl gerichtete als auch ungerichtete Kanten enthält. Oft helfen uns bereits bekannte Zusammenhänge, um noch näher an den tatsächlichen DAG zu kommen.""")

st.markdown(
    "<small style='color: gray;'>"
    "Quelle: <a href='https://www.emergentmind.com/topics/markov-equivalence-class-mec' "
    "target='_blank'>Emergent Mind</a>"
    "</small>",
    unsafe_allow_html=True,
)

# ------------------------
# INTERACTIVE BEISPIELE
# ------------------------

@st.cache_data
def load_datasets():
    return {
        "Independent": pd.read_csv(
            DATA_DIR / "dataset_1_unabhaengig.csv"
        ),
        "Chain": pd.read_csv(
            DATA_DIR / "dataset_2_kette.csv"
        ),
        "Collider": pd.read_csv(
            DATA_DIR / "dataset_3_collider.csv"
        ),
        "CPDAG": pd.read_csv(
            DATA_DIR / "dataset_4_cpdag.csv"
        ),
        "Mixed": pd.read_csv(
            DATA_DIR / "dataset_5_gemischt.csv"
        ),
    }

datasets = load_datasets()

# ============================================================
# PC ALGORITHM
# ============================================================

def run_pc(dataset, alpha=0.05):
    data = dataset.to_numpy(dtype=float)
    variable_names = list(dataset.columns)

    cg = pc(
        data,
        alpha=alpha,
        indep_test=fisherz,
        stable=True,
        node_names=variable_names,
        show_progress=False,
    )

    return cg

# ============================================================
# GRAPH PLOTTING
# ============================================================

def create_pc_plot(cg, title=None):
    graph = cg.G

    # Undirected graph used only to calculate node positions
    layout_graph = nx.Graph()

    for node in graph.get_nodes():
        layout_graph.add_node(node.get_name())

    for edge in graph.get_graph_edges():
        node1 = edge.get_node1().get_name()
        node2 = edge.get_node2().get_name()
        layout_graph.add_edge(node1, node2)

    pos = nx.spring_layout(
        layout_graph,
        seed=42,
        k=2,
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    nx.draw_networkx_nodes(
        layout_graph,
        pos,
        node_size=2600,
        ax=ax,
    )

    nx.draw_networkx_labels(
        layout_graph,
        pos,
        font_size=8,
        ax=ax,
    )

    for edge in graph.get_graph_edges():
        node1 = edge.get_node1().get_name()
        node2 = edge.get_node2().get_name()

        endpoint1 = edge.get_endpoint1()
        endpoint2 = edge.get_endpoint2()

        # A --- B
        if (
            endpoint1 == Endpoint.TAIL
            and endpoint2 == Endpoint.TAIL
        ):
            nx.draw_networkx_edges(
                layout_graph,
                pos,
                edgelist=[(node1, node2)],
                arrows=False,
                width=2,
                ax=ax,
            )

        # A --> B
        elif (
            endpoint1 == Endpoint.TAIL
            and endpoint2 == Endpoint.ARROW
        ):
            nx.draw_networkx_edges(
                layout_graph,
                pos,
                edgelist=[(node1, node2)],
                arrows=True,
                arrowstyle="-|>",
                arrowsize=24,
                width=2,
                node_size=2600,
                ax=ax,
            )

        # A <-- B
        elif (
            endpoint1 == Endpoint.ARROW
            and endpoint2 == Endpoint.TAIL
        ):
            nx.draw_networkx_edges(
                layout_graph,
                pos,
                edgelist=[(node2, node1)],
                arrows=True,
                arrowstyle="-|>",
                arrowsize=24,
                width=2,
                node_size=2600,
                ax=ax,
            )

        # Other endpoint types
        else:
            nx.draw_networkx_edges(
                layout_graph,
                pos,
                edgelist=[(node1, node2)],
                arrows=False,
                style="dashed",
                width=2,
                ax=ax,
            )

    if title:
        ax.set_title(title)

    ax.axis("off")

    return fig


# ============================================================
# EDGE TABLE
# ============================================================

def get_edges(cg):
    edge_list = []

    for edge in cg.G.get_graph_edges():
        node1 = edge.get_node1().get_name()
        node2 = edge.get_node2().get_name()

        endpoint1 = edge.get_endpoint1()
        endpoint2 = edge.get_endpoint2()

        if (
            endpoint1 == Endpoint.TAIL
            and endpoint2 == Endpoint.TAIL
        ):
            relation = "—"

        elif (
            endpoint1 == Endpoint.TAIL
            and endpoint2 == Endpoint.ARROW
        ):
            relation = "→"

        elif (
            endpoint1 == Endpoint.ARROW
            and endpoint2 == Endpoint.TAIL
        ):
            node1, node2 = node2, node1
            relation = "→"

        else:
            relation = "?"

        edge_list.append(
            {
                "From": node1,
                "Relation": relation,
                "To": node2,
            }
        )

    return pd.DataFrame(edge_list)




# ============================================================
# INTERAKTIVER EXPLORER
# ============================================================

st.divider()

st.header("Interaktive Anwendung des PC-Algorithmus")

control_col1, control_col2, control_col3 = st.columns(3)

with control_col1:
    selected_scenario = st.selectbox(
        "Kausale Struktur",
        list(datasets.keys()),
    )

selected_data = datasets[selected_scenario]

with control_col2:
    alpha = st.slider(
        "Signifikanzniveau α",
        min_value=0.001,
        max_value=0.20,
        value=0.05,
        step=0.001,
    )

with control_col3:
    sample_size = st.slider(
        "Stichprobengröße",
        min_value=50,
        max_value=len(selected_data),
        value=len(selected_data),
        step=50,
    )


# Use only the selected number of observations
analysis_data = selected_data.iloc[:sample_size]

# Run PC dynamically
pc_result = run_pc(
    analysis_data,
    alpha=alpha,
)


# ============================================================
# MAIN OUTPUT
# ============================================================

data_col, graph_col = st.columns([1, 2])

with data_col:
    st.subheader("Simulierte Daten")

    st.dataframe(
        analysis_data.head(10),
        use_container_width=True,
    )

    st.metric(
        "Beobachtungen",
        len(analysis_data),
    )

    st.metric(
        "Variablen",
        analysis_data.shape[1],
    )


with graph_col:
    st.subheader("Geschätzter CPDAG")

    fig = create_pc_plot(
        pc_result,
        title=f"PC Ergebnis – {selected_scenario}",
    )

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# KANTEN
# ============================================================

st.subheader("Vom PC-Algorithmus identifizierte Kanten")

edges = get_edges(pc_result)

if len(edges) == 0:
    st.info("Es wurden keine Kanten identifiziert.")
else:
    st.dataframe(
        edges,
        hide_index=True,
        use_container_width=True,
    )


# ============================================================
# ERKLÄRUNGEN
# ============================================================

st.divider()

st.header("Auf einen Blick: Wie funktioniert der PC-Algorithmus?")


with st.expander("Schritt 1 – Start mit einem vollständig verbundenen Graphen"):
    st.markdown(
        """
Der PC-Algorithmus beginnt zunächst mit der Annahme, dass alle Variablen
miteinander verbunden sein könnten.

Bei fünf Variablen startet er daher mit einem vollständig verbundenen,
ungerichteten Graphen.

Im nächsten Schritt werden Kanten entfernt, wenn die entsprechenden Variablen
als **conditionally independent** identifiziert werden.
"""
    )


with st.expander("Schritt 2 – Tests auf Conditional Independence"):
    st.markdown(
        """
Der PC-Algorithmus testet Aussagen der Form:

**X ⫫ Y | S**

Dabei sind:

- **X** und **Y** zwei Variablen,
- **S** eine Menge von Variablen, auf die konditioniert wird.

Beispielsweise fragt

**Coffee ⫫ Life Expectancy | SES**

danach, ob Coffee Consumption und Life Expectancy unabhängig voneinander sind,
wenn SES konstant gehalten wird.

Wird eine solche **Conditional Independence** gefunden, kann die entsprechende
Kante aus dem Graphen entfernt werden.

In dieser Anwendung verwenden wir dafür den **Fisher's Z Test**.
"""
    )


with st.expander("Schritt 3 – Identifikation von Collidern / V-Strukturen"):
    st.markdown(
        """
Bestimmte Muster von Conditional Independencies ermöglichen es dem
PC-Algorithmus, **Collider** bzw. **V-Structures** zu identifizieren.

Eine solche Struktur hat beispielsweise die Form:

**X → Z ← Y**

Dabei zeigen zwei Pfeile auf dieselbe Variable Z.

Collider sind besonders wichtig, weil sie es dem PC-Algorithmus ermöglichen,
bestimmte Kantenrichtungen aus Beobachtungsdaten zu identifizieren.

Sie gehören damit zu den zentralen Situationen, in denen der Algorithmus
gerichtete Pfeile bestimmen kann, anstatt eine Kante ungerichtet zu lassen.
"""
    )


with st.expander("Schritt 4 – Orientierung weiterer Kanten"):
    st.markdown(
        """
Nach der Identifikation von V-Structures versucht der PC-Algorithmus,
weitere Kanten zu orientieren.

Dafür werden logische Orientierungsregeln verwendet, die häufig als
**Meek's Rules** bezeichnet werden.

Dabei sollen insbesondere

- neue, nicht durch die Daten gestützte Collider und
- gerichtete Zyklen

vermieden werden.

Das Endergebnis ist in der Regel kein einzelner DAG, sondern ein **CPDAG
(Completed Partially Directed Acyclic Graph)**.
"""
    )


# ============================================================
# MARKOV ÄQUIVALENZKLASSEN
# ============================================================

with st.expander("Warum bleiben manche Kanten ungerichtet?"):
    st.markdown(
        """
Aus Beobachtungsdaten lassen sich nicht immer alle kausalen Richtungen
eindeutig bestimmen.

Beispielsweise können die Strukturen

**A → B → C**

**A ← B → C**

**A ← B ← C**

dieselben Conditional Independencies implizieren.

Diese DAGs gehören zur selben **Markov Equivalence Class**.

Der PC-Algorithmus kann anhand der beobachteten Conditional Independencies
nicht zwischen ihnen unterscheiden. Entsprechende Kanten bleiben daher im
CPDAG ungerichtet:

**A — B — C**

Eine ungerichtete Kante bedeutet also **nicht**, dass keine kausale Richtung
existiert. Sie bedeutet, dass die Richtung anhand der verfügbaren
Conditional-Independence-Informationen nicht eindeutig bestimmt werden kann.
"""
    )


# ============================================================
# LIMITATIONEN
# ============================================================

with st.expander("Annahmen und Limitationen"):
    st.markdown(
        """
Der PC-Algorithmus kann kausale Strukturen nicht ohne zusätzliche Annahmen
aus Beobachtungsdaten ableiten.

Zu den zentralen Annahmen gehören:

- **Causal Markov Condition**
- **Faithfulness**
- **Causal Sufficiency**
- geeignete Tests auf Conditional Independence
- eine ausreichende Stichprobengröße
- angemessene Messung der relevanten Variablen

In dieser Demonstration verwenden wir den **Fisher's Z Test**.

Einige unserer simulierten Variablen sind diskret oder ordinal. Die Annahmen
des Fisher's Z Tests sind für diese Variablen daher nicht vollständig erfüllt.

Die Anwendung sollte deshalb in erster Linie als **didaktische Demonstration
von Causal Discovery** verstanden werden und nicht als empirische Schätzung
des tatsächlichen kausalen Effekts von Kaffeekonsum auf die Lebenserwartung.
"""
    )


# ============================================================
# VERGLEICH DER FÜNF DATENSÄTZE
# ============================================================

st.divider()

st.header("Vergleich der fünf kausalen Strukturen")

st.markdown(
    """
Die folgenden Tabs zeigen das Ergebnis des PC-Algorithmus für jeden der fünf
simulierten Datensätze. Für alle Analysen wird das oben ausgewählte
**Signifikanzniveau α** verwendet.
"""
)

tabs = st.tabs(
    [
        "Independent",
        "Chain",
        "Collider",
        "CPDAG",
        "Mixed",
    ]
)


for tab, (name, dataset) in zip(
    tabs,
    datasets.items(),
):
    with tab:

        result = run_pc(
            dataset,
            alpha=alpha,
        )

        fig = create_pc_plot(
            result,
            title=f"PC Result – {name}",
        )

        st.pyplot(fig)

        plt.close(fig)

        tab_edges = get_edges(result)

        if len(tab_edges) == 0:
            st.info("Es wurden keine Kanten identifiziert.")
        else:
            st.dataframe(
                tab_edges,
                hide_index=True,
                use_container_width=True,
            )



# ENGLISCHER PART - NÖTIG?


# %%
data_path = Path(__file__).parent / "datasets"

dataset_unabhaengig = pd.read_csv(
    os.path.join(data_path, "dataset_1_unabhaengig.csv")
)

dataset_kette = pd.read_csv(
    os.path.join(data_path, "dataset_2_kette.csv")
)

dataset_collider = pd.read_csv(
    os.path.join(data_path, "dataset_3_collider.csv")
)

dataset_cpdag = pd.read_csv(
    os.path.join(data_path, "dataset_4_cpdag.csv")
)

dataset_gemischt = pd.read_csv(
    os.path.join(data_path, "dataset_5_gemischt.csv")
)

# %%
dataset_kette.head()


# %%
variables = list(dataset_kette.columns)

G_complete = nx.complete_graph(variables)

plt.figure(figsize=(12, 7))

pos = nx.spring_layout(G_complete, seed=42, k=2)

nx.draw(
    G_complete,
    pos,
    with_labels=True,
    node_size=2500,
    font_size=8
)






st.subheader("Implementierung")

st.markdown("""
Zur Erstellung der Datensätze haben wir eine LLM genutzt. 
Wir nutzen den PC-Algorithmus vom `causal-learn` Python package für die Schätzung der CPDAGs.
""")

# %%
pc_unabhaengig = run_pc(dataset_unabhaengig)
pc_kette = run_pc(dataset_kette)
pc_collider = run_pc(dataset_collider)
pc_cpdag = run_pc(dataset_cpdag)
pc_gemischt = run_pc(dataset_gemischt)

# %%
pc_results = {
    "Independent": pc_unabhaengig,
    "Chain": pc_kette,
    "Collider": pc_collider,
    "CPDAG": pc_cpdag,
    "Mixed": pc_gemischt
}

# %%
def plot_pc_graph_cpdag(cg, title=None):

    graph = cg.G

    G_layout = nx.Graph()

    for node in graph.get_nodes():
        G_layout.add_node(node.get_name())

    for edge in graph.get_graph_edges():
        node1 = edge.get_node1().get_name()
        node2 = edge.get_node2().get_name()
        G_layout.add_edge(node1, node2)

    pos = nx.spring_layout(G_layout, seed=42, k=2)

    plt.figure(figsize=(12, 7))

    nx.draw_networkx_nodes(
        G_layout,
        pos,
        node_size=2500
    )

    nx.draw_networkx_labels(
        G_layout,
        pos,
        font_size=8
    )

    for edge in graph.get_graph_edges():

        node1 = edge.get_node1().get_name()
        node2 = edge.get_node2().get_name()

        endpoint1 = edge.get_endpoint1()
        endpoint2 = edge.get_endpoint2()

        # Undirected edge: A --- B
        if endpoint1 == Endpoint.TAIL and endpoint2 == Endpoint.TAIL:

            nx.draw_networkx_edges(
                G_layout,
                pos,
                edgelist=[(node1, node2)],
                arrows=False,
                width=1.8
            )

        # Directed edge: A --> B
        elif endpoint1 == Endpoint.TAIL and endpoint2 == Endpoint.ARROW:

            nx.draw_networkx_edges(
                G_layout,
                pos,
                edgelist=[(node1, node2)],
                arrows=True,
                arrowstyle="-|>",
                arrowsize=20,
                width=1.8
            )

        # Directed edge: A <-- B
        elif endpoint1 == Endpoint.ARROW and endpoint2 == Endpoint.TAIL:

            nx.draw_networkx_edges(
                G_layout,
                pos,
                edgelist=[(node2, node1)],
                arrows=True,
                arrowstyle="-|>",
                arrowsize=20,
                width=1.8
            )

        else:

            nx.draw_networkx_edges(
                G_layout,
                pos,
                edgelist=[(node1, node2)],
                arrows=False,
                style="dashed"
            )

    if title:
        plt.title(title)

    plt.axis("off")
    st.pyplot(plt.gcf()) # <-- Replaced plt.show()
    plt.clf() # Clear the figure to prevent overlapping plots

# %%






# %% [markdown]

st.header("Ausblick auf weitere Algorithmen")

st.subheader("GES - Greedy Equivalence Search")
st.markdown("""GES ist ein greedy algorithm, das heißt um Rechenzeit zu sparen, werden nicht alle möglichen Kantenorientierungen getestet, sondern nur die, die den Score verbessern.
Die zugrunde liegende Scorefunktion soll hierbei Kanten, die kausale Zusammenhänge widerspiegeln belohnen und die große, Komplexe Graphen mit vielen Kanten bestrafen.""")
st.markdown("""Der Algorithmus startet mit einem leeren Graphen. In der forward phase wird in jedem Schritt diejendige Kante hinzugefügt, die den Score am meisten verbessert. 
In der backward phase wird in jedem Schritt die Kante entfernt, deren Entfernen den Score am meisten verbessert (denn es kann passieren, dass zwischenzeitlich Kanten hinzugefügt werden, die in der schlussendlichen Struktur negativ wirken).""")
st.markdown(
    "<small style='color: gray;'>"
    "Quelle: <a href='https://www.emergentmind.com/topics/greedy-equivalence-search-ges' "
    "target='_blank'>Emergent Mind</a>"
    "</small>",
    unsafe_allow_html=True,
)

st.subheader("NOTEARS")
st.markdown("""NOTEARS ist wie der PC-Algorithmus ein Verfahren für Causal Discovery, verfolgt aber einen grundlegend anderen Ansatz.
Der PC-Algorithmus ist constraint-based: Er nutzt Tests auf Conditional Independence, um Kanten zu entfernen und anschließend mögliche Richtungen zu bestimmen.
NOTEARS ist dagegen score-/optimization-based: Es sucht direkt nach einem gerichteten Graphen, der die Daten möglichst gut beschreibt.
Die zentrale Innovation von NOTEARS ist, dass die Bedingung „der Graph darf keine Zyklen enthalten“ als mathematische, kontinuierliche Nebenbedingung formuliert wird. Dadurch kann die Suche nach einem DAG als Optimierungsproblem gelöst werden.
Vereinfacht: PC fragt „Welche (Un-)Abhängigkeiten finden wir?“ – NOTEARS fragt „Welcher DAG passt insgesamt am besten zu den Daten?""")

st.markdown(
    "<small style='color: gray;'>"
    "Quelle: <a href='https://www.emergentmind.com/topics/notears-framework' "
    "target='_blank'>Emergent Mind</a>"
    "</small>",
    unsafe_allow_html=True,
)