from unittest.mock import MagicMock, patch

import pytest

from src.briefing import Briefing
from src.config import AppConfig
from src.talking_points import TalkingPointsError, TalkingPointsGenerator


def _briefing():
    return Briefing(
        person="Max Mustermann",
        company="Muster GmbH",
        topic="KI",
        branch="Software",
        company_info={"Branche": ["IT"]},
        company_summary="Ein Unternehmen.",
        company_news=[{"title": "Big News", "link": "https://example.com/1", "date": "heute"}],
        topic_news=[{"title": "Topic News", "link": "https://example.com/2", "date": "heute"}],
    )


def test_is_available_false_without_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert TalkingPointsGenerator.is_available() is False


def test_is_available_true_with_key(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    assert TalkingPointsGenerator.is_available() is True


def _make_anthropic_module(response_text="- Punkt eins\n- Punkt zwei"):
    fake_anthropic = MagicMock()

    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = response_text

    response = MagicMock()
    response.content = [text_block]

    client = MagicMock()
    client.messages.create.return_value = response
    fake_anthropic.Anthropic.return_value = client

    # Real exception classes so `except anthropic.AuthenticationError` works.
    class AuthenticationError(Exception):
        pass

    class RateLimitError(Exception):
        pass

    class APIConnectionError(Exception):
        pass

    class APIStatusError(Exception):
        def __init__(self, message, status_code=500):
            super().__init__(message)
            self.status_code = status_code

    fake_anthropic.AuthenticationError = AuthenticationError
    fake_anthropic.RateLimitError = RateLimitError
    fake_anthropic.APIConnectionError = APIConnectionError
    fake_anthropic.APIStatusError = APIStatusError

    return fake_anthropic, client


def test_generate_returns_text_and_uses_config_model():
    fake_anthropic, client = _make_anthropic_module()

    with patch.dict("sys.modules", {"anthropic": fake_anthropic}):
        config = AppConfig(anthropic_model="claude-opus-4-8", max_tokens=999)
        generator = TalkingPointsGenerator(config)

        result = generator.generate(_briefing())

    assert result == "- Punkt eins\n- Punkt zwei"
    _, kwargs = client.messages.create.call_args
    assert kwargs["model"] == "claude-opus-4-8"
    assert kwargs["max_tokens"] == 999
    assert "Muster GmbH" in kwargs["messages"][0]["content"]
    assert "Big News" in kwargs["messages"][0]["content"]


def test_generate_concatenates_multiple_text_blocks():
    fake_anthropic, client = _make_anthropic_module()
    block2 = MagicMock()
    block2.type = "text"
    block2.text = " mehr Text"
    client.messages.create.return_value.content = [
        client.messages.create.return_value.content[0],
        block2,
    ]

    with patch.dict("sys.modules", {"anthropic": fake_anthropic}):
        generator = TalkingPointsGenerator(AppConfig())
        result = generator.generate(_briefing())

    assert result == "- Punkt eins\n- Punkt zwei mehr Text"


def test_generate_authentication_error_wrapped():
    fake_anthropic, client = _make_anthropic_module()
    client.messages.create.side_effect = fake_anthropic.AuthenticationError("bad key")

    with patch.dict("sys.modules", {"anthropic": fake_anthropic}):
        generator = TalkingPointsGenerator(AppConfig())
        with pytest.raises(TalkingPointsError, match="API-Schlüssel ungültig"):
            generator.generate(_briefing())


def test_generate_rate_limit_error_wrapped():
    fake_anthropic, client = _make_anthropic_module()
    client.messages.create.side_effect = fake_anthropic.RateLimitError("slow down")

    with patch.dict("sys.modules", {"anthropic": fake_anthropic}):
        generator = TalkingPointsGenerator(AppConfig())
        with pytest.raises(TalkingPointsError, match="Rate-Limit"):
            generator.generate(_briefing())
