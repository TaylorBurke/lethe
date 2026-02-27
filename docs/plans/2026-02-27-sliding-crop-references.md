# Sliding Crop Window Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add deterministic sliding crop windows to style-transfer reference images so cards sharing a reference get naturally varied palettes.

**Architecture:** Extend `resize_image_to_aspect` with seed-based crop offsets scaled by a diversity dial. Generator encodes references per-card instead of once upfront. CLI adds a diversity prompt for style-transfer mode.

**Tech Stack:** Python 3.10+, Pillow (PIL), questionary

---

### Task 1: Add pytest and test infrastructure

**Files:**
- Modify: `pyproject.toml`
- Create: `tests/__init__.py`
- Create: `tests/test_consistency.py`

**Step 1: Add pytest dependency to pyproject.toml**

Add to the `[project]` section:

```toml
[project.optional-dependencies]
dev = ["pytest>=7.0"]
```

**Step 2: Create test directory and init file**

Create empty `tests/__init__.py`.

**Step 3: Write a smoke test for existing `resize_image_to_aspect`**

```python
"""Tests for tarot_gen.consistency module."""

from io import BytesIO
from pathlib import Path
import tempfile

from PIL import Image
import pytest

from tarot_gen.consistency import resize_image_to_aspect


def _make_test_image(width: int, height: int, color: tuple = (128, 64, 32)) -> Path:
    """Create a temporary solid-color PNG and return its path."""
    img = Image.new("RGB", (width, height), color)
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img.save(tmp, format="PNG")
    tmp.close()
    return Path(tmp.name)


class TestResizeImageToAspect:
    """Existing center-crop behavior (no card_seed)."""

    def test_center_crop_wider_image(self):
        """A wide image cropped to 2:3 should produce 768x1152 output."""
        path = _make_test_image(2000, 1000)
        result = resize_image_to_aspect(path, 768, 1152)
        img = Image.open(BytesIO(result))
        assert img.size == (768, 1152)

    def test_center_crop_taller_image(self):
        """A tall image cropped to 3:2 should produce 1152x768 output."""
        path = _make_test_image(1000, 2000)
        result = resize_image_to_aspect(path, 1152, 768)
        img = Image.open(BytesIO(result))
        assert img.size == (1152, 768)

    def test_exact_ratio_no_crop(self):
        """An image already at target ratio should resize without cropping."""
        path = _make_test_image(1536, 2304)  # exactly 2:3
        result = resize_image_to_aspect(path, 768, 1152)
        img = Image.open(BytesIO(result))
        assert img.size == (768, 1152)
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_consistency.py -v`
Expected: 3 PASS

**Step 5: Commit**

```
feat: add pytest infrastructure and consistency smoke tests
```

---

### Task 2: Add sliding crop to `resize_image_to_aspect`

**Files:**
- Modify: `tarot_gen/consistency.py:26-64`
- Modify: `tests/test_consistency.py`

**Step 1: Write failing tests for seed-based crop**

Add to `tests/test_consistency.py`:

```python
class TestSlidingCrop:
    """Seed-based crop offset behavior."""

    def test_no_seed_matches_center_crop(self):
        """card_seed=None should produce identical output to default."""
        path = _make_test_image(2000, 3000)
        center = resize_image_to_aspect(path, 768, 1152)
        no_seed = resize_image_to_aspect(path, 768, 1152, card_seed=None)
        assert center == no_seed

    def test_different_seeds_produce_different_crops(self):
        """Two different seeds on a large image should produce different bytes."""
        # Use a gradient image so different crops are visually distinct
        img = Image.new("RGB", (3000, 4000))
        for x in range(3000):
            for y in range(4000):
                img.putpixel((x, y), (x % 256, y % 256, (x + y) % 256))
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img.save(tmp, format="PNG")
        tmp.close()
        path = Path(tmp.name)

        crop_a = resize_image_to_aspect(path, 768, 1152, card_seed=42, diversity="high")
        crop_b = resize_image_to_aspect(path, 768, 1152, card_seed=99, diversity="high")
        assert crop_a != crop_b

    def test_same_seed_is_deterministic(self):
        """Same seed should always produce the same crop."""
        path = _make_test_image(2000, 3000)
        crop_1 = resize_image_to_aspect(path, 768, 1152, card_seed=42, diversity="medium")
        crop_2 = resize_image_to_aspect(path, 768, 1152, card_seed=42, diversity="medium")
        assert crop_1 == crop_2

    def test_small_image_falls_back_to_center(self):
        """An image at or below target size should center crop regardless of seed."""
        path = _make_test_image(768, 1152)
        center = resize_image_to_aspect(path, 768, 1152)
        seeded = resize_image_to_aspect(path, 768, 1152, card_seed=42, diversity="high")
        assert center == seeded

    def test_diversity_low_less_variation_than_high(self):
        """Low diversity should constrain offsets more than high."""
        # Create gradient image
        img = Image.new("RGB", (3000, 4000))
        for x in range(3000):
            for y in range(4000):
                img.putpixel((x, y), (x % 256, y % 256, (x + y) % 256))
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img.save(tmp, format="PNG")
        tmp.close()
        path = Path(tmp.name)

        # Generate crops for seeds 0-9 at low and high diversity
        low_crops = set()
        high_crops = set()
        for s in range(10):
            low_crops.add(resize_image_to_aspect(path, 768, 1152, card_seed=s, diversity="low"))
            high_crops.add(resize_image_to_aspect(path, 768, 1152, card_seed=s, diversity="high"))
        # High diversity should produce at least as many unique crops as low
        assert len(high_crops) >= len(low_crops)
```

**Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_consistency.py::TestSlidingCrop -v`
Expected: FAIL — `resize_image_to_aspect` doesn't accept `card_seed` or `diversity` params

**Step 3: Implement sliding crop in `resize_image_to_aspect`**

Replace the function in `tarot_gen/consistency.py`:

```python
DIVERSITY_SCALES = {"low": 0.25, "medium": 0.60, "high": 1.0}


def resize_image_to_aspect(
    image_path: Path,
    target_width: int,
    target_height: int,
    card_seed: int | None = None,
    diversity: str = "medium",
) -> bytes:
    """Resize and crop an image to match the target aspect ratio.

    When ``card_seed`` is None, uses center crop (original behavior).
    When a seed is provided, the crop window is offset deterministically
    based on the seed.  ``diversity`` controls how far from center the
    crop can drift: "low" (25%), "medium" (60%), or "high" (100%).

    Returns the resized image as PNG bytes.
    """
    with Image.open(image_path) as img:
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        orig_width, orig_height = img.size
        target_ratio = target_width / target_height
        orig_ratio = orig_width / orig_height

        if orig_ratio > target_ratio:
            # Image is wider than target — crop width
            new_width = int(orig_height * target_ratio)
            slack = orig_width - new_width
            if card_seed is not None and slack > 0:
                scale = DIVERSITY_SCALES.get(diversity, 0.60)
                usable = int(slack * scale)
                offset = (card_seed % (usable + 1)) if usable > 0 else 0
                # Center the usable range within the full slack
                margin = (slack - usable) // 2
                left = margin + offset
            else:
                left = (orig_width - new_width) // 2
            img = img.crop((left, 0, left + new_width, orig_height))
        elif orig_ratio < target_ratio:
            # Image is taller than target — crop height
            new_height = int(orig_width / target_ratio)
            slack = orig_height - new_height
            if card_seed is not None and slack > 0:
                scale = DIVERSITY_SCALES.get(diversity, 0.60)
                usable = int(slack * scale)
                offset = (card_seed % (usable + 1)) if usable > 0 else 0
                margin = (slack - usable) // 2
                top = margin + offset
            else:
                top = (orig_height - new_height) // 2
            img = img.crop((0, top, orig_width, top + new_height))

        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_consistency.py -v`
Expected: All PASS

**Step 5: Commit**

```
feat: add seed-based sliding crop to resize_image_to_aspect
```

---

### Task 3: Wire diversity into generator.py

**Files:**
- Modify: `tarot_gen/generator.py`

**Step 1: Add `diversity` parameter to `generate_deck`**

Add `diversity: str = "medium"` to the `generate_deck` signature (after `reference_map`).

**Step 2: Change reference encoding from pre-computed to per-card**

Replace the pre-encoding loop (lines 264-272) and the `_resolve_ref` function. Instead of encoding all references upfront into `reference_urls`, store the raw paths in `reference_paths` and encode per-card inside the generation loop.

In `generate_deck`, replace the style-transfer reference setup block:

```python
    # Style-transfer requires reference image(s)
    reference_paths: dict[str, Path] = {}
    if is_style_transfer:
        target_width, target_height = SDXL_DIMENSIONS.get(aspect_ratio, (768, 1152))
        if reference_map:
            for group_key, img_path in reference_map.items():
                p = Path(img_path)
                reference_paths[group_key] = p
                console.print(f"[bold cyan]  {group_key} reference:[/bold cyan] {img_path}")
            console.print(f"[bold cyan]Style transfer mode:[/bold cyan] {style_transfer_mode}")
            console.print(f"[bold cyan]Reference diversity:[/bold cyan] {diversity}")
        elif key_card_path:
            p = Path(key_card_path)
            reference_paths["_single"] = p
            console.print(f"[bold cyan]Using style reference:[/bold cyan] {key_card_path}")
            console.print(f"[bold cyan]Style transfer mode:[/bold cyan] {style_transfer_mode}")
            console.print(f"[bold cyan]Reference diversity:[/bold cyan] {diversity}")
        else:
            raise RuntimeError("style-transfer model requires reference images (--key-card or references/ directory)")
