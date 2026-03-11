# The Duat Oracle — Design

## Overview

A 42-card oracle deck based on the soul's journey through the Egyptian underworld (Duat). Each card corresponds to one of the 42 Negative Confessions — the declarations of innocence the deceased makes before 42 divine judges in the Hall of Two Truths. Ancient tomb painting aesthetic: flat profile figures, hieroglyphic borders, papyrus texture, the classic Egyptian palette. Meanings delivered in a ceremonial, inscriptional voice. Reversals represent blocked passage — the soul stuck at this stage, the lesson unlearned.

## Card Structure

Each card maps to one of the 42 Negative Confessions. The journey progresses from the soul entering the Duat through purification, trial, and ultimately the Field of Reeds.

**Per card:**
- **Card name** — the confession's theme (e.g., "Truth," "Abundance," "Stillness")
- **Judge** — the divine figure presiding (e.g., "Before Usekh-nemmt")
- **Confession** — the original declaration (e.g., "I have not committed sin")
- **Image** — tomb painting scene of the soul before this judge
- **Upright meaning** — the lesson mastered, passage granted
- **Reversed meaning** — blocked passage, the soul stuck here

## Visual World

- **Aesthetic:** Ancient Egyptian tomb painting — flat profile figures, strict side-view poses, hierarchical scaling, registers/bands of action
- **Palette:** Gold, lapis lazuli blue, turquoise, red ochre, black outline on warm papyrus/sandstone ground
- **Borders:** Hieroglyphic cartouche-style framing, lotus and papyrus column borders
- **Figures:** Gods in animal-headed human form (jackal, ibis, falcon, cobra, crocodile), the soul as a small human figure, ba-birds, scarabs, ankhs, was-scepters, djed pillars
- **Compositions:** Horizontal register format like actual tomb walls — figures in profile, offerings arranged in rows, minimal perspective
- **Avoid:** Three-quarter views, photorealism, Western perspective, modern aesthetics

## Tone

Ceremonial and direct. Priestly inscriptions carved in stone. Declarations, not suggestions. "You stand before the scales. What you carry is what you are." Second person address. 2-3 sentences per meaning. Every meaning rooted in Ma'at — cosmic order, truth, balance, justice.

- **Upright:** Passage granted — you have learned this truth
- **Reversed:** Blocked passage — you are stuck here, the confession rings hollow

## Generation Specs

| Setting | Value |
|---|---|
| Model | style-transfer |
| Reference | Egyptian tomb painting (user to source) |
| Deck type | oracle |
| Aspect ratio | 2:3 or 11:19 |
| Prompt strength | 0.55 |
| Cards file | oracle.yaml (copied from deckDescriptions/duat-oracle.yaml) |

## Deliverables

1. `deckDescriptions/duat-oracle.yaml` — 42-card oracle YAML with tomb painting prompts
2. `deckDescriptions/duat-oracle.json` — companion JSON with meanings, reversals, keywords
