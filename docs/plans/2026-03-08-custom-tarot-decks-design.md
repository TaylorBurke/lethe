# Custom Tarot Decks — Thresholds & Dreamer's Garden

## Overview

Two full 78-card tarot decks with reinterpreted suits, custom descriptions, and compositions optimized for flux-schnell. Each deck targets a different social media audience.

## Shared Specifications

- **Card count:** 78 (22 major arcana + 56 minor arcana)
- **Model:** flux-schnell (no reference images)
- **Court ranks:** Page / Knight / Queen / King (traditional)
- **Output:** Custom `cards.yaml` files for each deck
- **Companion JSON:** Matching `deckDescriptions/*.json` for the companion app

## Deck 1: Thresholds (TikTok — liminal/backrooms)

### Suits

| Traditional | Thresholds | Element | Visual anchor |
|---|---|---|---|
| Wands | Doors | Fire/will | Doorways, archways, gates — open, closed, ajar |
| Cups | Mirrors | Water/emotion | Reflective surfaces, glass, still water in tiles |
| Swords | Corridors | Air/thought | Hallways, tunnels, passages that narrow or branch |
| Pentacles | Stairs | Earth/material | Staircases, escalators, ladders, levels |

### Visual World

Empty malls at 3am, hotel hallways with infinite doors, drained swimming pools under fluorescent light, fog-filled parking garages, elevator lobbies. Figures are solitary, often seen from behind or at a distance, wearing nondescript modern clothing. No fantasy costumes.

### Palette

Desaturated pastels — fluorescent lavender, seafoam tile, yellowed ceiling light, concrete grey, faded peach.

### Style Prompt

`"liminal space dreamcore, empty interior, fluorescent lighting, desaturated pastels, eerie calm, no text, digital art"`

### Major Arcana Approach

Each major maps to a liminal experience. Examples:
- The Fool: figure stepping through a door into fog
- The Tower: collapsing parking structure
- The Star: single working light in a dark corridor
- Death: an empty room being renovated, walls stripped bare

## Deck 2: The Dreamer's Garden (Pinterest — cottagecore/dark academia)

### Suits

| Traditional | Dreamer's Garden | Element | Visual anchor |
|---|---|---|---|
| Wands | Moths | Fire/will | Moths, candle flames, lanterns, drawn to light |
| Cups | Pools | Water/emotion | Still ponds, flooded rooms, rain-filled vessels |
| Swords | Thorns | Air/thought | Briars, rose thorns, sharp branches, hedgerows |
| Pentacles | Roots | Earth/material | Tree roots, mycelium, buried things, soil |

### Visual World

Overgrown Victorian conservatories, moonlit walled gardens, abandoned greenhouses with broken glass roofs, flooded stone chapels with water lilies, forest clearings at predawn. Figures wear flowing linen and wool. Animals appear frequently: foxes, owls, hares, ravens.

### Palette

Deep moss green, moonlight silver, dusty rose, midnight blue, warm amber candlelight, fog white.

### Style Prompt

`"ethereal botanical dreamcore, moonlit garden, soft focus, painterly illustration, muted earth tones and silver light, no text, dark academia aesthetic"`

### Major Arcana Approach

Each major maps to a moment in the garden. Examples:
- The Fool: barefoot figure stepping through a gate into an overgrown path at dawn
- The High Priestess: seated between two ancient yew trees
- The Tower: crumbling stone folly struck by lightning
- Death: autumn consuming a garden that will return in spring
- The Star: bioluminescent mushrooms lighting a forest floor

## Deliverables

1. `deckDescriptions/thresholds.yaml` — full 78-card YAML for Thresholds
2. `deckDescriptions/dreamers-garden.yaml` — full 78-card YAML for Dreamer's Garden
3. `deckDescriptions/thresholds.json` — companion app JSON for Thresholds
4. `deckDescriptions/dreamers-garden.json` — companion app JSON for Dreamer's Garden

## Prompt Writing Guidelines (flux-schnell optimization)

- Lead with the strongest visual element, not abstract concepts
- Prefer concrete spatial descriptions ("a figure seen from behind at the end of a long corridor") over vague moods
- Avoid small details flux can't render (text on signs, specific facial expressions, intricate hand poses)
- Keep compositions simple: one focal point, clear foreground/background separation
- Include lighting direction when possible ("fluorescent light from above", "moonlight from the left")
- Limit key_symbols to 3-5 items that are large enough to be visually distinct
