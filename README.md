# Metaesthetics Image Gen — Companion Skill

A [Companion](https://companion.ai) skill that generates **medical-grade, photorealistic Metaesthetics clinical images** using OpenRouter's API.

- **Model:** Google Gemini 2.5 Flash Image (via OpenRouter)
- **Output:** 16:9 landscape, warm taupe clinical studio (#C9B99A)
- **Style:** Phase One IQ4 aesthetics + Aggressive Realism prompting
- **Logo:** Auto-applies Metaesthetics watermark — brown on light, white on dark backgrounds

---

## Installation

### Option 1 — Install via Companion (Recommended)

Just tell your Companion:

> "Install skill from https://github.com/biffcode/Meta_ImageGen"

Your Companion will automatically:
1. Clone this repo into `~/.aios/skills/metaesthetics-openrouter/`
2. Install the `requests` and `Pillow` dependencies
3. Prompt you to add your logo files and set your OpenRouter API key

### Option 2 — Manual Install

**1. Clone the repo into your skills folder:**
```bash
git clone https://github.com/biffcode/Meta_ImageGen ~/.aios/skills/metaesthetics-openrouter
```

**2. Install dependencies:**
```bash
pip install requests Pillow
```

**3. Add your logo files** into the `logos/` folder:
```
~/.aios/skills/metaesthetics-openrouter/logos/
  Logo_Horizontal_TM_white.png
  Logo_Horizontal_TM_brown.png
```

**4. Set your OpenRouter API key** — choose one method:

- **Environment variable (recommended):**
  ```bash
  # Add to your shell profile (.bashrc, .zshrc, or PowerShell $PROFILE)
  export OPENROUTER_API_KEY=sk-or-your-key-here
  ```

- **Config file:**
  Create `~/.aios/skills/metaesthetics-openrouter/config.txt`:
  ```
  OPENROUTER_API_KEY=sk-or-your-key-here
  ```

> Get your API key at [openrouter.ai/keys](https://openrouter.ai/keys)

---

## Usage

Once installed, tell your Companion to generate a Metaesthetics image:

> "Generate a Metaesthetics image of a 35yo woman, 1 week post lip filler, clinical portrait"

> "Create a Metaesthetics clinical photo of a 42yo man, post-rhinoplasty, 3/4 angle"

Your Companion will build the prompt and run the generation automatically. Two files are saved to `~/Downloads/`:
- `meta_<timestamp>.png` — original clean image
- `meta_<timestamp>_watermarked.png` — with Metaesthetics logo applied

---

## How It Works

### Image Generation
| Layer | What it does |
|-------|-------------|
| **Metaesthetics v2 Base** | Fixed clinical settings — Phase One IQ4 camera, warm taupe backdrop (#C9B99A), butterfly lighting. Always applied. |
| **Aggressive Realism** | Camera-first variable prompt — describes capture conditions, not aesthetic outcomes. Enforces real skin texture, natural imperfections, non-advertising feel. |

### Logo Watermark
| Brightness of logo area | Logo used |
|------------------------|-----------|
| > 180 (light background) | Brown logo |
| < 100 (dark background) | White logo |
| Mid-range | White logo (safe default) |

- Samples the actual logo placement zone (top-left, 50px margin) for accurate brightness reading
- Logo scaled to 20% of image width
- Original image is always preserved — watermark saved as a separate `_watermarked` copy

---

## Requirements

- Python 3.7+
- `requests` library (`pip install requests`)
- `Pillow` library (`pip install Pillow`)
- OpenRouter API key with access to `google/gemini-2.5-flash-image`
- Logo files in `logos/` folder (`Logo_Horizontal_TM_white.png`, `Logo_Horizontal_TM_brown.png`)
