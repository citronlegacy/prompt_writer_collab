# H3 Video-Prompt Writer

A Google Colab notebook app that helps write properly-formatted "H3" video-generation prompts — the structured prompt format used by MiniMax's H3 video model. Describe what you want in plain language (fix a rough prompt, combine two prompts, remix several, rewrite one with an added camera motion, or anything else) and get back a correctly formatted H3 prompt, ready to copy.

Maintained by **Citron Legacy** at [github.com/citronlegacy/prompt_writer_collab](https://github.com/citronlegacy/prompt_writer_collab).

## Launch App in Colab

Open in Colab [![Open in Colab](https://raw.githubusercontent.com/citronlegacy/kohya-colab/main/assets/colab-badge.svg)](https://colab.research.google.com/github/citronlegacy/prompt_writer_collab/blob/main/notebook.ipynb)

Open Dev Branch in Colab [![Open Dev Branch in Colab](https://raw.githubusercontent.com/citronlegacy/kohya-colab/main/assets/colab-badge.svg)](https://colab.research.google.com/github/citronlegacy/prompt_writer_collab/blob/dev/notebook.ipynb)

## What it does

- Runs a local LLM (Qwen3-14B-abliterated, GGUF quantized) entirely inside the Colab runtime — no external API keys, no paid inference service.
- Downloads the official H3 video-prompt-writing guide from Hugging Face and bakes its rules into a mode-aware system prompt, so output actually follows the spec instead of guessing at it.
- Launches a Gradio web UI with a single request box, a mode selector, and a copy-ready output box.
- Logs every input/output pair to a local JSON file (id + timestamp) that you can download on demand from the UI.

There's no fixed menu of request types — type whatever you want done ("fix this rough prompt," "combine these two, taking the setting from one and the dialogue from the other," "remix these three into one," "rewrite this and have the camera orbit," a critique, a brand-new prompt from scratch, etc.) and the model handles it.

## Modes

The app supports all four modes defined by the H3 spec, selectable via radio button (defaults to **T2VA**):

| Mode | Reference | Behavior |
|------|-----------|----------|
| **T2VA** | none | Text-to-video. Full scene, style, and subjects are established from your text alone. |
| **I2VA** | first frame | You describe a first-frame image in words; the prompt develops forward from it. |
| **FL2VA** | first + last frame | You describe both frames; the prompt describes the motion path connecting them. |
| **L2VA** | last frame only | You describe the final frame; the prompt describes convergence toward it. |

The app is text-only — there's no image upload. The backing LLM has no vision capability, so for I2VA/FL2VA/L2VA you describe the reference image(s) in your own words and the system prompt treats that description as standing in for the picture.

## Requirements

- A Google account with access to Colab (the free tier is sufficient).
- A free-tier **T4 GPU runtime** (12GB VRAM) — confirmed sufficient for the Q4_K_M-quantized 14B model via `llama-cpp-python`. No paid tier needed.
- Python 3.11+ (this is what the Colab runtime provides; not something you need to set up yourself).
- No Hugging Face login or access token — both the model repo and the guide repo are public, so downloads happen anonymously.

## Setup notes

The notebook has exactly three cells:

1. **Header/info** — what the app is and how to use it.
2. **Install + setup** — installs dependencies (`requirements.txt`, plus a CUDA-enabled build of `llama-cpp-python`) and downloads the model and guide from Hugging Face. This happens on every run, since Colab has no persistent disk.
3. **Run app** — launches the Gradio UI with `share=True`, producing a public tunnel URL. Because that URL is otherwise guessable/public, the cell also generates a random username and password at startup and prints both alongside the URL — you'll need them to log in.

Just run the cells in order and open the printed link.

## History logging

Every request/response pair is written to a local JSON file (`/content/prompt_history.json` inside the Colab runtime) with a unique id and timestamp. A **Download history (.json)** button in the UI lets you pull the file down whenever you want.

This history is **local to the current Colab session only** — it is not saved anywhere else. If you want to keep it, download it before the runtime disconnects or recycles; once that happens, the file (and everything in it) is gone for good.

## How it works

- `app.py` builds the Gradio UI and wires up generation: `generate()` builds the mode-aware system prompt, runs it through the local `llama_cpp.Llama` model, and appends the result to the history file.
- `system_prompt.py` assembles the system prompt from a shared body (the downloaded guide's rules plus the bundled good/bad example bank in `h3_good_bad_examples.md`) and a small per-mode header snippet (`build_system_prompt()`), so a guide-rule fix only needs to change in one place instead of four.
- Generation is single-turn: each request is independent, with no chat history fed back into the model between requests.

## Repo layout

- `notebook.ipynb` — the Colab notebook (3 cells, described above).
- `app.py` — the Gradio app.
- `system_prompt.py` — builds the mode-aware system prompt.
- `h3_good_bad_examples.md` — good/bad example bank embedded in the system prompt.
- `requirements.txt` — Python dependencies.
