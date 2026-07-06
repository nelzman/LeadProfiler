# -*- coding: utf-8 -*-
"""Qt-free orchestration of a lead research run.

This module contains the data-gathering and per-section error handling that
used to live inside the PyQt5 ``LeadProfilerApp.searchLead`` method. Keeping it
free of any UI framework makes it reusable (e.g. by the Streamlit frontend) and
testable without a browser or display.
"""

import logging
from typing import Callable, Dict, Optional, Tuple

import requests
import wikipedia

from .briefing import Briefing
from .config import AppConfig
from .lead_profile import InfoboxNotFoundError, LeadProfile
from .talking_points import TalkingPointsError, TalkingPointsGenerator

logger = logging.getLogger(__name__)

# Section keys used both for the progress labels and the returned errors dict.
SECTION_COMPANY_INFO = "company_info"
SECTION_COMPANY_SUMMARY = "company_summary"
SECTION_COMPANY_NEWS = "company_news"
SECTION_TOPIC_NEWS = "topic_news"
SECTION_PERSON = "person"
SECTION_TALKING_POINTS = "talking_points"

ProgressCallback = Callable[[float, str], None]


def gather_briefing(
    name: str,
    company: str,
    topic: str,
    branch: str,
    config: AppConfig,
    progress_callback: Optional[ProgressCallback] = None,
) -> Tuple[Briefing, Dict[str, str]]:
    """Run a :class:`LeadProfile` end to end and assemble a :class:`Briefing`.

    Returns the populated ``Briefing`` plus an ``errors`` dict mapping a section
    key to a user-facing German error/notice string (only for sections that
    failed or came back empty). This function never raises — every data source
    is best-effort, mirroring the original desktop behaviour.

    ``progress_callback`` (optional) is called as ``(fraction, label)`` between
    sections, where ``fraction`` is a float in ``[0.0, 1.0]``.
    """

    def report(fraction: float, label: str) -> None:
        if progress_callback is not None:
            progress_callback(fraction, label)

    errors: Dict[str, str] = {}

    lead_profile = LeadProfile(name, company, topic, branch, config)
    briefing = Briefing(person=name, company=company, topic=topic, branch=branch)
    report(0.10, "Recherche gestartet …")

    # Company Info: ------------------------------------------------------
    try:
        briefing.company_info = lead_profile.get_company_info()
    except InfoboxNotFoundError:
        errors[SECTION_COMPANY_INFO] = "Keine Unternehmens-Infobox im Wikipedia-Artikel gefunden."
    except wikipedia.exceptions.DisambiguationError as e:
        errors[SECTION_COMPANY_INFO] = "Mehrdeutiger Begriff. Meinten Sie: " + ", ".join(e.options[:5])
    except wikipedia.exceptions.PageError:
        errors[SECTION_COMPANY_INFO] = "Kein Wikipedia-Artikel zu '{}' gefunden.".format(company)
    except wikipedia.exceptions.HTTPTimeoutError:
        errors[SECTION_COMPANY_INFO] = "Wikipedia nicht erreichbar (Timeout)."
    except wikipedia.exceptions.WikipediaException as e:
        logger.exception("Wikipedia error while fetching company info")
        errors[SECTION_COMPANY_INFO] = "Wikipedia-Fehler: {}".format(e)
    except requests.exceptions.RequestException:
        logger.exception("Network error while fetching company info")
        errors[SECTION_COMPANY_INFO] = "Netzwerkfehler — bitte Internetverbindung prüfen."
    report(0.25, "Unternehmens-Infobox …")

    # Company Summary: ---------------------------------------------------
    try:
        briefing.company_summary = lead_profile.get_company_summary()
    except wikipedia.exceptions.DisambiguationError as e:
        errors[SECTION_COMPANY_SUMMARY] = "Mehrdeutiger Begriff. Meinten Sie: " + ", ".join(e.options[:5])
    except wikipedia.exceptions.PageError:
        errors[SECTION_COMPANY_SUMMARY] = "Kein Wikipedia-Artikel zu '{}' gefunden.".format(company)
    except wikipedia.exceptions.HTTPTimeoutError:
        errors[SECTION_COMPANY_SUMMARY] = "Wikipedia nicht erreichbar (Timeout)."
    except wikipedia.exceptions.WikipediaException as e:
        logger.exception("Wikipedia error while fetching company summary")
        errors[SECTION_COMPANY_SUMMARY] = "Wikipedia-Fehler: {}".format(e)
    except requests.exceptions.RequestException:
        logger.exception("Network error while fetching company summary")
        errors[SECTION_COMPANY_SUMMARY] = "Netzwerkfehler — bitte Internetverbindung prüfen."
    report(0.40, "Wikipedia-Zusammenfassung …")

    # Company News: ------------------------------------------------------
    try:
        briefing.company_news = lead_profile.get_company_news()
        if not briefing.company_news:
            errors[SECTION_COMPANY_NEWS] = (
                "Keine News gefunden (ggf. Suchbegriff prüfen oder Google-Rate-Limit — später erneut versuchen)."
            )
    except requests.exceptions.RequestException:
        logger.exception("Network error while fetching company news")
        errors[SECTION_COMPANY_NEWS] = "Netzwerkfehler — bitte Internetverbindung prüfen."
    except Exception:
        logger.exception("Unexpected error while fetching company news")
        errors[SECTION_COMPANY_NEWS] = "Company News not found"
    report(0.55, "News zur Firma …")

    # Topic News: --------------------------------------------------------
    try:
        briefing.topic_news = lead_profile.get_topic_news()
        if not briefing.topic_news:
            errors[SECTION_TOPIC_NEWS] = (
                "Keine News gefunden (ggf. Suchbegriff prüfen oder Google-Rate-Limit — später erneut versuchen)."
            )
    except requests.exceptions.RequestException:
        logger.exception("Network error while fetching topic news")
        errors[SECTION_TOPIC_NEWS] = "Netzwerkfehler — bitte Internetverbindung prüfen."
    except Exception:
        logger.exception("Unexpected error while fetching topic news")
        errors[SECTION_TOPIC_NEWS] = "Topic News not found"
    report(0.70, "News zum Thema …")

    # Person Info: -------------------------------------------------------
    try:
        person_info = lead_profile.get_person_info()
        briefing.person_info = person_info
        summary = person_info.get("wiki_summary")
        news = person_info.get("news") or []
        if not summary and not news:
            errors[SECTION_PERSON] = "Keine Informationen zur Person gefunden."
    except requests.exceptions.RequestException:
        logger.exception("Network error while fetching person info")
        errors[SECTION_PERSON] = "Netzwerkfehler — bitte Internetverbindung prüfen."
    except Exception:
        logger.exception("Unexpected error while fetching person info")
        errors[SECTION_PERSON] = "Info über den Lead nicht gefunden."
    report(0.85, "Info über den Lead …")

    # Talking Points (KI): -----------------------------------------------
    generator = TalkingPointsGenerator(config)
    if generator.is_available():
        try:
            briefing.talking_points = generator.generate(briefing)
        except TalkingPointsError as e:
            logger.exception("Talking points generation failed")
            errors[SECTION_TALKING_POINTS] = str(e)
    else:
        errors[SECTION_TALKING_POINTS] = (
            "KI-Gesprächspunkte deaktiviert: Umgebungsvariable ANTHROPIC_API_KEY nicht gesetzt."
        )
    report(1.0, "Fertig.")

    return briefing, errors
