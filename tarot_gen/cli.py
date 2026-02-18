"""CLI entry point for tarot deck generator."""

import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import questionary
from rich.console import Console

from tarot_gen.cards import Card, get_cards, get_card_by_index
from tarot_gen.generator import generate_deck, generate_single_card, generate_card_back, MODELS, STYLE_TRANSFER_MODES, REFERENCE_FILES

console = Console()
LOGS_DIR = Path("output-logs")

ASPECT_RATIOS = ["11:19", "300x575", "2:3", "3:2", "1:1", "16:9", "9:16", "4:5", "5:4", "21:9", "9:21"]
CARD_SUBSETS = ["sample", "major", "minor", "all", "single"]


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

    # Single-card mode options
    single_card_index = None
    single_card_count = 1
    single_card_desc = None
    single_card_symbols = None
    single_card_composition = None

    if cards == "single":
        idx_str = questionary.text(
            "Card index (0-78):",
            instruction="(0-77 for cards, 78 for card back)",
        ).ask()
        if idx_str is None:
            sys.exit(0)
        try:
            single_card_index = int(idx_str.strip())
        except ValueError:
            console.print("[red]Invalid index. Must be an integer 0-78.[/red]")
            sys.exit(1)
        if single_card_index < 0 or single_card_index > 78:
            console.print("[red]Index must be between 0 and 78.[/red]")
            sys.exit(1)

        # Show card name for confirmation (skip for card back)
        if single_card_index < 78:
            # Peek at the card name (cards_file not known yet, use built-in)
            try:
                preview_card = get_card_by_index(single_card_index)
                console.print(f"[bold cyan]Selected: {preview_card.name}[/bold cyan]")
            except ValueError:
                pass

            use_default = questionary.confirm(
                "Use default description?",
                default=True,
            ).ask()
            if use_default is None:
                sys.exit(0)

            if not use_default:
                single_card_desc = questionary.text("Description:").ask()
                if single_card_desc is None:
                    sys.exit(0)

                symbols_str = questionary.text(
                    "Key symbols:",
                    instruction="(comma-separated)",
                ).ask()
                if symbols_str is None:
                    sys.exit(0)
                single_card_symbols = [s.strip() for s in symbols_str.split(",") if s.strip()]

                single_card_composition = questionary.text("Composition:").ask()
                if single_card_composition is None:
                    sys.exit(0)
        else:
            console.print("[bold cyan]Selected: Card Back[/bold cyan]")

        count_str = questionary.text(
            "Number of copies (1-20):",
            default="1",
        ).ask()
        if count_str is None:
            sys.exit(0)
        try:
            single_card_count = int(count_str.strip())
        except ValueError:
            console.print("[red]Invalid count. Must be an integer 1-20.[/red]")
            sys.exit(1)
        if single_card_count < 1 or single_card_count > 20:
            console.print("[red]Count must be between 1 and 20.[/red]")
            sys.exit(1)

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

    num_decks = questionary.select(
        "Number of decks to generate:",
        choices=[
            questionary.Choice("1", value=1),
            questionary.Choice("2", value=2),
            questionary.Choice("3", value=3),
            questionary.Choice("4", value=4),
            questionary.Choice("5", value=5),
        ],
        default=1,
    ).ask()
    if num_decks is None:
        sys.exit(0)

    # Model-specific options
    key_card = None
    prompt_strength = 0.47
    style_transfer_mode = "high-quality"

    reference_map = None
    if model == "style-transfer":
        ref_count = questionary.select(
            "Reference images:",
            choices=[
                questionary.Choice("1 image (my-ref.png)", value="1"),
                questionary.Choice("5 images (per-group from references/)", value="5"),
            ],
            default="5",
        ).ask()
        if ref_count is None:
            sys.exit(0)

        if ref_count == "1":
            ref_path = Path("my-ref.png")
            if not ref_path.exists():
                console.print("[red]my-ref.png not found in project root.[/red]")
                sys.exit(1)
            key_card = str(ref_path)
            console.print(f"[bold cyan]Using single reference image: my-ref.png[/bold cyan]")
        else:
            # Build reference map from references/ directory
            ref_dir = Path("references")
            reference_map = {}
            for group_key, filename in REFERENCE_FILES.items():
                ref_path = ref_dir / filename
                if ref_path.exists():
                    reference_map[group_key] = str(ref_path)
            if reference_map:
                console.print(f"[bold cyan]Using {len(reference_map)} reference images from references/[/bold cyan]")
            else:
                console.print("[red]No reference images found in references/ directory.[/red]")
                console.print(f"[red]Expected files: {', '.join(REFERENCE_FILES.values())}[/red]")
                sys.exit(1)

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
        "num_decks": num_decks,
        "key_card": Path(key_card) if key_card else None,
        "prompt_strength": prompt_strength,
        "style_transfer_mode": style_transfer_mode,
        "cards_file": Path(cards_file) if cards_file else None,
        "reference_map": reference_map,
        "single_card_index": single_card_index,
        "single_card_count": single_card_count,
        "single_card_desc": single_card_desc,
        "single_card_symbols": single_card_symbols,
        "single_card_composition": single_card_composition,
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
        f"Decks: {options.get('num_decks', 1)}",
    ]
    if options.get('key_card'):
        lines.append(f"Key Card: {options['key_card']}")
    if options.get('model') == 'sdxl':
        lines.append(f"Prompt Strength: {options['prompt_strength']}")
    if options.get('model') == 'style-transfer':
        lines.append(f"Style Transfer Mode: {options['style_transfer_mode']}")
    if options.get('cards_file'):
        lines.append(f"Cards File: {options['cards_file']}")
    if options.get('single_card_index') is not None:
        lines.append(f"Single Card Index: {options['single_card_index']}")
        lines.append(f"Copies: {options.get('single_card_count', 1)}")
        if options.get('single_card_desc'):
            lines.append(f"Custom Description: {options['single_card_desc']}")
        if options.get('single_card_symbols'):
            lines.append(f"Custom Symbols: {', '.join(options['single_card_symbols'])}")
        if options.get('single_card_composition'):
            lines.append(f"Custom Composition: {options['single_card_composition']}")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    prompt_path.write_text("\n".join(lines))
    return prompt_path


