# The Wicker Arcana Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Write a 78-card folk horror tarot deck (YAML + deck-attributes JSON) ready for style-transfer generation.

**Architecture:** Two subagents write the YAML and deck-attributes JSON in parallel. The YAML contains image prompts optimized for style-transfer with a linocut/woodblock reference image. The deck-attributes JSON follows the template format with suit aliases (Torches/Cauldrons/Sickles/Bones), rank aliases (Maiden/Hunter/Crone/Horned King), and all 78 cards with meanings, reversals, and keywords.

**Tech Stack:** YAML, JSON, style-transfer image generation via existing CLI

---

### Task 1: Write the 78-card YAML

**Files:**
- Create: `deckDescriptions/wicker-arcana.yaml`

**Card structure follows existing custom tarot YAML format:**

```yaml
major_arcana:
  - name: "The Fool"
    numeral: "0"
    description: "style-transfer-optimized image prompt"
    key_symbols: [symbol1, symbol2, symbol3]
    composition: "framing and layout"

minor_arcana:
  torches:
    pips:
      "1":
        description: "image prompt for Ace of Torches"
        key_symbols: [symbol1, symbol2]
        composition: "framing"
      "2":
        description: "..."
        ...
    court:
      Maiden:
        description: "..."
        key_symbols: [...]
        composition: "..."
      Hunter:
        description: "..."
      Crone:
        description: "..."
      Horned King:
        description: "..."
  cauldrons:
    ...
  sickles:
    ...
  bones:
    ...
```

**Suit mapping and territories:**

| Suit key | Alias | Standard | Territory |
|---|---|---|---|
| torches | Torches | Wands | Passion, will, bonfires, illumination, things that burn |
| cauldrons | Cauldrons | Cups | Emotion, intuition, the well, the bog, what brews beneath |
| sickles | Sickles | Swords | Thought, severance, harvest, the reaping, what must be cut |
| bones | Bones | Pentacles | Body, legacy, the barrow, the ancestor, what remains |

**Court card mapping:**

| Standard | Alias | Archetype |
|---|---|---|
| Page | Maiden | Youth, innocence at the threshold |
| Knight | Hunter | Pursuit, action, tracking through the forest |
| Queen | Crone | Wisdom, sight, the old ways |
| King | Horned King | Authority, the land itself, antler-crowned |

**Major Arcana — folk horror recastings (all 22):**

0. **The Fool** — Barefoot wanderer approaching a stone circle at dusk, bundle on a stick, a hare crossing the path
1. **The Magician** — Figure at a crossroads altar with torch, cauldron, sickle, and bone laid out, raven overhead
2. **The High Priestess** — Veiled figure seated between two standing stones, full moon behind, owl on the lintel stone
3. **The Empress** — Pregnant figure crowned with wheat sheaves sitting on a mossy throne of roots, hares at her feet
4. **The Emperor** — Antlered figure on a stone seat at the center of a hill fort, oak staff, iron torc around the neck
5. **The Hierophant** — Masked elder in a stave church doorway, two kneeling figures, candle smoke rising
6. **The Lovers** — Two figures facing each other across a bonfire, hands almost touching through the flames
7. **The Chariot** — A wicker cart pulled by two stags through a dark forest path, driver holding a torch
8. **Strength** — A woman with bare hands calmly holding the jaws of a great black dog beside a standing stone
9. **The Hermit** — Cloaked figure walking alone on a moorland ridge carrying a lantern made of bone and horn
10. **Wheel of Fortune** — A great stone wheel carved with seasonal symbols half-buried in a barley field
11. **Justice** — A blindfolded figure at a crossroads holding an iron sickle and a set of hanging scales, raven on each post
12. **The Hanged Man** — A wicker figure suspended from a great oak tree, mistletoe growing where the rope meets the branch
13. **Death** — A straw effigy burning in a harvested field at dusk, sparks rising into the sky
14. **Temperance** — A figure pouring water between two clay vessels at a holy well, ferns and mossy stones
15. **The Devil** — A horned mask nailed to a tree, red ribbons trailing, two figures chained to the trunk with flower garlands
16. **The Tower** — A stone church steeple struck by lightning, crows scattering, timber falling into a churchyard
17. **The Star** — A naked figure kneeling at a dark pool, pouring water from a clay vessel, seven moths circling above
18. **The Moon** — A path between two burial mounds under a full moon, a hare and a black dog on opposite sides, bog mist rising
19. **The Sun** — Children dancing around a maypole in a sunlit clearing, flower garlands, a white horse in the background
20. **Judgement** — Figures rising from barrow graves at the sound of a great bronze horn, earth falling from their shoulders
21. **The World** — A figure dancing inside a wreath of woven wheat and ivy, the four suit symbols at the corners (torch, cauldron, sickle, bone)

