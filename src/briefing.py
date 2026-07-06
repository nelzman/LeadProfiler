# -*- coding: utf-8 -*-
"""Pure, Qt-free briefing assembly: gathers the LeadProfile results into a
single object and renders it as Markdown for export."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Briefing:
    person: str
    company: str
    topic: str
    branch: str
    created_at: datetime = field(default_factory=datetime.now)
    company_info: Dict = field(default_factory=dict)
    company_summary: Optional[str] = None
    company_news: List[Dict] = field(default_factory=list)
    topic_news: List[Dict] = field(default_factory=list)
    person_info: Optional[Dict] = None
    talking_points: Optional[str] = None


def _format_infobox(info: Dict) -> str:
    if not info:
        return "_Keine Daten gefunden._\n"
    lines = []
    for key, value in info.items():
        if isinstance(value, list):
            value_str = ", ".join(str(v) for v in value)
        else:
            value_str = str(value)
        lines.append("- **{}**: {}".format(key, value_str))
    return "\n".join(lines) + "\n"


def _format_news(items: List[Dict]) -> str:
    if not items:
        return "_Keine News gefunden._\n"
    lines = []
    for item in items:
        title = item.get("title") or "(ohne Titel)"
        link = item.get("link")
        date = item.get("date") or ""
        if link:
            lines.append("- [{}]({}) ({})".format(title, link, date))
        else:
            lines.append("- {} ({})".format(title, date))
    return "\n".join(lines) + "\n"


def _format_person(person_info: Optional[Dict]) -> str:
    if not person_info:
        return "_Keine Daten gefunden._\n"
    parts = []
    summary = person_info.get("wiki_summary")
    if summary:
        parts.append(summary + "\n")
    parts.append(_format_news(person_info.get("news", [])))
    return "\n".join(parts)


def build_markdown(b: Briefing) -> str:
    """Render a Briefing as a Markdown document. Never raises on missing data."""
    sections = [
        "# Briefing: {} — {}".format(b.company, b.person),
        "",
        "*Erstellt am {}. Thema: {}. Branche: {}.*".format(
            b.created_at.strftime("%Y-%m-%d %H:%M"), b.topic, b.branch
        ),
        "",
        "## Unternehmens-Infobox",
        "",
        _format_infobox(b.company_info),
        "## Zusammenfassung (Wikipedia)",
        "",
        b.company_summary if b.company_summary else "_Keine Daten gefunden._",
        "",
        "## Gesprächspunkte (KI)",
        "",
        b.talking_points if b.talking_points else "_Keine Gesprächspunkte generiert._",
        "",
        "## News zur Firma",
        "",
        _format_news(b.company_news),
        "## News zum Thema",
        "",
        _format_news(b.topic_news),
        "## Person",
        "",
        _format_person(b.person_info),
    ]
    return "\n".join(sections)
