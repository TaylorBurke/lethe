"""Style consistency logic for tarot deck generation."""


def get_seed(base_seed: int, index: int) -> int:
    """Derive a deterministic seed for card at given index.

    Uses a fixed offset from the base seed so each card gets a unique
    but reproducible seed, keeping the overall style consistent when
    combined with an identical prompt prefix.
    """
    return base_seed + index


def build_style_prefix(style: str) -> str:
    """Wrap the user's style string into a consistent prefix.

    The same prefix is prepended to every card prompt to maximize
    stylistic coherence across the deck.
    """
    return f"consistent art style, {style}"
