"""Tests for tarot_gen.cards module — oracle deck loading."""

import tempfile
from pathlib import Path

import pytest
import yaml

from tarot_gen.cards import Card, load_oracle_cards


def _write_oracle_yaml(cards: list[dict], deck_name: str = "Test Deck") -> Path:
    """Write an oracle YAML file to a temp path and return it."""
    data = {"deck_name": deck_name, "cards": cards}
    tmp = tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False, encoding="utf-8")
    yaml.dump(data, tmp, default_flow_style=False)
    tmp.close()
    return Path(tmp.name)


class TestLoadOracleCards:

    def test_loads_basic_cards(self):
        """Oracle cards should load with correct fields."""
        path = _write_oracle_yaml([
            {"name": "The Dawn", "description": "A sunrise over the sea",
             "keywords": ["sunrise", "sea"], "meaning": "New beginnings"},
            {"name": "The Mirror", "description": "A mirror reflecting stars",
             "keywords": ["mirror", "stars"], "meaning": "Self-reflection"},
        ])
        cards = load_oracle_cards(path)
        assert len(cards) == 2
        assert cards[0].name == "The Dawn"
        assert cards[0].numeral == "00"
        assert cards[0].arcana_type == "oracle"
        assert cards[0].suit is None
        assert cards[0].description == "A sunrise over the sea"
        assert cards[0].key_symbols == ["sunrise", "sea"]
        assert cards[0].meaning == "New beginnings"
        assert cards[1].numeral == "01"

    def test_sequential_numerals(self):
        """Cards should get 00, 01, 02... numerals based on position."""
        raw = [{"name": f"Card {i}", "description": f"Desc {i}",
                "keywords": [f"kw{i}"], "meaning": ""} for i in range(15)]
        path = _write_oracle_yaml(raw)
        cards = load_oracle_cards(path)
        assert cards[0].numeral == "00"
        assert cards[9].numeral == "09"
        assert cards[14].numeral == "14"

    def test_composition_optional(self):
        """Cards without composition should default to empty string."""
        path = _write_oracle_yaml([
            {"name": "No Comp", "description": "Desc", "keywords": ["kw"], "meaning": "M"},
        ])
        cards = load_oracle_cards(path)
        assert cards[0].composition == ""

    def test_composition_included(self):
        """Cards with composition should have it set."""
        path = _write_oracle_yaml([
            {"name": "With Comp", "description": "Desc", "keywords": ["kw"],
             "meaning": "M", "composition": "wide shot"},
        ])
        cards = load_oracle_cards(path)
        assert cards[0].composition == "wide shot"

    def test_meaning_optional(self):
        """Cards without meaning should default to empty string."""
        path = _write_oracle_yaml([
            {"name": "No Meaning", "description": "Desc", "keywords": ["kw"]},
        ])
        cards = load_oracle_cards(path)
        assert cards[0].meaning == ""

    def test_rejects_empty_deck(self):
        """An oracle YAML with no cards should raise ValueError."""
        path = _write_oracle_yaml([])
        with pytest.raises(ValueError, match="at least 1"):
            load_oracle_cards(path)

    def test_rejects_over_100_cards(self):
        """An oracle YAML with >100 cards should raise ValueError."""
        raw = [{"name": f"Card {i}", "description": f"D{i}",
                "keywords": ["k"], "meaning": ""} for i in range(101)]
        path = _write_oracle_yaml(raw)
        with pytest.raises(ValueError, match="100"):
            load_oracle_cards(path)

    def test_card_has_correct_slug_and_filename(self):
        """Oracle card slug/filename should work like tarot cards."""
        path = _write_oracle_yaml([
            {"name": "The Dawn", "description": "D", "keywords": ["k"], "meaning": "M"},
        ])
        cards = load_oracle_cards(path)
        assert cards[0].slug == "the_dawn"
        assert cards[0].filename == "00_the_dawn.png"
