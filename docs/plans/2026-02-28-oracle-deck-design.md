# Oracle Deck Support

**Date:** 2026-02-28

## Problem

The tool only generates 78-card tarot decks. Users want to create oracle decks with arbitrary card definitions, using the same generation models and style-transfer pipeline.

## Solution: Extend Card Model + Oracle CLI Flow

Oracle cards reuse the existing `Card` dataclass and generation pipeline. A new "Deck type: tarot / oracle" prompt at the CLI top routes into the appropriate flow.

## Oracle YAML Template

Default file: `oracle.yaml` in project root. User edits this file before running.

```yaml
deck_name: "My Oracle Deck"
cards:
  - name: "Card Name"
    description: "Scene/imagery description for image generation"
    keywords: [keyword1, keyword2]
    meaning: "Card meaning (metadata, not used for image)"
    composition: "optional framing hint"
```

- Cards get sequential numerals (`00`, `01`, ...) based on list position
- Maximum 100 cards per deck
- `description` + `keywords` drive image generation
- `meaning` is stored metadata only (not sent to model)
- `composition` is optional framing hint (same as tarot)

## Card Model Change

Add one optional field to `Card` in `cards.py`:

```python
meaning: str = ""
```

Oracle cards use `arcana_type="oracle"`, `suit=None`.

## CLI Flow

New first prompt: `Deck type: tarot / oracle`

**Tarot path:** Unchanged. Existing flow exactly as-is.

**Oracle path:**
- Cards file defaults to `oracle.yaml` (no prompt, auto-loaded)
- Validate: file exists, parses, 1-100 cards
- Card subset: `all` or `single` only (no major/minor/sample)
- Style-transfer: single reference only (`my-ref.png`), no 5-image per-suit option
- All other prompts identical: model, aspect ratio, seed, parallel, num decks, diversity

## YAML Loader

New function `_load_oracle_cards_from_yaml(path) -> list[Card]` in `cards.py`:
- Reads the oracle YAML structure
- Returns list of `Card` objects with `arcana_type="oracle"`, `suit=None`
- Validates card count (1-100)
- Auto-assigns sequential numerals

New function `get_oracle_cards(yaml_path) -> list[Card]` as the public API.

## Generator / Prompts / Consistency

No changes. Oracle cards are `Card` objects — `build_prompt`, `generate_deck`, `_generate_one`, style transfer, diversity all work as-is.

## Card Back

Card back numeral = one past last card index. E.g., 44 cards → `44_card_back.png`.

## prompt.txt

Adds `Deck Type: oracle` (or `tarot`) to the saved run metadata.

## Files Changed

- `oracle.yaml` (new) — template in project root
- `tarot_gen/cards.py` — add `meaning` field, oracle YAML loader
- `tarot_gen/cli.py` — deck type prompt, oracle flow branching
- `tarot_gen/generator.py` — no changes
- `tarot_gen/prompts.py` — no changes
- `tarot_gen/consistency.py` — no changes
