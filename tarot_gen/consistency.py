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
    """Wrap the user's style string into a structured consistency prefix.

    The same prefix is prepended to every card prompt to maximize
    stylistic coherence across the deck.
    """
    return (
        f"unified collection, consistent art style throughout, "
        f"same color palette, same line weight, same rendering technique, {style}"
    )


def resize_image_to_aspect(
    image_path: Path,
    target_width: int,
    target_height: int,
) -> bytes:
    """Resize and crop an image to match the target aspect ratio.

    Uses center crop to maintain the most important part of the image,
    then resizes to the exact target dimensions.

    Returns the resized image as PNG bytes.
    """
    with Image.open(image_path) as img:
        # Convert to RGB if necessary (handles RGBA, palette, etc.)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        orig_width, orig_height = img.size
        target_ratio = target_width / target_height
        orig_ratio = orig_width / orig_height

        if orig_ratio > target_ratio:
            # Image is wider than target - crop width
            new_width = int(orig_height * target_ratio)
            left = (orig_width - new_width) // 2
            img = img.crop((left, 0, left + new_width, orig_height))
        elif orig_ratio < target_ratio:
            # Image is taller than target - crop height
            new_height = int(orig_width / target_ratio)
            top = (orig_height - new_height) // 2
            img = img.crop((0, top, orig_width, top + new_height))

        # Resize to exact target dimensions
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        # Save to bytes
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
