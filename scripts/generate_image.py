import requests
import base64
import sys
import os
import time

# --- METAESTHETICS MASTER PROMPT BLOCK ---
META_BASE = """Hyperrealistic professional medical photography,
shot on Phase One IQ4 150MP medium format camera, 85mm portrait lens, f/2.8 aperture, ISO 200.
Lighting: soft diffused warm studio light.
Background: warm seamless paper backdrop (#C9B99A).
Subject: natural skin texture, real pores, micro-imperfections.
Neutral expression. Photorealism score: maximum.
Aspect ratio: 16:9, landscape orientation, widescreen format."""


def get_api_key():
    """Read API key from environment variable or local config file."""
    # 1. Try environment variable
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key

    # 2. Try config file in skill directory
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.txt")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            for line in f:
                if line.startswith("OPENROUTER_API_KEY="):
                    return line.strip().split("=", 1)[1]

    return None


def generate_image(prompt, model="google/gemini-2.5-flash-image"):
    api_key = get_api_key()
    if not api_key:
        print("ERROR: No API key found.")
        print("Set it via environment variable:  OPENROUTER_API_KEY=sk-or-...")
        print("Or create a config.txt file in the skill root with:  OPENROUTER_API_KEY=sk-or-...")
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
                # Base64 encoded image
                _, encoded = image_data.split("base64,", 1)
                img_bytes = base64.b64decode(encoded)
                with open(filepath, "wb") as f:
                    f.write(img_bytes)
            else:
                # Remote URL — download it
                print("Downloading image...")
                img_bytes = requests.get(image_data).content
                with open(filepath, "wb") as f:
                    f.write(img_bytes)

            print(f"SUCCESS: Image saved to {filepath}")
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
