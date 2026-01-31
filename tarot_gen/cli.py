"""CLI entry point for tarot deck generator."""

from pathlib import Path

import click
from rich.console import Console

from tarot_gen.cards import get_cards
from tarot_gen.generator import generate_deck, MODELS

console = Console()


@click.command()
@click.argument("style")
@click.option(
    "--model",
    type=click.Choice(list(MODELS.keys()), case_sensitive=False),
    default="flux-schnell",
    help="Image generation model to use.",
)
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    default=Path("output"),
    help="Output directory for generated images.",
)
@click.option(
    "--cards",
    "card_subset",
    type=click.Choice(["all", "major", "minor"], case_sensitive=False),
    default="all",
    help="Which cards to generate.",
)
@click.option("--seed", type=int, default=42, help="Base seed for reproducibility.")
@click.option("--parallel", type=int, default=1, help="Number of concurrent API calls.")
def main(
    style: str,
    model: str,
    output: Path,
    card_subset: str,
    seed: int,
    parallel: int,
) -> None:
    """Generate a complete tarot deck with a consistent art style.

    STYLE is the art style prompt, e.g. "dark gothic ink wash style".
    """
    cards = get_cards(card_subset)
    console.print(f"[bold]Generating {len(cards)} tarot cards[/bold]")
    console.print(f"  Style:  {style}")
    console.print(f"  Model:  {model}")
    console.print(f"  Output: {output.resolve()}")
    console.print(f"  Seed:   {seed}")
    console.print()

    paths = generate_deck(
        cards=cards,
        style=style,
        model=model,
        output_dir=output,
        base_seed=seed,
        parallel=parallel,
    )

    console.print(f"\n[bold green]Done![/bold green] Generated {len(paths)} images in {output.resolve()}")


if __name__ == "__main__":
    main()
