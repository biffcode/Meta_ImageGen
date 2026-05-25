---
name: metaesthetics-openrouter
description: Generate professional Metaesthetics clinical images via OpenRouter. Combines Metaesthetics v2 fixed studio settings (Phase One IQ4, warm taupe background, butterfly lighting) with nano-banana's Aggressive Realism prompt engineering. Use when the user asks to generate a Metaesthetics image, treatment photo, or clinical portrait.
---

# Metaesthetics Image Gen

Generates **medical-grade, photorealistic Metaesthetics imagery** using OpenRouter's API.

Combines two systems:
- **Metaesthetics v2 Fixed Base** — Phase One IQ4 camera, warm taupe studio (#C9B99A), clinical butterfly lighting. Auto-applied by the script.
- **Aggressive Realism** — Camera-first prompt engineering. Describe *how the photo was taken*, not *what it should look like*.

---

## Procedure

### Step 1 — Gather Subject Details
Ask the user (if not already provided):
- **Subject**: Who/what is being photographed (e.g., "45yo woman, post-lip injection")
- **Framing**: Portrait / bust / full-body / detail shot
- **Context**: Clinical, before/after, treatment area
- **Specifics**: expression, head tilt, skin tone, clothing/draping

### Step 2 — Build the Aggressive Realism Variable Prompt
**Rule: Describe the capture conditions, not the desired outcome.**

```
[SUBJECT]: [age, skin tone, expression, head position, treatment area, clothing/draping].
[FRAMING]: [portrait/bust/full-body], [angle — frontal/3/4/profile], [distance — close-up/mid-shot].
[SKIN]: natural pore texture, micro-imperfections, real sebaceous sheen — NOT smooth, NOT retouched.
[LIGHTING DETAIL]: [any override, e.g., "slight shadow on left side", "catch light in both eyes"].
[IMPERFECTIONS]: natural skin texture, fine lines appropriate to age, subtle micro-redness if post-treatment.
[INTENT]: clinical documentation, not advertising — neutral, factual, medical.
NO plastic sheen. NO AI-smoothed skin. NO perfect symmetry. NO retouched appearance. NO CGI look.
```

### Step 3 — Execute
```bash
python ~/.aios/skills/metaesthetics-openrouter/scripts/generate_image.py "[assembled variable prompt]"
```

### Step 4 — Deliver
Report the saved file path from the script output (`~/Downloads/meta_<timestamp>.png`).

---

## Fixed Base (Auto-Applied by Script)
Do NOT repeat these in the variable prompt — already baked in:
```
Hyperrealistic professional medical photography,
shot on Phase One IQ4 150MP medium format camera, 85mm portrait lens, f/2.8 aperture, ISO 200.
Lighting: soft diffused warm studio light.
Background: warm seamless paper backdrop (#C9B99A).
Subject: natural skin texture, real pores, micro-imperfections.
Neutral expression. Photorealism score: maximum.
Aspect ratio: 16:9, landscape orientation, widescreen format.
```

**Model:** `google/gemini-2.5-flash-image` via OpenRouter
**Aspect Ratio:** 16:9 landscape
**Output:** `~/Downloads/meta_<timestamp>.png`

---

## Aggressive Realism Quick Reference

> "Don't describe what you want — describe how the photo was taken."

### Power Phrases
- `"candid clinical documentation"` — removes posed/ad feel
- `"visible natural skin texture, pores visible at 100% crop"` — enforces realism
- `"catch light visible in iris"` — anchors lighting
- `"micro-redness consistent with 48h post-treatment"` — contextual realism
- `"no post-production skin smoothing"` — explicit anti-AI-look instruction

### Always Exclude
- NO studio-perfect symmetry
- NO AI-clean skin smoothing
- NO plastic or wax-like sheen
- NO CGI or render appearance
- NO advertising aesthetic

---

## Example

**User:** "Generate a Metaesthetics image of a 38yo woman, 3 days after lip filler"

**Assembled Variable Prompt:**
```
[SUBJECT]: 38-year-old Southeast Asian woman, subtle lip augmentation, 3 days post-treatment. Slight natural fullness in upper and lower lip. Neutral closed-mouth expression. Light medical draping at neckline.
[FRAMING]: bust portrait, slight 3/4 angle (15 degrees right), mid-shot.
[SKIN]: natural pore texture, slight T-zone sheen, fine perioral lines — NOT retouched.
[LIGHTING DETAIL]: soft butterfly light, catch light centered in both irises, minimal chin shadow.
[IMPERFECTIONS]: minimal residual periorbital puffiness, natural skin translucency.
[INTENT]: clinical documentation — factual, medical, non-advertising.
NO plastic sheen. NO AI-smoothed skin. NO perfect symmetry. NO CGI look.
```

**Command:**
```bash
python ~/.aios/skills/metaesthetics-openrouter/scripts/generate_image.py "[SUBJECT]: 38-year-old Southeast Asian woman, subtle lip augmentation, 3 days post-treatment. Neutral closed-mouth expression. Light medical draping. [FRAMING]: bust portrait, slight 3/4 angle, mid-shot. [SKIN]: natural pore texture, T-zone sheen — NOT retouched. [LIGHTING DETAIL]: butterfly light, catch light in both irises. [IMPERFECTIONS]: minimal puffiness. [INTENT]: clinical documentation. NO plastic sheen. NO AI-smooth skin. NO CGI."
```
