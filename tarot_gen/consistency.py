"""Style consistency logic for tarot deck generation."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image


def get_seed(base_seed: int, index: int) -> int:
    """Derive a deterministic seed for card at given index.

    Uses a fixed offset from the base seed so each card gets a unique
    but reproducible seed, keeping the overall style consistent when
    combined with an identical prompt prefix.
    """
    return base_seed + index


def build_style_prefix(style: str) -> str:
    """Return the user's style string for use in prompts."""
    return style


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


def build_sdxl_img2img_input(
    prompt: str,
    negative_prompt: str,
    seed: int,
    image_url: str,
    width: int = 768,
    height: int = 1152,
    prompt_strength: float = 0.47,
) -> dict:
    """Build SDXL input dict for img2img using a key card as style reference.

    ``image_url`` is the Replicate URL of the key card.  ``prompt_strength``
    controls how much the new prompt overrides the reference (lower = closer
    to the reference image's style).
    """
    return {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "seed": seed,
        "width": width,
        "height": height,
        "num_outputs": 1,
        "image": image_url,
        "prompt_strength": prompt_strength,
    }