**Minor Arcana — Torches (Wands) pip themes:**
- Ace: Single torch thrust into the earth at a crossroads, flame against darkness
- 2: Two torches flanking a doorway, figure choosing which to enter
- 3: Three torches on a hilltop, ships visible on a distant sea
- 4: Four torches forming corners of a celebration circle, garlands between them
- 5: Five torches clashing, sparks flying, a scuffle at a harvest fair
- 6: A torchlit procession through a village at night, a victorious figure carried aloft
- 7: A lone figure defending a ridge with a torch against six others climbing
- 8: Eight torches thrown like spears through night air over a dark valley
- 9: A battered figure behind a fence of nine planted torches, watching the dark
- 10: A figure bent under a bundle of ten unlit torches on a moorland path

**Minor Arcana — Cauldrons (Cups) pip themes:**
- Ace: A single cauldron on a stone altar, overflowing with clear spring water, fern fronds
- 2: Two figures sharing a drink from paired cauldrons beside a stream
- 3: Three women dancing around a cauldron at a feast, harvest abundance
- 4: A figure sitting under an oak ignoring three cauldrons, a fourth offered by a hand from the trunk
- 5: Three overturned cauldrons, liquid spilling on stone, two still standing behind
- 6: A child offering a small cauldron of flowers to an elder in a doorway
- 7: Seven cauldrons floating in mist, each containing a different vision
- 8: A cloaked figure walking away from eight stacked cauldrons toward a mountain pass
- 9: A satisfied figure seated before nine full cauldrons arranged on a feasting table
- 10: A family gathered around ten cauldrons at a riverside, rainbow in the mist

**Minor Arcana — Sickles (Swords) pip themes:**
- Ace: A single iron sickle driven into a tree stump, storm clouds gathering
- 2: A blindfolded figure holding two crossed sickles, sea behind in moonlight
- 3: Three sickles pinning a corn dolly to a wooden door in the rain
- 4: A figure lying on a stone tomb with four sickles arranged around them, stained glass above
- 5: A figure gathering scattered sickles from the ground while two others walk away
- 6: A ferryman poling a flat boat with six sickles bundled as cargo, calm dark water
- 7: A figure creeping away from a camp with an armful of sickles, five still stuck in the ground
- 8: A bound figure surrounded by eight sickles driven into the earth, cloth over eyes
- 9: A figure sitting upright on a bed of straw, nine sickles hung on the wall behind
- 10: A figure fallen on a field road with ten sickles in the earth around them, dawn breaking

**Minor Arcana — Bones (Pentacles) pip themes:**
- Ace: A single large animal skull resting on a mossy altar stone, gold coins in the eye sockets
- 2: A juggler tossing two carved bone discs at a market fair, infinity path
- 3: Three figures building a stone wall together, each setting a bone-carved keystone
- 4: A miser sitting on a barrow mound clutching four bone tokens, village in the distance
- 5: Two ragged figures in snow passing a lit church window, five bone tokens on the sill
- 6: A wealthy figure distributing bone tokens to kneeling villagers from a stone doorway
- 7: A farmer leaning on a fence regarding seven bone-marked boundary posts, patient waiting
- 8: A craftsman at a workbench carving bone tokens by candlelight, eight finished pieces in a row
- 9: A solitary figure in a lush walled garden with nine bone talismans hung from tree branches
- 10: A multi-generational family at a long table with ten bone heirlooms, a great house behind them

