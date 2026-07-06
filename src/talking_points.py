# -*- coding: utf-8 -*-
"""LLM-generated sales talking points, via the Anthropic API.

The `anthropic` package is imported lazily inside generate() so the rest of
the application works even when it isn't installed or no API key is set.
"""

import logging
import os

from .briefing import Briefing
from .config import AppConfig

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Du bist ein Vertriebsassistent. Erstelle aus den bereitgestellten "
    "Informationen zu einem Unternehmen, einer Kontaktperson und aktuellen "
    "News prägnante Gesprächspunkte für ein bevorstehendes Verkaufsgespräch. "
    "Antworte auf Deutsch, in Stichpunkten, maximal 8 Punkte."
)


class TalkingPointsError(Exception):
    """Raised when talking points could not be generated."""


class TalkingPointsGenerator:
    def __init__(self, config: AppConfig):
        self.config = config

    @staticmethod
    def is_available() -> bool:
        return bool(os.environ.get("ANTHROPIC_API_KEY"))

    def _build_context(self, briefing: Briefing) -> str:
        lines = [
            "Unternehmen: {}".format(briefing.company),
            "Thema: {}".format(briefing.topic),
            "Branche: {}".format(briefing.branch),
            "Ansprechpartner: {}".format(briefing.person),
            "",
        ]

        if briefing.company_info:
            lines.append("Infobox:")
            for key, value in briefing.company_info.items():
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value)
                lines.append("- {}: {}".format(key, value))
            lines.append("")

        if briefing.company_summary:
            lines.append("Zusammenfassung: {}".format(briefing.company_summary))
            lines.append("")

        if briefing.company_news:
            lines.append("Aktuelle News zum Unternehmen:")
            for item in briefing.company_news[:10]:
                lines.append("- {} ({})".format(item.get("title"), item.get("date")))
            lines.append("")

        if briefing.topic_news:
            lines.append("Aktuelle News zum Thema/Branche:")
            for item in briefing.topic_news[:10]:
                lines.append("- {} ({})".format(item.get("title"), item.get("date")))
            lines.append("")

        if briefing.person_info:
            summary = briefing.person_info.get("wiki_summary")
            if summary:
                lines.append("Info zur Person: {}".format(summary))
            for item in (briefing.person_info.get("news") or [])[:5]:
                lines.append("- {} ({})".format(item.get("title"), item.get("date")))
            lines.append("")

        return "\n".join(lines)

    def generate(self, briefing: Briefing) -> str:
        try:
            import anthropic
        except ImportError as exc:
            raise TalkingPointsError(
                "Das anthropic-Paket ist nicht installiert."
            ) from exc

        client = anthropic.Anthropic()
        context = self._build_context(briefing)

        try:
            response = client.messages.create(
                model=self.config.anthropic_model,
                max_tokens=self.config.max_tokens,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": context}],
            )
        except anthropic.AuthenticationError as exc:
            raise TalkingPointsError("API-Schlüssel ungültig.") from exc
        except anthropic.RateLimitError as exc:
            raise TalkingPointsError("Rate-Limit erreicht — später erneut versuchen.") from exc
        except anthropic.APIConnectionError as exc:
            raise TalkingPointsError("Keine Verbindung zur Anthropic API.") from exc
        except anthropic.APIStatusError as exc:
            raise TalkingPointsError(
                "Anthropic-API-Fehler (Status {}).".format(exc.status_code)
            ) from exc

        text = "".join(block.text for block in response.content if block.type == "text")
        return text
