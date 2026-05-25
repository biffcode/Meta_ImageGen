# Metaesthetics Image Gen — Companion Skill

A [Companion](https://companion.ai) skill that generates **medical-grade, photorealistic Metaesthetics clinical images** using OpenRouter's API.

- **Model:** Google Gemini 2.5 Flash Image (via OpenRouter)
- **Output:** 16:9 landscape, warm taupe clinical studio (#C9B99A)
- **Style:** Phase One IQ4 aesthetics + Aggressive Realism prompting

---

## Installation

### Option 1 — Install via Companion (Recommended)

Just tell your Companion:

> "Install skill from https://github.com/biffcode/Meta_ImageGen"

Your Companion will automatically:
1. Clone this repo into `~/.aios/skills/metaesthetics-openrouter/`
2. Install the `requests` dependency
3. Prompt you to set your OpenRouter API key

### Option 2 — Manual Install

**1. Clone the repo into your skills folder:**
```bash
git clone https://github.com/biffcode/Meta_ImageGen ~/.aios/skills/metaesthetics-openrouter
```

**2. Install dependencies:**
```bash
pip install requests
```

**3. Set your OpenRouter API key** — choose one method:

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

Your Companion will build the prompt and run the generation automatically. The image is saved to `~/Downloads/meta_<timestamp>.png`.

---

## How It Works

The skill combines two prompt engineering systems:

| Layer | What it does |
|-------|-------------|
| **Metaesthetics v2 Base** | Fixed clinical settings — Phase One IQ4 camera, warm taupe backdrop (#C9B99A), butterfly lighting. Always applied. |
| **Aggressive Realism** | Camera-first variable prompt — describes capture conditions, not aesthetic outcomes. Enforces real skin texture, natural imperfections, non-advertising feel. |

---

## Requirements

- Python 3.7+
- `requests` library (`pip install requests`)
- OpenRouter API key with access to `google/gemini-2.5-flash-image`
