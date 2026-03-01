# Oracle Deck Support Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add oracle deck generation alongside tarot, using the same models and pipeline with a user-defined YAML card list.

**Architecture:** Extend the `Card` dataclass with an optional `meaning` field. Add an oracle YAML loader to `cards.py`. Branch the CLI flow based on a new "Deck type" prompt at the top. Oracle cards feed into the existing `generate_deck` pipeline unchanged.

**Tech Stack:** Python 3.10+, PyYAML, questionary, Pillow, pytest

---

### Task 1: Create oracle.yaml template

**Files:**
- Create: `oracle.yaml`

**Step 1: Create the template file**

```yaml
# Oracle Deck Template
# Fill in your cards below. Each card needs a name, description, and keywords.
# 'meaning' is optional metadata (not used in image generation).
# 'composition' is optional framing/layout hint for the AI.
# Maximum 100 cards per deck.

deck_name: "My Oracle Deck"

cards:
  - name: "The Dawn"
    description: "A radiant sunrise breaking over a calm sea, golden light spilling across the water"
    keywords: [sunrise, calm sea, golden light, horizon]
    meaning: "New beginnings, fresh starts, hope on the horizon"
    composition: "wide landscape view, sun centered on horizon, water in foreground"

  - name: "The Mirror"
    description: "An ornate hand mirror reflecting a starry night sky instead of the holder's face"
    keywords: [hand mirror, starry sky, reflection, ornate frame]
    meaning: "Self-reflection, inner truth, seeing beyond the surface"
    composition: "close-up of mirror in hand, starfield visible in reflection, dark background"
```

**Step 2: Commit**

```
feat: add oracle deck YAML template
```

---

### Task 2: Add `meaning` field to Card and oracle YAML loader

**Files:**
- Modify: `tarot_gen/cards.py`
- Create: `tests/test_cards.py`

**Step 1: Write failing tests for oracle card loading**

Create `tests/test_cards.py`:

```python
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
```

**Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_cards.py -v`
Expected: FAIL — `load_oracle_cards` doesn't exist, `Card` has no `meaning` field

**Step 3: Add `meaning` field to Card and implement `load_oracle_cards`**

In `tarot_gen/cards.py`:

Add `meaning` field to the `Card` dataclass (after `composition`):

```python
    meaning: str = ""  # Oracle card meaning (metadata, not used in prompts)
```

Add the `load_oracle_cards` function (after `get_card_by_index`):

```python
MAX_ORACLE_CARDS = 100


def load_oracle_cards(yaml_path: Path) -> list[Card]:
    """Load oracle cards from a YAML file.

    Returns a list of Card objects with arcana_type="oracle" and
    sequential numerals (00, 01, 02...).

    Raises ValueError if the deck has 0 or more than 100 cards.
    """
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    raw_cards = data.get("cards", [])
    if len(raw_cards) < 1:
        raise ValueError("Oracle deck must have at least 1 card.")
    if len(raw_cards) > MAX_ORACLE_CARDS:
        raise ValueError(f"Oracle deck exceeds maximum of {MAX_ORACLE_CARDS} cards.")

    cards: list[Card] = []
    for i, card_data in enumerate(raw_cards):
        cards.append(Card(
            name=card_data["name"],
            numeral=f"{i:02d}",
            arcana_type="oracle",
            suit=None,
            description=card_data["description"],
            key_symbols=card_data.get("keywords", []),
            meaning=card_data.get("meaning", ""),
            composition=card_data.get("composition", ""),
        ))
    return cards
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_cards.py tests/test_consistency.py -v`
Expected: All PASS (new oracle tests + existing consistency tests)

**Step 5: Commit**

```
feat: add meaning field to Card and oracle YAML loader
```

---

### Task 3: Add deck type prompt and oracle CLI flow

**Files:**
- Modify: `tarot_gen/cli.py`

**Step 1: Add "Deck type" prompt at the top of `prompt_for_options`**

Insert right after the style prompt (after line 33), before the model prompt:

```python
    deck_type = questionary.select(
        "Deck type:",
        choices=["tarot", "oracle"],
        default="tarot",
    ).ask()
    if deck_type is None:
        sys.exit(0)
```

**Step 2: Branch the card subset and cards_file logic based on deck_type**

For the "Cards to generate" prompt, branch:

```python
    if deck_type == "oracle":
        cards = questionary.select(
            "Cards to generate:",
            choices=["all", "single"],
            default="all",
        ).ask()
    else:
        cards = questionary.select(
            "Cards to generate:",
            choices=CARD_SUBSETS,
            default="sample",
        ).ask()
    if cards is None:
        sys.exit(0)
```

**Step 3: Handle oracle cards_file defaulting**

For oracle mode, set `cards_file` to `oracle.yaml` automatically instead of prompting. Replace the cards_file prompt section:

```python
    if deck_type == "oracle":
        cards_file = "oracle.yaml"
        oracle_path = Path(cards_file)
        if not oracle_path.exists():
            console.print(f"[red]{cards_file} not found in project root.[/red]")
            sys.exit(1)
        # Validate card count
        from tarot_gen.cards import load_oracle_cards
        try:
            oracle_cards = load_oracle_cards(oracle_path)
        except ValueError as e:
            console.print(f"[red]Invalid oracle deck: {e}[/red]")
            sys.exit(1)
        console.print(f"[bold cyan]Oracle deck: {len(oracle_cards)} cards from {cards_file}[/bold cyan]")
    elif cards == "single":
        cards_file = None
    else:
        cards_file_str = questionary.text(
            "Custom cards YAML file:",
            instruction="(leave empty for built-in cards)",
            default="",
        ).ask()
        if cards_file_str is None:
            sys.exit(0)
        cards_file = cards_file_str.strip() if cards_file_str.strip() else None
