# The Duat Oracle Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Write a 42-card Egyptian underworld oracle deck (YAML + companion JSON) ready for style-transfer generation.

**Architecture:** Two subagents write the YAML and companion JSON in parallel. The YAML contains image prompts optimized for style-transfer with an Egyptian tomb painting reference image. The companion JSON contains meanings, reversals (blocked passage theme), and keywords for all 42 cards. Each card maps to one of the 42 Negative Confessions from the Book of the Dead.

**Tech Stack:** YAML, JSON, style-transfer image generation via existing CLI

---

### Task 1: Write the 42-card YAML

**Files:**
- Create: `deckDescriptions/duat-oracle.yaml`

**Oracle YAML format follows existing structure (same as frida-kahlo-oracle.yaml):**

```yaml
# The Duat Oracle
# 42 cards — the soul's journey through the Duat,
# one card for each of the 42 Negative Confessions.
# Maximum 100 cards per deck.

deck_name: "The Duat Oracle"

cards:
  - name: "Card Name"
    description: "style-transfer-optimized image prompt"
    keywords: [keyword1, keyword2, keyword3]
    meaning: "Brief inline meaning for display"
    composition: "framing and layout"
```

**The 42 Negative Confessions mapped to card themes:**

The cards follow the soul's journey through the Duat. Each card is named for its confession's positive theme (not the negative statement). The judge's name and original confession inform the imagery. Progress from entering the underworld through purification, trial, and the Field of Reeds.

**Journey structure (roughly grouped but flowing as a continuous path):**

**Entering the Duat (1-7):**
1. **Innocence** — Confession: "I have not committed sin." Judge: Usekh-nemmt. The soul steps through the western gate into darkness, jackal-headed Anubis waiting.
2. **Truth** — "I have not committed robbery with violence." Judge: Hept-khet. The soul stands before scales, feather of Ma'at visible.
3. **Peace** — "I have not stolen." Judge: Fenti. The soul crosses a still dark river on a reed boat.
4. **Mercy** — "I have not slain men and women." Judge: Am-khaibit. The soul kneels before a lioness-headed judge, hands open.
5. **Generosity** — "I have not stolen grain." Judge: Neha-her. The soul offers sheaves of wheat at an altar, golden fields behind.
6. **Honor** — "I have not purloined offerings." Judge: Ruruti. The soul passes between twin obelisks, offerings untouched on pedestals.
7. **Reverence** — "I have not stolen the property of the gods." Judge: Maati-f-em-tes. The soul bows before a shrine with sacred objects gleaming inside.

**Trials of the Heart (8-14):**
8. **Honesty** — "I have not uttered lies." Judge: Neba-per-em-khetkhet. The soul speaks before an ibis-headed Thoth who writes on papyrus.
9. **Contentment** — "I have not carried away food." Judge: Set-qesu. The soul sits before a laden table, hands in lap, not reaching.
10. **Kindness** — "I have not uttered curses." Judge: Utu-nesert. The soul stands with sealed lips before a cobra-headed judge, words dissolving into flowers.
11. **Fidelity** — "I have not committed adultery." Judge: Qerrti. Two figures face each other across a lotus pool, a single thread of gold connecting their hearts.
12. **Compassion** — "I have not made none to weep." Judge: Heri-seru. The soul catches falling tears in a vessel before a weeping figure.
13. **Harmony** — "I have not eaten the heart." Judge: Uamenti. The soul's heart rests on one scale, the feather on the other, perfectly balanced.
14. **Discipline** — "I have not attacked any man." Judge: Maa-antuf. The soul stands with hands behind its back before a warrior judge, weapons on the ground.

**Purification (15-21):**
15. **Integrity** — "I am not a man of deceit." Judge: Her-uru. The soul walks through a corridor of mirrors, each reflection identical.
16. **Stewardship** — "I have not stolen cultivated land." Judge: Neb-Maat. The soul tends a garden at the edge of the Nile, boundary stones intact.
17. **Discretion** — "I have not been an eavesdropper." Judge: Tenemiu. The soul turns away from a doorway where voices speak, eyes forward.
18. **Justice** — "I have not slandered." Judge: Sertiu. The soul holds its tongue before a crocodile-headed judge, papyrus scrolls unfurling clean.
19. **Temperance** — "I have not been angry without just cause." Judge: Tutu. The soul stands in flame without burning, expression serene.
20. **Purity** — "I have not debauched the wife of any man." Judge: Uamemti. The soul washes in a sacred pool, lotus flowers opening around.
21. **Devotion** — "I have not debauched the wife of any man." Judge: Maa-antuf. The soul kneels before an altar flame that burns blue and steady.

**The Weighing Hall (22-28):**
22. **Restraint** — "I have not polluted myself." Judge: Her-uru. The soul stands purified in white linen before a gateway of light.
23. **Calm** — "I have terrorised none." Judge: Khem. The soul sits cross-legged in a dark chamber, a single oil lamp, shadows retreating.
24. **Patience** — "I have not transgressed the law." Judge: Shet-kheru. The soul waits in line among other souls at the great gate, patient.
25. **Acceptance** — "I have not been wroth." Judge: Nekhen. The soul releases a red bird from cupped hands, anger leaving.
26. **Openness** — "I have not shut my ears to the words of truth." Judge: Kenemti. The soul sits with hands over ears removed, listening to Ma'at speak.
27. **Silence** — "I have not blasphemed." Judge: An-hetep-f. The soul stands mute before a falcon-headed Horus, mouth sealed with gold.
28. **Humility** — "I am not a man of violence." Judge: Sera-kheru. The soul prostrates before the scales, forehead touching stone.

