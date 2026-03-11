# The Fillmore Arcana Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Write a 78-card psychedelic poster tarot deck (YAML + deck-attributes JSON) ready for style-transfer generation.

**Architecture:** Two subagents write the YAML and deck-attributes JSON in parallel. The YAML contains image prompts optimized for style-transfer with a 1960s psychedelic concert poster reference image. The deck-attributes JSON follows the template format with no aliases (standard names throughout) and all 78 cards with meanings, reversals, and keywords.

**Tech Stack:** YAML, JSON, style-transfer image generation via existing CLI

---

### Task 1: Write the 78-card YAML

**Files:**
- Create: `deckDescriptions/fillmore-arcana.yaml`

**YAML format follows existing custom tarot structure (same as wicker-arcana.yaml).**

**Suits use standard names with standard keys:**

| Suit key | Standard | Territory |
|---|---|---|
| wands | Wands | Passion, creative fire, the spark that starts movements |
| cups | Cups | Emotion, connection, community, what flows between people |
| swords | Swords | Thought, truth, protest, what cuts through illusion |
| pentacles | Pentacles | Body, craft, the handmade, what you build with your hands |

**Court cards use standard names:**

| Standard | Archetype |
|---|---|
| Page | Youth, curiosity, the newcomer arriving at the festival |
| Knight | Action, pursuit, the one marching for the cause |
| Queen | Wisdom, nurture, the one who holds the community together |
| King | Mastery, authority, the one who channels creative power |

**Major Arcana — psychedelic poster imagery (all 22):**

0. **The Fool** — A barefoot figure in bell-bottoms and a fringed vest stepping off a rainbow-striped cliff edge, a flower tucked behind one ear, a small dog with a bandana following, sunburst behind
1. **The Magician** — A figure at a low table draped in paisley cloth with wand, cup, sword, and pentacle arranged before them, one hand raised holding a crystal, mandala halo radiating behind the head
2. **The High Priestess** — A woman seated between two pillars wrapped in flowering vines, a crescent moon crown, a scroll in her lap, owl eyes peering from the dark background, Art Nouveau border framing
3. **The Empress** — A woman reclining in a field of giant sunflowers and poppies, flowing hair merging with the flower stems, a Venus symbol on her headband, fruit and bread at her side
4. **The Emperor** — A figure on a throne made of stacked amplifiers, legs crossed, a ram's head medallion on the chest, a desert mesa landscape behind, bold geometric patterns on the robes
5. **The Hierophant** — A guru figure seated cross-legged on a raised platform, two students kneeling, incense smoke forming sacred geometry, a peacock feather fan behind, temple archway framing
6. **The Lovers** — Two figures embracing beneath a giant blooming tree, a winged figure in the branches above, the sun directly overhead, their clothes patterned with complementary paisley designs
7. **The Chariot** — A figure standing in a VW van converted to a chariot, painted with stars and moons, two sphinxes (one black, one white) pulling it forward, a highway stretching to the horizon
8. **Strength** — A woman with flowers in her hair gently holding open the jaws of a lion, both calm, a peace sign pendant at her throat, wildflowers growing around the lion's paws
9. **The Hermit** — A solitary figure on a mountain trail at twilight, holding up a lantern with a star inside, a long walking stick, patchwork cloak, distant festival lights in the valley below
10. **Wheel of Fortune** — A giant mandala wheel floating in a cosmic sky, four figures at the cardinal points (angel, eagle, bull, lion), tie-dye spiral at the center, zodiac symbols around the rim
11. **Justice** — A figure seated on a geometric throne holding balanced scales in one hand and a raised sword in the other, blindfold pushed up onto the forehead, protest banners flanking the throne
12. **The Hanged Man** — A figure suspended by one foot from a tree branch hung with prayer flags, arms relaxed, a halo of light around the head, serene expression, the world inverted but peaceful
13. **Death** — A skeleton riding a pale horse through a field of dying sunflowers, a black flag with a white rose, figures kneeling — a child offering a flower to the rider, a sunrise on the horizon
14. **Temperance** — A winged figure pouring liquid between two vessels at the edge of a stream, one foot on land, one in water, irises and lilies growing, a rainbow arcing through the pour
15. **The Devil** — A horned figure on a black cube pedestal, two figures chained loosely below (chains they could slip), bat wings spread wide, the chains made of dollar bills and TV antennas
16. **The Tower** — A tall narrow tower struck by lightning, two figures falling, a crown blown off the top, flames shaped like flowers pouring from the windows, night sky cracking open
17. **The Star** — A nude figure kneeling at a pool, pouring water from two jugs — one into the pool, one onto the earth, seven eight-pointed stars above, an ibis in the background, night garden
18. **The Moon** — A winding path between two towers leading to mountains, a full moon with a face in profile, a wolf and a dog howling on either side, a crayfish emerging from a pool, psychedelic ripples
19. **The Sun** — Two children dancing in a walled garden, a huge radiant sun with a face, sunflowers lining the wall, a white horse, butterflies, pure golden light flooding every surface
20. **Judgement** — Figures rising from flower-covered graves, arms raised, a great angel above blowing a trumpet with a banner, clouds parting to reveal brilliant light, mountains behind
21. **The World** — A dancing figure inside a laurel wreath, the four suit symbols at the corners, flowing scarves creating an infinity pattern, a globe visible behind the figure, cosmic starfield background

