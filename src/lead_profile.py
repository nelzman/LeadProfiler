# -*- coding: utf-8 -*-
"""
LeadProfiler - Profile
"""

import logging

import wikipedia
from GoogleNews import GoogleNews
from lxml import html

from .config import AppConfig, news_date_range

logger = logging.getLogger(__name__)


class LeadProfileError(Exception):
    """Base exception for LeadProfile data-gathering errors."""


class InfoboxNotFoundError(LeadProfileError):
    """Raised when the Wikipedia article has no company infobox table."""


INFOBOX_VALUE_KEYS = [
    "Rechtsform",
    "ISIN",
    "Gründung",
    "Sitz",
    "Leitung",
    "Mitarbeiterzahl",
    "Umsatz",
    "Branche",
    "Website",
]


def split_at_values(lst, values=INFOBOX_VALUE_KEYS):
    """Split a flat list into sublists, each starting at one of `values`."""
    indices = [i for i, x in enumerate(lst) if x in values]
    result_list = []
    for start, end in zip([0, *indices], [*indices, len(lst)]):
        result_list.append(lst[start:end])
    return result_list


def parse_infobox(html_content: str) -> dict:
    """Parse the German Wikipedia company infobox out of raw page HTML.

    Raises InfoboxNotFoundError if the article has no
    'Vorlage_Infobox_Unternehmen' table.
    """
    tree = html.fromstring(html_content)

    z = tree.xpath('//table[@id="Vorlage_Infobox_Unternehmen"]/tbody/descendant::*/text()')
    z = [i.replace("\n", "").replace("\xa0", "") for i in z if i not in ["\n", "\xa0", ", ", "[1]"]]

    if not z:
        raise InfoboxNotFoundError("No company infobox table found in the article.")

    company_info = {}
    company_info["comp_name"] = z.pop(0)
    if z:
        company_info["infostand"] = z.pop(len(z) - 1)

    grouped = split_at_values(z)
    grouped = [g for g in grouped if g]
    for group in grouped:
        key, value = group[0], group[1:]
        company_info[key] = value

    return company_info


def _strip_tracking_param(link: str) -> str:
    """Strip Google's '&ved=...' / '?ved=...' tracking suffix from a link."""
    for sep in ("&ved=", "?ved="):
        if sep in link:
            return link.split(sep)[0]
    return link


class LeadProfile:
    def __init__(self, lead_person, lead_company, topic, branch, config: AppConfig = None):
        self.lead_person = lead_person
        self.lead_company = lead_company
        self.topic = topic
        self.branch = branch
        self.config = config if config is not None else AppConfig()
        self.start, self.end = news_date_range(self.config.news_months)

        self._page = None

        wikipedia.set_lang(self.config.language)

    def _get_page(self):
        """Fetch (and cache) the Wikipedia page for the lead company."""
        if self._page is not None:
            return self._page
        try:
            self._page = wikipedia.page(self.lead_company, auto_suggest=False)
        except wikipedia.exceptions.PageError:
            # Retry once with auto-suggest, which can find a near-match title.
            self._page = wikipedia.page(self.lead_company, auto_suggest=True)
        return self._page

    def get_company_info(self) -> dict:
        page = self._get_page()
        return parse_infobox(page.html())

    def get_company_summary(self) -> str:
        page = self._get_page()
        return page.summary

    def get_person_info(self) -> dict:
        """Best-effort research on the lead person: an optional Wikipedia
        summary plus recent news mentioning the person and company."""
        wiki_summary = None
        try:
            wiki_summary = wikipedia.summary(self.lead_person, sentences=5, auto_suggest=False)
        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
            logger.debug("No unambiguous Wikipedia article found for person: %s", self.lead_person)
        except wikipedia.exceptions.WikipediaException:
            logger.exception("Wikipedia error while looking up person: %s", self.lead_person)

        searchterm = '"{}" {}'.format(self.lead_person, self.lead_company)
        news = self._search_news(searchterm, pages=1)

        return {"wiki_summary": wiki_summary, "news": news}

    def _search_news(self, searchterm: str, pages: int) -> list:
        gn = GoogleNews(start=self.start, end=self.end)
        gn.set_lang(self.config.language)
        gn.search(searchterm)  # page 1 loads automatically

        for i in range(2, 1 + pages):
            gn.getpage(i)

        results = gn.result()

        seen_links = set()
        news = []
        for item in results:
            link = item.get("link", "")
            link = _strip_tracking_param(link)
            if link in seen_links:
                continue
            seen_links.add(link)
            news.append({"title": item.get("title"), "link": link, "date": item.get("date")})
            if len(news) >= self.config.news_max_items:
                break

        return news

    def get_company_news(self) -> list:
        return self._search_news(self.lead_company, pages=self.config.news_pages)

    def get_topic_news(self) -> list:
        searchterm = self.topic + " " + self.branch
        return self._search_news(searchterm, pages=self.config.news_pages)