```

Replace `_resolve_ref` with a function that encodes per-card:

```python
        def _resolve_ref(card: Card, card_seed: int) -> str | None:
            """Encode the right reference for this card with seed-based crop."""
            if reference_paths:
                ref_key = _reference_key(card) if len(reference_paths) > 1 else "_single"
                ref_path = reference_paths.get(ref_key)
                if ref_path:
                    resized = resize_image_to_aspect(
                        ref_path, target_width, target_height,
                        card_seed=card_seed, diversity=diversity,
                    )
                    encoded = base64.b64encode(resized).decode()
                    return f"data:image/png;base64,{encoded}"
            return key_card_url
```

Update the call sites in both the sequential and parallel loops to pass `card_seed=seed`:

```python
                key_card_url=_resolve_ref(card, seed),
```

**Step 3: Apply the same pattern to `generate_single_card`**

Add `diversity: str = "medium"` to its signature. Replace its pre-encoding with path storage and per-card encoding, same pattern as `generate_deck`.

**Step 4: Apply to `generate_card_back`**

Add `diversity: str = "medium"` to its signature. The card back uses a single reference — encode it with `card_seed=get_seed(base_seed, 999)` and the diversity setting.

**Step 5: Commit**

```
feat: wire diversity-based per-card crop into generator
```

---

### Task 4: Add CLI prompt and plumb diversity through

**Files:**
- Modify: `tarot_gen/cli.py`

**Step 1: Add diversity prompt in `prompt_for_options`**

After the `style_transfer_mode` prompt (line 227), add:

```python
        diversity = questionary.select(
            "Reference diversity:",
            choices=["low", "medium", "high"],
            default="medium",
        ).ask()
        if diversity is None:
            sys.exit(0)
```

For non-style-transfer models, set `diversity = "medium"` as default.

**Step 2: Add `diversity` to the returned options dict**

Add `"diversity": diversity` to the return dict.

**Step 3: Add `diversity` to `save_prompt_file`**

Add this line in the style-transfer block:

```python
    if options.get('model') == 'style-transfer':
        lines.append(f"Style Transfer Mode: {options['style_transfer_mode']}")
        lines.append(f"Reference Diversity: {options.get('diversity', 'medium')}")
```

**Step 4: Plumb `diversity` through `run_generation` and `_generate_single_deck`**

Add `diversity: str = "medium"` parameter to both functions. Pass it through to `generate_deck`, `generate_single_card`, and `generate_card_back`.

**Step 5: Commit**

```
feat: add reference diversity prompt to CLI
```

---

### Task 5: Manual integration test

**Step 1: Verify backward compatibility**

Run the generator with style-transfer and confirm the new diversity prompt appears. Select "medium" and verify it generates as before (the crop offset will differ slightly from center but the workflow should complete).

**Step 2: Test with a large reference image**

Place a large image (e.g. 3000x4000) as `my-ref.png`. Run single-card mode with 3-5 copies at "high" diversity. Verify the generated cards show palette variation.

**Step 3: Commit any fixes discovered during manual testing**

---

### Task 6: Final cleanup and commit

**Step 1: Run full test suite**

Run: `python -m pytest tests/ -v`
Expected: All PASS

**Step 2: Final commit with issue reference**

```
docs: add sliding crop design and implementation plan

Closes #6
```
