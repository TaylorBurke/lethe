"""CLI entry point for tarot deck generator."""

import shutil
import sys
from datetime import datetime
from pathlib import Path

import questionary
from rich.console import Console

from tarot_gen.cards import get_cards
from tarot_gen.generator import generate_deck, MODELS, STYLE_TRANSFER_MODES

console = Console()
LOGS_DIR = Path("output-logs")

ASPECT_RATIOS = ["11:19", "300x575", "2:3", "3:2", "1:1", "16:9", "9:16", "4:5", "5:4", "21:9", "9:21"]
CARD_SUBSETS = ["sample", "major", "minor", "all"]


def prompt_for_options() -> dict:
    """Interactively prompt user for all generation options."""

    style = questionary.text(
        "Style prompt:",
        instruction="(e.g., 'dark gothic ink wash style')",
    ).ask()
    if style is None:  # User pressed Ctrl+C
        sys.exit(0)
    if not style.strip():
        console.print("[red]Style prompt is required.[/red]")
        sys.exit(1)

    model = questionary.select(
        "Model:",
        choices=list(MODELS.keys()),
        default="flux-schnell",
    ).ask()
    if model is None:
        sys.exit(0)

    cards = questionary.select(
        "Cards to generate:",
        choices=CARD_SUBSETS,
        default="sample",
    ).ask()
    if cards is None:
        sys.exit(0)

    aspect_ratio = questionary.select(
        "Aspect ratio:",
        choices=ASPECT_RATIOS,
        default="11:19",
    ).ask()
    if aspect_ratio is None:
        sys.exit(0)

    output = questionary.text(
        "Output directory:",
        default="output",
    ).ask()
    if output is None:
        sys.exit(0)

    seed_str = questionary.text(
        "Seed:",
        default="42",
    ).ask()
    if seed_str is None:
        sys.exit(0)
    seed = int(seed_str) if seed_str.strip() else 42

    parallel_str = questionary.text(
        "Parallel API calls:",
        default="1",
    ).ask()
    if parallel_str is None:
        sys.exit(0)
    parallel = int(parallel_str) if parallel_str.strip() else 1

    # Model-specific options
    key_card = None
    prompt_strength = 0.47
    style_transfer_mode = "high-quality"

    if model == "style-transfer":
        # Style-transfer requires a reference image
        key_card_str = questionary.select(
            "Style reference image:",
            choices=["my-ref.png"],
            default="my-ref.png",
        ).ask()
        if key_card_str is None:
            sys.exit(0)
        key_card = key_card_str

        style_transfer_mode = questionary.select(
            "Style transfer mode:",
            choices=STYLE_TRANSFER_MODES,
            default="high-quality",
        ).ask()
        if style_transfer_mode is None:
            sys.exit(0)

    elif model == "sdxl":
        key_card_str = questionary.text(
            "Key card image path:",
            instruction="(leave empty to auto-generate)",
            default="",
        ).ask()
        if key_card_str is None:
            sys.exit(0)
        key_card = key_card_str.strip() if key_card_str.strip() else None

        ps_str = questionary.text(
            "Prompt strength:",
            instruction="(0.0-1.0, lower = closer to key card)",
            default="0.47",
        ).ask()
        if ps_str is None:
            sys.exit(0)
        prompt_strength = float(ps_str) if ps_str.strip() else 0.47

    cards_file_str = questionary.text(
        "Custom cards YAML file:",
        instruction="(leave empty for built-in cards)",
        default="",
    ).ask()
    if cards_file_str is None:
        sys.exit(0)
    cards_file = cards_file_str.strip() if cards_file_str.strip() else None

    return {
        "style": style,
        "model": model,
        "card_subset": cards,
        "aspect_ratio": aspect_ratio,
        "output": Path(output),
        "seed": seed,
        "parallel": parallel,
        "key_card": Path(key_card) if key_card else None,
        "prompt_strength": prompt_strength,
        "style_transfer_mode": style_transfer_mode,
        "cards_file": Path(cards_file) if cards_file else None,
    }


