"""Nachbardateien eines Projektordners importieren -- ohne Namenskollision.

Alle Projekte haben eine Datei `analyse.py`. Ein schlichtes `import analyse`
laedt aber nur EINMAL pro Streamlit-Prozess: Wer zuerst kommt, belegt den
Modulnamen `analyse` fuer alle anderen Seiten mit. Auf der Cloud-Instanz
fuehrt das zu `AttributeError: module 'analyse' has no attribute ...`.

Deshalb laden wir das Modul ueber seinen Dateipfad und geben ihm einen
eindeutigen Namen (z. B. `projekt_XAI.analyse`).

Verwendung in eurer app.py:

    from utils.projektmodul import lade_modul
    analyse = lade_modul(__file__, "analyse")
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def lade_modul(app_datei: str, modulname: str) -> ModuleType:
    """Laedt `modulname`.py aus dem Ordner von `app_datei`.

    `app_datei` ist immer `__file__` der aufrufenden Seite.
    """
    ordner = Path(app_datei).resolve().parent
    pfad = ordner / f"{modulname}.py"
    if not pfad.exists():
        raise FileNotFoundError(f"Modul fehlt: {pfad}")

    eindeutig = f"projekt_{ordner.name}.{modulname}"
    if eindeutig in sys.modules:
        return sys.modules[eindeutig]

    # Der Projektordner muss im Suchpfad liegen, falls das Modul selbst
    # weitere Nachbardateien importiert.
    if str(ordner) not in sys.path:
        sys.path.insert(0, str(ordner))

    spec = importlib.util.spec_from_file_location(eindeutig, pfad)
    if spec is None or spec.loader is None:
        raise ImportError(f"Modul nicht ladbar: {pfad}")
    modul = importlib.util.module_from_spec(spec)
    sys.modules[eindeutig] = modul
    spec.loader.exec_module(modul)
    return modul
