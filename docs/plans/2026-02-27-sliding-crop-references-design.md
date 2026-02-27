# Sliding Crop Window for Reference Images

**Issue:** #6 — [enhancement] better references
**Date:** 2026-02-27

## Problem

Style transfer matches reference image colors too closely. All cards sharing the same reference get near-identical palettes, making the deck lack visual diversity.

## Solution: Sliding Crop Window

Instead of always center-cropping the reference image, compute a deterministic (x, y) offset for each card's crop window based on its seed. Different regions of the reference produce naturally different color palettes while maintaining the overall style.

A single "diversity" dial (low / medium / high) controls how far the crop can drift from center.

## How It Works

1. After aspect-ratio correction, compute the "slack" — extra pixels beyond the crop window in each axis
2. Use the card's seed to pick a position within the slack (deterministic modular hash)
3. Diversity scales usable slack: low = 25%, medium = 60%, high = 100%
4. Small images with no slack naturally fall back to center crop (current behavior)

## Changes

### consistency.py — `resize_image_to_aspect`

Add optional parameters:
- `card_seed: int | None = None` — when None, center crop (backward compatible)
- `diversity: str = "medium"` — controls crop offset range

### generator.py

- `generate_deck`, `generate_single_card`, `generate_card_back` gain `diversity: str = "medium"`
- Reference encoding moves from pre-computed (once per reference) to per-card (each card gets its own crop)
- Works with both 1-image and 5-image reference modes

### cli.py

- New prompt after reference image selection: "Reference diversity: low / medium / high"
- Default: medium
- Only shown for style-transfer model
- Saved to prompt.txt

## Performance

Per-card crop+resize+base64 is ~5-10ms each — negligible vs API call latency. Up to 78 encodes per deck run.

## Compatibility

- `card_seed=None` preserves exact current behavior
- Small reference images degrade gracefully (zero slack = center crop)
- Works with 1-image mode, 5-image mode, and single-card mode
- Deterministic: same seed + settings = same crops every time