def archive_output(output: Path) -> Path | None:
    """Move existing output contents to output-logs/<timestamp>/.

    Returns the archive path if files were moved, None otherwise.
    """
    if not output.exists():
        return None

    # Check if there are any files to archive
    files = list(output.iterdir())
    if not files:
        return None

    # Create timestamped archive folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = LOGS_DIR / timestamp
    archive_path.mkdir(parents=True, exist_ok=True)

    # Move all files from output to archive
    for item in files:
        shutil.move(str(item), str(archive_path / item.name))

    return archive_path


def save_prompt_file(output: Path, options: dict) -> Path:
    """Save generation options to prompt.txt in the output folder."""
    output.mkdir(parents=True, exist_ok=True)
    prompt_path = output / "prompt.txt"

    lines = [
        f"Style: {options['style']}",
        f"Model: {options['model']}",
        f"Cards: {options['card_subset']}",
        f"Aspect Ratio: {options['aspect_ratio']}",
        f"Seed: {options['seed']}",
        f"Parallel: {options['parallel']}",
    ]
    if options.get('key_card'):
        lines.append(f"Key Card: {options['key_card']}")
    if options.get('model') == 'sdxl':
        lines.append(f"Prompt Strength: {options['prompt_strength']}")
    if options.get('model') == 'style-transfer':
        lines.append(f"Style Transfer Mode: {options['style_transfer_mode']}")
    if options.get('cards_file'):
        lines.append(f"Cards File: {options['cards_file']}")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    prompt_path.write_text("\n".join(lines))
    return prompt_path


def run_generation(
    style: str,
    model: str,
    output: Path,
    card_subset: str,
    seed: int,
    parallel: int,
    key_card: Path | None,
    cards_file: Path | None,
    aspect_ratio: str,
    prompt_strength: float,
    style_transfer_mode: str,
) -> None:
    """Execute the deck generation with the given options."""
    # Archive existing output if present
    archive_path = archive_output(output)
    if archive_path:
        console.print(f"[yellow]Archived previous output to:[/yellow] {archive_path}")

    # Build options dict for saving
    options = {
        "style": style,
        "model": model,
        "card_subset": card_subset,
        "aspect_ratio": aspect_ratio,
        "seed": seed,
        "parallel": parallel,
        "key_card": key_card,
        "prompt_strength": prompt_strength,
        "style_transfer_mode": style_transfer_mode,
        "cards_file": cards_file,
    }

    # Save prompt.txt before generation
    save_prompt_file(output, options)

    cards = get_cards(card_subset, cards_file=cards_file)
    console.print()
    console.print(f"[bold]Generating {len(cards)} tarot cards[/bold]")
    console.print(f"  Style:  {style}")
    console.print(f"  Model:  {model}")
    console.print(f"  Output: {output.resolve()}")
    console.print(f"  Seed:   {seed}")
    console.print(f"  Aspect: {aspect_ratio}")
    if key_card:
        console.print(f"  Key card: {key_card}")
    if model == "sdxl":
        console.print(f"  Prompt strength: {prompt_strength}")
    if model == "style-transfer":
        console.print(f"  Style transfer mode: {style_transfer_mode}")
    if cards_file:
        console.print(f"  Cards file: {cards_file.resolve()}")
    console.print()

    paths = generate_deck(
        cards=cards,
        style=style,
        model=model,
        output_dir=output,
        base_seed=seed,
        parallel=parallel,
        key_card_path=str(key_card) if key_card else None,
        aspect_ratio=aspect_ratio,
        prompt_strength=prompt_strength,
        style_transfer_mode=style_transfer_mode,
    )

    console.print(f"\n[bold green]Done![/bold green] Generated {len(paths)} images in {output.resolve()}")


def main() -> None:
    """Generate a complete tarot deck with a consistent art style."""
    options = prompt_for_options()
    run_generation(**options)


if __name__ == "__main__":
    main()
