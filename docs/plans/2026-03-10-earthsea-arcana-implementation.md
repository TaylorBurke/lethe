# The Earthsea Arcana Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Write a 78-card Earthsea-inspired tarot deck (YAML + deck-attributes JSON) ready for style-transfer generation.

**Architecture:** Two subagents write the YAML and deck-attributes JSON in parallel. The YAML contains image prompts optimized for style-transfer with a sumi-e/ink wash reference image. The deck-attributes JSON follows the template format with suit aliases (Winds/Waves/Flames/Stones), rank aliases (Child/Seeker/Keeper/Namer), and all 78 cards with meanings, reversals, and keywords.

**Tech Stack:** YAML, JSON, style-transfer image generation via existing CLI

---

### Task 1: Write the 78-card YAML

**Files:**
- Create: `deckDescriptions/earthsea-arcana.yaml`

**YAML format follows existing custom tarot structure (same as wicker-arcana.yaml).**

**Suit mapping:**

| Suit key | Alias | Standard | Territory |
|---|---|---|---|
| flames | Flames | Wands | Will, power, transformation, dragonfire, the cost of magic |
| waves | Waves | Cups | Emotion, intuition, the sea between islands, what connects and separates |
| winds | Winds | Swords | Thought, speech, the Old Speech, true naming, what carries across the sea |
| stones | Stones | Pentacles | Body, craft, the land, Gont's mountain, what endures |

**Court card mapping:**

| Standard | Alias | Archetype |
|---|---|---|
| Page | Child | Curiosity, potential, the apprentice on the threshold |
| Knight | Seeker | Journey, pursuit, the one crossing open water |
| Queen | Keeper | Wisdom, guardianship, the one who holds the balance |
| King | Namer | Mastery, true knowing, the one who speaks the name |

**Major Arcana — Earthsea imagery (all 22):**

0. **The Fool** — A young figure with a staff setting out from a mountain village, the sea visible below, a hawk circling overhead
1. **The Magician** — A figure at a stone table with the four elements before them (candle flame, bowl of water, feather, stone), runes carved in the table
2. **The High Priestess** — A robed figure in an underground labyrinth, single candle flame, walls carved with ancient symbols
3. **The Empress** — A woman seated in a grove of ancient trees, roots visible, fruit heavy on branches, an otak curled in her lap
4. **The Emperor** — A figure on a stone throne at a cliff edge overlooking the sea, a carved staff across the knees, islands on the horizon
5. **The Hierophant** — An old master teaching in a courtyard of a tower school, two young students kneeling, open sky above
6. **The Lovers** — Two figures standing on opposite shores of a narrow strait, reaching across the water, a single boat between them
7. **The Chariot** — A small sailing boat cutting through rough open sea, single figure at the tiller, stars visible through storm clouds
8. **Strength** — A figure with open hands facing a dragon, no weapon drawn, the dragon's eye meeting the human's gaze
9. **The Hermit** — A solitary figure on a fog-wrapped mountain path, one hand touching the bark of a tree, herbs bundled at the belt
10. **Wheel of Fortune** — A great stone circle on a hilltop, shadows turning with the sun, the sea visible in every direction
11. **Justice** — A figure holding balanced scales on a rocky shore, one side holding a feather, the other a stone, calm sea behind
12. **The Hanged Man** — A figure suspended upside-down from the mast of a beached boat, the tide coming in, face serene
13. **Death** — A solitary figure walking across the dry land under a starless sky, dust rising from each step, a low stone wall in the distance
14. **Temperance** — A figure pouring water between two bronze vessels at a spring where fresh water meets the sea, mist rising
15. **The Devil** — A figure staring into a dark mirror, a shadowy double staring back, chains of their own making draped loosely at the wrists
16. **The Tower** — A wizard's tower on a rocky island struck by dragonfire, stones falling into the sea, smoke rising
17. **The Star** — A figure kneeling at the edge of a tide pool at night, pouring water back into the sea, constellations reflected in the pool
18. **The Moon** — A boat drifting on a still sea under a full moon, the water surface showing a different sky beneath, two islands like sentinels
19. **The Sun** — Children playing on a sunlit beach, a beached sailing boat, a dolphin leaping in the shallows, bright morning light
20. **Judgement** — Figures emerging from underground tombs into daylight, hands raised to shield eyes, an open sky after long darkness
21. **The World** — A dragon and a human facing each other in perfect stillness on a cliff above the sea, wind in the grass, complete balance

**Minor Arcana — Flames (Wands) pip themes:**
- Ace: A single flame burning on a stone altar on a cliff edge, wind unable to extinguish it
- 2: A figure holding two torches at a crossroads on a coastal path, looking toward two islands
- 3: Three signal fires burning on hilltops across a chain of islands, ships on the water between
- 4: Four torches marking the corners of a celebration in a village square, dancers within
- 5: Five figures with staffs clashing in a dusty courtyard, a tower school in the background
- 6: A figure on a boat holding a torch aloft, a procession of boats following through a channel
- 7: A lone figure on a rocky outcrop defending with a flaming staff, six shadows climbing below
- 8: Eight streaks of fire arcing across a night sky over the sea, like falling stars
- 9: A weary figure gripping a staff behind a wall of eight planted torches, watching the dark sea
- 10: A figure carrying a heavy bundle of unlit brands up a steep mountain path, village far below

