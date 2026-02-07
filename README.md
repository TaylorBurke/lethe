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
├── references/            # Style reference images for style-transfer model
│   ├── major.png          # Reference for Major Arcana (Fool to World)
│   ├── wands.png          # Reference for Wands suit
│   ├── cups.png           # Reference for Cups suit
│   ├── swords.png         # Reference for Swords suit
│   └── coins.png          # Reference for Coins suit
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

Simply run the command and follow the interactive prompts:

```bash
python -m tarot_gen
```

You'll be guided through each option:
1. **Style prompt** - Describe your art style (e.g., "dark gothic ink wash style")
2. **Model** - Use arrow keys to select `flux-schnell` or `sdxl`
3. **Cards to generate** - Choose `sample` (17 cards), `major` (22), `minor` (56), or `all` (78)
4. **Aspect ratio** - Select from common ratios (default: 11:19 portrait)
5. **Output directory** - Where to save images (default: `output`)
6. **Seed** - For reproducibility (default: 42)
7. **Parallel API calls** - Concurrent requests (default: 1)
8. **Key card** (SDXL only) - Reference image for style consistency
9. **Prompt strength** (SDXL with key card) - How much prompt overrides reference (0.0-1.0)
10. **Custom cards file** - Optional YAML with custom card definitions

### Style Transfer with Reference Images

When using the `style-transfer` model, you can provide 5 reference images in the `references/` folder to guide the visual style of each card group:

| Reference File | Cards |
|---|---|
| `references/major.png` | Major Arcana (The Fool through The World) |
| `references/wands.png` | Ace through King of Wands |
| `references/cups.png` | Ace through King of Cups |
| `references/swords.png` | Ace through King of Swords |
| `references/coins.png` | Ace through King of Coins |

Each card group is generated using its corresponding reference image for style consistency. The groups are processed concurrently for faster generation.

Output files are named alphabetically to maintain the traditional tarot order: Major Arcana first (Fool to World), followed by the four suits (Wands, Cups, Swords, Coins), each ordered Ace through King.

Press **Enter** to accept defaults, or **Ctrl+C** to cancel.

### Options Reference

| Option | Default | Description |
|---|---|---|
| Style prompt | *required* | Art style, e.g. `"dark gothic ink wash style"` |
| Model | `flux-schnell` | `flux-schnell` or `sdxl` |
| Cards | `sample` | `sample` (17), `major` (22), `minor` (56), or `all` (78) |
| Aspect ratio | `11:19` | `11:19`, `2:3`, `3:2`, `1:1`, `16:9`, `9:16`, `4:5`, `5:4`, `21:9`, `9:21` |
| Output | `./output` | Output directory for generated images |
| Seed | `42` | Base seed for reproducibility |
| Parallel | `1` | Number of concurrent API calls |
| Key card | *none* | Reference image for style transfer (SDXL only) |
| Prompt strength | `0.47` | How much prompt overrides key card (SDXL only, 0.0-1.0) |
| Cards file | *none* | Path to custom card definitions YAML |

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