def _generate_single_deck(
    deck_num: int | None,
    cards: list,
    style: str,
    model: str,
    output: Path,
    seed: int,
    parallel: int,
    key_card: Path | None,
    aspect_ratio: str,
    prompt_strength: float,
    style_transfer_mode: str,
    reference_map: dict[str, str] | None,
) -> list[Path]:
    """Generate one complete deck (cards + card back).

    When ``deck_num`` is set, filenames are suffixed (e.g. ``00_the_fool_2.png``)
    and the seed is offset so each deck produces unique images.
    """
    deck_seed = seed if deck_num is None else seed + (deck_num - 1) * 1000

    paths = generate_deck(
        cards=cards,
        style=style,
        model=model,
        output_dir=output,
        base_seed=deck_seed,
        parallel=parallel,
        key_card_path=str(key_card) if key_card else None,
        aspect_ratio=aspect_ratio,
        prompt_strength=prompt_strength,
        style_transfer_mode=style_transfer_mode,
        reference_map=reference_map,
        deck_num=deck_num,
    )

    card_back_path = generate_card_back(
        style=style,
        model=model,
        output_dir=output,
        base_seed=deck_seed,
        key_card_path=str(key_card) if key_card else None,
        aspect_ratio=aspect_ratio,
        style_transfer_mode=style_transfer_mode,
        reference_map=reference_map,
        deck_num=deck_num,
    )
    paths.append(card_back_path)
    return paths


