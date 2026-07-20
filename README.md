# KI und das „Warum“ | Sommerakademie Leysin 2026

Begleitwebsite zur Arbeitsgruppe **„Eine Einführung in Maschinelles Lernen und
Kausalität“** der Sommerakademie Leysin der Studienstiftung des deutschen
Volkes (18.–27. August 2026, Leysin, Schweiz).

Die Website enthält interaktive Kapitel zu Maschinellem Lernen und Kausalität
sowie die Projektseiten der Gruppen und bleibt nach der Akademie dauerhaft
öffentlich.

**Dozenten:** Dr. Oliver Schacht & Jan Teichert-Kluge (Universität Hamburg,
Lehrstuhl für Statistik)

## Lokal starten

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows; unter macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Struktur

```text
streamlit_app.py       Einstieg und Navigation
views/ml/              Gemeinsamer ML-Lehrpfad; Explainable AI im Appendix
views/kausalitaet/     Gemeinsamer Kausalitätspfad; drei Kapitel im Appendix
views/projekte/        Themenkatalog, Arbeitsweise und Team-Template
content/themen.yaml    Zentrale Quelle für neun Tracks, Abstracts und Literatur
content/projekte/      Team-Apps und gemeinsames Streamlit-Template
utils/                 Theming, Simulationen, Katalog- und Projekt-Rendering
tests/                 Smoke- und Strukturtests
```

Der Appendix enthält ausschließlich:

- Explainable AI
- Quasi-Experimente: DiD/RDD
- Bayesian Methods
- SEMs & Survey Experiments

Die übrigen Kapitel sind Teil der Einführung. Teamnahe Spezialthemen werden
dort nur so weit behandelt, wie es für die gemeinsame begriffliche Grundlage
nötig ist. Fertige Projektlösungen, Quizze und prüfungsartige Kontrollen sind
nicht Bestandteil der Plattform.

## Eine Team-App hinzufügen

**Streamlit ist der Standardmodus.** Der zu einem Track gehörige Ordner steht
in dessen `project_path` in `content/themen.yaml`.

1. `content/projekte/_vorlage/` an diesen Pfad kopieren.
2. `app.py` entlang der Abschnitte Fragestellung, Hintergrund, Annahmen,
   interaktive Analyse, Ergebnisse, Grenzen und Literatur bearbeiten.
3. Kein `st.set_page_config()` aufrufen und lokale Dateien relativ zu
   `Path(__file__).parent` laden.

`projekt.md` bleibt als technischer Fallback möglich. Fehler in einer Team-App
werden auf der betroffenen Track-Seite isoliert.

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest tests/
```
