from unittest.mock import MagicMock, patch

import pytest
import wikipedia

from src.config import AppConfig
from src.lead_profile import (
    InfoboxNotFoundError,
    LeadProfile,
    parse_infobox,
    split_at_values,
)

INFOBOX_HTML = """
<table id="Vorlage_Infobox_Unternehmen">
<tbody>
<tr><th colspan="2">Muster GmbH</th></tr>
<tr><td>Rechtsform</td><td>GmbH</td></tr>
<tr><td>ISIN</td><td>DE0001234567</td></tr>
<tr><td>Gr&uuml;ndung</td><td>1990</td></tr>
<tr><td>Sitz</td><td>Berlin</td></tr>
<tr><td>Leitung</td><td>Max Mustermann</td></tr>
<tr><td>Mitarbeiterzahl</td><td>500</td></tr>
<tr><td>Umsatz</td><td>10 Mio. Euro</td></tr>
<tr><td>Branche</td><td>IT</td></tr>
<tr><td>Website</td><td>www.muster.de</td></tr>
<tr><td colspan="2">Stand: 31. Dezember 2023</td></tr>
</tbody>
</table>
"""

NO_INFOBOX_HTML = "<html><body><p>No infobox here.</p></body></html>"


def test_split_at_values_basic():
    lst = ["Rechtsform", "GmbH", "ISIN", "DE1234"]
    assert split_at_values(lst) == [[], ["Rechtsform", "GmbH"], ["ISIN", "DE1234"]]


def test_split_at_values_empty():
    assert split_at_values([]) == [[]]


def test_split_at_values_key_at_end():
    lst = ["some", "text", "Website"]
    assert split_at_values(lst) == [["some", "text"], ["Website"]]


def test_parse_infobox_ok():
    info = parse_infobox(INFOBOX_HTML)

    assert info["comp_name"] == "Muster GmbH"
    assert info["infostand"] == "Stand: 31. Dezember 2023"
    assert info["Rechtsform"] == ["GmbH"]
    assert info["Website"] == ["www.muster.de"]
    assert info["Branche"] == ["IT"]


def test_parse_infobox_missing_table_raises():
    with pytest.raises(InfoboxNotFoundError):
        parse_infobox(NO_INFOBOX_HTML)


def _make_page_mock(html_content, summary_text="A summary."):
    page = MagicMock()
    page.html.return_value = html_content
    page.summary = summary_text
    return page


@patch("src.lead_profile.wikipedia.page")
def test_page_fetched_only_once(mock_page):
    mock_page.return_value = _make_page_mock(INFOBOX_HTML)
    profile = LeadProfile("Max Mustermann", "Muster GmbH", "KI", "IT", AppConfig())

    profile.get_company_info()
    profile.get_company_summary()

    assert mock_page.call_count == 1


@patch("src.lead_profile.wikipedia.page")
def test_company_info_page_error_propagates(mock_page):
    mock_page.side_effect = wikipedia.exceptions.PageError("Muster GmbH")
    profile = LeadProfile("Max Mustermann", "Muster GmbH", "KI", "IT", AppConfig())

    with pytest.raises(wikipedia.exceptions.PageError):
        profile.get_company_info()


@patch("src.lead_profile.wikipedia.page")
def test_company_info_disambiguation_propagates(mock_page):
    mock_page.side_effect = wikipedia.exceptions.DisambiguationError(
        "Muster", ["Muster GmbH", "Muster AG"]
    )
    profile = LeadProfile("Max Mustermann", "Muster GmbH", "KI", "IT", AppConfig())

    with pytest.raises(wikipedia.exceptions.DisambiguationError):
        profile.get_company_info()


def _make_gn_mock(results):
    gn = MagicMock()
    gn.result.return_value = results
    return gn


