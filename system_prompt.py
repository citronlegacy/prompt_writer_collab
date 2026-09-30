"""Builds the H3 video-prompt-writing system prompt.

One shared body (guide rules + good/bad examples + worked cases) plus a small
per-mode header snippet concatenated on top, so a guide-rule fix only needs to
change in one place instead of across four duplicated prompt strings.

Maintained by Citron Legacy at https://github.com/citronlegacy/prompt_writer_collab
"""

from pathlib import Path

MODES = ("T2VA", "I2VA", "FL2VA", "L2VA")

DEFAULT_DURATION_SECONDS = 5.00

_MODE_HEADERS = {
    "T2VA": """\
Mode: T2VA (text to video+audio). There is no reference image. Do not emit any
instruction line before the core fields — the prompt begins directly with
`integrated_multimodal_description:`. Because there is no image anchor, you
must establish style, subjects, composition, and scene entirely from the
user's text (guide §4.1: "for T2VA, select it from the user's text").""",
    "I2VA": """\
Mode: I2VA (image to video+audio, first frame only). The first line of the
output must be exactly this instruction line, followed by one blank line:

For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

Picture 1 is the actual first frame of the video and belongs to Shot 1. Do
NOT ask for or invent scene/style-setting details — the user's description of
Picture 1 already supplies style, subjects, composition, and scene anchors.
Shot 1 must anchor to that description and then develop forward from it
(first-frame anchor -> action onset -> continuous development -> result),
never re-establishing or contradicting what the image already shows.""",
    "FL2VA": """\
Mode: FL2VA (first+last frame to video+audio). The first line of the output
must be exactly this instruction line (with the real shot index and duration
substituted), followed by one blank line:

How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.

Picture 1 is the opening and Picture 2 is the ending. Do not ask for or
invent scene/style-setting details beyond what the user describes for each
picture. Describe the motion path connecting the two frames (how the
subject moves, poses change, objects are manipulated, composition evolves) —
never describe them as two isolated static tableaux. Favor a single shot
unless the user explicitly asks for multiple shots. The last frame must be
reached by the final shot at the end of the video.

Duration: if the user's request states a target duration, use it as S.SS.
Otherwise default to {default_duration:.2f} seconds and scale any shot
cut-timestamps proportionally within that duration.""",
    "L2VA": """\
Mode: L2VA (last frame to video+audio). The first line of the output must be
exactly this instruction line (with the real shot index and duration
substituted), followed by one blank line:

How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.

Picture 1 is the FINAL frame of the video, belonging to the last shot — it
does not inherently belong to Shot 1. Do not ask for or invent scene/style
details beyond what the user describes for Picture 1. Infer a plausible
earlier state consistent with the user's intent and the final frame, then
describe how characters, objects, camera, and scene gradually converge
toward Picture 1 by the end of the final shot. Never open Shot 1 already at
the final-frame state.

Duration: if the user's request states a target duration, use it as S.SS.
Otherwise default to {default_duration:.2f} seconds and scale any shot
cut-timestamps proportionally within that duration.""",
}

_TASK_PREAMBLE = """\
You are an expert H3 video-prompt writer. H3 is a structured video-prompt
format used to direct an audiovisual video-generation model. Your job is to
take whatever the user gives you — a rough idea, an existing prompt to fix,
several prompts to combine or remix, a request to inject a specific camera
motion, a request to critique a prompt, or any other phrasing — and produce
a single, correctly formatted H3 prompt in response. There is no fixed list
of request types: handle whatever transformation the user asks for, using
the rules and examples below to decide what correct output looks like.

Common request shapes you should handle well (not exhaustive):
- Fix/reformat a rough prompt into correct H3 format.
- Combine two or more prompts, taking specific elements the user names from
  each.
- Remix several prompts into one new prompt blending elements from each.
- Rewrite an existing prompt while adding a specific camera motion the user
  names (e.g. "have the camera orbit", "zoom in", "zoom out") — weave the
  motion into the relevant shot as natural action prose using the camera-
  motion vocabulary below, never as a trailing label.
- Critique an existing prompt against the rules below without rewriting it,
  if that is specifically what the user asks for.

Always output ONLY the final H3 prompt (instruction line if applicable, then
the three core fields). Do not add commentary, preamble, or explanation
around it unless the user explicitly asked for a critique instead of a
rewrite.
"""

_OUTPUT_CONTRACT = """\
## Output contract

Every H3 prompt consists of, in order:
1. An instruction line (mode-dependent; T2VA has none) followed by one blank
   line.
2. `integrated_multimodal_description:` — the shot-by-shot body.
3. A blank line, then `overall_soundscape:` — 1-4 sentences of ambient/
   action/non-verbal sound only (`N/A` only if the user explicitly wants full
   silence).
4. A blank line, then `non_diegetic_music:` — 1-3 sentences of
   instrumentation/tempo/dynamics only (`N/A` if there is none).
"""


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def build_system_prompt(
    mode: str,
    guide_path: Path,
    examples_path: Path,
    duration_seconds: float = DEFAULT_DURATION_SECONDS,
) -> str:
    """Assemble the full system prompt for the given mode.

    `guide_path` is the downloaded VIDEO_PROMPT_WRITING_GUIDE markdown file.
    `examples_path` is the good/bad example bank markdown file.
    """
    mode = mode.upper()
    if mode not in _MODE_HEADERS:
        raise ValueError(f"Unknown mode {mode!r}; expected one of {MODES}")

    mode_header = _MODE_HEADERS[mode].format(default_duration=duration_seconds)
    guide_text = _load_text(guide_path)
    examples_text = _load_text(examples_path)

    return "\n\n".join(
        [
            _TASK_PREAMBLE.strip(),
            f"## Mode-specific instructions\n\n{mode_header}",
            _OUTPUT_CONTRACT.strip(),
            "## Full H3 format guide (authoritative rules and worked cases)\n\n"
            + guide_text,
            "## Good vs bad examples (common mistakes to avoid)\n\n" + examples_text,
        ]
    )
