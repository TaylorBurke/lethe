"""Replicate API client and image generation logic."""

from __future__ import annotations

import base64
import os
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from PIL import Image
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, MofNCompleteColumn

from tarot_gen.cards import Card

# Map card group to reference filename in references/ directory.
# Suit "Pentacles" maps to "coins.png" to match the traditional name.
REFERENCE_FILES = {
    "major": "major.png",
    "Wands": "wands.png",
    "Cups": "cups.png",
    "Swords": "swords.png",
    "Pentacles": "coins.png",
}


def _reference_key(card: Card) -> str:
    """Return the reference map key for a card (arcana_type for major, suit for minor)."""
    if card.arcana_type == "major":
        return "major"
    return card.suit
from tarot_gen.prompts import build_prompt, build_negative_prompt
from tarot_gen.consistency import get_seed, build_style_prefix, build_sdxl_img2img_input, resize_image_to_aspect

MODELS = {
    "flux-schnell": "black-forest-labs/flux-schnell",
    "sdxl": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
    "style-transfer": "fofr/style-transfer:f1023890703bc0a5a3a2c21b5e498833be5f6ef6e70e9daf6b9b3a4fd8309cf0",
}

STYLE_TRANSFER_MODES = ["fast", "high-quality", "realistic", "cinematic", "animated"]

# SDXL dimension mappings for each aspect ratio (width, height)
SDXL_DIMENSIONS = {
    "1:1": (1024, 1024),
    "16:9": (1344, 768),
    "9:16": (768, 1344),
    "2:3": (768, 1152),
    "3:2": (1152, 768),
    "4:5": (896, 1120),
    "5:4": (1120, 896),
    "21:9": (1536, 640),
    "9:21": (640, 1536),
}

API_BASE = "https://api.replicate.com/v1"

console = Console()


def _get_token() -> str:
    token = os.environ.get("REPLICATE_API_TOKEN", "")
    if not token:
        raise RuntimeError("REPLICATE_API_TOKEN environment variable is not set.")
    return token


def _api_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_get_token()}",
        "Content-Type": "application/json",
        "Prefer": "wait",
    }


def _download_image(url: str, dest: Path) -> None:
    """Download an image from a URL and save to dest."""
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    dest.write_bytes(resp.content)


def _run_model(model_id: str, input_data: dict) -> list[str]:
    """Run a model via the Replicate HTTP API and return output URLs."""
    headers = _api_headers()

    # For versioned models (owner/name:version), use the predictions endpoint
    if ":" in model_id:
        owner_name, version = model_id.split(":", 1)
        resp = requests.post(
            f"{API_BASE}/predictions",
            headers=headers,
            json={"version": version, "input": input_data},
            timeout=300,
        )
    else:
        # For official models (owner/name), use the models run endpoint
        resp = requests.post(
            f"{API_BASE}/models/{model_id}/predictions",
            headers=headers,
            json={"input": input_data},
            timeout=300,
        )

    resp.raise_for_status()
    data = resp.json()

    # The "Prefer: wait" header makes Replicate block until done,
    # but if status isn't succeeded we need to poll.
    while data.get("status") not in ("succeeded", "failed", "canceled"):
        time.sleep(2)
        poll = requests.get(data["urls"]["get"], headers=_api_headers(), timeout=30)
        poll.raise_for_status()
        data = poll.json()

    if data["status"] != "succeeded":
        raise RuntimeError(f"Prediction failed: {data.get('error', 'unknown error')}")

    output = data["output"]
    if isinstance(output, list):
        return [str(u) for u in output]
    return [str(output)]


