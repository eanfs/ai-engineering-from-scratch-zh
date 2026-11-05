# Runbook: finish a hand-drawn episode in MiniMax Design

This is the operating manual for an agent picking up the handoff. It assumes
no context from the session that wrote it. Read `README.md` first for the
transport and the verified MCP call shapes, then this file for the work order.

The repo episode is the source of truth for narration, timing, captions and
acceptance. MiniMax Design only supplies the nine redrawn page images and the
image-to-video clips. Everything that decides whether the film is correct —
the narration master, the caption timing, the loudness, the final encode — runs
locally.

## Where things stand

| Episode | Project | State |
|---|---|---|
| 07-07 GPT 因果语言建模 | `p_7668f8b12a93c0f6dba9cde7` | 4 refs delivered, image probe blocked by billing |
| 07-08 T5 与 BART | not created | brief ready, nothing submitted |

`STATE.md` holds the live project snapshot: composition id, delivered resource
ids, the stopped task, and the exact error that blocked generation.

Local job directories are complete for the visual and voice inputs, but not
ready to build. This is the per-job readiness as of 2026-11-03:

| Artifact | 07-07 | 07-08 |
|---|---|---|
| `job.json`, `design.json`, `style/`, `options/` | present | present |
| `inputs/p01..p09.png`, `inputs/cover.png`, `inputs/music.wav` | present | present |
| `inputs/narration/{script.txt,master.wav,alignment.json}` | present | present |
| `design/drawing-plan.json`, `design/briefs/`, `design/prompts/` | present | present |
| `design/drawing-plan.preflight.json` | generated 2026-11-03 | generated 2026-11-03 |
| `design/art-direction.json` | **missing** | **missing** |
| `design/drawing-review.json` | **missing** | **missing** |
| `outputs/` (film, cover, verification) | preview only | empty |

`design/art-direction.json` and `design/drawing-review.json` are review
records, not generated artifacts. They bind a per-image sha256, brief and
prompt hashes, and prose evidence that describes what is actually visible on
the page; `art_direction.py` and `drawing_contract.py` reject the build when a
record is stale, missing an entry, or carries empty evidence. Use
`handdraw-jobs/07-06-bert-mlm/design/{art-direction,drawing-review}.json` as
the schema template. Do not copy their evidence text — it describes a different
episode's pages.

## Prerequisites

- The MiniMax Design app is running; the MCP server listens on
  `http://127.0.0.1:18810/mcp`. The Claude session's native MCP client may
  report `ECONNREFUSED` while the app starts. That is not a missing capability:
  open a JSON-RPC session directly (see `README.md`) and it answers.
- The account has balance. Verify with one page before submitting the batch.
- `ffmpeg` and `ffprobe` are on `PATH` (Homebrew build is fine; the assembly
  script does not need `libass` or `drawtext`).
- Assembly runs under the skill virtualenv:
  `~/.cache/sweety-handdraw-video/venv/bin/python` (it needs numpy and Pillow).

## Rail A: app-generated visuals (the intended path)

All commands are relative to the repo root. `H` is
`python3 video-productions/handoff/handoff_maxdesign.py`.

1. **Plan.** `$H plan 07-07-gpt-causal-lm` — prints the 9 image jobs and the
   per-page clip list (`clip_plan`). Cheap, no submission.
2. **References.** `$H refs 07-07-gpt-causal-lm` — delivers the two style
   anchors, the cover and the nine page images into one composition
   (`分镜`). Free; only imports files. Writes
   `<job>/outputs/maxdesign/state.json` with every resource id.
3. **Probe one image.** `$H images 07-07-gpt-causal-lm --i-approve-cost`
   submits all nine. To probe a single page first, call `execute` by hand with
   the arguments in step 4 of `README.md` and only page `p01`; inspect the
   returned version with `get_output` before spending on the rest.
4. **Review the images** against the acceptance list below. Regenerate a
   failure with `execute` + `output.resources[].mode: "new_version"` on the
   same `resourceId`; do not create a duplicate.
5. **Clips.** `$H videos 07-07-gpt-causal-lm --i-approve-cost` submits one H3
   clip per entry of each page's `clip_plan` (13 clips for 07-07, 12 for 07-08),
   `mode: reference`, `resolution: 2k`, `aspect_ratio: 16:9`, `audio: false`.
   Clips are named `p02a`, `p02b` in the state file.
6. **Download.** `$H fetch 07-07-gpt-causal-lm` copies every clip into
   `<job>/outputs/maxdesign/` as `pXXa.mp4`, `pXXb.mp4`.
7. **Assemble.** `~/.cache/sweety-handdraw-video/venv/bin/python
   video-productions/handoff/handoff_assemble.py 07-07-gpt-causal-lm` produces
   `outputs/maxdesign/film.mp4` plus `verification.json` / `verification.txt`.
8. **Review.** Read the verification report and the acceptance list; only then
   write `review.json` in the style of
   `handdraw-jobs/07-06-bert-mlm/review.json`.

Order matters: `videos` needs the image resource ids, `fetch` needs the clip
version ids, `assemble` needs the files on disk. Each step reads
`state.json`, so a stopped run resumes where it left off instead of
resubmitting.