**Minor Arcana — Waves (Cups) pip themes:**
- Ace: A single bronze bowl overflowing with clear spring water on a mossy stone, ferns around
- 2: Two figures sharing a drink from paired cups on a boat deck, calm sea, islands behind
- 3: Three women pouring water together into a shared basin at a village well, celebration
- 4: A figure sitting under a tree on a shore, ignoring three vessels, a fourth offered from the tide
- 5: Three overturned vessels on wet rocks, water spilling into the sea, two vessels upright behind
- 6: A child offering a small clay cup of flowers to an elder at a cottage door, island village
- 7: Seven bronze bowls arranged on a rock shelf, each reflecting a different vision — islands, dragons, towers
- 8: A cloaked figure walking away from eight stacked vessels on a beach, toward a distant island
- 9: A satisfied figure seated before nine full vessels on a table in a lamplit room, window showing sea
- 10: A family gathered at a long table near the shore, ten vessels between them, a rainbow over the water

**Minor Arcana — Winds (Swords) pip themes:**
- Ace: A single feather standing upright in a crack in a standing stone, storm clouds gathering
- 2: A blindfolded figure holding two crossed feathers, seated on a cliff edge, sea wind blowing
- 3: Three rune-carved arrows pinning a torn sail to a mast, rain falling
- 4: A figure lying on a stone slab in a quiet cave, four feathers arranged around them, candlelight
- 5: A figure gathering scattered feathers from a windswept beach while others walk away
- 6: A ferryman poling a boat through fog, six feathered pennants on the bow, calm dark water
- 7: A figure slipping away from a camp with an armful of scrolls, five feathered markers still in ground
- 8: A bound figure surrounded by eight tall feathered stakes driven into sand, cloth over eyes
- 9: A figure sitting upright in bed, nine feathered runes hung on the wall behind, moonlit room
- 10: A figure fallen on a shore with ten feathered shafts around them, the first light of dawn on the water

**Minor Arcana — Stones (Pentacles) pip themes:**
- Ace: A single smooth stone with a carved rune resting on a moss-covered altar, forest light
- 2: A juggler tossing two carved stones at a harbor market, the infinity pattern in the air
- 3: Three figures building a stone wall together on a hillside, each fitting a carved keystone
- 4: A figure sitting on a boulder clutching four rune stones, a village visible in the valley below
- 5: Two ragged figures in rain passing a lit window, five carved stones on the windowsill
- 6: A figure distributing rune stones to kneeling villagers from a doorway, generous gesture
- 7: A farmer leaning on a stone wall regarding seven boundary markers, patient waiting, fields behind
- 8: A craftsman at a workbench carving rune stones by candlelight, eight finished pieces in a row
- 9: A solitary figure in a walled garden with nine carved stones hung from tree branches
- 10: A multi-generational family at a stone table, ten carved heirlooms between them, a great house behind

**Prompt writing rules (style-transfer / sumi-e optimized):**
- Lead with the ink quality — flowing brushstrokes, wet-on-wet edges, suggestion over depiction
- White space is compositional — leave room for emptiness, do not fill the frame
- Monochrome dominant: black ink, sea grey, bone white. Sparse color: deep blue, burnt amber
- Simple compositions: one focal point, minimal background detail
- Earthsea imagery: archipelago sea, wizard towers, small boats, mountains, dragons, underground passages
- Avoid: detailed faces, photorealism, busy compositions, bright saturated color
- 3-5 key symbols per card, rendered as bold ink forms

**Step 1:** Write all 78 cards to `deckDescriptions/earthsea-arcana.yaml`.

**Step 2:** Commit.

```bash
git add deckDescriptions/earthsea-arcana.yaml
git commit -m "feat: add Earthsea Arcana tarot YAML (78 cards)"
```

---

### Task 2: Write the deck-attributes JSON

**Files:**
- Create: `deckDescriptions/earthsea-arcana-deck-attributes.json`
- Reference: `deckDescriptions/deck-attributes-template.json` for structure

**Structure follows deck-attributes-template.json exactly.**

**Suit aliases:**
- Wands → "Flames"
- Cups → "Waves"
- Swords → "Winds"
- Pentacles → "Stones"

**Rank aliases:**
- Ace through Ten → empty (standard names)
- Page → "Child"
- Knight → "Seeker"
- Queen → "Keeper"
- King → "Namer"

**Card aliases:**
- Major arcana: empty (standard names)
- Minor pips: "Ace of Flames", "Two of Waves", etc.
- Minor court: "Child of Flames", "Seeker of Waves", "Keeper of Winds", "Namer of Stones", etc.

**Meaning writing rules:**
- Major arcana: Spare, proverbial, Le Guin's Taoist voice. Short sentences that land like proverbs. "To light a candle is to cast a shadow." "You cannot control the sea. You can only learn to sail."
- Minor arcana: Warmer storyteller voice. Earthsea vocabulary — the dry land, the Immanent Grove, true names, the Balance, the Archipelago.
- Second person ("you") address
- Each meaning 2-3 sentences max
- Reversed meanings: shadow-self — the same energy turned against the Balance
- No generic advice — every meaning rooted in Le Guin's philosophy: balance, true naming, the cost of power, shadow integration, death as completion

**Step 1:** Write all 78 cards in deck-attributes format.

**Step 2:** Commit.

```bash
git add deckDescriptions/earthsea-arcana-deck-attributes.json
git commit -m "feat: add Earthsea Arcana deck attributes JSON"
```

---

### Task 3: Copy YAML and push

**Step 1:** Copy to cards.yaml.

```bash
cp deckDescriptions/earthsea-arcana.yaml cards.yaml
```

**Step 2:** Verify.

```bash
python -c "from tarot_gen.cards import get_cards; cards = get_cards('all', cards_file='cards.yaml'); print(f'{len(cards)} cards loaded')"
```

Expected: `78 cards loaded`

**Step 3:** Commit and push.

```bash
git add cards.yaml
git commit -m "chore: load Earthsea Arcana into cards.yaml for generation"
git push
```
