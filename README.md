# AI Tarot Deck Generator

Python CLI tool that generates a complete 78-card tarot deck using Replicate's API (SDXL/Flux models), with style consistency across all cards.

## Project Structure

```
tarot-gen/
├── tarot_gen/
│   ├── __init__.py
│   ├── __main__.py        # python -m tarot_gen entry point
│   ├── cli.py             # Click-based CLI
│   ├── cards.py           # 78 card definitions (22 Major + 56 Minor Arcana)
│   ├── prompts.py         # Prompt template builder
│   ├── generator.py       # Replicate API client + generation logic
│   └── consistency.py     # Seed derivation + style prefix for consistency
├── output/                # Default output directory
├── pyproject.toml
└── README.md
```

## Setup

```bash
pip install -e .
```

Requires a `REPLICATE_API_TOKEN` environment variable:

```bash
export REPLICATE_API_TOKEN=r8_...
```

## Usage

```bash
# Generate 22 Major Arcana cards in watercolor style
python -m tarot_gen "watercolor botanical" --cards major --seed 42

# Generate full 78-card deck with SDXL, 4 concurrent API calls
python -m tarot_gen "dark gothic ink wash style" --model sdxl --parallel 4 --output ./my-deck

# Use a custom reference image as the style key card (SDXL)
python -m tarot_gen "art nouveau gold leaf" --model sdxl --key-card ./my-ref.png --cards major
```

### Options

| Option | Default | Description |
|---|---|---|
| `STYLE` (argument) | *required* | Art style prompt, e.g. `"dark gothic ink wash style"` |
| `--model` | `flux-schnell` | Model to use (`flux-schnell` or `sdxl`) |
| `--output` | `./output` | Output directory for generated images |
| `--cards` | `all` | Card subset: `all`, `major`, or `minor` |
| `--seed` | `42` | Base seed for reproducibility |
| `--parallel` | `1` | Number of concurrent API calls |
| `--key-card` | *none* | Path to a reference image used as style key card (SDXL only) |

## How It Works

- **cards.py** — Defines all 78 cards as frozen dataclasses with name, numeral, scene description, and key symbols.
- **prompts.py** — Combines the user's style prompt with each card's description and symbols into a structured image generation prompt. Includes a negative prompt to avoid common artifacts.
- **consistency.py** — Wraps the style in a structured consistency prefix, derives deterministic per-card seeds from a base seed, and builds SDXL img2img inputs for key-card-based style transfer.
- **generator.py** — Calls the Replicate API with retry logic, downloads images, and shows a progress bar. Supports sequential or parallel generation. For SDXL, the first card is generated as a "key card" and used as an img2img reference for all subsequent cards to improve style consistency. A custom key card image can be supplied via `--key-card`.