@patch("src.lead_profile.GoogleNews")
def test_get_company_news(mock_gn_cls):
    results = [
        {"title": "Title A", "link": "https://example.com/a?ved=xyz", "date": "1 day ago"},
        {"title": "Title B", "link": "https://example.com/b", "date": "2 days ago"},
        {"title": "Dup", "link": "https://example.com/a", "date": "3 days ago"},
    ]
    mock_gn_cls.return_value = _make_gn_mock(results)
    config = AppConfig(news_pages=3, news_max_items=20)
    profile = LeadProfile("Max Mustermann", "Muster GmbH", "KI", "IT", config)

    news = profile.get_company_news()

    mock_gn_cls.assert_called_once_with(start=profile.start, end=profile.end)
    gn_instance = mock_gn_cls.return_value
    gn_instance.set_lang.assert_called_once_with("de")
    gn_instance.search.assert_called_once_with("Muster GmbH")
    assert gn_instance.getpage.call_count == 2  # pages 2 and 3
    # deduped by link (tracking suffix stripped before comparing)
    assert [n["link"] for n in news] == ["https://example.com/a", "https://example.com/b"]


@patch("src.lead_profile.GoogleNews")
def test_get_company_news_respects_max_items(mock_gn_cls):
    results = [
        {"title": "T{}".format(i), "link": "https://example.com/{}".format(i), "date": "today"}
        for i in range(5)
    ]
    mock_gn_cls.return_value = _make_gn_mock(results)
    config = AppConfig(news_max_items=2)
    profile = LeadProfile("Max Mustermann", "Muster GmbH", "KI", "IT", config)

    news = profile.get_company_news()

    assert len(news) == 2


@patch("src.lead_profile.GoogleNews")
def test_get_company_news_empty_result(mock_gn_cls):
    mock_gn_cls.return_value = _make_gn_mock([])
    profile = LeadProfile("Max Mustermann", "Muster GmbH", "KI", "IT", AppConfig())

    assert profile.get_company_news() == []


@patch("src.lead_profile.GoogleNews")
def test_get_topic_news_search_term(mock_gn_cls):
    mock_gn_cls.return_value = _make_gn_mock([])
    profile = LeadProfile("Max Mustermann", "Muster GmbH", "KI", "Softwareentwicklung", AppConfig())

    profile.get_topic_news()

    mock_gn_cls.return_value.search.assert_called_once_with("KI Softwareentwicklung")


@patch("src.lead_profile.GoogleNews")
@patch("src.lead_profile.wikipedia.summary")
def test_get_person_info_shape(mock_summary, mock_gn_cls):
    mock_summary.return_value = "Person summary."
    mock_gn_cls.return_value = _make_gn_mock(
        [{"title": "News", "link": "https://example.com/n", "date": "today"}]
    )
    profile = LeadProfile("Max Mustermann", "Muster GmbH", "KI", "IT", AppConfig())

    info = profile.get_person_info()

    assert info["wiki_summary"] == "Person summary."
    assert info["news"][0]["title"] == "News"
    mock_gn_cls.return_value.search.assert_called_once_with('"Max Mustermann" Muster GmbH')


@patch("src.lead_profile.GoogleNews")
@patch("src.lead_profile.wikipedia.summary")
def test_get_person_info_no_wiki_article(mock_summary, mock_gn_cls):
    mock_summary.side_effect = wikipedia.exceptions.PageError("Max Mustermann")
    mock_gn_cls.return_value = _make_gn_mock([])
    profile = LeadProfile("Max Mustermann", "Muster GmbH", "KI", "IT", AppConfig())

    info = profile.get_person_info()

    assert info["wiki_summary"] is None
    assert info["news"] == []


@patch("src.lead_profile.GoogleNews")
@patch("src.lead_profile.wikipedia.summary")
def test_get_person_info_disambiguation_is_swallowed(mock_summary, mock_gn_cls):
    mock_summary.side_effect = wikipedia.exceptions.DisambiguationError(
        "Max Mustermann", ["Max Mustermann (Politiker)", "Max Mustermann (Musiker)"]
    )
    mock_gn_cls.return_value = _make_gn_mock([])
    profile = LeadProfile("Max Mustermann", "Muster GmbH", "KI", "IT", AppConfig())

    info = profile.get_person_info()

    assert info["wiki_summary"] is None
