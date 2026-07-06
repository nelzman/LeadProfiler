import datetime
import json

from src.config import AppConfig, load_config, news_date_range


def test_defaults_when_no_file(tmp_path):
    config = load_config(tmp_path / "does_not_exist.json")
    assert config == AppConfig()


def test_json_overlay(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"news_months": 6, "language": "en"}), encoding="utf-8")

    config = load_config(path)

    assert config.news_months == 6
    assert config.language == "en"
    # Untouched fields keep their defaults.
    assert config.news_pages == AppConfig().news_pages


def test_unknown_keys_ignored(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"news_months": 3, "totally_unknown": "value"}), encoding="utf-8")

    config = load_config(path)

    assert config.news_months == 3
    assert not hasattr(config, "totally_unknown")


def test_malformed_json_falls_back_to_defaults(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("{not valid json", encoding="utf-8")

    config = load_config(path)

    assert config == AppConfig()


def test_non_object_json_falls_back_to_defaults(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps([1, 2, 3]), encoding="utf-8")

    config = load_config(path)

    assert config == AppConfig()


def test_news_date_range_exact_strings():
    today = datetime.date(2026, 7, 5)
    start, end = news_date_range(12, today=today)

    assert end == "07/05/2026"
    assert start == (today - datetime.timedelta(days=360)).strftime("%m/%d/%Y")


def test_news_date_range_one_month():
    today = datetime.date(2026, 1, 31)
    start, end = news_date_range(1, today=today)

    assert end == "01/31/2026"
    assert start == (today - datetime.timedelta(days=30)).strftime("%m/%d/%Y")
