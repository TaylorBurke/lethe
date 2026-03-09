# Frida Kahlo Oracle Deck — Design

## Overview

A 36-card oracle deck drawn from Frida Kahlo's paintings, diary, recurring symbols, and personal mythology. Each card blends confessional directness with mythic symbolism, matching the emotional register of its subject.

## Generation Specs

- **Card count:** 36
- **Model:** SDXL with reference image
- **Reference image:** `my-ref.jpg` (*The Love Embrace of the Universe* — Frida-inspired)
- **Prompt strength:** 0.55
- **Aspect ratio:** 2:3 or 11:19
- **Style prompt:** `"Frida Kahlo folk art painting, rich terracotta and deep green palette, flat perspective, visible brushwork, botanical elements, Mexican folk symbolism, no text, painterly illustration"`

## Card Design

### Approach: Hybrid

- ~14 cards anchor to specific iconic paintings, interpreted as oracle compositions
- ~22 cards build original scenes from Frida's visual vocabulary (monkeys, parrots, cacti, ribbons, corsets, bleeding hearts, fruit, skulls, Tehuana dresses)

### Painting-Anchored Cards

These draw directly from specific works:

1. The Two Fridas
2. The Broken Column
3. Self-Portrait with Thorn Necklace and Hummingbird
4. The Wounded Deer
5. Roots (Raices)
6. Henry Ford Hospital
7. The Love Embrace of the Universe
8. What the Water Gave Me
9. Diego and I
10. Tree of Hope
11. Self-Portrait with Cropped Hair
12. The Bus
13. Without Hope
14. A Few Small Nips

### Thematic Groups (writing organization only)

| Group | Cards | Territory |
|---|---|---|
| Body & Pain | ~7 | Wounds, the column, corsets, surgery, physical suffering as teacher |
| Love & Duality | ~7 | Diego, the two Fridas, heartbreak, passion, co-dependency, devotion |
| Nature & Roots | ~7 | Botanical growth, monkeys, deer, parrots, earth, fruit, the garden |
| Identity & Defiance | ~8 | Self-portraits, the unibrow, Tehuana dress, political self, ancestry |
| Death & Rebirth | ~7 | Dia de los Muertos, skeletons, birth, miscarriage, transformation |

## Tone

- **Upright meanings:** Alternate between raw confessional voice (Frida's diary) and mythic/botanical tone, depending on the card's emotional territory
- **Reversed meanings:** Shadow-self pattern — the destructive version of the card's energy when it turns against you

## Prompt Writing Guidelines (SDXL optimization)

- Lead with concrete visual elements, not abstract concepts
- Lean into Frida's palette: terracotta, deep green, magenta, gold, blood red, earth brown
- Reference folk-art flatness: frontal compositions, visible brushwork, botanical framing
- Avoid small details SDXL can't render (text, specific facial expressions, hand poses)
- Keep compositions simple: one focal point, botanical or symbolic border elements
- 3-5 keywords per card, all visually distinct at card size

## CLI Configuration

| Setting | Value |
|---|---|
| Style prompt | See above |
| Deck type | oracle |
| Model | sdxl |
| Key card image path | my-ref |
| Prompt strength | 0.55 |
| Cards to generate | all |
| Aspect ratio | 2:3 or 11:19 |
| Cards file | oracle.yaml (default) |

## Pre-Run Steps

1. Back up current `oracle.yaml` (Dali) to `deckDescriptions/dali-oracle.yaml`
2. Write Frida YAML to `oracle.yaml`

## Deliverables

1. `deckDescriptions/frida-kahlo-oracle.yaml` — 36-card oracle YAML
2. `deckDescriptions/frida-kahlo-oracle.json` — companion app JSON
3. `oracle.yaml` — copy of the Frida YAML for generation
