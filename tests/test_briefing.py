import datetime

from src.briefing import Briefing, build_markdown


def _full_briefing():
    return Briefing(
        person="Max Mustermann",
        company="Müster GmbH",
        topic="KI",
        branch="Software",
        created_at=datetime.datetime(2026, 7, 5, 10, 30),
        company_info={"Rechtsform": ["GmbH"], "Website": ["www.muster.de"]},
        company_summary="Ein deutsches Unternehmen mit Umlauten: äöü.",
        company_news=[{"title": "News 1", "link": "https://example.com/1", "date": "heute"}],
        topic_news=[{"title": "Topic News", "link": "https://example.com/t", "date": "gestern"}],
        person_info={
            "wiki_summary": "Kurzbiografie.",
            "news": [{"title": "Person News", "link": "https://example.com/p", "date": "heute"}],
        },
        talking_points="- Punkt eins\n- Punkt zwei",
    )


def test_build_markdown_full_contains_all_sections():
    md = build_markdown(_full_briefing())

    assert "# Briefing: Müster GmbH — Max Mustermann" in md
    assert "Rechtsform" in md
    assert "GmbH" in md
    assert "[www.muster.de](https://" not in md  # website isn't a link itself, just a value
    assert "äöü" in md
    assert "[News 1](https://example.com/1)" in md
    assert "[Topic News](https://example.com/t)" in md
    assert "Kurzbiografie." in md
    assert "[Person News](https://example.com/p)" in md
    assert "Punkt eins" in md


def test_build_markdown_partial_never_raises():
    briefing = Briefing(person="Max", company="Muster", topic="KI", branch="IT")

    md = build_markdown(briefing)

    assert "# Briefing: Muster — Max" in md
    assert "Keine Daten gefunden" in md
    assert "Keine Gesprächspunkte generiert" in md