### Why some pages have two clips

H3 caps a clip at 15 s. Four pages of 07-07 and three of 07-08 run longer than
that (up to 20.15 s). `clip_plan` splits those pages into two parts that are
cross-faded for 0.4 s and retimed onto the page window. Sending one 15 s clip
for a 20 s page would either truncate the drawing or slow it past 1.35x, so do
not collapse the plan.

### Timing contract

- Page windows come from `alignment.json`, not from the brief: page 1 runs
  from the end of the cover, every later page starts at its first beat, the
  last page ends when the narration ends.
- The film is longer than the narration by design: a 1.0 s cover and a 0.65 s
  end hold sit outside the speech. 07-07 narration is 144.703 s, so the film is
  146.353 s; 07-08 narration is 131.694 s, so the film is 133.344 s.
- The narration master starts speaking at 0.000 s — the cover lead is silence
  added at mux time (`adelay`), never a padded master. Picture and audio must
  both land within 0.08 s of the computed total.
- Retime is a `setpts` stretch onto the page window, accepted in the range
  0.5x–1.35x. Outside that range the clip is wrong — regenerate it.
- The 0.65 s hold is a frozen last frame; the 0.55 s fade is applied to the
  picture only, starting at `total − 0.55`.

### Captions

Captions are burned locally from `alignment.json` with the skill's
`caption_assets.build_caption`, using the options in `job.json.captions`
(font size 42, bottom margin 54, stroke 4, `#1E1E1E`). They are never generated
or typed in the app, so the text stays character-for-character identical to the
narration. Each cue is a full-canvas RGBA frame streamed into the final encode;
no intermediate caption file is written.

## Rail B: local hand-drawn render (zero cost fallback)

If the account cannot be topped up, the same episode can ship from the local
drawings already in `inputs/`. Two review records stand in the way first; see
the readiness table above. Once they exist:

```bash
SK=~/.hub/skills/handdrawn-explainer-video/scripts
PY=~/.cache/sweety-handdraw-video/venv/bin/python
cd video-productions/handdraw-jobs/07-07-gpt-causal-lm
$PY $SK/drawing_contract.py . design/drawing-plan.json   # refreshes the preflight receipt
$PY $SK/handdraw_video.py build .
$PY $SK/handdraw_video.py render .
$PY $SK/handdraw_video.py verify .
$PY $SK/handdraw_video.py finalize .
```

This is the rail 07-04/07-05/07-06 shipped on. It produces the
`work/timeline.json` the strict verifier needs; the app rail cannot pass that
verifier because its artifacts describe a Pillow-rendered timeline, which is
why `handoff_assemble.py` carries its own checks.

To rehearse the app rail's assembly without spending anything:

```bash
~/.cache/sweety-handdraw-video/venv/bin/python \
  video-productions/handoff/handoff_assemble.py 07-07-gpt-causal-lm --preview
```

`--preview` animates the local page images with a slow zoom and writes
`preview.mp4`. It exercises the cover lead, the page windows, the cross-fades,
the caption burn, the mux and the verification, and never touches `film.mp4`.
On 2026-11-03 it produced a 146.353 s 07-07 preview that passed every check.

## Failure modes

| Symptom | Meaning | Action |
|---|---|---|
| `ECONNREFUSED` on the native MCP client | app still starting, or client session stale | open a fresh JSON-RPC session against `127.0.0.1:18810` |
| `No project is open in this session` | every fresh `initialize` starts with no project | `open_project` before any capability or deliver call |
| `BILLING_INSUFFICIENT`, `waiting_user` | balance is short; nothing submitted, nothing billed | top up, then resubmit the same arguments; do not confirm cost for the user |
| `output.resources: ... no target is primary` | you gave the single output a `key` | omit `key` on the primary output and on its placement |
| `... would be created without a place in a Composition` | created resources need a composition member | pass `output.composition` with `placements` inside it |
| `cancelled` task | the user declined the cost prompt | do not resubmit unless the user asks again |
| `page needs 20.15s but the clips give 15.00s (1.34x)` | clip plan collapsed to one clip | regenerate the page's second clip |

## Acceptance checklist

The film passes when `verification.txt` reports `PASS`, and:

- 1920×1080, 30 fps, H.264 + AAC, duration within 0.08 s of the master.
- Audio correlation against `master.wav` above 0.99; integrated loudness within
  ±1.5 LU of −17.
- Every page keeps the exact Chinese labels of its reference image — no
  garbled or invented characters, no garbled Latin or symbols.
- Warm off-white paper, dark marker outline, warm-yellow fill, brown streaks;
  no photoreal elements, no people, no watermark.
- No camera cuts inside a page, no text animation; labels static and legible.
- Captions match `alignment.json` cue for cue and stay inside the safe area.

## Do not

- Do not generate captions, narrations or music in the app for these episodes.
- Do not overwrite `inputs/p01..p09.png`; they are the composition references.
- Do not commit `outputs/maxdesign/*.mp4`, `work/`, or `state.json` blobs of
  large media — `video-productions/.gitignore` already covers the heavy paths;
  check `git status` before committing.
- Do not treat a preview film as a deliverable.
