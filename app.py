# -*- coding: utf-8 -*-
"""Streamlit frontend for Lead-Profiler.

Run with:

    streamlit run app.py

This replaces the former PyQt5 desktop GUI. All research logic lives in the
Qt-free ``src`` package; this module is only the presentation layer.
"""

import streamlit as st

from src.briefing import build_markdown
from src.config import load_config
from src.logging_setup import setup_logging
from src.research import (
    SECTION_COMPANY_INFO,
    SECTION_COMPANY_NEWS,
    SECTION_COMPANY_SUMMARY,
    SECTION_PERSON,
    SECTION_TALKING_POINTS,
    SECTION_TOPIC_NEWS,
    gather_briefing,
)


def _render_news(items, error):
    """Render a list of news dicts (title/link/date) as Markdown."""
    if error:
        st.info(error)
        return
    if not items:
        st.caption("Keine News gefunden.")
        return
    for item in items:
        title = item.get("title") or "(ohne Titel)"
        link = item.get("link")
        date = item.get("date") or ""
        if link:
            st.markdown("[{}]({})".format(title, link))
        else:
            st.markdown(title)
        if date:
            st.caption(date)
        st.divider()


def _render_infobox(info, error):
    if error:
        st.info(error)
        return
    if not info:
        st.caption("Keine Daten gefunden.")
        return
    rows = []
    for key, value in info.items():
        value_str = ", ".join(str(v) for v in value) if isinstance(value, list) else str(value)
        rows.append({"Feld": key, "Wert": value_str})
    st.table(rows)


def _render_person(person_info, error):
    if error:
        st.info(error)
        return
    if not person_info:
        st.caption("Keine Daten gefunden.")
        return
    summary = person_info.get("wiki_summary")
    if summary:
        st.write(summary)
    _render_news(person_info.get("news") or [], None)


def _render_results(briefing, errors):
    st.subheader("Gesprächspunkte (KI)")
    if briefing.talking_points:
        st.markdown(briefing.talking_points)
    elif errors.get(SECTION_TALKING_POINTS):
        st.info(errors[SECTION_TALKING_POINTS])

    col_company, col_topic = st.columns(2)
    with col_company:
        st.subheader("News zur Firma")
        _render_news(briefing.company_news, errors.get(SECTION_COMPANY_NEWS))
    with col_topic:
        st.subheader("News zum Thema in der Branche")
        _render_news(briefing.topic_news, errors.get(SECTION_TOPIC_NEWS))

    col_person, col_summary = st.columns(2)
    with col_person:
        st.subheader("Info über den Lead")
        _render_person(briefing.person_info, errors.get(SECTION_PERSON))
    with col_summary:
        st.subheader("Wiki Zusammenfassung zur Firma")
        if briefing.company_summary:
            st.write(briefing.company_summary)
        elif errors.get(SECTION_COMPANY_SUMMARY):
            st.info(errors[SECTION_COMPANY_SUMMARY])
        else:
            st.caption("Keine Daten gefunden.")

    st.subheader("Wiki Infobox zur Firma")
    _render_infobox(briefing.company_info, errors.get(SECTION_COMPANY_INFO))


def main():
    config = load_config()
    setup_logging(config.log_level)

    st.set_page_config(page_title="Lead-Profiler", layout="wide")
    st.title("Lead-Profiler")

    with st.sidebar:
        st.header("Lead")
        with st.form("lead"):
            prename = st.text_input("Vorname")
            postname = st.text_input("Nachname")
            company = st.text_input("Firma")
            topic = st.text_input("Thema")
            branch = st.text_input("Branche")
            months = st.number_input(
                "Zeitraum (Monate)",
                min_value=1,
                max_value=60,
                value=config.news_months,
            )
            submitted = st.form_submit_button("Search")

    if submitted:
        config.news_months = int(months)
        name = "{} {}".format(prename, postname).strip()

        progress = st.progress(0.0, text="Recherche gestartet …")

        def on_progress(fraction, label):
            progress.progress(fraction, text=label)

        with st.spinner("Recherchiere …"):
            briefing, errors = gather_briefing(
                name, company, topic, branch, config, progress_callback=on_progress
            )
        progress.empty()

        st.session_state["briefing"] = briefing
        st.session_state["errors"] = errors

    briefing = st.session_state.get("briefing")
    errors = st.session_state.get("errors", {})

    if briefing is None:
        st.info("Geben Sie links die Lead-Daten ein und klicken Sie auf **Search**.")
        return

    safe_company = (briefing.company or "lead").strip().replace(" ", "_") or "lead"
    file_name = "briefing_{}_{}.md".format(
        safe_company, briefing.created_at.strftime("%Y-%m-%d")
    )
    st.download_button(
        "Export (Markdown)",
        data=build_markdown(briefing),
        file_name=file_name,
        mime="text/markdown",
    )

    _render_results(briefing, errors)


if __name__ == "__main__":
    main()
