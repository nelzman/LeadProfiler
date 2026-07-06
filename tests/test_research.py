from unittest.mock import MagicMock, patch

import requests

from src.config import AppConfig
from src.lead_profile import InfoboxNotFoundError
from src.research import (
    SECTION_COMPANY_INFO,
    SECTION_COMPANY_NEWS,
    SECTION_PERSON,
    SECTION_TALKING_POINTS,
    gather_briefing,
)


def _make_lead_profile(**overrides):
    """Build a MagicMock standing in for a LeadProfile instance.

    Defaults describe a fully successful research run; pass overrides to make an
    individual method raise or return something else.
    """
    lp = MagicMock()
    lp.get_company_info.return_value = {"Branche": ["IT"], "Sitz": "Berlin"}
    lp.get_company_summary.return_value = "Ein Unternehmen."
    lp.get_company_news.return_value = [
        {"title": "Firma News", "link": "https://example.com/c", "date": "heute"}
    ]
    lp.get_topic_news.return_value = [
        {"title": "Thema News", "link": "https://example.com/t", "date": "heute"}
    ]
    lp.get_person_info.return_value = {
        "wiki_summary": "Eine Person.",
        "news": [{"title": "Person News", "link": "https://example.com/p", "date": "heute"}],
    }
    for name, value in overrides.items():
        method = getattr(lp, name)
        if isinstance(value, Exception):
            method.side_effect = value
        else:
            method.return_value = value
    return lp


def _run(monkeypatch, lead_profile):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with patch("src.research.LeadProfile", return_value=lead_profile):
        return gather_briefing("Max Mustermann", "Muster GmbH", "KI", "Software", AppConfig())


def test_happy_path_populates_briefing(monkeypatch):
    briefing, errors = _run(monkeypatch, _make_lead_profile())

    assert briefing.person == "Max Mustermann"
    assert briefing.company == "Muster GmbH"
    assert briefing.company_info == {"Branche": ["IT"], "Sitz": "Berlin"}
    assert briefing.company_summary == "Ein Unternehmen."
    assert briefing.company_news[0]["title"] == "Firma News"
    assert briefing.topic_news[0]["title"] == "Thema News"
    assert briefing.person_info["wiki_summary"] == "Eine Person."
    # No data errors; only talking points disabled (no API key).
    assert set(errors) == {SECTION_TALKING_POINTS}


def test_infobox_not_found_recorded_as_error(monkeypatch):
    lp = _make_lead_profile(get_company_info=InfoboxNotFoundError())
    briefing, errors = _run(monkeypatch, lp)

    assert briefing.company_info == {}
    assert errors[SECTION_COMPANY_INFO] == (
        "Keine Unternehmens-Infobox im Wikipedia-Artikel gefunden."
    )
    # A failure in one section does not abort the rest.
    assert briefing.company_summary == "Ein Unternehmen."


def test_network_error_on_company_news_recorded(monkeypatch):
    lp = _make_lead_profile(get_company_news=requests.exceptions.ConnectionError())
    briefing, errors = _run(monkeypatch, lp)

    assert briefing.company_news == []
    assert errors[SECTION_COMPANY_NEWS] == "Netzwerkfehler — bitte Internetverbindung prüfen."


def test_empty_company_news_recorded_as_notice(monkeypatch):
    lp = _make_lead_profile(get_company_news=[])
    _, errors = _run(monkeypatch, lp)

    assert "Keine News gefunden" in errors[SECTION_COMPANY_NEWS]


def test_empty_person_info_recorded(monkeypatch):
    lp = _make_lead_profile(get_person_info={"wiki_summary": None, "news": []})
    briefing, errors = _run(monkeypatch, lp)

    assert errors[SECTION_PERSON] == "Keine Informationen zur Person gefunden."


def test_talking_points_disabled_without_key(monkeypatch):
    _, errors = _run(monkeypatch, _make_lead_profile())

    assert errors[SECTION_TALKING_POINTS] == (
        "KI-Gesprächspunkte deaktiviert: Umgebungsvariable ANTHROPIC_API_KEY nicht gesetzt."
    )


def test_progress_callback_reaches_one(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    calls = []
    with patch("src.research.LeadProfile", return_value=_make_lead_profile()):
        gather_briefing(
            "Max Mustermann",
            "Muster GmbH",
            "KI",
            "Software",
            AppConfig(),
            progress_callback=lambda frac, label: calls.append(frac),
        )
    assert calls[-1] == 1.0
    assert calls == sorted(calls)
