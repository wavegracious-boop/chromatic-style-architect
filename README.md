# Chromatic Style Architect: Multimodal AI Styling Engine

An automated, multimodal Python pipeline that analyzes portrait photography to generate bespoke chromatic skin profiles and high-contrast wardrobe lookbooks. Designed specifically to solve color-theory blind spots for high-melanin complexions (Fitzpatrick Skin Types IV–VI).

## System Architecture & Workflow

1. **In-Memory Image Optimization (`Pillow`)**: Converts raw user uploads to RGB, strips heavy alpha channels, and downscales dimensions to a maximum of 1024px to minimize API latency, bandwidth consumption, and token overhead.
2. **Deterministic JSON Prompting (`Claude Sonnet 5.5`)**: Enforces a strict schema via a system-level guardrail prompt, ensuring reliable, parseable color coordinates and styling specifications without conversational drift.
3. **Multi-Block Payload Parsing**: Iterates through Anthropic's SDK response blocks to isolate final `TextBlock` outputs from internal reasoning (`ThinkingBlock`) structures.
4. **Dynamic Lookbook Compilation**: Injects parsed hexadecimal values into a responsive, dark-mode HTML/CSS interface featuring interactive click-to-copy color swatches.

## Security & Privacy Practices

* **Zero-Hardcoded Secrets**: All API credentials are injected dynamically at runtime via local environment variables (`ANTHROPIC_API_KEY`) with automated whitespace sanitization.
* **Ephemeral Processing**: User images are encoded in memory (`io.BytesIO`) without creating temporary duplicate files on disk.
* **Repository Hygiene**: Strict `.gitignore` rules prevent local portrait assets, generated customer reports, and environment files from ever touching version control.

## Local Setup & Execution

### 1. Clone the Repository
```bash
git clone https://github.com
cd chromatic-style-architect
```

### 2. Install Dependencies
```bash
pip install anthropic pillow
```

### 3. Configure Environment Variables
**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=your_api_key_here
```

**macOS / Linux:**
```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

### 4. Run the Pipeline
Place a target portrait named `me.jpg` in the root directory and execute:
```bash
python style_app.py
```
The script will process the image and automatically launch `Style_Lookbook.html` in your default web browser.
