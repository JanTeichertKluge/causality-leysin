"""Discovery und Rendering der Gruppenprojekte (Hybrid-Mechanik).

Jede Gruppe bekommt einen Ordner unter content/projekte/<slug>/:

- ``projekt.md`` mit YAML-Frontmatter (titel, emoji, mitglieder,
  kurzbeschreibung) — wird automatisch als Seite gerendert.
- Liegt zusätzlich eine ``app.py`` im Ordner, wird stattdessen diese als
  vollwertige Streamlit-Seite registriert (die Metadaten für die Galerie
  kommen weiterhin aus projekt.md).

Ordner mit führendem Unterstrich (z. B. ``_vorlage``) werden übersprungen.
Fehler in einem Projekt dürfen nie die ganze App reißen — kaputte Projekte
bekommen eine Fehlerseite statt eines Crashs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import streamlit as st
import yaml

_ROOT = Path(__file__).resolve().parent.parent
PROJEKTE_DIR = _ROOT / "content" / "projekte"

_FRONTMATTER_MUSTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)
_BILD_MUSTER = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")


@dataclass
class Projekt:
    slug: str
    titel: str
    emoji: str = "📊"
    mitglieder: list[str] = field(default_factory=list)
    kurzbeschreibung: str = ""
    md_datei: Path | None = None
    app_datei: Path | None = None
    fehler: str | None = None


def _frontmatter(text: str) -> tuple[dict, str]:
    """Trennt YAML-Frontmatter vom Markdown-Inhalt."""
    treffer = _FRONTMATTER_MUSTER.match(text)
    if treffer is None:
        return {}, text
    meta = yaml.safe_load(treffer.group(1)) or {}
    if not isinstance(meta, dict):
        meta = {}
    return meta, treffer.group(2)


def _lade_projekt(ordner: Path) -> Projekt:
    projekt = Projekt(slug=ordner.name, titel=ordner.name.replace("-", " ").title())
    md = ordner / "projekt.md"
    app = ordner / "app.py"
    if app.exists():
        projekt.app_datei = app
    if md.exists():
        projekt.md_datei = md
        try:
            meta, _ = _frontmatter(md.read_text(encoding="utf-8"))
            projekt.titel = str(meta.get("titel", projekt.titel))
            projekt.emoji = str(meta.get("emoji", projekt.emoji))
            projekt.kurzbeschreibung = str(meta.get("kurzbeschreibung", ""))
            mitglieder = meta.get("mitglieder", [])
            if isinstance(mitglieder, list):
                projekt.mitglieder = [str(m) for m in mitglieder]
        except yaml.YAMLError as exc:
            projekt.fehler = f"Frontmatter in projekt.md nicht lesbar: {exc}"
    elif projekt.app_datei is None:
        projekt.fehler = "Weder projekt.md noch app.py im Projektordner gefunden."
    return projekt


def lade_projekte() -> list[Projekt]:
    """Scannt content/projekte/ und liefert alle Gruppenprojekte."""
    if not PROJEKTE_DIR.exists():
        return []
    return [
        _lade_projekt(ordner)
        for ordner in sorted(PROJEKTE_DIR.iterdir())
        if ordner.is_dir() and not ordner.name.startswith("_")
    ]


def _markdown_mit_bildern(inhalt: str, basis: Path) -> None:
    """Rendert Markdown und löst lokale Bildpfade über st.image auf.

    st.markdown kann lokale Dateien nicht anzeigen; http(s)-URLs bleiben
    im Markdown und funktionieren dort direkt.
    """
    pos = 0
    for treffer in _BILD_MUSTER.finditer(inhalt):
        alt, quelle = treffer.group(1), treffer.group(2)
        if quelle.startswith(("http://", "https://")):
            continue
        davor = inhalt[pos : treffer.start()]
        if davor.strip():
            st.markdown(davor)
        bild = (basis / quelle).resolve()
        if basis.resolve() not in bild.parents:
            st.warning(f"Bildpfad außerhalb des Projektordners: {quelle}")
        elif bild.exists():
            st.image(str(bild), caption=alt or None)
        else:
            st.warning(f"Bild nicht gefunden: {quelle}")
        pos = treffer.end()
    rest = inhalt[pos:]
    if rest.strip():
        st.markdown(rest)


def render_markdown_projekt(projekt: Projekt) -> None:
    """Seiteninhalt für ein Markdown-Projekt (Fehler bleiben lokal)."""
    try:
        text = projekt.md_datei.read_text(encoding="utf-8")
        _, inhalt = _frontmatter(text)
    except Exception as exc:  # noqa: BLE001 — Projektfehler nie eskalieren
        st.error(f"Projekt „{projekt.titel}“ konnte nicht geladen werden: {exc}")
        return
    st.markdown(f"# {projekt.emoji} {projekt.titel}")
    if projekt.mitglieder:
        st.caption("Team: " + ", ".join(projekt.mitglieder))
    if projekt.fehler:
        st.warning(projekt.fehler)
    try:
        _markdown_mit_bildern(inhalt, projekt.md_datei.parent)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Fehler beim Rendern des Projektinhalts: {exc}")


def _fehlerseite(projekt: Projekt) -> None:
    st.markdown(f"# ⚠️ {projekt.titel}")
    st.error(projekt.fehler or "Unbekannter Fehler im Projektordner.")
    st.info(
        "Prüft euren Ordner unter `content/projekte/` — er braucht mindestens "
        "eine `projekt.md` (siehe `_vorlage/`) oder eine `app.py`."
    )


def _seiten_funktion(projekt: Projekt) -> Callable[[], None]:
    """Erzeugt eine benannte Render-Funktion (st.Page braucht __name__)."""
    if projekt.fehler and projekt.md_datei is None and projekt.app_datei is None:
        rumpf = _fehlerseite
    else:
        rumpf = render_markdown_projekt

    def _seite() -> None:
        rumpf(projekt)

    _seite.__name__ = "projekt_" + re.sub(r"\W", "_", projekt.slug)
    return _seite


def projekt_seiten(projekte: list[Projekt]) -> dict[str, st.Page]:
    """Baut pro Projekt eine st.Page; Rückgabe als {slug: Seite}.

    Das Emoji wandert in den Titel statt in `icon=`, weil ungültige
    icon-Werte aus Frontmatter sonst die ganze Navigation crashen würden.
    """
    seiten: dict[str, st.Page] = {}
    for projekt in projekte:
        url = f"projekt-{projekt.slug}"
        titel = f"{projekt.emoji} {projekt.titel}"
        if projekt.app_datei is not None:
            seiten[projekt.slug] = st.Page(
                str(projekt.app_datei), title=titel, url_path=url
            )
        else:
            seiten[projekt.slug] = st.Page(
                _seiten_funktion(projekt), title=titel, url_path=url
            )
    return seiten
