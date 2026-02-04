"""Prompt template builder for tarot card image generation."""

from tarot_gen.cards import Card


DEFAULT_NEGATIVE = (
    "text, letters, words, title, label, card name, typography, font, "
    "watermark, signature, blurry, low quality, deformed, ugly, duplicate, "
    "cropped, out of frame, bad anatomy, border, frame, card border, "
    "decorative border, ornate frame, white border, black border, any border, "
    "edge decoration, margin, matting"
)


def build_prompt(card: Card, style: str) -> str:
    """Build a positive prompt for a tarot card image."""
    symbols = ", ".join(card.key_symbols)
    parts = [
        f"{style}, tarot card artwork",
        f"depicting {card.description}",
        f"with {symbols}",
    ]
    if card.composition:
        parts.append(card.composition)
    parts.append(
        "full bleed illustration extending to all edges, "
        "no border, no frame, no text, no title, seamless edge-to-edge artwork"
    )
    return ", ".join(parts)


def build_negative_prompt(extra: str | None = None) -> str:
    """Build a negative prompt to avoid common artifacts."""
    if extra:
        return f"{DEFAULT_NEGATIVE}, {extra}"
    return DEFAULT_NEGATIVE