**The Field of Reeds (29-35):**
29. **Stillness** — "I have not been a stirrer up of strife." Judge: Neb-heru. The soul stands at the center of a still pool, no ripples.
30. **Deliberation** — "I have not acted with undue haste." Judge: Sekhriu. The soul walks a long corridor, measuring each step.
31. **Clarity** — "I have not pried into matters." Judge: Neb-abui. The soul stands at a crossroads with clear eyes, choosing the lit path.
32. **Simplicity** — "I have not multiplied my words in speaking." Judge: Nefer-Tem. The soul speaks a single word before a lotus-crowned judge, one hieroglyph glowing.
33. **Forgiveness** — "I have wronged none, I have done no evil." Judge: Tem-Sepu. The soul embraces its own shadow-self, the two merging into one.
34. **Gratitude** — "I have not worked witchcraft against the king." Judge: Ari-em-ab-f. The soul raises hands in offering before a seated pharaoh figure, sunlight streaming.
35. **Abundance** — "I have never stopped the flowing of water." Judge: Ahi. The soul stands beside a great irrigation channel, water flowing freely to fields beyond.

**Resurrection (36-42):**
36. **Voice** — "I have never raised my voice." Judge: Uatch-rekhit. The soul sings a hymn before an assembly of gods, sound visible as golden waves.
37. **Reverence** — "I have not cursed God." Judge: Neheb-ka. The soul kneels beneath a sky full of stars in the shape of Nut arching overhead.
38. **Worthiness** — "I have not acted with arrogance." Judge: Neheb-nefert. The soul stands small before the colossal seated Osiris, green-skinned on his throne.
39. **Balance** — "I have not stolen the bread of the gods." Judge: Tcheser-tep. The soul places bread and beer on an altar, giving rather than taking.
40. **Fulfillment** — "I have not carried away the khenfu cakes." Judge: An-af. The soul receives the crook and flail crossed over its chest, transformation complete.
41. **Eternity** — "I have not snatched away the bread of the child." Judge: Hetch-abhu. The soul walks into the Field of Reeds, golden wheat stretching to the horizon, the sun overhead.
42. **Ma'at** — "I have not driven away the cattle of the gods." Judge: The Forty-Two. The soul stands crowned with the feather of truth before all 42 judges assembled, the journey complete.

**Prompt writing rules (style-transfer / tomb painting optimized):**
- Lead with the ancient Egyptian quality — flat profile figures, papyrus/sandstone ground, hieroglyphic borders
- Strict side-view poses, hierarchical scaling (gods larger than the soul)
- Classic palette: gold, lapis lazuli blue, turquoise, red ochre, black outlines
- Horizontal register format like actual tomb walls
- Key symbols: ankhs, was-scepters, djed pillars, scarabs, ba-birds, eye of Horus, feather of Ma'at
- Animal-headed gods: jackal (Anubis), ibis (Thoth), falcon (Horus), lioness (Sekhmet), cobra (Wadjet), crocodile (Sobek)
- The soul depicted as a small human figure in white linen
- Avoid: three-quarter views, photorealism, Western perspective, modern aesthetics
- 3-5 key symbols per card, rendered as bold flat forms with black outlines

**Step 1:** Write all 42 cards to `deckDescriptions/duat-oracle.yaml`.

**Step 2:** Commit.

```bash
git add deckDescriptions/duat-oracle.yaml
git commit -m "feat: add Duat Oracle YAML (42 cards)"
```

---

### Task 2: Write the companion JSON

**Files:**
- Create: `deckDescriptions/duat-oracle.json`
- Reference: `deckDescriptions/frida-kahlo-oracle.json` for structure

**JSON format follows existing oracle companion structure:**

```json
{
  "cards": [
    {
      "name": "Innocence",
      "meaning": "...",
      "reversedMeaning": "...",
      "keywords": "..."
    }
  ]
}
```

**Meaning writing rules:**
- Ceremonial and direct — priestly inscriptions carved in stone
- Declarations, not suggestions. "You stand before the scales. What you carry is what you are."
- Second person ("you") address
- Each meaning 2-3 sentences max
- Upright: passage granted — you have learned this truth, the judge lets you pass
- Reversed: blocked passage — the soul is stuck here, the confession rings hollow, the lesson is unlearned
- Every meaning rooted in Ma'at — cosmic order, truth, balance, justice
- Keywords: 3-5 comma-separated, drawing from Egyptian imagery and the confession's theme

**Step 1:** Write all 42 cards in companion JSON format.

**Step 2:** Commit.

```bash
git add deckDescriptions/duat-oracle.json
git commit -m "feat: add Duat Oracle companion JSON"
```

---

### Task 3: Copy YAML and push

**Step 1:** Copy to oracle.yaml.

```bash
cp deckDescriptions/duat-oracle.yaml oracle.yaml
```

**Step 2:** Verify.

```bash
python -c "from tarot_gen.cards import load_oracle_cards; cards = load_oracle_cards('oracle.yaml'); print(f'{len(cards)} cards loaded')"
```

Expected: `42 cards loaded`

**Step 3:** Commit and push.

```bash
git add oracle.yaml
git commit -m "chore: load Duat Oracle into oracle.yaml for generation"
git push
```
