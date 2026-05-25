import requests
import base64
import sys
import os
import time
from PIL import Image, ImageStat

# --- METAESTHETICS MASTER PROMPT BLOCK ---
META_BASE = """Hyperrealistic professional medical photography,
shot on Phase One IQ4 150MP medium format camera, 85mm portrait lens, f/2.8 aperture, ISO 200.
Lighting: soft diffused warm studio light.
Background: warm seamless paper backdrop (#C9B99A).
Subject: natural skin texture, real pores, micro-imperfections.
Neutral expression. Photorealism score: maximum.
Aspect ratio: 16:9, landscape orientation, widescreen format."""

# --- LOGO PATHS ---
LOGOS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logos")
LOGO_WHITE = os.path.join(LOGOS_DIR, "Logo_Horizontal_TM_white.png")
LOGO_BROWN = os.path.join(LOGOS_DIR, "Logo_Horizontal_TM_brown.png")


def get_api_key():
    """Read API key from environment variable or local config file."""
    # 1. Try environment variable
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key

    # 2. Try config file in skill root
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.txt")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            for line in f:
                if line.startswith("OPENROUTER_API_KEY="):
                    return line.strip().split("=", 1)[1]

    return None


def apply_logo(input_path):
    """
    Detect brightness at the logo placement area and overlay the correct logo.
    - Brightness > 180  -> brown logo (light background)
    - Brightness < 100  -> white logo (dark background)
    - In between        -> white logo (safer default)
    Saves a separate _watermarked copy, original is preserved.
    """
    img = Image.open(input_path).convert("RGBA")

    # Sample the actual logo placement zone for accurate brightness reading
    margin = 50
    sample_w = int(img.width * 0.20)
    sample_h = int(sample_w * 0.35)
    sample_area = (margin, margin, margin + sample_w, margin + sample_h)
    crop = img.convert("RGB").crop(sample_area)
    brightness = sum(ImageStat.Stat(crop).mean) / 3

    if brightness > 180:
        logo_path = LOGO_BROWN
        variant = "brown"
    else:
        logo_path = LOGO_WHITE
        variant = "white"

    print(f"Brightness: {brightness:.1f} -> {variant} logo")

    if not os.path.exists(logo_path):
        print(f"Warning: logo not found at {logo_path}, skipping watermark.")
        return input_path

    logo = Image.open(logo_path).convert("RGBA")

    # Scale to 20% of image width, preserve aspect ratio
    target_width = int(img.width * 0.20)
    scale = target_width / logo.width
    target_height = int(logo.height * scale)
    logo = logo.resize((target_width, target_height), Image.LANCZOS)

    # Paste at top-left with 50px fixed margin
    img.paste(logo, (margin, margin), logo)

    # Save as a separate watermarked file — original untouched
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_watermarked{ext}"
    img.convert("RGB").save(output_path, "PNG")
    print(f"Watermarked image saved to {output_path}")
    return output_path


def generate_image(prompt, model="google/gemini-2.5-flash-image"):
    api_key = get_api_key()
    if not api_key:
        print("ERROR: No API key found.")
        print("Set it via environment variable:  OPENROUTER_API_KEY=sk-or-...")
        print("Or create a config.txt in the skill root with:  OPENROUTER_API_KEY=sk-or-...")
        sys.exit(1)

    url = "https://openrouter.ai/api/v1/chat/completions"
    full_prompt = f"{META_BASE}\n\n[VARIABLES]\n{prompt}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://metaesthetics.net",
        "X-Title": "Metaesthetics Image Gen"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": full_prompt}],
        "image_config": {
            "aspect_ratio": "16:9"
        }
    }

    print(f"Generating image with {model}...")

    try:
        response = requests.post(url, headers=headers, json=payload)
        res_json = response.json()

        image_data = None

        # Primary: choices[0].message.images[0].image_url.url (Gemini via OpenRouter)
        if "choices" in res_json:
            message = res_json["choices"][0].get("message", {})
            images = message.get("images", [])
            if images:
                image_data = images[0].get("image_url", {}).get("url")
                if not image_data:
                    image_data = images[0].get("url")  # fallback flat structure

        # Fallback: top-level images array
        if not image_data and "images" in res_json and res_json["images"]:
            image_data = res_json["images"][0].get("url")

        if image_data:
            filename = f"meta_{int(time.time())}.png"
            filepath = os.path.join(os.path.expanduser("~"), "Downloads", filename)

            if image_data.startswith("data:image"):
                _, encoded = image_data.split("base64,", 1)
                img_bytes = base64.b64decode(encoded)
                with open(filepath, "wb") as f:
                    f.write(img_bytes)
            else:
                print("Downloading image...")
                img_bytes = requests.get(image_data).content
                with open(filepath, "wb") as f:
                    f.write(img_bytes)

            print(f"SUCCESS: Image saved to {filepath}")

            # Apply Metaesthetics logo watermark
            apply_logo(filepath)

        else:
            print("No image generated. The model returned text instead:")
            if "choices" in res_json:
                print(res_json["choices"][0]["message"].get("content"))

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_image.py \"your subject prompt here\"")
        sys.exit(1)
    generate_image(sys.argv[1])
