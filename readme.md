# Lead-Profiler

This app makes it easier to get information about potential new customers, finding
interesting things to talk about during sales calls, and saving time researching a
company. Enter a lead's first name, last name, company, topic, and industry
("Branche"), and it gathers:

- The company's German Wikipedia infobox and summary
- Recent news about the company and about the topic/industry
- Best-effort background on the contact person (Wikipedia summary + news mentions)
- Optional AI-generated talking points for the call (see below)

Results can be exported as a Markdown briefing file.

## Setup

### Option A: conda

```
conda env create -f infrastructure/environment.yml
conda activate lead_profiler
```

### Option B: pip

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## AI talking points (optional)

If the `ANTHROPIC_API_KEY` environment variable is set, the app calls the
[Anthropic API](https://platform.claude.com) to generate a short list of talking
points from the gathered company/news/person data. Without the key, this feature is
simply disabled — everything else in the app works normally.

```
export ANTHROPIC_API_KEY=sk-...
```

## Configuration

Optional settings can be overridden via `~/.lead_profiler.json` (all keys optional):

```json
{
  "language": "de",
  "news_months": 12,
  "news_pages": 2,
  "news_max_items": 20,
  "anthropic_model": "claude-opus-4-8",
  "max_tokens": 1500,
  "log_level": "INFO"
}
```

`news_months` can also be adjusted per search from the app itself (the "Zeitraum
(Monate)" field). Logs are written to `~/.lead_profiler.log`.

## Running the app

The frontend is a [Streamlit](https://streamlit.io/) web app — it opens in your
browser (by default at http://localhost:8501).

```
make start_app
# or: streamlit run app.py
```

## Tests

```
make test
# or: python -m pytest tests/ -v
```

## Development notes

- The UI layer (`app.py`) is deliberately thin: it only renders. All research
  logic lives in the Qt-free `src` package, with `src/research.py::gather_briefing`
  orchestrating a full run and returning a `Briefing` plus per-section error
  messages. This keeps the app testable without a browser (see
  `tests/test_research.py`).
- News search relies on scraping Google News (via the `GoogleNews` package), which
  is inherently fragile — Google may rate-limit or change its markup at any time.
  An empty news result is treated as normal, not an error.
- PDF export is a possible follow-up; only Markdown export is implemented today.