def _generate_one(
    card: Card,
    style: str,
    model_id: str,
    seed: int,
    output_dir: Path,
    key_card_url: str | None = None,
    aspect_ratio: str = "2:3",
    prompt_strength: float = 0.47,
    style_transfer_mode: str = "high-quality",
    max_retries: int = 5,
    deck_num: int | None = None,
) -> tuple[Path, str]:
    """Generate a single card image via Replicate, with retries.

    Returns a (local_path, output_url) tuple.
    When ``deck_num`` is set, the filename is suffixed (e.g. ``00_the_fool_2.png``).
    """
    prompt = build_prompt(card, style)
    negative = build_negative_prompt()
    if deck_num is not None:
        dest = output_dir / f"{card.numeral}_{card.slug}_{deck_num}.png"
    else:
        dest = output_dir / card.filename

    console.print(f"[dim]Prompt: {prompt}[/dim]")
    console.print(f"[dim]Negative: {negative}[/dim]")

    is_flux = "flux" in model_id
    is_style_transfer = "style-transfer" in model_id
    is_sdxl = not is_flux and not is_style_transfer

    for attempt in range(1, max_retries + 1):
        try:
            if is_style_transfer and key_card_url:
                console.print(f"[bold magenta]Using style-transfer with mode={style_transfer_mode}[/bold magenta]")
                width, height = SDXL_DIMENSIONS.get(aspect_ratio, (768, 1152))
                input_data = {
                    "prompt": prompt,
                    "negative_prompt": negative,
                    "style_image": key_card_url,
                    "model": style_transfer_mode,
                    "width": width,
                    "height": height,
                    "seed": seed,
                    "number_of_images": 1,
                    "output_format": "png",
                }
            elif is_sdxl and key_card_url:
                console.print(f"[bold magenta]Using img2img with prompt_strength={prompt_strength} from key card[/bold magenta]")
                width, height = SDXL_DIMENSIONS.get(aspect_ratio, (768, 1152))
                input_data = build_sdxl_img2img_input(
                    prompt=prompt,
                    negative_prompt=negative,
                    seed=seed,
                    image_url=key_card_url,
                    width=width,
                    height=height,
                    prompt_strength=prompt_strength,
                )
                console.print(f"[dim]img2img input has 'image' key: {'image' in input_data}[/dim]")
            elif is_flux:
                input_data = {
                    "prompt": prompt,
                    "seed": seed,
                    "num_outputs": 1,
                    "aspect_ratio": aspect_ratio,
                }
            else:
                width, height = SDXL_DIMENSIONS.get(aspect_ratio, (768, 1152))
                input_data = {
                    "prompt": prompt,
                    "negative_prompt": negative,
                    "seed": seed,
                    "width": width,
                    "height": height,
                    "num_outputs": 1,
                }

            urls = _run_model(model_id, input_data)
            _download_image(urls[0], dest)
            return dest, urls[0]

        except Exception as exc:
            if attempt == max_retries:
                raise RuntimeError(
                    f"Failed to generate {card.name} after {max_retries} attempts: {exc}"
                ) from exc
            is_rate_limit = "429" in str(exc)
            delay = 60 if is_rate_limit else 2 ** attempt
            console.print(f"[yellow]Retry {attempt}/{max_retries} for {card.name} "
                          f"(waiting {delay}s)...[/yellow]")
            time.sleep(delay)

    raise RuntimeError("Unreachable")


def generate_deck(
    cards: list[Card],
    style: str,
    model: str = "flux-schnell",
    output_dir: Path = Path("output"),
    base_seed: int = 42,
    parallel: int = 1,
    key_card_path: str | None = None,
    aspect_ratio: str = "2:3",
    prompt_strength: float = 0.47,
    style_transfer_mode: str = "high-quality",
    reference_map: dict[str, str] | None = None,
    diversity: str = "medium",
    deck_num: int | None = None,
) -> list[Path]:
    """Generate images for all cards in the list.

    For SDXL, the first card (The Fool) is generated as a key card whose
    output URL is fed to all subsequent cards via img2img.  If
    ``key_card_path`` is supplied, that image is used as the reference
    instead of auto-generating one.

    For style-transfer, provide ``reference_map`` (a dict mapping group
    keys like ``"major"``, ``"Wands"``, etc. to image file paths) to use
    per-group reference images.  Falls back to ``key_card_path`` as a
    single reference for all cards.

    ``diversity`` controls how much the reference crop varies per card:
    ``"low"``, ``"medium"``, or ``"high"``.
    """
    model_id = MODELS.get(model, model)
    output_dir.mkdir(parents=True, exist_ok=True)
    style_prefix = build_style_prefix(style)
    results: list[Path] = []

    is_flux = "flux" in model_id
    is_style_transfer = "style-transfer" in model_id
    is_sdxl = not is_flux and not is_style_transfer
    key_card_url: str | None = None

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

    # Resolve the key card reference for SDXL
    elif is_sdxl:
        target_width, target_height = SDXL_DIMENSIONS.get(aspect_ratio, (768, 1152))
        if key_card_path:
            # Resize key card to match target aspect ratio and convert to data URI
            p = Path(key_card_path)
            console.print(f"[bold cyan]Resizing key card to {target_width}x{target_height}...[/bold cyan]")
            resized_bytes = resize_image_to_aspect(p, target_width, target_height)
            encoded = base64.b64encode(resized_bytes).decode()
            key_card_url = f"data:image/png;base64,{encoded}"
            console.print(f"[bold cyan]Using supplied key card:[/bold cyan] {key_card_path}")
        elif cards:
            # Generate The Fool (first card) as key card
            first_card = cards[0]
            seed = get_seed(base_seed, 0)
            console.print(f"[bold cyan]Generating key card:[/bold cyan] {first_card.name}")
            path, key_card_url = _generate_one(
                first_card, style_prefix, model_id, seed, output_dir,
                aspect_ratio=aspect_ratio,
                deck_num=deck_num,
            )
            results.append(path)
            console.print(f"[bold green]Key card ready:[/bold green] {first_card.name}")
            cards = cards[1:]

    remaining_start_index = len(results)

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Generating deck", total=len(cards))

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

        if parallel <= 1:
            for i, card in enumerate(cards):
                seed = get_seed(base_seed, remaining_start_index + i)
                path, _ = _generate_one(
                    card, style_prefix, model_id, seed, output_dir,
                    key_card_url=_resolve_ref(card, seed),
                    aspect_ratio=aspect_ratio,
                    prompt_strength=prompt_strength,
                    style_transfer_mode=style_transfer_mode,
                    deck_num=deck_num,
                )
                results.append(path)
                progress.update(task, advance=1, description=f"Generated {card.name}")
        else:
            futures = {}
            with ThreadPoolExecutor(max_workers=parallel) as pool:
                for i, card in enumerate(cards):
                    seed = get_seed(base_seed, remaining_start_index + i)
                    fut = pool.submit(
                        _generate_one, card, style_prefix, model_id, seed, output_dir,
                        key_card_url=_resolve_ref(card, seed),
                        aspect_ratio=aspect_ratio,
                        prompt_strength=prompt_strength,
                        style_transfer_mode=style_transfer_mode,
                        deck_num=deck_num,
                    )
                    futures[fut] = card

                for fut in as_completed(futures):
                    card = futures[fut]
                    path, _ = fut.result()
                    results.append(path)
                    progress.update(task, advance=1, description=f"Generated {card.name}")

    return results


