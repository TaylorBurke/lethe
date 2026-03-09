# Frida Kahlo Oracle Deck — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Write a 36-card Frida Kahlo oracle deck (YAML + companion JSON) ready for SDXL generation.

**Architecture:** Two subagents write the YAML and JSON in parallel. The YAML contains image prompts optimized for SDXL with the *Love Embrace* reference at 0.55 prompt strength. The JSON contains upright meanings, reversed meanings (shadow-self pattern), and keywords for the companion app.

**Tech Stack:** YAML, JSON, SDXL image generation via existing CLI

---

### Task 1: Back up existing Dalí oracle

**Files:**
- Copy: `oracle.yaml` → `deckDescriptions/dali-oracle.yaml`

**Step 1:** Copy the current Dalí oracle to deckDescriptions for safekeeping.

```bash
cp oracle.yaml deckDescriptions/dali-oracle.yaml
```

**Step 2:** Commit the backup.

```bash
git add deckDescriptions/dali-oracle.yaml
git commit -m "chore: back up Dalí oracle before Frida deck"
```

---

### Task 2: Write the 36-card Frida YAML

**Files:**
- Create: `deckDescriptions/frida-kahlo-oracle.yaml`

**Card list by thematic group:**

#### Body & Pain (~7 cards)
1. **The Broken Column** (painting) — Ionic column splitting her open torso, landscape cracked behind her, nails in skin, white surgical corset
2. **Henry Ford Hospital** (painting) — Figure on a hospital bed trailing red ribbons connected to floating symbols, barren red earth, Detroit skyline
3. **The Corset** (motif) — Plaster body cast decorated with painted flowers and a hammer-and-sickle, cracking at the seams, terracotta wall behind
4. **The Surgical Table** (motif) — Surgical instruments arranged on an embroidered cloth like a still life, marigolds growing between the tools
5. **The Spine of Thorns** (motif) — A human spine made of braided nopal cactus, each vertebra flowering, roots descending into red earth
6. **Without Hope** (painting) — Figure in bed being force-fed a funnel of grotesque abundance — skulls, fish, sausage, a sugar skull — tears on cheeks, volcanic landscape
7. **Tree of Hope** (painting) — Split scene: surgical body on a gurney in daylight, defiant standing figure in Tehuana dress holding a back brace under a night sky

#### Love & Duality (~7 cards)
8. **The Two Fridas** (painting) — Two seated women in different dresses sharing an exposed vein between their hearts, stormy sky, one heart whole, one cut and bleeding
9. **Diego and I** (painting) — Close portrait with a small figure embedded in the forehead, hair wrapping around the throat like a noose, tears on the face
10. **The Love Embrace** (painting) — Layered embrace: earth mother holding a woman holding a man, cacti and roots framing them, sun and moon flanking
11. **The Bleeding Heart** (motif) — An anatomical heart sitting on a stone altar, pierced by small silver milagro charms, marigold petals pooling beneath
12. **The Ribbon** (motif) — A single red ribbon unspooling from a wound in the chest across a landscape, connecting two distant figures who cannot see each other
13. **The Empty Bed** (motif) — An iron-frame bed with rumpled white sheets in a blue room, a single wilted sunflower on the pillow, Diego's hat on a chair
14. **A Few Small Nips** (painting) — A figure covered in small cuts standing calmly while doves circle, each dove trailing a thin red ribbon, a banner reading nothing

#### Nature & Roots (~7 cards)
15. **Roots (Raíces)** (painting) — A reclining figure whose body opens into vines and roots that penetrate dry cracked earth, green tendrils spreading across a barren landscape
16. **The Monkey** (motif) — A spider monkey with dark eyes sitting on a shoulder, one arm draped across a collarbone, jungle leaves and orchids pressing close
17. **The Wounded Deer** (painting) — A deer with a human face and antlers, pierced by arrows, running through a dense forest, the sea visible through the tree trunks
18. **The Parrot** (motif) — A bright green parrot perched on a hand outstretched from a window framed by bougainvillea, the bird's feathers catching golden light
19. **The Watermelons** (motif) — Split watermelons on a blue table, seeds scattered like constellations, the flesh vivid red against deep green rind, "VIVA LA VIDA" energy without text
20. **The Garden of Casa Azul** (motif) — A courtyard overflowing with tropical plants, clay pots, a stone fountain, painted blue walls, pre-Columbian sculptures among the ferns
21. **The Xoloitzcuintli** (motif) — A hairless black dog sitting alert on terracotta tiles, surrounded by marigolds and papel picado shadows, loyal and ancient

