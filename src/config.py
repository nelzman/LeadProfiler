# -*- coding: utf-8 -*-

import json
import logging
from dataclasses import dataclass, fields
from datetime import date, timedelta
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path.home() / ".lead_profiler.json"


@dataclass
class AppConfig:
    language: str = "de"
    news_months: int = 12
    news_pages: int = 2
    news_max_items: int = 20
    anthropic_model: str = "claude-opus-4-8"
    max_tokens: int = 1500
    log_level: str = "INFO"


def load_config(path: Optional[Path] = None) -> AppConfig:
    """Load AppConfig defaults, overlaid with a JSON file if present.

    Unknown keys are ignored. A missing or malformed file falls back to
    defaults rather than crashing the app.
    """
    config_path = path if path is not None else DEFAULT_CONFIG_PATH
    config = AppConfig()

    if not config_path.exists():
        return config

    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Could not read config file %s: %s. Using defaults.", config_path, exc)
        return config

    if not isinstance(data, dict):
        logger.warning("Config file %s did not contain a JSON object. Using defaults.", config_path)
        return config

    known_fields = {f.name for f in fields(AppConfig)}
    for key, value in data.items():
        if key in known_fields:
            setattr(config, key, value)
        else:
            logger.debug("Ignoring unknown config key: %s", key)

    return config


def news_date_range(months: int, today: Optional[date] = None) -> Tuple[str, str]:
    """Return a (start, end) date range in MM/DD/YYYY format spanning
    the given number of months up to `today` (defaults to date.today())."""
    reference = today if today is not None else date.today()
    start = reference - timedelta(days=months * 30)
    return start.strftime("%m/%d/%Y"), reference.strftime("%m/%d/%Y")
