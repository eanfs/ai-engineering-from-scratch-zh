# Live MiniMax Design state

Snapshot taken 2026-11-03 on the machine that ran the handoff. It records what
exists in the app so the next agent can resume without re-deriving ids.

## Account

Generating is blocked by balance. The probe image task settled into
`waiting_user` with:

```json
{"problem": {"source": "billing", "code": "BILLING_INSUFFICIENT",
             "message": "Balance is insufficient; top up, then retry"},
 "billing": {"estimatedCredits": 240}}
```

240 credits is the quote for one image at the capability defaults
(`resolution: 2k`, `quality: high`, `aspect_ratio: 16:9`). Nothing was
generated and nothing was billed. The task was resolved with `stop`:

| Field | Value |
|---|---|
| Task | `tsk_06b6bcbab871` |
| Final status | `accepted`, `progress.phase = stopped`, `reason = user_stopped` |
| Revision after stop | 3 |
| Outputs | none |

Do not call `retry` or `confirm_cost` on this task. After a top-up, submit a
fresh `execute` call with the same arguments and a new task is created.

## Project

| Field | Value |
|---|---|
| Name | 07-07 GPT 因果语言建模 |
| Project id | `p_7668f8b12a93c0f6dba9cde7` |
| Folder | `/Users/lirichen/Movies/Hub/Projects/07-07 GPT 因果语言建模` |
| Open | yes, at snapshot time |

The project starts empty and every `initialize` on the MCP server opens a new
session with no project, so always call `open_project` first.

## Composition

| Field | Value |
|---|---|
| Composition id | `cmp_9e2ddfe54faa` |
| Type label | 分镜 |
| Name | 07-07 GPT 因果语言建模 |
| Revision | 2 |

Created implicitly by the `deliver` call, because created resources must have a
place in a composition.

## Delivered references

| Key | Resource | Version | Role |
|---|---|---|---|
| anchor1 | `res_14419caf785c` | `ver_bfbd794ff639` | 风格参考 |
| anchor5 | `res_9d5702a690d8` | `ver_33cdc4433290` | 风格参考 |
| cover | `res_15855867dacd` | `ver_a9546eca473c` | 封面参考 |
| p01 | `res_687b04ec3a4b` | `ver_2b219a91c2b1` | 构图参考 |

Request id `0707-refs-2`, delivery status `completed`, every placement
`applied`. The remaining eight page references (`p02`–`p09`) are **not** in the
project yet; `handoff_maxdesign.py refs` delivers them (`0707-refs-1` is the
request id it will use, and re-running the four above is harmless).

Source files for all of them are in
`video-productions/handdraw-jobs/07-07-gpt-causal-lm/`
(`style/anchors/1.jpg`, `style/anchors/5.jpg`, `inputs/cover.png`,
`inputs/p01..p09.png`).

## Nothing else exists

- No generated page image.
- No clip.
- No download in `outputs/maxdesign/`.
- Local `state.json` has not been written yet, because `refs` was run by hand
  before the script existed. Running `handoff_maxdesign.py refs` writes it.

## What the file system holds

```text
video-productions/handdraw-jobs/07-07-gpt-causal-lm/
  job.json, design.json, design/, options/
  style/{catalog,selection,resolved}.json, style/anchors/1..13.jpg
  inputs/p01..p09.png, inputs/cover.png, inputs/music.wav
  inputs/narration/{script.txt,master.wav,master-original.wav,
                    alignment.json,boundaries.json}
  work/clean-*.json
  outputs/            # empty at snapshot
```

`alignment.json` is the timing authority: 27 beats, pages `p01`–`p09`,
narration ends at 144.703 s.

## Local rail readiness

`design/drawing-plan.preflight.json` was generated for both episodes on
2026-11-03 with the skill's `drawing_contract.py` (status
`ready_for_generation`, 9 illustrations each). Still missing before `build`
will run:

- `design/art-direction.json` — per-image review record.
- `design/drawing-review.json` — per-illustration narrative checks.

Both are review artifacts: they bind image, brief and prompt hashes and carry
prose evidence about what the page actually shows, so they cannot be generated
without looking at the images. `handdraw-jobs/07-06-bert-mlm/design/` holds a
filled-in example of each shape.

A preview film for 07-07 was assembled on 2026-11-03 from the local page images
(`outputs/maxdesign/preview.mp4`, 146.353 s) to validate the timing, caption,
mux and verification chain without spending anything.