**Minor Arcana — Wands pip themes:**
- Ace: A single wand thrust upright from a mountaintop, a hand emerging from a cloud gripping it, leaves sprouting from the wood, sunburst radiating behind
- 2: A figure standing on a castle battlement holding two wands, looking out over the sea, a globe in one hand, choosing between two paths
- 3: A figure on a cliff watching three ships on the horizon, three wands planted beside them, golden sky, a journey beginning
- 4: Four wands forming a canopy decorated with flower garlands, two figures celebrating beneath, a castle in the background, harvest festival scene
- 5: Five figures each wielding a wand in a chaotic scuffle, a muddy field, no clear winner, competitive energy spilling everywhere
- 6: A figure on horseback wearing a flower-crown wreath of victory, holding a wand aloft, five more wands carried by a crowd following behind, a parade
- 7: A figure on a hilltop defending with a single wand against six wands rising from below, determined stance, advantage of high ground
- 8: Eight wands flying diagonally through a clear sky over an open landscape, speed lines, a river below, everything in motion
- 9: A bandaged figure leaning on a wand behind a fence of eight more, watchful and weary, bruised but standing, night sky
- 10: A figure bent under the weight of ten bundled wands, walking toward a distant town, heavy burden but almost home

**Minor Arcana — Cups pip themes:**
- Ace: A great chalice overflowing with water, held by a hand from a cloud, a dove descending into the cup, lotus flowers floating on the overflow, five streams pouring down
- 2: Two figures exchanging cups beneath a winged lion's head, a caduceus between the cups, a cottage garden behind, mutual connection
- 3: Three women raising cups in a toast in a garden, flower garlands overhead, grapes and harvest on the table, celebration
- 4: A figure sitting under a tree, arms crossed, ignoring three cups before them while a fourth is offered by a hand from a cloud, dissatisfaction
- 5: A cloaked figure staring at three spilled cups, two cups still standing behind, a bridge to a distant house, river flowing, partial loss
- 6: A boy offering a cup of flowers to a girl in a cottage garden, six cups arranged in a row, nostalgia, innocence, a memory scene
- 7: Seven cups floating in clouds, each containing a different vision — a castle, jewels, a wreath, a dragon, a snake, a glowing figure, a veiled mystery
- 8: A figure walking away from eight stacked cups toward a mountain pass under a moon, leaving what's known behind, a gap in the row
- 9: A satisfied figure seated on a wooden bench, arms crossed, nine cups arranged in an arc on a shelf behind, contentment, wish fulfilled
- 10: A family beneath a rainbow, ten cups arcing overhead, two children dancing, a cottage with a garden, complete emotional fulfillment

**Minor Arcana — Swords pip themes:**
- Ace: A hand from a cloud gripping an upright sword, a crown at the tip with an olive branch and palm frond, mountain peaks below, clarity cutting through fog
- 2: A blindfolded figure on a stone bench holding two crossed swords, a crescent moon over calm water behind, balanced tension, a decision suspended
- 3: Three swords piercing a heart against a storm sky, rain falling, a graphic symbol of heartbreak rendered in bold poster style
- 4: A figure lying on a stone slab in a chapel, hands folded, three swords on the wall, one beneath the slab, stained glass window, enforced rest
- 5: A smirking figure holding three swords while two others walk away defeated, two swords on the ground, storm clouds, a hollow victory
- 6: A ferryman poling a boat with six swords standing upright in the hull, a woman and child as passengers, calm water, moving to safer ground
- 7: A figure sneaking away from a camp carrying five swords, two still planted in the ground, looking back over the shoulder, a risky scheme
- 8: A bound and blindfolded figure surrounded by eight swords driven into the ground, water pooling at their feet, a castle on a hill behind, feeling trapped
- 9: A figure sitting upright in bed, head in hands, nine swords hung on the dark wall behind, moonlit room, anxiety and sleepless worry
- 10: A figure face-down on the ground with ten swords in their back, a dawn sky over water on the horizon, the worst has happened but the sun is rising

