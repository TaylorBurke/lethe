"""Style consistency logic for tarot deck generation."""

from __future__ import annotations


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
