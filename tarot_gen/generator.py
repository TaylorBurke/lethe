"""Replicate API client and image generation logic."""

from __future__ import annotations

import os
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, MofNCompleteColumn

from tarot_gen.cards import Card
from tarot_gen.prompts import build_prompt, build_negative_prompt
from tarot_gen.consistency import get_seed, build_style_prefix

MODELS = {
    "flux-schnell": "black-forest-labs/flux-schnell",
    "sdxl": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
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
    max_retries: int = 5,
) -> Path:
    """Generate a single card image via Replicate, with retries."""
    prompt = build_prompt(card, style)
    negative = build_negative_prompt()
    dest = output_dir / card.filename

    is_flux = "flux" in model_id

    for attempt in range(1, max_retries + 1):
        try:
            if is_flux:
                input_data = {
                    "prompt": prompt,
                    "seed": seed,
                    "num_outputs": 1,
                    "aspect_ratio": "2:3",
                }
            else:
                input_data = {
                    "prompt": prompt,
                    "negative_prompt": negative,
                    "seed": seed,
                    "width": 768,
                    "height": 1152,
                    "num_outputs": 1,
                }

            urls = _run_model(model_id, input_data)
            _download_image(urls[0], dest)
            return dest

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
) -> list[Path]:
    """Generate images for all cards in the list."""
    model_id = MODELS.get(model, model)
    output_dir.mkdir(parents=True, exist_ok=True)
    style_prefix = build_style_prefix(style)
    results: list[Path] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Generating tarot deck", total=len(cards))

        if parallel <= 1:
            for i, card in enumerate(cards):
                seed = get_seed(base_seed, i)
                path = _generate_one(card, style_prefix, model_id, seed, output_dir)
                results.append(path)
                progress.update(task, advance=1, description=f"Generated {card.name}")
        else:
            futures = {}
            with ThreadPoolExecutor(max_workers=parallel) as pool:
                for i, card in enumerate(cards):
                    seed = get_seed(base_seed, i)
                    fut = pool.submit(_generate_one, card, style_prefix, model_id, seed, output_dir)
                    futures[fut] = card

                for fut in as_completed(futures):
                    card = futures[fut]
                    path = fut.result()
                    results.append(path)
                    progress.update(task, advance=1, description=f"Generated {card.name}")

    return results