def generate_single_card(
    card: Card,
    style: str,
    model: str = "flux-schnell",
    output_dir: Path = Path("output"),
    base_seed: int = 42,
    count: int = 1,
    key_card_path: str | None = None,
    aspect_ratio: str = "2:3",
    prompt_strength: float = 0.47,
    style_transfer_mode: str = "high-quality",
    reference_map: dict[str, str] | None = None,
    diversity: str = "medium",
) -> list[Path]:
    """Generate N copies of a single card with varied seeds.

    Each copy uses ``base_seed + i`` as the seed so the outputs differ while
    remaining reproducible.  When ``count > 1``, filenames are suffixed
    (e.g. ``00_the_fool_1.png``, ``00_the_fool_2.png``).

    ``diversity`` controls how much the reference crop varies per card:
    ``"low"``, ``"medium"``, or ``"high"``.
    """
    model_id = MODELS.get(model, model)
    output_dir.mkdir(parents=True, exist_ok=True)
    style_prefix = build_style_prefix(style)
    results: list[Path] = []

    is_flux = "flux" in model_id
    is_style_transfer = "style-transfer" in model_id
    is_sdxl = not is_flux and not is_style_transfer
    key_card_url: str | None = None

    # Reference setup (same logic as generate_deck)
    reference_paths: dict[str, Path] = {}
    if is_style_transfer:
        target_width, target_height = SDXL_DIMENSIONS.get(aspect_ratio, (768, 1152))
        if reference_map:
            for group_key, img_path in reference_map.items():
                reference_paths[group_key] = Path(img_path)
        elif key_card_path:
            reference_paths["_single"] = Path(key_card_path)
        else:
            raise RuntimeError("style-transfer model requires reference images")
    elif is_sdxl and key_card_path:
        target_width, target_height = SDXL_DIMENSIONS.get(aspect_ratio, (768, 1152))
        p = Path(key_card_path)
        resized_bytes = resize_image_to_aspect(p, target_width, target_height)
        encoded = base64.b64encode(resized_bytes).decode()
        key_card_url = f"data:image/png;base64,{encoded}"

    def _resolve_ref(c: Card, card_seed: int) -> str | None:
        if reference_paths:
            ref_key = _reference_key(c) if len(reference_paths) > 1 else "_single"
            ref_path = reference_paths.get(ref_key)
            if ref_path:
                resized = resize_image_to_aspect(
                    ref_path, target_width, target_height,
                    card_seed=card_seed, diversity=diversity,
                )
                encoded = base64.b64encode(resized).decode()
                return f"data:image/png;base64,{encoded}"
        return key_card_url

    console.print(f"[bold]Generating {count} copy/copies of {card.name}[/bold]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(f"Generating {card.name}", total=count)

        for i in range(count):
            seed = base_seed + i
            copy_num = (i + 1) if count > 1 else None
            path, _ = _generate_one(
                card, style_prefix, model_id, seed, output_dir,
                key_card_url=_resolve_ref(card, seed),
                aspect_ratio=aspect_ratio,
                prompt_strength=prompt_strength,
                style_transfer_mode=style_transfer_mode,
                deck_num=copy_num,
            )
            results.append(path)
            progress.update(task, advance=1, description=f"Generated copy {i + 1}/{count}")

    return results


def _mirror_4way(image_path: Path) -> None:
    """Post-process an image for true 4-way symmetry.

    Crops the top-left quadrant, mirrors it horizontally to fill the top half,
    then mirrors the top half vertically to fill the full image. Overwrites
    the file in place.
    """
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    quadrant = img.crop((0, 0, w // 2, h // 2))
    top_half = Image.new("RGB", (w, h // 2))
    top_half.paste(quadrant, (0, 0))
    top_half.paste(quadrant.transpose(Image.FLIP_LEFT_RIGHT), (w // 2, 0))
    full = Image.new("RGB", (w, h))
    full.paste(top_half, (0, 0))
    full.paste(top_half.transpose(Image.FLIP_TOP_BOTTOM), (0, h // 2))
    full.save(image_path, format="PNG")


def generate_card_back(
    style: str,
    model: str,
    output_dir: Path,
    base_seed: int,
    aspect_ratio: str = "11:19",
    key_card_path: str | None = None,
    style_transfer_mode: str = "high-quality",
    reference_map: dict[str, str] | None = None,
    diversity: str = "medium",
    deck_num: int | None = None,
    card_count: int = 78,
) -> Path:
    """Generate a 4-way symmetrical card back image.

    Uses the same model and style as the deck, with a prompt focused on
    ornamental symmetry. The raw output is post-processed with PIL to
    guarantee true 4-way symmetry by mirroring the top-left quadrant.
    """
    model_id = MODELS.get(model, model)
    output_dir.mkdir(parents=True, exist_ok=True)
    style_prefix = build_style_prefix(style)
    if deck_num is not None:
        dest = output_dir / f"{card_count:02d}_card_back_{deck_num}.png"
    else:
        dest = output_dir / f"{card_count:02d}_card_back.png"
    seed = get_seed(base_seed, 999)

    prompt = (
        f"{style_prefix}, ornamental symmetrical pattern, decorative card back design, "
        "intricate mandala, geometric tilework, no text, no figures, no faces, no characters, "
        "full bleed illustration extending to all edges, no border, no frame, seamless edge-to-edge artwork"
    )
    negative = build_negative_prompt()

    console.print("[bold cyan]Generating card back...[/bold cyan]")
    console.print(f"[dim]Prompt: {prompt}[/dim]")

    is_flux = "flux" in model_id
    is_style_transfer = "style-transfer" in model_id

    ref_url: str | None = None
    if is_style_transfer:
        target_width, target_height = SDXL_DIMENSIONS.get(aspect_ratio, (768, 1152))
        ref_path = None
        if reference_map:
            ref_path = Path(reference_map.get("major") or next(iter(reference_map.values())))
        elif key_card_path:
            ref_path = Path(key_card_path)
        if ref_path:
            card_back_seed = get_seed(base_seed, 999)
            resized_bytes = resize_image_to_aspect(
                ref_path, target_width, target_height,
                card_seed=card_back_seed, diversity=diversity,
            )
            encoded = base64.b64encode(resized_bytes).decode()
            ref_url = f"data:image/png;base64,{encoded}"

    if is_style_transfer and ref_url:
        width, height = SDXL_DIMENSIONS.get(aspect_ratio, (768, 1152))
        input_data = {
            "prompt": prompt,
            "negative_prompt": negative,
            "style_image": ref_url,
            "model": style_transfer_mode,
            "width": width,
            "height": height,
            "seed": seed,
            "number_of_images": 1,
            "output_format": "png",
        }
    elif is_flux:
        input_data = {
            "prompt": prompt,
            "seed": seed,
            "num_outputs": 1,
            "aspect_ratio": aspect_ratio,
        }
    else:
        width, height = SDXL_DIMENSIONS.get(aspect_ratio, (768, 1152))
        input_data = {
            "prompt": prompt,
            "negative_prompt": negative,
            "seed": seed,
            "width": width,
            "height": height,
            "num_outputs": 1,
        }

    urls = _run_model(model_id, input_data)
    _download_image(urls[0], dest)

    console.print("[bold cyan]Applying 4-way symmetry mirror...[/bold cyan]")
    _mirror_4way(dest)

    console.print(f"[bold green]Card back ready:[/bold green] {dest}")
    return dest
