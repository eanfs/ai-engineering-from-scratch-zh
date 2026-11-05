# MiniMax Design handoff

This directory holds the handoff package for producing a `handdraw-jobs` episode
inside the MiniMax Design app instead of the local Pillow renderer. The local
job stays the source of truth for narration timing, captions and acceptance.

## Scope

| Episode | Handoff | Project |
|---|---|---|
| 07-07 GPT 因果语言建模 | `07-07-gpt-causal-lm.md` / `.json` | `p_7668f8b12a93c0f6dba9cde7` (created, nothing generated) |
| 07-08 T5 与 BART | `07-08-t5-bart.md` / `.json` | not created yet |

Start with **`RUNBOOK.md`** (the work order) and **`STATE.md`** (the live
project snapshot). This file covers the transport and the call shapes.

| File | Role |
|---|---|
| `RUNBOOK.md` | step-by-step work order, timing contract, failure table, acceptance |
| `STATE.md` | ids, delivered resources, the stopped billing task |
| `handoff_maxdesign.py` | `plan`, `refs`, `images`, `videos`, `fetch` against the MCP server |
| `handoff_assemble.py` | retime, concat, caption burn, mux, verify; `--preview` renders from local stills |

## What the app owns

- 9 redrawn page images per episode (`generate_image:gpt-image-2.5-sunburst`, 2K).
- Image-to-video clips (`generate_video:MiniMax-H3`, 2K, 16:9, `audio:false`).
  One clip per page when the page fits in 15 s, two cross-faded clips when it
  does not: 13 clips / 150 s for 07-07, 12 clips / 141 s for 07-08, as listed in
  each page's `clip_plan`.

## What stays local

- `inputs/narration/master.wav` and `alignment.json` (already produced with edge-tts).
- Caption burn-in, retiming, concat, mux, verification, and `review.json`.
- The hand-drawn look is defined by `style/anchors/1.jpg`, `style/anchors/5.jpg`
  and `inputs/cover.png`, which are passed as image references on every page.

## Transport

The `minimax-design` MCP server listens on `http://127.0.0.1:18810/mcp`
(Streamable HTTP). The Claude session's MCP client may report `ECONNREFUSED`
while the app is still starting; initialize a fresh JSON-RPC session and reuse
the returned `mcp-session-id` header:

```bash
curl -s -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -X POST http://127.0.0.1:18810/mcp \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{
        "protocolVersion":"2024-11-05","capabilities":{},
        "clientInfo":{"name":"claude-code","version":"1"}}}'
```

Then `tools/call` with `{"name": "...", "arguments": {...}}` and the
`mcp-session-id` response header. `handoff_maxdesign.py` wraps that sequence;
every MCP session starts with no project open, so `open_project` comes first.

## Call sequence per episode

`handoff_maxdesign.py` implements these steps and keeps the ids it needs in
`<job>/outputs/maxdesign/state.json`, so a stopped run resumes instead of
resubmitting.

1. `open_project` with the id from `STATE.md` (or `create_project` for 07-08).
2. `deliver` the two style anchors, the cover and `inputs/p01..p09.png` into one
   composition; this is the `refs` command and costs nothing.
3. `execute` `generate_image` per page: the brief's prompt, `aspect_ratio:
   "16:9"`, `resolution: "2k"`, the four references attached.
4. Review the nine images against the acceptance list; regenerate only failures
   with `new_version` on the same resource.
5. `execute` `generate_video` per `clip_plan` entry: `MiniMax-H3`, mode
   `reference`, `resolution: "2k"`, `aspect_ratio: "16:9"`, `audio: false`.
6. `get_output` each version into
   `video-productions/handdraw-jobs/<episode>/outputs/maxdesign/`.
7. Run `handoff_assemble.py`: retime to the page window, cross-fade the parts,
   concat, mux the narration master, burn captions, verify.

## Cost gate

Nothing has been generated. H3 is quoted at about ¥0.23/s on the current yearly
plan; 13 clips totalling 150 s are roughly ¥35 for 07-07 before image redraws and
retries (12 clips / 141 s, about ¥32, for 07-08). Image pricing is metered by the app. Do not call `execute`
until the spend is approved; the briefs carry the exact prompts so approval can
be given once and reused.

The first probe on 2026-11-03 was stopped at the billing gate. A default image
(`2k`, `quality: high`) is quoted at 240 credits, and `execute` returned
`waiting_user` with `problem.source: "billing"`, `problem.code:
"BILLING_INSUFFICIENT"` (`Balance is insufficient; top up, then retry`). The
task was resolved with `stop`; nothing was generated or billed. Top up the
account, then resubmit the same call — the frozen request is reusable.

## Verified call shapes

The schema descriptions do not spell these out; each was confirmed against a
live call.

- `deliver` needs `output.composition`, not a top-level `placements` array:
  `{"sources": [{"key","path"}...],
    "output": {"resources": [{"key","mode":"create","name"}...],
               "composition": {"type": {"label": "分镜"}, "name": "...",
                               "placements": [{"key","role"}...]}}}`
  Every created Resource must be placed, or the call is rejected with
  `Nothing was submitted`.
- `execute` addresses its primary output with no `key`; adding one fails with
  "no target is primary". Additional outputs are the only entries that carry a
  `key`. The same applies to the matching entry in
  `output.composition.placements`.
- References are `{"resourceId": "res_..."}` (follows the current version) or
  `{"versionId": "ver_..."}` (pins an exact version); media paths never go in
  `params`.

## Fallback

If the MCP server is unreachable and the app UI is needed instead, drive
`com.minimax.hub` with `orca computer` (`/computer-use`): open the project,
paste the `.md` brief into the chat, attach the same references, then copy the
finished takes out of the project folder
(`~/Movies/Hub/Projects/<project name>/`). `/orchestration` can run one Orca
worker per episode against the same call sequence when both episodes are
approved; workers must not call `execute` without the coordinator's spend
approval.
