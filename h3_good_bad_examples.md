# H3 Prompt: Good vs Bad Examples

Reference examples of common mistakes when writing H3-format video prompts, paired with corrected versions. Each entry cites the guide rule it violates.

---

## 1. Timestamp on Shot 1

Shot 1 never carries a timestamp — only later shots get a cut time.

**Bad:**
```text
[Shot 1] At 00:00.000, Live-action, cinematic, a medium-wide shot frames a baker opening the shutters...
```

**Good:**
```text
[Shot 1] Live-action, cinematic, a medium-wide shot frames a baker opening the shutters...
```

*Why:* Guide §4.2: "Do not add a timestamp to the first shot." Only Shot 2 and beyond get `At HH:MM:SS.sss,`.

---

## 2. Non-increasing or out-of-range cut timestamps

Every shot after Shot 1 needs a strictly increasing timestamp that fits inside the video's total duration.

**Bad:**
```text
[Shot 1] Live-action, a runner starts down the track. [Shot 2] At 00:04.000, the camera cuts to a close-up of her shoes. [Shot 3] At 00:02.500, the camera cuts to the finish line banner.
```
(Shot 3's timestamp is earlier than Shot 2's, and if the clip is only 4 seconds long, Shot 2's own timestamp is already at the edge.)

**Good:**
```text
[Shot 1] Live-action, a runner starts down the track. [Shot 2] At 00:01.800, the camera cuts to a close-up of her shoes. [Shot 3] At 00:03.200, the camera cuts to the finish line banner.
```

*Why:* Guide §4.2: cut times must be "sequential" and "strictly increasing" and must "fall within the video duration."

---

## 3. Camera motion written as a trailing label instead of prose

Camera motion is expressed as natural action inside the sentence, not appended as a tag.

**Bad:**
```text
[Shot 2] At 00:03.500, the camera cuts to the hallway. Pan Right, large amplitude, fast.
```

**Good:**
```text
[Shot 2] At 00:03.500, the camera cuts to the hallway. The camera pans right with large amplitude at fast speed, revealing the open doorway at the far end.
```

*Why:* Guide §4.3: "Camera motion should be written as a natural English action within the shot, rather than stacked as separate labels at the end of a sentence." Amplitude/speed are only added when meaningful — "medium amplitude and normal speed are usually omitted."

---

## 4. Dialogue, singing, or diegetic music repeated inside `overall_soundscape`

`overall_soundscape` covers ambient, action, and non-verbal human sound only. Spoken lines, lyrics, and diegetic music belong solely in the multimodal description.

**Bad:**
```text
overall_soundscape: The baker says "First batch of the morning" as trays clink inside the bakery. A radio plays a cheerful pop song in the background. The doorbell rings once.
```

**Good:**
```text
overall_soundscape: Wooden shutters scrape open over a quiet street as trays clink softly inside the bakery. The doorbell rings once, followed by light footsteps.
```

*Why:* Guide §4.6: "Dialogue, singing, and diegetic music already belong in the multimodal description and should not be repeated here."

---

## 5. Mood words in `non_diegetic_music` instead of concrete musical detail

`non_diegetic_music` describes instrumentation, tempo, rhythm, and dynamics — never emotional labels or the score's narrative function.

**Bad:**
```text
non_diegetic_music: Tense, melancholic music that builds dread and underscores her sadness.
```

**Good:**
```text
non_diegetic_music: Sparse piano notes at a slow tempo, joined by sustained low strings that gradually increase in volume before fading out.
```

*Why:* Guide §4.7: "Focus on instrumentation, speed, rhythm, and dynamic changes; do not use abstract mood words or explain the emotional function of the score."

---

## 6. Missing or duplicated speaker ID across shots

A speaker gets one stable ID the first time they're introduced and keeps it in every later shot. Don't renumber them, and don't forget the ID once established.

**Bad:**
```text
[Shot 1] The young woman with a quiet voice (S1) says: <d>[English] I get off at the next station.</d>
[Shot 2] At 00:05.000, the camera cuts to the same woman, who says: <d>[English] Wait, this is my stop.</d>
```
(No ID at all in Shot 2, even though this is the same speaker.)

**Good:**
```text
[Shot 1] The young woman with a quiet voice (S1) says: <d>[English] I get off at the next station.</d>
[Shot 2] At 00:05.000, the camera cuts to the same woman (S1), who says: <d>[English] Wait, this is my stop.</d>
```

*Why:* Guide §4.4: "A speaker keeps the same ID across shots." Assigning her `(S2)` in Shot 2 instead of reusing `(S1)` would be an equally wrong variant of this mistake.

---

## 7. Non-dialogue content placed inside the `<d>` tag

Only the actual spoken (or sung) words go inside `<d>...</d>`. Identifying phrases, actions, and delivery style stay outside it.

**Bad:**
```text
The man (S1) says: <d>The tired old fisherman sighs heavily and mutters in a low voice, [English] The tide's turned against us.</d>
```

**Good:**
```text
The tired old fisherman with a low, weary voice (S1) sighs and says: <d>[English] The tide's turned against us.</d>
```

*Why:* Guide §4.4: "Place the speaker's identifying phrase, ID, action, and delivery outside `<d>`. Inside `<d>`, include only the language tag and the actual user-provided spoken content."

---

## 8. Missing "lips remain closed" clause after an off-screen voiceover

Every voiceover `<d>` block must be immediately followed by a statement that the on-screen character's lips stay closed, since the voice is heard but not being spoken on camera.

**Bad:**
```text
The man (S1) says in an off-screen voiceover: <d>[English] I still remember that road.</d> He stares out the window.
```

**Good:**
```text
The man (S1) says in an off-screen voiceover: <d>[English] I still remember that road.</d> while his lips remain completely closed. He stares out the window.
```

*Why:* Guide §4.4: "Immediately after every voiceover `<d>` block, state that the corresponding on-screen character's lips remain closed."

---

## 9. I2VA: redundant scene-setting that restates the reference image

For I2VA, Shot 1 should anchor to what's already in Picture 1 and then move forward — it should not re-describe the scene/style as if establishing it from scratch, and must not contradict what the image already shows.

**Bad:**
```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, a young woman with long brown hair wearing a blue coat sits by a train window at dusk, the carriage lit by warm overhead lights. The camera trucks right with small amplitude at slow speed as she lifts her gaze from the folded letter toward the passing city lights.
```
(The bolded clause re-establishes hair, coat color, lighting, and time of day as if the reader has never seen the image — this is redundant scene-setting, and risks contradicting Picture 1's actual details.)

**Good:**
```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, the young woman shown in <Picture 1> remains beside the rain-covered train window, preserving her appearance, clothing, seat position, and the carriage layout. The camera trucks right with small amplitude at slow speed as she lifts her gaze from the folded letter toward the passing city lights.
```

*Why:* Guide §3.1: "The description should first establish the style, subjects, composition, and scene anchors in the image, then describe the next action... Character identity, clothing, colors, key objects, and spatial relationships should remain consistent" — referencing the image, not re-inventing its contents.

---

## 10. FL2VA: describing two static tableaux instead of the connecting motion

For FL2VA, the body must describe the path between the frames — the movement, pose changes, and transitions — not two separate freeze-frame descriptions with nothing joining them.

**Bad:**
```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the 8.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, a rain-soaked cyclist stands holding a closed black umbrella beside a silver bicycle, as shown in Picture 1. Later, the cyclist stands under an open umbrella in the final pose and composition shown in Picture 2.
```
(This is two isolated snapshots with "later" doing all the work — no described motion connects them.)

**Good:**
```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the 8.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, a rain-soaked cyclist begins in the position and framing established by Picture 1, holding a closed black umbrella beside a silver bicycle. The camera pulls out with small amplitude at slow speed as she releases the bicycle handle, raises the umbrella above her shoulder, and presses the runner upward until the canopy opens, settling into the pose and composition established by Picture 2 at the end of the shot.
```

*Why:* Guide §3.2: "Focus on how the subject moves, how poses change, how objects are manipulated, how the composition evolves... The body should not repeat two static image descriptions; instead, it should supply the motion path that connects them."

---

## 11. L2VA: anchoring Shot 1 to Picture 1 instead of converging toward it in the final shot

For L2VA, Picture 1 is the *last* frame, not the first. Shot 1 must open from an inferred, plausible earlier state and gradually converge toward Picture 1 by the end of the final shot — it must not treat Picture 1 as the starting point.

**Bad:**
```text
How the reference pictures align with the target video — <Picture 1> (from [Shot 1]) aligns with the 6.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, a close shot begins with the broken glass fragments and hand position already arranged exactly as shown in <Picture 1>. The camera pushes in with small amplitude at slow speed as the scene holds on the shattered glass.
```
(This opens Shot 1 already at the final-frame state, leaving no room for an approach or convergence.)

**Good:**
```text
How the reference pictures align with the target video — <Picture 1> (from [Shot 1]) aligns with the 6.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, a close shot begins with an intact drinking glass near the edge of a dark wooden table, while the same hand and sleeve visible in <Picture 1> approach from the right. The camera pushes in with small amplitude at slow speed as the fingertips strike the rim. The glass tips, falls, and hits the floor with a sharp impact; cracks spread through it as fragments slide outward. Toward the end, the moving pieces lose momentum and settle into the exact broken arrangement, hand position, camera angle, lighting, and final composition established by <Picture 1>.
```

*Why:* Guide §3.3: "`<Picture 1>` is the final frame of the video and belongs to the last `[Shot N]`; it does not inherently belong to Shot 1. Infer a plausible earlier state from the user's intent and the last frame, then describe how [things] gradually approach the reference image."

---

## 12. Wrong or malformed instruction-line phrasing

I2VA, FL2VA, and L2VA each require one specific fixed-phrasing instruction line as the first line of the prompt, followed by a blank line before the core fields. Paraphrasing it, dropping required brackets, or misordering the shot/timestamp references is a formatting error.

**Bad (I2VA):**
```text
Note: Picture 1 is the first frame of the video at Shot 1.

integrated_multimodal_description: [Shot 1] ...
```

**Good (I2VA):**
```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] ...
```

**Bad (FL2VA):**
```text
Picture 1 is the start and Picture 2 is the end at 8 seconds.

integrated_multimodal_description: [Shot 1] ...
```

**Good (FL2VA):**
```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the 8.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] ...
```

*Why:* Guide §2.1 gives the exact fixed phrasing for each mode and requires it as "the first line of the final prompt, followed by one blank line before the core fields." The timestamp must also use exactly two decimal places (`S.SS`).

---

## 13. On-screen text not quoted, or translated instead of preserved verbatim

Any visible banner, sign, subtitle, or neon text must appear in English double quotation marks, exactly as written, with no translation.

**Bad:**
```text
A red neon sign reading Open For Business glows above the doorway.
```
(missing quotes, and if the source text was non-English, translating it rather than preserving the original)

**Good:**
```text
A red neon sign reading "营业中" glows above the doorway.
```

*Why:* Guide §4.5: "Place any banner, sign, label, subtitle, or neon text that is actually visible on screen in English double quotation marks. Preserve the original text and punctuation verbatim, without translation."
