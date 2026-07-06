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

```
make start_app
# or: python -m src.lead_profiler_app
```

## Tests

```
make test
# or: python -m pytest tests/ -v
```

A headless GUI smoke test is also available (requires PyQt5 and a virtual display):

```
make smoke
```

## Development notes

- `src/lead_profiler_app.py` was originally generated from `src/LeadProfiler.ui` by
  the PyQt5 UI code generator, but has since been hand-edited (business logic,
  additional widgets, signal connections). **Do not regenerate it with `pyuic5`** —
  doing so would discard those changes. `LeadProfiler.ui` is kept only as a
  historical reference of the original layout; if you want to change the layout in
  Qt Designer, you'll need to manually port the result back into the `.py` file.
- News search relies on scraping Google News (via the `GoogleNews` package), which
  is inherently fragile — Google may rate-limit or change its markup at any time.
  An empty news result is treated as normal, not an error.
- PDF export is a possible follow-up; only Markdown export is implemented today.
