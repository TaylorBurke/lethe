"""Prompt template builder for tarot card image generation."""

from tarot_gen.cards import Card


DEFAULT_NEGATIVE = (
    "text, letters, words, watermark, signature, blurry, low quality, "
    "deformed, ugly, duplicate, cropped, out of frame, bad anatomy"
)


def build_prompt(card: Card, style: str) -> str:
    """Build a positive prompt for a tarot card image."""
    symbols = ", ".join(card.key_symbols)
    return (
        f"{style}, tarot card, {card.name}, "
        f"depicting {card.description}, "
        f"with {symbols}, ornate card border"
    )


def build_negative_prompt(extra: str | None = None) -> str:
    """Build a negative prompt to avoid common artifacts."""
    if extra:
        return f"{DEFAULT_NEGATIVE}, {extra}"
    return DEFAULT_NEGATIVE
