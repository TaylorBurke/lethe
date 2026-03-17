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

# Map card group to reference base name in references/ directory.
# Suit "Pentacles" maps to "coins" to match the traditional name.
# Actual file may be .png, .jpg, or .jpeg — resolved at lookup time.
REFERENCE_FILES = {
    "major": "major",
    "Wands": "wands",
    "Cups": "cups",
    "Swords": "swords",
    "Pentacles": "coins",
}


def _reference_key(card: Card) -> str:
    """Return the reference map key for a card (arcana_type for major, suit for minor)."""
    if card.arcana_type == "major":
        return "major"
    return card.suit


def _load_rw_ref(rw_dir: Path, card: Card) -> str | None:
    """Encode the Rider-Waite reference image for *card* as a base64 data URI.

    Looks for ``{rw_dir}/{card.numeral}{ext}`` for each supported extension.
    Returns None if no matching file is found.
    """
    for ext in _IMAGE_EXTENSIONS:
        p = rw_dir / f"{card.numeral}{ext}"
        if p.exists():
            data = p.read_bytes()
            encoded = base64.b64encode(data).decode()
            mime = "jpeg" if ext in (".jpg", ".jpeg") else "png"
            return f"data:image/{mime};base64,{encoded}"
    return None


from tarot_gen.prompts import build_prompt, build_img2img_prompt, build_negative_prompt
from tarot_gen.consistency import get_seed, build_style_prefix, build_sdxl_img2img_input, resize_image_to_aspect

MODELS = {
    "flux-schnell": "black-forest-labs/flux-schnell",
    "flux-img2img": "black-forest-labs/flux-dev",
    "sdxl": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
    "style-transfer": "fofr/style-transfer:f1023890703bc0a5a3a2c21b5e498833be5f6ef6e70e9daf6b9b3a4fd8309cf0",
}

_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg")

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


