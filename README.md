# AI Tarot Deck Generator

Python CLI tool that generates a complete 78-card tarot deck using Replicate's API (SDXL/Flux models), with style consistency across all cards.

## Project Structure

```
tarot-gen/
├── tarot_gen/
│   ├── __init__.py
│   ├── __main__.py        # python -m tarot_gen entry point
│   ├── cli.py             # Click-based CLI
│   ├── cards.py           # Card dataclass + YAML loader
│   ├── prompts.py         # Prompt template builder
│   ├── generator.py       # Replicate API client + generation logic
│   └── consistency.py     # Seed derivation + style prefix for consistency
├── cards.yaml             # Customizable card definitions (descriptions, symbols, composition)
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
# Generate sample cards (17 representative cards) for quick iteration
python -m tarot_gen "watercolor botanical" --cards sample --seed 42

# Generate 22 Major Arcana cards
python -m tarot_gen "dark gothic ink wash style" --cards major

# Generate full 78-card deck with SDXL, 4 concurrent API calls
python -m tarot_gen "dark gothic ink wash style" --model sdxl --parallel 4 --output ./my-deck

# Use custom card definitions from a YAML file
python -m tarot_gen "art nouveau gold leaf" --cards-file ./my-cards.yaml --cards major

# Use a custom reference image as the style key card (SDXL)
python -m tarot_gen "art nouveau gold leaf" --model sdxl --key-card ./my-ref.png --cards major
```

### Options

| Option | Default | Description |
|---|---|---|
| `STYLE` (argument) | *required* | Art style prompt, e.g. `"dark gothic ink wash style"` |
| `--model` | `flux-schnell` | Model to use (`flux-schnell` or `sdxl`) |
| `--output` | `./output` | Output directory for generated images |
| `--cards` | `all` | Card subset: `all`, `major`, `minor`, or `sample` |
| `--seed` | `42` | Base seed for reproducibility |
| `--parallel` | `1` | Number of concurrent API calls |
| `--key-card` | *none* | Path to a reference image for style transfer (SDXL only) |
| `--cards-file` | *none* | Path to a YAML file with custom card definitions |

## Customizing Cards

Card definitions are stored in `cards.yaml`. Each card has:

- **description** — Scene/imagery description for the card
- **key_symbols** — List of visual elements to emphasize
- **composition** — Framing and layout hints (figure placement, camera angle, etc.)

Example:
```yaml
- name: The Fool
  numeral: "00"
  description: A young traveler at cliff's edge with a small dog, about to step into the unknown
  key_symbols: [cliff, knapsack, white rose, small dog]
  composition: full-body figure in profile facing right, standing at cliff edge, dog at feet, sky background
```

Edit this file to customize card imagery, then run with `--cards-file cards.yaml`.

## How It Works

- **cards.py** — Defines the Card dataclass and loads definitions from YAML (or falls back to built-in defaults).
- **prompts.py** — Combines the user's style prompt with each card's description, symbols, and composition hints into a structured image generation prompt. Images are generated without borders, with content that has breathing room from the edges.
- **consistency.py** — Wraps the style in a structured consistency prefix, derives deterministic per-card seeds from a base seed, and builds SDXL img2img inputs for key-card-based style transfer.
- **generator.py** — Calls the Replicate API with retry logic, downloads images, and shows a progress bar. Supports sequential or parallel generation. For SDXL, the first card is generated as a "key card" and used as an img2img reference for all subsequent cards to improve style consistency. A custom key card image can be supplied via `--key-card`.
