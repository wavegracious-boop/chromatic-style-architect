import os
import io
import base64
import traceback
from pathlib import Path
from PIL import Image
from anthropic import Anthropic

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Missing ANTHROPIC_API_KEY environment variable.")

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Missing ANTHROPIC_API_KEY environment variable.")

client = Anthropic(api_key=api_key.strip())


SYSTEM_PROMPT = """
You are the core AI engine for "The Digital Skin & Style Palette," an elite virtual styling consultant specialized in high-melanin complexions.
Analyze the user's uploaded portrait photo and generate a highly structured Style Architecture Report.

### OPERATIONAL CONSTRAINTS:
- Output using clean Markdown headings, bullet points, and explicit Hexadecimal color codes.
- Do not include conversational filler, meta-commentary, or introductory summaries. Deliver the raw data immediately.
- Use short sentences and crisp single-sentence fragments for lists.

### REQUIRED REPORT STRUCTURE:
#### 1. CHROMATIC SKIN ANALYSIS
* Baseline Tone: Name (#Hex)
* Secondary Undertone: Name (#Hex)
* Reflectivity Profile: One crisp sentence.

#### 2. THE COMPLEMENTARY WARDROBE PALETTE
* High-Contrast Accent (Jewel Tones): Name (#Hex). One sentence use-case.
* Harmonious Core (Earth/Warm Tones): Name (#Hex). One sentence use-case.
* High-Status Neutral: Name (#Hex). One sentence use-case.

#### 3. WARDROBE LOOKBOOK SPECIFICATIONS
* Optimal Metal: Profile description.
* Fabrication Textures: Three bulleted items.
* High-Risk Colors to Avoid: Two bulleted items with reasoning.
"""


def optimize_and_encode_image(image_path):
    """Resizes large images safely so they transmit fast without dropping connections."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Could not locate target image at: {image_path}")

    with Image.open(path) as img:
        img = img.convert("RGB")
        img.thumbnail((1024, 1024))

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        encoded_string = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return encoded_string, "image/jpeg"


def generate_style_report(image_filename):
    print(f"[*] Optimizing and encoding image asset: {image_filename}...")

    try:
        base64_data, media_type = optimize_and_encode_image(image_filename)

        print("[*] Transmitting lightweight payload to Claude...")
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": base64_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Perform a precise chromatic skin analysis on this profile portrait."
                        }
                    ],
                }
            ],
        )

        for block in response.content:
            if block.type == "text":
                return block.text
        return "No text block returned."

    except Exception as e:
        print("\n--- DETAILED NETWORK DIAGNOSTICS ---")
        traceback.print_exc()
        return f"Execution Error: {str(e)}"


if __name__ == "__main__":
    TARGET_IMAGE = "me.jpg"
    OUTPUT_FILE = "Style_Architecture_Report.md"

    if not os.path.exists(TARGET_IMAGE):
        print(f"[X] Error: Please place a selfie image named '{TARGET_IMAGE}' in this directory.")
    else:
        markdown_output = generate_style_report(TARGET_IMAGE)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(markdown_output)

        print("\n" + "=" * 40)
        print(f"[SUCCESS] Process completed. Check {OUTPUT_FILE}")
        print("=" * 40 + "\n")