#### Identity & Defiance (~8 cards)
22. **Self-Portrait with Thorn Necklace** (painting) — Frontal portrait with a necklace of thorns drawing blood at the throat, a dead hummingbird pendant, a black cat and monkey flanking, butterflies in the hair
23. **Self-Portrait with Cropped Hair** (painting) — A figure in an oversized man's suit sitting on a yellow chair, shorn hair scattered on the floor like living things, scissors in hand
24. **The Tehuana Dress** (motif) — An elaborate Tehuana headdress and huipil displayed on a wooden stand, embroidered flowers cascading down the fabric, a mirror behind showing no reflection
25. **The Unibrow** (motif) — Extreme close-up of two eyes with a thick connected brow like a bird in flight, flowers growing from the brow ridge, unflinching gaze
26. **The Diary** (motif) — An open journal with painted pages — watercolor figures, handwritten words blurred into brushstrokes, dried flowers pressed between pages, ink stains
27. **The Palette** (motif) — A wooden painter's palette floating above a table, the paint colors mixing into a self-portrait on the surface, brushes scattered like bones
28. **The Communist Heart** (motif) — A clenched fist holding a hammer emerging from a field of red flowers, a dove perched on the wrist, mountains behind under a workers' banner sky
29. **The Ancestor** (motif) — A pre-Columbian stone figure sitting in a niche of a blue wall, surrounded by modern objects — a camera, a lipstick, a surgical needle — bridging centuries

#### Death & Rebirth (~7 cards)
30. **The Bus** (painting) — Passengers on a wooden bench in a cramped bus interior — a worker, a mother, a businessman — each holding something precious, moment before impact
31. **The Skeleton** (motif) — A papier-mache skeleton bride (calaca) in a Tehuana dress dancing on a rooftop at dusk, papel picado streamers, marigold garlands draped on railings
32. **The Miscarriage** (motif) — A stone cradle filled with earth instead of a child, a single green shoot emerging from the soil, moonlight through a window
33. **What the Water Gave Me** (painting) — A bathtub scene viewed from above: feet at the far end, the water filled with floating miniature scenes — a volcano, a skeleton, flowers, buildings, a drowning dress
34. **The Sun and Moon** (motif) — A face split vertically — one half lit by blazing sun over desert, the other half in cool moonlight over jungle — the division line running through a third eye
35. **The Offering** (motif) — A Dia de los Muertos ofrenda table laden with marigolds, sugar skulls, candles, pan de muerto, a painted self-portrait photograph, and a shot of tequila
36. **The Wings** (motif) — A figure mid-stride shedding a plaster body cast that cracks and falls away, underneath the skin is covered in monarch butterfly wings, the cast fragments becoming birds

**YAML format per card:**

```yaml
- name: "Card Name"
  description: "SDXL-optimized image prompt — concrete, spatial, palette-aware"
  keywords: [3-5 visually distinct symbols]
  meaning: "Upright oracle meaning in confessional or mythic voice"
  composition: "Framing, focal point, spatial arrangement"
```

**Prompt writing rules:**
- Lead with the strongest visual element
- Include palette cues: terracotta, deep green, magenta, gold, blood red, earth brown
- Reference folk-art flatness: frontal compositions, botanical framing
- Avoid: text, specific facial expressions, intricate hand poses
- Compositions: one focal point, clear foreground/background, botanical borders when appropriate

**Step 1:** Write all 36 cards in YAML format to `deckDescriptions/frida-kahlo-oracle.yaml` with deck_name "The Frida Oracle".

**Step 2:** Copy to `oracle.yaml` for generation.

```bash
cp deckDescriptions/frida-kahlo-oracle.yaml oracle.yaml
```

**Step 3:** Commit.

```bash
git add deckDescriptions/frida-kahlo-oracle.yaml oracle.yaml
git commit -m "feat: add Frida Kahlo oracle deck YAML (36 cards)"
```

---

### Task 3: Write the companion JSON

**Files:**
- Create: `deckDescriptions/frida-kahlo-oracle.json`

**JSON format:**

```json
{
  "cards": [
    {
      "name": "Card Name",
      "meaning": "Upright meaning (matches YAML)",
      "reversedMeaning": "Shadow-self reversal",
      "keywords": "comma-separated keyword string"
    }
  ]
}
```

**Reversal pattern (shadow-self):** The destructive version of the card's energy — what happens when the truth the card holds turns against you or is wielded without wisdom.

**Step 1:** Write the companion JSON with all 36 cards including reversed meanings.

**Step 2:** Commit.

```bash
git add deckDescriptions/frida-kahlo-oracle.json
git commit -m "feat: add Frida Kahlo oracle companion JSON"
```

---

### Task 4: Verify and push

**Step 1:** Validate the oracle YAML loads correctly.

```bash
python -c "from tarot_gen.cards import load_oracle_cards; from pathlib import Path; cards = load_oracle_cards(Path('oracle.yaml')); print(f'{len(cards)} cards loaded')"
```

Expected: `36 cards loaded`

**Step 2:** Push all commits.

```bash
git push
```
