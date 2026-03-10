# The Wicker Arcana — Design

## Overview

A 78-card folk horror tarot rooted in pan-European folk traditions — standing stones, harvest rituals, masks, bonfires, bog bodies, birch forests, stave churches. Linocut/woodblock aesthetic generated via style-transfer. Suits renamed to folk ritual objects, court cards to folk archetypes. Meanings are unsettling but grounded — rural wisdom that knows the cost of every harvest.

## Suits

| Standard | Alias | Element | Territory |
|---|---|---|---|
| Wands | Torches | Fire | Passion, will, illumination, the bonfire, things that burn |
| Cups | Cauldrons | Water | Emotion, intuition, what brews beneath, the well, the bog |
| Swords | Sickles | Air | Thought, severance, harvest, what must be cut, the reaping |
| Pentacles | Bones | Earth | Body, legacy, what remains, the barrow, the ancestor |

## Court Cards

| Standard | Alias | Archetype |
|---|---|---|
| Page | Maiden | Youth, innocence at the threshold, the one who is chosen |
| Knight | Hunter | Pursuit, action, the one who tracks through the forest |
| Queen | Crone | Wisdom, sight, the one who remembers the old ways |
| King | Horned King | Authority, the land itself, the one who wears the antlers |

## Major Arcana

Standard 22 cards (Fool through World), each recast through folk horror imagery. No renamed aliases for majors — standard tarot names, folk horror compositions.

## Visual World

- **Landscapes:** Moorlands, barley fields, birch forests, chalk downs, river crossings, stone circles, bog pools
- **Objects:** Wicker constructions, antler crowns, clay masks, iron sickles, tallow candles, animal skulls, corn dollies, rune stones
- **Animals:** Hares, ravens, stags, owls, black dogs, moths, adders
- **Palette:** Bone white, charcoal black, dried blood red, harvest gold, forest green, bog brown — high contrast like a woodcut
- **Aesthetic:** Bold linocut/woodblock — strong black outlines, flat color fields, visible carving marks, no gradients

## Tone

Unsettling but grounded. Rural wisdom that acknowledges the cost of every harvest. The darkness serves as teacher. Uncomfortable truths delivered plainly, like advice from someone who has buried things in the field and knows what grows back.

- Upright meanings: Folk wisdom with an edge
- Reversed meanings: Shadow-self — the same energy turned destructive or denied

## Prompt Writing Guidelines

- Lead with linocut/woodblock texture: bold lines, carved quality
- High contrast: black ink dominates, color is sparse and intentional
- Folk horror visual grammar: masks, processions, fire in darkness, figures at thresholds
- Simple compositions that read like prints: one focal point, strong silhouettes
- Avoid photorealistic detail — embrace flat, graphic quality of relief printing
- Animals and landscape as prominent as figures

## Generation Specs

| Setting | Value |
|---|---|
| Model | style-transfer |
| Reference | Linocut or woodblock print (user to source) |
| Deck type | tarot |
| Aspect ratio | 2:3 or 11:19 |
| Cards file | cards.yaml (copied from deckDescriptions/wicker-arcana.yaml) |

## Deliverables

1. `deckDescriptions/wicker-arcana.yaml` — 78-card tarot YAML with image prompts
2. `deckDescriptions/wicker-arcana-deck-attributes.json` — deck-attributes format with suit/rank aliases, all 78 card meanings, reversals, and keywords