def run_generation(
    style: str,
    model: str,
    output: Path,
    card_subset: str,
    seed: int,
    parallel: int,
    num_decks: int,
    key_card: Path | None,
    cards_file: Path | None,
    aspect_ratio: str,
    prompt_strength: float,
    style_transfer_mode: str,
    reference_map: dict[str, str] | None = None,
    single_card_index: int | None = None,
    single_card_count: int = 1,
    single_card_desc: str | None = None,
    single_card_symbols: list[str] | None = None,
    single_card_composition: str | None = None,
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
        "num_decks": num_decks,
        "key_card": key_card,
        "prompt_strength": prompt_strength,
        "style_transfer_mode": style_transfer_mode,
        "cards_file": cards_file,
        "single_card_index": single_card_index,
        "single_card_count": single_card_count,
        "single_card_desc": single_card_desc,
        "single_card_symbols": single_card_symbols,
        "single_card_composition": single_card_composition,
    }

    # Save prompt.txt before generation
    save_prompt_file(output, options)

    # --- Single card mode ---
    if card_subset == "single" and single_card_index is not None:
        is_card_back = single_card_index == 78

        console.print()
        if is_card_back:
            console.print(f"[bold]Generating {single_card_count} card back copy/copies[/bold]")
        else:
            card = get_card_by_index(single_card_index, cards_file=cards_file)
            # Apply custom description overrides
            if single_card_desc is not None:
                card = Card(
                    name=card.name,
                    numeral=card.numeral,
                    arcana_type=card.arcana_type,
                    suit=card.suit,
                    description=single_card_desc,
                    key_symbols=single_card_symbols or card.key_symbols,
                    composition=single_card_composition or card.composition,
                )
            console.print(f"[bold]Generating {single_card_count} copy/copies of {card.name}[/bold]")

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

        all_paths: list[Path] = []

        if is_card_back:
            for i in range(single_card_count):
                copy_seed = seed + i * 100
                copy_num = (i + 1) if single_card_count > 1 else None
                path = generate_card_back(
                    style=style,
                    model=model,
                    output_dir=output,
                    base_seed=copy_seed,
                    key_card_path=str(key_card) if key_card else None,
                    aspect_ratio=aspect_ratio,
                    style_transfer_mode=style_transfer_mode,
                    reference_map=reference_map,
                    deck_num=copy_num,
                )
                all_paths.append(path)
        else:
            all_paths = generate_single_card(
                card=card,
                style=style,
                model=model,
                output_dir=output,
                base_seed=seed,
                count=single_card_count,
                key_card_path=str(key_card) if key_card else None,
                aspect_ratio=aspect_ratio,
                prompt_strength=prompt_strength,
                style_transfer_mode=style_transfer_mode,
                reference_map=reference_map,
            )

        console.print(f"\n[bold green]Done![/bold green] Generated {len(all_paths)} images in {output.resolve()}")
        return

    # --- Normal deck mode ---
    cards = get_cards(card_subset, cards_file=cards_file)
    console.print()
    console.print(f"[bold]Generating {len(cards)} tarot cards × {num_decks} deck(s)[/bold]")
    console.print(f"  Style:  {style}")
    console.print(f"  Model:  {model}")
    console.print(f"  Output: {output.resolve()}")
    console.print(f"  Seed:   {seed}")
    console.print(f"  Aspect: {aspect_ratio}")
    console.print(f"  Decks:  {num_decks}")
    if key_card:
        console.print(f"  Key card: {key_card}")
    if model == "sdxl":
        console.print(f"  Prompt strength: {prompt_strength}")
    if model == "style-transfer":
        console.print(f"  Style transfer mode: {style_transfer_mode}")
    if cards_file:
        console.print(f"  Cards file: {cards_file.resolve()}")
    console.print()

    all_paths: list[Path] = []

    if num_decks <= 1:
        # Single deck — no filename suffix
        all_paths = _generate_single_deck(
            deck_num=None,
            cards=cards,
            style=style,
            model=model,
            output=output,
            seed=seed,
            parallel=parallel,
            key_card=key_card,
            aspect_ratio=aspect_ratio,
            prompt_strength=prompt_strength,
            style_transfer_mode=style_transfer_mode,
            reference_map=reference_map,
        )
    else:
        # Multiple decks — run concurrently, suffix filenames with deck number
        with ThreadPoolExecutor(max_workers=num_decks) as pool:
            futures = {}
            for d in range(1, num_decks + 1):
                console.print(f"[bold cyan]Launching deck {d}/{num_decks}...[/bold cyan]")
                fut = pool.submit(
                    _generate_single_deck,
                    deck_num=d,
                    cards=cards,
                    style=style,
                    model=model,
                    output=output,
                    seed=seed,
                    parallel=parallel,
                    key_card=key_card,
                    aspect_ratio=aspect_ratio,
                    prompt_strength=prompt_strength,
                    style_transfer_mode=style_transfer_mode,
                    reference_map=reference_map,
                )
                futures[fut] = d

            for fut in as_completed(futures):
                d = futures[fut]
                paths = fut.result()
                all_paths.extend(paths)
                console.print(f"[bold green]Deck {d} complete![/bold green] ({len(paths)} images)")

    console.print(f"\n[bold green]Done![/bold green] Generated {len(all_paths)} images in {output.resolve()}")


def main() -> None:
    """Generate a complete tarot deck with a consistent art style."""
    options = prompt_for_options()
    run_generation(**options)


if __name__ == "__main__":
    main()
