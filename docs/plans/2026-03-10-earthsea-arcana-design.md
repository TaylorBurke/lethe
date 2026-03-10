# The Earthsea Arcana — Design

## Overview

A 78-card tarot inspired by Ursula K. Le Guin's Earthsea series. Ink wash/sumi-e aesthetic generated via style-transfer. Suits mapped to the elemental magic system (Winds, Waves, Flames, Stones). Court cards as archetypes of the wizard's journey (Child, Seeker, Keeper, Namer). Philosophy-driven meanings blending Le Guin's Taoist-influenced worldview with the visual vocabulary of the Archipelago.

## Suits

| Standard | Alias | Element | Territory |
|---|---|---|---|
| Swords | Winds | Air | Thought, speech, the Old Speech, true naming, what carries across the sea |
| Cups | Waves | Water | Emotion, intuition, the sea between islands, what connects and separates |
| Wands | Flames | Fire | Will, power, transformation, dragonfire, the cost of magic |
| Pentacles | Stones | Earth | Body, craft, the land, Gont's mountain, what endures |

## Court Cards

| Standard | Alias | Archetype |
|---|---|---|
| Page | Child | Curiosity, potential, the apprentice on the threshold |
| Knight | Seeker | Journey, pursuit, the one crossing open water |
| Queen | Keeper | Wisdom, guardianship, the one who holds the balance |
| King | Namer | Mastery, true knowing, the one who speaks the name |

## Major Arcana

Standard 22 cards (Fool through World), universal names, described through Earthsea imagery. No renamed aliases for majors.

## Minor Arcana Earthsea References

Major arcana stay universal and accessible. Minor arcana use Earthsea vocabulary more freely — the dry land, the Immanent Grove, true names, specific island imagery — without naming characters directly.

## Visual World

- **Landscapes:** Island archipelagos, open sea, mountain villages, wizard towers, underground labyrinths, the Immanent Grove, the dry land
- **Objects:** Wizard staffs, sailing boats, bronze vessels, stone altars, woven rope, carved runes, candles, herbs
- **Animals:** Dragons, hawks, otaks, dolphins, goats, ravens
- **Palette:** Black ink, sea grey, bone white, touches of deep blue and burnt amber — mostly monochrome with sparse color
- **Aesthetic:** Sumi-e / ink wash — flowing brushstrokes, white space as compositional element, wet-on-wet bleeding edges, minimal detail, suggestion over depiction

## Tone

- **Major arcana:** Spare, proverbial, Le Guin's Taoist voice. "To light a candle is to cast a shadow."
- **Minor arcana:** Warmer storyteller voice, like Ogion teaching Ged. Earthsea vocabulary used freely.
- **Reversals:** Shadow-self pattern — the same energy turned against the Balance.

## Generation Specs

| Setting | Value |
|---|---|
| Model | style-transfer |
| Reference | Sumi-e / ink wash painting (user to source) |
| Deck type | tarot |
| Aspect ratio | 2:3 or 11:19 |
| Cards file | cards.yaml (copied from deckDescriptions/earthsea-arcana.yaml) |

## Deliverables

1. `deckDescriptions/earthsea-arcana.yaml` — 78-card tarot YAML with image prompts
2. `deckDescriptions/earthsea-arcana-deck-attributes.json` — deck-attributes format with aliases, meanings, reversals, keywords
