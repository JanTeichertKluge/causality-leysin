"""Zentraler, validierter Themenkatalog für die neun Gruppenprojekte."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
THEMEN_DATEI = ROOT / "content" / "themen.yaml"


@dataclass(frozen=True)
class Source:
    title: str
    authors: str
    description: str
    url: str


@dataclass(frozen=True)
class DeepeningLink:
    path: str
    label: str


@dataclass(frozen=True)
class Topic:
    slug: str
    title: str
    emoji: str
    abstract: str
    required_sources: tuple[Source, Source]
    optional_source: Source
    group_members: tuple[str, ...] = ()
    project_path: str = ""
    deepening: tuple[DeepeningLink, ...] = field(default_factory=tuple)

    @property
    def absolute_project_path(self) -> Path:
        return ROOT / self.project_path


def _source(data: object, context: str) -> Source:
    if not isinstance(data, dict):
        raise ValueError(f"{context} muss ein Mapping sein.")
    required = ("title", "authors", "description", "url")
    missing = [key for key in required if not str(data.get(key, "")).strip()]
    if missing:
        raise ValueError(f"{context}: Pflichtfelder fehlen: {', '.join(missing)}")
    return Source(**{key: str(data[key]).strip() for key in required})


def load_topics(path: Path = THEMEN_DATEI) -> list[Topic]:
    """Lädt den Katalog und bricht bei redaktionell unvollständigen Daten klar ab."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("content/themen.yaml muss eine Liste enthalten.")

    topics: list[Topic] = []
    slugs: set[str] = set()
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Thema {index} muss ein Mapping sein.")
        context = f"Thema {index}"
        for key in ("slug", "title", "abstract", "sources", "project_path"):
            if not item.get(key):
                raise ValueError(f"{context}: Pflichtfeld {key!r} fehlt.")
        slug = str(item["slug"])
        if slug in slugs:
            raise ValueError(f"Doppelter Themen-Slug: {slug}")
        slugs.add(slug)

        sources = item["sources"]
        if not isinstance(sources, dict):
            raise ValueError(f"{context}.sources muss ein Mapping sein.")
        required = sources.get("required", [])
        if not isinstance(required, list) or len(required) != 2:
            raise ValueError(f"{context} braucht genau zwei Einstiegsquellen.")
        optional = sources.get("optional")

        links = item.get("deepening", [])
        if not isinstance(links, list):
            raise ValueError(f"{context}.deepening muss eine Liste sein.")
        deepening = tuple(
            DeepeningLink(path=str(link["path"]), label=str(link["label"]))
            for link in links
        )
        topics.append(
            Topic(
                slug=slug,
                title=str(item["title"]),
                emoji=str(item.get("emoji", "📊")),
                abstract=str(item["abstract"]).strip(),
                required_sources=(
                    _source(required[0], f"{context}.sources.required[0]"),
                    _source(required[1], f"{context}.sources.required[1]"),
                ),
                optional_source=_source(optional, f"{context}.sources.optional"),
                group_members=tuple(str(name) for name in item.get("group_members", [])),
                project_path=str(item["project_path"]),
                deepening=deepening,
            )
        )

    if len(topics) != 9:
        raise ValueError(f"Der Akademie-Katalog muss genau neun Themen enthalten, gefunden: {len(topics)}")
    return topics
