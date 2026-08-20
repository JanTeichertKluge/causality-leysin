# Mini-Live-Coding: „Neue Studie ziehen“ 🎲

**Zeit:** 6–8 Minuten am Ende der Einführung  
**App:** `views/kausalitaet/potential_outcomes.py`  
**Didaktische Pointe:** Randomisierung bedeutet nicht, dass *jede* kleine Studie perfekt balanciert ist. Sie macht die Gruppen im Mittel vergleichbar; mit wachsendem $n$ werden zufällige Ungleichgewichte kleiner.

## Zielbild

In der Demo *„Der Zuteilungsmechanismus entscheidet“* gibt es zusätzlich einen Button **„🎲 Neue Studie ziehen“**. Mit jedem Klick wird bei gleicher Studiengröße eine neue Stichprobe simuliert. Die Klasse beobachtet: Auch bei randomisierter Zuweisung schwanken Balance und Schätzung in kleinen Stichproben – aber nicht systematisch in eine Richtung.

Das Feature ergänzt die bestehende App, ohne ihre Logik zu verändern: Die Simulationsfunktion besitzt bereits einen `seed`-Parameter.

## Vorbereitung vor der Sitzung

- Die Website lokal starten: `streamlit run streamlit_app.py`.
- `views/kausalitaet/potential_outcomes.py` im Editor öffnen und die Stelle bei `n_studie = st.select_slider(...)` vorbereiten.
- In der App zunächst **Randomisierte Zuweisung** und **Stichprobengröße 50** wählen. So sind die Unterschiede nach einem Neuziehen sichtbar.
- Die folgenden zwei Code-Blöcke in einem separaten Editor-Tab bereithalten. Nur der markierte Code wird live ergänzt.

## Moderationsablauf

### 1. Vorhersage einholen (ca. 45 Sekunden)

> Wir haben gerade gesagt: Randomisierung schafft Vergleichbarkeit. Heißt das, dass bei jeder randomisierten Studie mit $n=50$ die Gruppen *exakt* gleich krank sind?

Kurz per Handzeichen oder Positionslinie abstimmen lassen: **immer exakt** / **meist ungefähr** / **keine Ahnung**. Nicht sofort auflösen.

### 2. Die Idee übersetzen (ca. 45 Sekunden)

> Die App zeigt bisher nur *eine* gezogene Studie. Ich möchte einen Knopf ergänzen, der dieselbe Studie unter denselben Regeln noch einmal zieht.

Dabei knapp erklären:

- Der **Seed** ist die Startzahl des Zufallsgenerators.
- Ein anderer Seed erzeugt eine neue, reproduzierbare Stichprobe.
- Das Datenentstehungsmodell und der wahre Effekt bleiben unverändert.

## Live-Code

### Schritt A: Zustand und Button ergänzen

Direkt **nach** dem `n_studie = st.select_slider(...)`-Block einfügen:

```python
if "studien_seed" not in st.session_state:
    st.session_state.studien_seed = 4

if st.button("🎲 Neue Studie ziehen"):
    st.session_state.studien_seed += 1
```

Während des Tippens sagen:

> Streamlit rendert nach jeder Interaktion neu. Damit unsere neue Studie nicht sofort wieder verschwindet, merken wir uns den Seed im `session_state`.

### Schritt B: Den gespeicherten Seed nutzen

Die bestehende Zeile

```python
schwere, d, y_beob = studie_simulieren(zuteilung.startswith("Randomisierte"), n_studie)
```

ersetzen durch:

```python
schwere, d, y_beob = studie_simulieren(
    zuteilung.startswith("Randomisierte"),
    n_studie,
    seed=st.session_state.studien_seed,
)
```

Optional, wenn noch 30 Sekunden bleiben: Direkt unter dem Button einfügen:

```python
st.caption(f"Gezogene Studie Nr. {st.session_state.studien_seed - 3}")
```

## Die Interaktion durchführen

1. Bei **randomisierter Zuweisung** und $n=50$ den Button zwei- bis dreimal klicken.
2. Jedes Mal kurz fragen: „Ist die Balance jetzt perfekt? Wo liegt der Schätzer relativ zur grünen Linie?“
3. Dann auf $n=1000$ wechseln und erneut ein- bis zweimal ziehen.
4. Abschlusssatz:

> Randomisierung verspricht keine perfekte einzelne Stichprobe. Sie verhindert aber, dass Krankheitsschwere *systematisch* die Zuweisung steuert. Größere Stichproben machen die zufälligen Abweichungen kleiner.

## Verbindung zur Vorlesung

- **Potential Outcomes:** Randomisierung zielt auf Austauschbarkeit der Gruppen.
- **Schätzung vs. Identifikation:** Ein einzelnes Estimate kann schwanken, obwohl der ATE identifiziert ist.
- **Konfidenzintervalle:** Sie werden bei größerem $n$ enger; die Schätzung wird präziser, nicht erst dann „kausal“.
- **Abgrenzung zur Selbstselektion:** Dort kann der Button ebenfalls neue Stichproben ziehen, aber der Bias bleibt strukturell bestehen.

## Falls etwas hakt

- **Reload dauert zu lange:** Den vorbereiteten Code einfügen und die Aussage anhand des ersten neuen Draws erklären.
- **Die Balance sieht zufällig sehr gut aus:** Noch einmal klicken oder bei $n=50$ bleiben; kleine Abweichungen reichen bereits für die Pointe.
- **Syntaxfehler:** Live-Coding stoppen und den vorbereiteten Diff zeigen. Inhaltlich ist die Botschaft wichtiger als eine perfekte Tipp-Performance.
- **Kein Zeitpuffer:** Nur Schritt A zeigen, dann den vorbereiteten Schritt B einfügen und einmal klicken.

## Nachbereitung

Wenn das Feature gut funktioniert, kann der Code in der App bleiben. Er ist klein, verbessert die Demo dauerhaft und macht die Rolle von Stichprobenvariabilität unmittelbar sichtbar.
