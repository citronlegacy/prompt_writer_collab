"""Gradio UI for the H3 video-prompt writer.

Single-turn request/response: the user submits one request, picks a mode,
and gets back one H3-formatted prompt. No chat history is fed back into the
model between requests.

Maintained by Citron Legacy at https://github.com/citronlegacy/prompt_writer_collab
"""

import json
import secrets
import time
import uuid
from pathlib import Path

import gradio as gr
from llama_cpp import Llama

from system_prompt import MODES, build_system_prompt

CONTENT_DIR = Path("/content")
MODEL_PATH = CONTENT_DIR / "Qwen3-14B-abliterated.Q4_K_M.gguf"
GUIDE_PATH = CONTENT_DIR / "VIDEO_PROMPT_WRITING_GUIDE_base_en.md"
EXAMPLES_PATH = Path(__file__).parent / "h3_good_bad_examples.md"
HISTORY_PATH = CONTENT_DIR / "prompt_history.json"

N_CTX = 16384  # system prompt (guide + examples) alone runs ~7k tokens
N_GPU_LAYERS = -1  # offload all layers to GPU (fits the free-tier T4 at Q4_K_M)

_llm: Llama | None = None


def get_llm() -> Llama:
    global _llm
    if _llm is None:
        _llm = Llama(
            model_path=str(MODEL_PATH),
            n_ctx=N_CTX,
            n_gpu_layers=N_GPU_LAYERS,
            verbose=False,
        )
    return _llm


def load_history() -> list[dict]:
    if HISTORY_PATH.exists():
        return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    return []


def append_history(entry: dict) -> None:
    history = load_history()
    history.append(entry)
    HISTORY_PATH.write_text(json.dumps(history, indent=2), encoding="utf-8")


def generate(request_text: str, mode: str) -> str:
    request_text = request_text.strip()
    if not request_text:
        return "Please enter a request."

    system_prompt = build_system_prompt(
        mode=mode,
        guide_path=GUIDE_PATH,
        examples_path=EXAMPLES_PATH,
    )

    llm = get_llm()
    completion = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request_text},
        ],
        temperature=0.7,
    )
    output_text = completion["choices"][0]["message"]["content"].strip()

    append_history(
        {
            "id": str(uuid.uuid4()),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "mode": mode,
            "input": request_text,
            "output": output_text,
        }
    )

    return output_text


def download_history() -> str:
    if not HISTORY_PATH.exists():
        HISTORY_PATH.write_text("[]", encoding="utf-8")
    return str(HISTORY_PATH)


def build_app() -> gr.Blocks:
    with gr.Blocks(title="H3 Video-Prompt Writer") as demo:
        gr.Markdown("# H3 Video-Prompt Writer")
        gr.Markdown(
            "Describe what you want (fix a prompt, combine prompts, remix "
            "several, add a camera motion, generate from scratch, etc.), "
            "pick a mode, and submit."
        )
        gr.Markdown(
            "Maintained by Citron Legacy — "
            "[github.com/citronlegacy/prompt_writer_collab]"
            "(https://github.com/citronlegacy/prompt_writer_collab)"
        )

        with gr.Row():
            mode = gr.Radio(choices=list(MODES), value="T2VA", label="Mode")

        request_box = gr.Textbox(
            label="Request",
            placeholder="e.g. 'Fix this prompt: ...' or 'Combine prompt 1 and "
            "prompt 2, taking the setting from 1 and the dialogue from 2.'",
            lines=10,
        )

        submit_btn = gr.Button("Generate", variant="primary")

        output_box = gr.Textbox(label="H3 Prompt", lines=14, show_copy_button=True)

        download_btn = gr.DownloadButton("Download history (.json)")

        submit_btn.click(fn=generate, inputs=[request_box, mode], outputs=output_box)
        download_btn.click(fn=download_history, inputs=None, outputs=download_btn)

    return demo


def launch() -> None:
    username = secrets.token_urlsafe(6)
    password = secrets.token_urlsafe(12)

    demo = build_app()
    print(f"Gradio login — username: {username}  password: {password}")
    demo.launch(share=True, auth=(username, password))


if __name__ == "__main__":
    launch()
