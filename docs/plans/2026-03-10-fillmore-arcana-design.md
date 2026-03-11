# The Fillmore Arcana — Design

## Overview

A 78-card tarot in the style of 1960s Fillmore/Avalon Ballroom concert posters. Standard tarot names throughout — no suit or rank aliases. Bold graphic compositions with Art Nouveau-influenced linework, flat saturated color fields, and organic flowing forms. Meanings grounded in countercultural values — peace, freedom, authenticity, community, questioning authority.

## Suits

Standard names, no aliases.

| Standard | Element | Territory |
|---|---|---|
| Wands | Fire | Passion, creative fire, the spark that starts movements |
| Cups | Water | Emotion, connection, community, what flows between people |
| Swords | Air | Thought, truth, protest, what cuts through illusion |
| Pentacles | Earth | Body, craft, the handmade, what you build with your hands |

## Court Cards

Standard names, no aliases: Page, Knight, Queen, King.

## Major Arcana

Standard 22 cards (Fool through World), universal names, described through psychedelic poster imagery. No renamed aliases.

## Visual World

- **Aesthetic:** Fillmore concert poster style — bold black outlines, flat color fills, Art Nouveau curves, organic flowing forms, graphic flatness
- **Palette:** Acid orange, electric purple, hot pink, chartreuse, cyan, gold — high saturation, high contrast, black outlines
- **Compositions:** Poster-style — strong central figure/symbol, decorative borders, readable silhouettes, graphic flatness like actual relief prints
- **Motifs:** Paisley, mandalas, sunbursts, flowing hair, doves, guitars, wildflowers, peace signs, third eyes, rising suns, mushrooms, VW vans, incense smoke
- **Avoid:** Photorealism, gradients, muted colors, digital/modern aesthetics

## Tone

Grounded countercultural. Peace, freedom, questioning authority, community, authenticity. Warm and direct, like advice from someone who's been to the festival and come back wiser. Not cosmic/transcendent — practical wisdom with a rebellious edge.

- Upright meanings: Countercultural wisdom — freedom, authenticity, community, creative fire
- Reversed meanings: Shadow-self — the same energy turned hollow, co-opted, or performative

## Prompt Writing Guidelines

- Lead with poster-style graphic quality: bold outlines, flat color, Art Nouveau linework
- High saturation, high contrast — no muted tones or pastels
- Simple compositions that read like concert posters: one focal point, decorative framing
- Organic flowing forms — hair, smoke, vines, waves used as compositional elements
- Avoid photorealistic detail — embrace flat, graphic quality of poster art
- 3-5 key symbols per card, rendered as bold graphic forms

## Generation Specs

| Setting | Value |
|---|---|
| Model | style-transfer |
| Reference | 1960s psychedelic concert poster (user to source) |
| Deck type | tarot |
| Aspect ratio | 2:3 or 11:19 |
| Prompt strength | 0.75 |
| Cards file | cards.yaml (copied from deckDescriptions/fillmore-arcana.yaml) |

## Deliverables

1. `deckDescriptions/fillmore-arcana.yaml` — 78-card tarot YAML with psychedelic poster-style prompts
2. `deckDescriptions/fillmore-arcana-deck-attributes.json` — deck-attributes format with meanings, reversals, and keywords (no aliases needed)