**Prompt writing rules (style-transfer optimized):**
- Lead with bold, high-contrast imagery — black ink, carved lines
- Reference linocut/woodblock quality: flat color, strong outlines, visible carving marks
- Folk horror grammar: masks, processions, fire in darkness, threshold figures
- Simple silhouette-driven compositions — one focal point
- Palette cues: bone white, charcoal black, dried blood red, harvest gold, forest green, bog brown
- Avoid photorealistic detail — embrace graphic flatness
- 3-5 key symbols per card, visually large and distinct

**Step 1:** Write all 78 cards to `deckDescriptions/wicker-arcana.yaml`.

**Step 2:** Commit.

```bash
git add deckDescriptions/wicker-arcana.yaml
git commit -m "feat: add Wicker Arcana folk horror tarot YAML (78 cards)"
```

---

### Task 2: Write the deck-attributes JSON

**Files:**
- Create: `deckDescriptions/wicker-arcana-deck-attributes.json`
- Reference: `deckDescriptions/deck-attributes-template.json` for structure

**Structure:**

```json
{
  "suitAliases": [
    { "standardName": "Wands", "alias": "Torches" },
    { "standardName": "Cups", "alias": "Cauldrons" },
    { "standardName": "Swords", "alias": "Sickles" },
    { "standardName": "Pentacles", "alias": "Bones" }
  ],
  "rankAliases": [
    { "standardName": "Ace", "alias": "" },
    { "standardName": "Two", "alias": "" },
    ...
    { "standardName": "Page", "alias": "Maiden" },
    { "standardName": "Knight", "alias": "Hunter" },
    { "standardName": "Queen", "alias": "Crone" },
    { "standardName": "King", "alias": "Horned King" }
  ],
  "cards": [
    {
      "standardName": "The Fool",
      "arcana": "major",
      "suit": null,
      "number": 0,
      "alias": "",
      "uprightMeaning": "...",
      "reversedMeaning": "...",
      "keywords": "..."
    },
    ...
    {
      "standardName": "King of Pentacles",
      "arcana": "minor",
      "suit": "pentacles",
      "number": 14,
      "alias": "Horned King of Bones",
      "uprightMeaning": "...",
      "reversedMeaning": "...",
      "keywords": "..."
    }
  ]
}
```

**Meaning writing rules:**
- Unsettling but grounded — rural wisdom that knows the cost
- Second person ("you") address
- Each meaning 2-3 sentences max
- Reversed meanings follow shadow-self pattern
- No generic advice — every meaning should feel like it was spoken by firelight at the edge of a field

**Alias rules:**
- Major arcana: alias stays empty (standard names)
- Minor pips: alias = "Ace of Torches", "Two of Cauldrons", etc.
- Minor court: alias = "Maiden of Torches", "Hunter of Cauldrons", "Crone of Sickles", "Horned King of Bones", etc.
- Rank aliases: only Page→Maiden, Knight→Hunter, Queen→Crone, King→Horned King. Ace through Ten stay empty.

**Step 1:** Write all 78 cards in deck-attributes format to `deckDescriptions/wicker-arcana-deck-attributes.json`.

**Step 2:** Commit.

```bash
git add deckDescriptions/wicker-arcana-deck-attributes.json
git commit -m "feat: add Wicker Arcana deck attributes JSON"
```

---

### Task 3: Copy YAML and push

**Step 1:** Copy the YAML to cards.yaml for generation.

```bash
cp deckDescriptions/wicker-arcana.yaml cards.yaml
```

**Step 2:** Verify the YAML loads.

```bash
python -c "from tarot_gen.cards import get_cards; cards = get_cards('all', cards_file='cards.yaml'); print(f'{len(cards)} cards loaded')"
```

Expected: `78 cards loaded`

**Step 3:** Commit and push.

```bash
git add cards.yaml
git commit -m "chore: load Wicker Arcana into cards.yaml for generation"
git push
```