def _run_model(model_id: str, input_data: dict, _max_retries: int = 5) -> list[str]:
    """Run a model via the Replicate HTTP API and return output URLs.

    Retries with exponential backoff on 429 (rate limit) responses.
    """
    headers = _api_headers()

    for attempt in range(_max_retries):
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

        if resp.status_code == 429:
            wait = 2 ** attempt * 5  # 5s, 10s, 20s, 40s, 80s
            console.print(f"[yellow]Rate limited (429). Retrying in {wait}s...[/yellow]")
            time.sleep(wait)
            continue

        resp.raise_for_status()
        break
    else:
        # All retries exhausted
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
    is_flux_dev = "flux-dev" in model_id
    is_flux = "flux" in model_id

    # For flux img2img the reference image carries the composition — use style only.
    if is_flux_dev and key_card_url:
        prompt = build_img2img_prompt(style)
    else:
        prompt = build_prompt(card, style)
    negative = build_negative_prompt()
    if deck_num is not None:
        dest = output_dir / f"{card.numeral}_{card.slug}_{deck_num}.png"
    else:
        dest = output_dir / card.filename

    console.print(f"[dim]Prompt: {prompt}[/dim]")
    console.print(f"[dim]Negative: {negative}[/dim]")
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
            elif is_flux_dev and key_card_url:
                console.print(f"[bold magenta]Flux img2img prompt_strength={prompt_strength}[/bold magenta]")
                input_data = {
                    "prompt": prompt,
                    "image": key_card_url,
                    "prompt_strength": prompt_strength,
                    "seed": seed,
                    "num_outputs": 1,
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
    rw_dir: Path | None = None,
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
            if rw_dir is not None:
                ref = _load_rw_ref(rw_dir, card)
                if ref is None:
                    console.print(f"[yellow]No RW reference found for {card.name} ({card.numeral}) — generating without reference[/yellow]")
                return ref
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
    rw_dir: Path | None = None,
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

    is_flux_dev = "flux-dev" in model_id
    is_flux = "flux" in model_id
    is_style_transfer = "style-transfer" in model_id
    is_sdxl = not is_flux and not is_style_transfer
    key_card_url: str | None = None

    # Reference setup
    reference_paths: dict[str, Path] = {}
    if is_flux_dev and rw_dir is not None:
        key_card_url = _load_rw_ref(rw_dir, card)
        if key_card_url is None:
            console.print(f"[yellow]No RW reference found for {card.name} ({card.numeral}) — generating without reference[/yellow]")
    elif is_style_transfer:
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


def _card_target_dimensions(aspect_ratio: str) -> tuple[int, int]:
    """Return (width, height) in pixels for a given aspect ratio string."""
    if aspect_ratio in SDXL_DIMENSIONS:
        return SDXL_DIMENSIONS[aspect_ratio]
    # "WxH" literal (e.g. "300x575")
    if "x" in aspect_ratio and ":" not in aspect_ratio:
        w_str, h_str = aspect_ratio.split("x", 1)
        return int(w_str), int(h_str)
    # "W:H" ratio — scale to ~768px wide
    if ":" in aspect_ratio:
        w_r, h_r = (int(x) for x in aspect_ratio.split(":"))
        base = 768
        return base, int(base * h_r / w_r)
    return 768, 1152


def _assemble_tile_grid(tile_path: Path, density: int, target_width: int, target_height: int, dest: Path) -> None:
    """Assemble a seamless tile into a card-sized image.

    Resizes *tile_path* to (target_width // density) square, then repeats it
    to fill *target_width* × *target_height*, saving the result to *dest*.
    """
    tile_img = Image.open(tile_path).convert("RGB")
    tile_size = max(1, target_width // density)
    tile_resized = tile_img.resize((tile_size, tile_size), Image.LANCZOS)
    result = Image.new("RGB", (target_width, target_height))
    for y in range(0, target_height, tile_size):
        for x in range(0, target_width, tile_size):
            result.paste(tile_resized, (x, y))
    result.save(dest, format="PNG")


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
    cardback_style: str = "4-way-symmetry",
    tile_density: int = 3,
) -> Path:
    """Generate a card back image.

    Uses the same model and style as the deck, with a prompt focused on the
    chosen design style. Post-processing options:
    - "4-way-symmetry": mirrors the top-left quadrant for a mandala effect
    - "tile": generates a seamless square tile then assembles it at the
      given density across the final card dimensions
    - "none": uses the raw model output
    """
    model_id = MODELS.get(model, model)
    output_dir.mkdir(parents=True, exist_ok=True)
    style_prefix = build_style_prefix(style)
    if deck_num is not None:
        dest = output_dir / f"{card_count:02d}_card_back_{deck_num}.png"
    else:
        dest = output_dir / f"{card_count:02d}_card_back.png"
    seed = get_seed(base_seed, 999)

    # For tile mode we generate a square tile then assemble; track separately.
    is_tile = cardback_style == "tile"
    tile_path = dest.with_stem(dest.stem + "_tile") if is_tile else None

    if cardback_style == "4-way-symmetry":
        prompt = (
            f"{style_prefix}, ornamental symmetrical pattern, decorative card back design, "
            "intricate mandala, geometric tilework, no text, no figures, no faces, no characters, "
            "full bleed illustration extending to all edges, no border, no frame, seamless edge-to-edge artwork"
        )
    elif is_tile:
        prompt = (
            f"{style_prefix}, seamless tileable texture, decorative pattern, "
            "top edge connects to bottom edge, left edge connects to right edge, "
            "perfectly seamless repeat, no text, no figures, no faces, no characters, no border, no frame"
        )
    else:
        prompt = (
            f"{style_prefix}, decorative card back design, ornamental pattern, "
            "no text, no figures, no faces, no characters, "
            "full bleed illustration extending to all edges, no border, no frame"
        )
    negative = build_negative_prompt()

    console.print("[bold cyan]Generating card back...[/bold cyan]")
    console.print(f"[dim]Prompt: {prompt}[/dim]")

    is_flux = "flux" in model_id
    is_style_transfer = "style-transfer" in model_id

    # Tile mode: generate at 1:1 so we get a clean square tile to assemble.
    gen_aspect = "1:1" if is_tile else aspect_ratio

    ref_url: str | None = None
    if is_style_transfer:
        ref_dims = (1024, 1024) if is_tile else SDXL_DIMENSIONS.get(aspect_ratio, (768, 1152))
        ref_path = None
        if reference_map:
            ref_path = Path(reference_map.get("major") or next(iter(reference_map.values())))
        elif key_card_path:
            ref_path = Path(key_card_path)
        if ref_path:
            card_back_seed = get_seed(base_seed, 999)
            resized_bytes = resize_image_to_aspect(
                ref_path, ref_dims[0], ref_dims[1],
                card_seed=card_back_seed, diversity=diversity,
            )
            encoded = base64.b64encode(resized_bytes).decode()
            ref_url = f"data:image/png;base64,{encoded}"

    if is_style_transfer and ref_url:
        gen_w, gen_h = (1024, 1024) if is_tile else SDXL_DIMENSIONS.get(aspect_ratio, (768, 1152))
        input_data = {
            "prompt": prompt,
            "negative_prompt": negative,
            "style_image": ref_url,
            "model": style_transfer_mode,
            "width": gen_w,
            "height": gen_h,
            "seed": seed,
            "number_of_images": 1,
            "output_format": "png",
        }
    elif is_flux:
        input_data = {
            "prompt": prompt,
            "seed": seed,
            "num_outputs": 1,
            "aspect_ratio": gen_aspect,
        }
    else:
        gen_w, gen_h = (1024, 1024) if is_tile else SDXL_DIMENSIONS.get(aspect_ratio, (768, 1152))
        input_data = {
            "prompt": prompt,
            "negative_prompt": negative,
            "seed": seed,
            "width": gen_w,
            "height": gen_h,
            "num_outputs": 1,
        }

    urls = _run_model(model_id, input_data)

    if is_tile:
        _download_image(urls[0], tile_path)
        card_w, card_h = _card_target_dimensions(aspect_ratio)
        console.print(f"[bold cyan]Assembling tile grid (density {tile_density}, {card_w}×{card_h})...[/bold cyan]")
        _assemble_tile_grid(tile_path, tile_density, card_w, card_h, dest)
    else:
        _download_image(urls[0], dest)
        if cardback_style == "4-way-symmetry":
            console.print("[bold cyan]Applying 4-way symmetry mirror...[/bold cyan]")
            _mirror_4way(dest)

    console.print(f"[bold green]Card back ready:[/bold green] {dest}")
    return dest