```

**Step 4: Force single reference for oracle + style-transfer**

In the style-transfer reference image section, when `deck_type == "oracle"`, skip the 1/5 image prompt and always use `my-ref.png`:

```python
    if model == "style-transfer":
        if deck_type == "oracle" or cards == "single":
            ref_path = Path("my-ref.png")
            if not ref_path.exists():
                console.print("[red]my-ref.png not found in project root.[/red]")
                sys.exit(1)
            key_card = str(ref_path)
            if deck_type == "oracle":
                console.print(f"[bold cyan]Using single reference image: my-ref.png[/bold cyan]")
        else:
            # existing 1/5 image prompt for tarot...
```

**Step 5: Add `deck_type` to the returned options dict**

```python
        "deck_type": deck_type,
```

**Step 6: Add `deck_type` to `save_prompt_file`**

At the top of the lines list:

```python
    lines = [
        f"Deck Type: {options.get('deck_type', 'tarot')}",
        f"Style: {options['style']}",
        ...
    ]
```

**Step 7: Wire `deck_type` through `run_generation`**

Add `deck_type: str = "tarot"` parameter to `run_generation` signature.

In the deck mode section, when loading cards, branch on deck_type:

```python
    # --- Normal deck mode ---
    if deck_type == "oracle":
        from tarot_gen.cards import load_oracle_cards
        cards = load_oracle_cards(cards_file)
    else:
        cards = get_cards(card_subset, cards_file=cards_file)
```

For the single card mode, when `deck_type == "oracle"`, use `load_oracle_cards` to look up by index:

```python
    if card_subset == "single" and single_card_index is not None:
        if deck_type == "oracle":
            from tarot_gen.cards import load_oracle_cards
            all_oracle = load_oracle_cards(cards_file)
            if single_card_index >= len(all_oracle):
                console.print(f"[red]Card index {single_card_index} out of range (0-{len(all_oracle) - 1}).[/red]")
                sys.exit(1)
            card = all_oracle[single_card_index]
            is_card_back = False
        else:
            is_card_back = single_card_index == 78
            ...
```

For oracle card back, the card back index is `len(cards)` (one past last card). Handle this in the card back generation call by setting the numeral dynamically.

Display `Deck Type: oracle` in the run summary.

**Step 8: Commit**

```
feat: add deck type prompt and oracle CLI flow
```

---

### Task 4: Handle oracle card back numbering

**Files:**
- Modify: `tarot_gen/generator.py`

Currently `generate_card_back` hardcodes the filename as `78_card_back.png`. For oracle decks with fewer cards, this needs to be dynamic.

**Step 1: Add `card_count` parameter to `generate_card_back`**

Add `card_count: int = 78` to the signature. Use it for the filename:

```python
    if deck_num is not None:
        dest = output_dir / f"{card_count:02d}_card_back_{deck_num}.png"
    else:
        dest = output_dir / f"{card_count:02d}_card_back.png"
```

**Step 2: Pass `card_count` from CLI**

In `_generate_single_deck` and `run_generation`, pass `card_count=len(cards)` to `generate_card_back`.

For tarot this is 78 (unchanged behavior). For oracle it's however many cards are in the deck.

**Step 3: Verify existing tests still pass**

Run: `python -m pytest tests/ -v`
Expected: All PASS

**Step 4: Commit**

```
feat: dynamic card back numbering for oracle decks
```

---

### Task 5: Single card mode for oracle decks

**Files:**
- Modify: `tarot_gen/cli.py`

**Step 1: Adjust single card prompts for oracle**

When `deck_type == "oracle"` and `cards == "single"`:
- The card index prompt should show `(0-N)` where N is the card count minus 1 (read from `oracle.yaml`)
- Card back index = card count (not hardcoded 78)
- Skip the "Use default description?" prompt since oracle cards always use their YAML description

```python
    if cards == "single":
        if deck_type == "oracle":
            oracle_path = Path("oracle.yaml")
            from tarot_gen.cards import load_oracle_cards
            oracle_cards = load_oracle_cards(oracle_path)
            max_idx = len(oracle_cards)  # card back is at len(oracle_cards)
            idx_str = questionary.text(
                f"Card index (0-{max_idx}):",
                instruction=f"(0-{max_idx - 1} for cards, {max_idx} for card back)",
            ).ask()
        else:
            idx_str = questionary.text(
                "Card index (0-78):",
                instruction="(0-77 for cards, 78 for card back)",
            ).ask()
```

**Step 2: Commit**

```
feat: oracle single card mode with dynamic index range
```

---

### Task 6: Final integration test and cleanup

**Step 1: Run full test suite**

Run: `python -m pytest tests/ -v`
Expected: All PASS

**Step 2: Verify CLI imports**

Run: `python -c "from tarot_gen.cli import main; print('OK')"`
Expected: `OK`

**Step 3: Commit design doc and plan**

```
docs: add oracle deck design and implementation plan
```