**Minor Arcana — Pentacles pip themes:**
- Ace: A hand from a cloud holding a golden pentacle over a garden archway, a path leading through lush hedges to a mountain, lilies blooming, abundance offered
- 2: A juggler dancing with two pentacles, an infinity loop connecting them, ships on rough seas in the background, balancing two priorities
- 3: A craftsperson working on a cathedral archway with chisel and mallet, three pentacles carved into the stonework, apprenticeship and mastery
- 4: A figure sitting on a bench, clutching a pentacle to the chest, one under each foot, one on the head, a city behind, hoarding and control
- 5: Two ragged figures trudging through snow past a lit stained-glass church window, five pentacles in the window pattern, hardship but help is near
- 6: A wealthy figure holding scales, distributing pentacles to two kneeling figures, a balanced exchange, generosity from a position of stability
- 7: A farmer leaning on a hoe, regarding seven pentacles growing on a bush, patient waiting, a harvest not yet ready, fields behind
- 8: A craftsperson at a workbench carefully carving pentacles, eight finished pieces in a row on the bench, focused skill, steady progress
- 9: A figure in a lush walled garden, a falcon on one gloved hand, nine pentacles hanging from vines and trellises, earned abundance and solitude
- 10: A multi-generational family gathered under an archway, ten pentacles arranged in the Tree of Life pattern, dogs at their feet, a great estate behind

**Prompt writing rules (style-transfer / psychedelic poster optimized):**
- Lead with poster-style graphic quality — bold black outlines, flat saturated color fields, Art Nouveau curves
- High saturation, high contrast — acid orange, electric purple, hot pink, chartreuse, cyan, gold
- Simple compositions that read like concert posters: one focal point, decorative framing elements
- Organic flowing forms — hair, smoke, vines, scarves used as compositional elements
- Avoid: photorealism, gradients, muted colors, digital aesthetics, busy overlapping compositions
- 3-5 key symbols per card, rendered as bold graphic forms

**Step 1:** Write all 78 cards to `deckDescriptions/fillmore-arcana.yaml`.

**Step 2:** Commit.

```bash
git add deckDescriptions/fillmore-arcana.yaml
git commit -m "feat: add Fillmore Arcana tarot YAML (78 cards)"
```

---

### Task 2: Write the deck-attributes JSON

**Files:**
- Create: `deckDescriptions/fillmore-arcana-deck-attributes.json`
- Reference: `deckDescriptions/deck-attributes-template.json` for structure

**Structure follows deck-attributes-template.json exactly.**

**No aliases needed — all alias fields stay empty.**

**Suit aliases:** All empty (standard names used).

**Rank aliases:** All empty (standard names used).

**Card aliases:** All empty (standard names used).

**Meaning writing rules:**
- Grounded countercultural voice — peace, freedom, questioning authority, community, authenticity
- Warm and direct, like advice from someone who's been to the festival and come back wiser
- Not cosmic/transcendent — practical wisdom with a rebellious edge
- Second person ("you") address
- Each meaning 2-3 sentences max
- Reversed meanings: shadow-self — the same energy turned hollow, co-opted, or performative
- No generic advice — every meaning should feel like it was spoken around a campfire by someone who chose freedom over conformity

**Step 1:** Write all 78 cards in deck-attributes format.

**Step 2:** Commit.

```bash
git add deckDescriptions/fillmore-arcana-deck-attributes.json
git commit -m "feat: add Fillmore Arcana deck attributes JSON"
```

---

### Task 3: Copy YAML and push

**Step 1:** Copy to cards.yaml.

```bash
cp deckDescriptions/fillmore-arcana.yaml cards.yaml
```

**Step 2:** Verify.

```bash
python -c "from tarot_gen.cards import get_cards; cards = get_cards('all', cards_file='cards.yaml'); print(f'{len(cards)} cards loaded')"
```

Expected: `78 cards loaded`

**Step 3:** Commit and push.

```bash
git add cards.yaml
git commit -m "chore: load Fillmore Arcana into cards.yaml for generation"
git push
```
