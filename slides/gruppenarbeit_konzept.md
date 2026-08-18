
# Gemeinsames Ziel der Gruppenarbeit

Ich würde den Gruppen ungefähr Folgendes kommunizieren:

> Ziel ist **nicht**, euer gesamtes Themengebiet abzudecken. Wählt innerhalb eures Themas eine präzise wissenschaftliche Frage und untersucht sie anhand eines geeigneten Beispiels, Datensatzes, Experiments oder einer Simulation.
>
> Eure Streamlit-App soll dabei nicht bloß Ergebnisse präsentieren, sondern eine zentrale methodische Idee, Annahme oder Grenze **interaktiv untersuchbar** machen.
---

# Zielstruktur eines Projekts

### 1. Frage & Motivation

**Was genau wollt ihr herausfinden?**

* eine klar abgegrenzte Forschungsfrage,
* warum sie wissenschaftlich oder praktisch relevant ist,
* warum die Antwort nicht trivial ist.

Idealerweise lässt sich die Frage in **einem Satz** formulieren.

---

### 2. Konzept / Methode

**Welche Idee braucht man, um diese Frage zu bearbeiten?**

Hier gehört die theoretische Einführung hin:

* zentrale Begriffe,
* Intuition,
* bei Bedarf 1–2 wichtige Formeln,
* Bezug auf passende wissenschaftliche Quellen.

Nicht das ganze Forschungsfeld erklären.

---

### 3. Annahmen & Gültigkeit

**Was muss gelten, damit eure Schlussfolgerung trägt?**

Das ist der wissenschaftlich wichtigste Teil.

Bei klassischen CI-Themen ist hier insbesondere die **Identifikation** relevant:

* RCT → Randomisierung / SUTVA
* DiD → Parallel Trends
* RDD → Kontinuität am Cutoff
* CML → Exchangeability / Overlap

Bei anderen Themen allgemeiner:

* XAI → Was erklärt die Methode tatsächlich?
* LLMs → Wann ist ein Test ein valider Test von causal reasoning?
* Causal Discovery → Markov/Faithfulness etc.
* Bayes → Modell- und Priorannahmen

Damit bleibt eure starke ursprüngliche Idee erhalten: Nicht das Rechnen ist der schwierige Teil, sondern zu begründen, **welche Aussage die Analyse erlaubt**.

---

### 4. Daten / Experiment / Simulation

**Woran untersucht ihr eure Frage?**

Erlaubt würde ich ausdrücklich:

* reale Daten,
* Replikationsdaten,
* simulierte Daten,
* eigene Experimente,
* Benchmarks,
* LLM-Abfragen.

Simulationen sind kein „Plan B“ — gerade für methodische Fragen können sie besonders geeignet sein, weil die Ground Truth bekannt ist.

---

### 5. Interaktive Analyse

**Was kann man in eurer App verändern, um etwas zu lernen?**

Das ist der Kern des Datenprodukts.

Zum Beispiel:

* Annahmen verletzen,
* Confounding erhöhen,
* Stichprobengröße variieren,
* Priors verändern,
* Cutoff verschieben,
* Prompt verändern,
* Features korrelieren,
* Modell wechseln.

Die Leitfrage sollte sein:

> **Was können Nutzer:innen durch die Interaktion erkennen, was eine statische Folie weniger gut zeigen würde?**

---

### 6. Findings

**Was habt ihr herausgefunden?**

Nicht nur:

> „Wir haben Methode X implementiert.“

Sondern eine tatsächliche Aussage:

> „Unter diesen Bedingungen funktioniert X gut, unter diesen Bedingungen scheitert es.“

Auch Nullbefunde oder unerwartete Ergebnisse sind völlig legitim.

---

### 7. Grenzen & offene Fragen

**Was folgt aus eurer Analyse ausdrücklich nicht?**

Mindestens:

* eine zentrale Limitation,
* eine Annahme, deren Verletzung das Ergebnis gefährdet,
* eine offene Frage, die mit mehr Zeit interessant wäre.

---

# Arbeitsplan für 4 × 90 Minuten

Den würde ich unbedingt ebenfalls auf die Projektseite stellen.

### Block 1 — Scope & Design

Am Ende sollen feststehen:

* Forschungsfrage
* Methode / Konzept
* Daten oder Simulation
* wichtigste Annahme
* Skizze der App

**Wichtigster Checkpoint:** Ist die Frage klein genug?

---

### Block 2 — Analyse zuerst

Noch keine Schönheit.

Ziel:

* Daten funktionieren,
* Methode läuft,
* zentrale Analyse erzeugt ein sinnvolles Ergebnis,
* erste Grafik existiert.

> Erst muss das wissenschaftliche Argument funktionieren, dann wird daraus eine App.

---

### Block 3 — Streamlit & Story

Jetzt:

* relevante Controls einbauen,
* Visualisierung verbessern,
* theoretischen Input reduzieren und schärfen,
* Findings und Grenzen formulieren.

---

### Block 4 — Finalisierung & Peer Review

* App testen,
* Präsentation fertigstellen,
* zentrale Aussage auf **einen Satz** reduzieren,
* Limitationen prüfen.

Ich würde die letzten ~20 Minuten für einen Austausch zwischen jeweils zwei Gruppen reservieren:

> **Was habt ihr aus der App verstanden? Welche Annahme bleibt unklar? Was könnte weg?**
