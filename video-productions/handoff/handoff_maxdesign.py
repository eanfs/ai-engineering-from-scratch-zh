#!/usr/bin/env python3
"""Submit a handoff package to the MiniMax Design MCP server.

Dry-run by default: prints the calls it would make. Generation calls need
--i-approve-cost, the spend gate described in README.md. `refs` only imports
files, so it never bills.

Usage:
  python3 handoff_maxdesign.py plan   07-07-gpt-causal-lm
  python3 handoff_maxdesign.py refs   07-07-gpt-causal-lm
  python3 handoff_maxdesign.py images 07-07-gpt-causal-lm --i-approve-cost
  python3 handoff_maxdesign.py videos 07-07-gpt-causal-lm --i-approve-cost

State (composition, delivered resources, generated page images) is written to
<job>/outputs/maxdesign/state.json so later commands can resume.
"""
import argparse
import json
import pathlib
import shutil
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
URL = "http://127.0.0.1:18810/mcp"
SESSION_FILE = pathlib.Path("/tmp/minimax_mcp_session.txt")


class Mcp:
    def __init__(self):
        self.sid = None

    def _post(self, payload, expect_session=False):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.sid:
            headers["mcp-session-id"] = self.sid
        req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers=headers)
        with urllib.request.urlopen(req, timeout=600) as resp:
            if expect_session:
                self.sid = resp.headers.get("mcp-session-id") or self.sid
            body = resp.read().decode()
        for line in body.splitlines():
            if line.startswith("data: "):
                doc = json.loads(line[6:])
                result = doc.get("result", doc)
                if isinstance(result, dict) and "content" in result:
                    for item in result["content"]:
                        if item.get("type") == "text":
                            return item["text"]
                return json.dumps(result, ensure_ascii=False)
        return body

    def connect(self):
        self._post({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                       "clientInfo": {"name": "handoff-maxdesign", "version": "2"}},
        }, expect_session=True)
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})
        if self.sid:
            SESSION_FILE.write_text(self.sid)

    def call(self, name, arguments):
        payload = {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                   "params": {"name": name, "arguments": arguments}}
        return self._post(payload)

    def json(self, name, arguments):
        raw = self.call(name, arguments)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            sys.exit(f"{name}: unparsed response:\n{raw}")


def load(episode):
    path = pathlib.Path(__file__).resolve().parent / f"{episode}.json"
    return json.loads(path.read_text())


def job_dir(hand):
    return ROOT / hand["source_job"]


def state_path(hand):
    return job_dir(hand) / "outputs/maxdesign/state.json"


def load_state(hand):
    path = state_path(hand)
    return json.loads(path.read_text()) if path.exists() else {}


def save_state(hand, state):
    path = state_path(hand)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=1) + "\n")


def reference_sources(hand):
    """The four images every page image is conditioned on."""
    job = job_dir(hand)
    return [
        ("anchor1", job / "style/anchors/1.jpg", "风格参考一"),
        ("anchor5", job / "style/anchors/5.jpg", "风格参考二"),
        ("cover", job / "inputs/cover.png", "封面参考"),
    ] + [(page["page"], job / f"inputs/{page['page']}.png", f"{page['page']} 构图参考")
         for page in hand["pages"]]


def plan(hand):
    print(f"episode: {hand['episode']}  project: {hand['project_name']} ({hand['project_id']})")
    print(f"refs    deliver {len(reference_sources(hand))} images into a composition")
    clips = 0
    for page in hand["pages"]:
        plan_clips = page.get("clip_plan") or [page.get("target_seconds", 15)]
        clips += len(plan_clips)
        print(f"  {page['page']}  image 2k 16:9  {page['title']}  "
              f"({page['page_seconds']:.2f}s page)")
        print(f"  {page['page']}  video H3  {plan_clips}  audio off")
    print(f"totals  {len(hand['pages'])} images, {clips} clips")
    print("then fetch, retime, concat, mux narration, burn captions, verify")


def open_project(hand, mcp):
    res = mcp.json("open_project", {"projectId": hand["project_id"]})
    if "error" in res:
        sys.exit(f"open_project failed: {res['error']['message']}")


def deliver_refs(hand, mcp, state):
    sources = reference_sources(hand)
    args = {
        "requestId": f"{hand['episode']}-refs-1",
        "sources": [{"key": key, "path": str(path)} for key, path, _ in sources],
        "output": {
            "resources": [{"key": key, "mode": "create", "name": name}
                          for key, _, name in sources],
            "composition": {
                "type": {"label": "分镜"},
                "name": hand["project_name"],
                "placements": [{"key": key,
                                "role": "风格参考" if key.startswith("anchor") else (
                                    "封面参考" if key == "cover" else "构图参考")}
                               for key, _, _ in sources],
            },
        },
    }
    res = mcp.json("deliver", args)
    if "error" in res:
        sys.exit(f"deliver failed: {res['error']['message']}")
    delivery = res["delivery"]
    state["compositionId"] = delivery["placements"][0]["compositionId"]
    state["refs"] = {out["key"]: out["resourceId"] for out in delivery["outputs"]}
    save_state(hand, state)
    print(f"delivered {len(delivery['outputs'])} refs into {state['compositionId']}")
    for key, rid in state["refs"].items():
        print(f"  {key}  {rid}")


def run_execute(mcp, args, label):
    res = mcp.json("execute", args)
    if "error" in res:
        sys.exit(f"{label}: {res['error']['message']}")
    task = res["task"]
    if task["status"] == "waiting_user":
        problem = task.get("problem") or {}
        sys.exit(f"{label}: task {task['id']} is waiting for the user "
                 f"({problem.get('source')}/{problem.get('code')}: {problem.get('message')}). "
                 f"Revisions: {task['revision']}. Nothing was generated.")
    if task["status"] != "completed":
        print(f"{label}: task {task['id']} {task['status']}; call task_wait")
    return task


def page_references(state, page):
    refs = state.get("refs") or {}
    return [{"resourceId": refs[key]}
            for key in ("anchor1", "anchor5", "cover", page["page"])]


def submit_images(hand, mcp, state):
    for page in hand["pages"]:
        args = {
            "capabilityId": hand["image_model"]["id"],
            "prompt": page["image_prompt"],
            "params": {"aspect_ratio": "16:9", "resolution": "2k"},
            "references": page_references(state, page),
            "output": {
                "resources": [{"mode": "create", "name": f"{page['title']} 插图"}],
                "composition": {"compositionId": state["compositionId"],
                                "placements": [{"role": "分镜页"}]},
            },
        }
        task = run_execute(mcp, args, f"image {page['page']}")
        for out in task.get("outputs", []):
            print(f"  {page['page']}  {out.get('versionId')}  {out.get('resourceId')}")
            state.setdefault("pages", {})[page["page"]] = {
                "resourceId": out.get("resourceId"),
                "versionId": out.get("versionId"),
            }
        save_state(hand, state)


def submit_videos(hand, mcp, state):
    pages = (state.get("pages") or {})
    for page in hand["pages"]:
        image = pages.get(page["page"], {}).get("resourceId")
        if not image:
            sys.exit(f"video {page['page']}: no generated image yet; run `images` first")
        plan = page.get("clip_plan") or [page.get("target_seconds", 15)]
        for index, seconds in enumerate(plan):
            suffix = chr(ord("a") + index)
            prompt = page["video_prompt"]
            if len(plan) > 1:
                prompt += (f" This is part {index + 1} of {len(plan)} covering "
                           f"{seconds} seconds of the same page; keep the motion continuous "
                           f"and gentle so the parts can be cross-faded.")
            args = {
                "capabilityId": hand["video_model"]["id"],
                "prompt": prompt,
                "params": {"mode": "reference", "resolution": "2k",
                           "aspect_ratio": "16:9", "audio": False,
                           "duration": seconds},
                "references": [{"resourceId": image}],
                "output": {
                    "resources": [{"mode": "create",
                                   "name": f"{page['title']} 动画 {index + 1}"}],
                    "composition": {"compositionId": state["compositionId"],
                                    "placements": [{"role": "分镜动画"}]},
                },
            }
            task = run_execute(mcp, args, f"video {page['page']}{suffix}")
            for out in task.get("outputs", []):
                print(f"  {page['page']}{suffix}  {out.get('versionId')}  {out.get('resourceId')}")
                state.setdefault("clips", {})[f"{page['page']}{suffix}"] = {
                    "resourceId": out.get("resourceId"),
                    "versionId": out.get("versionId"),
                }
            save_state(hand, state)


def fetch_clips(hand, mcp, state):
    clips = state.get("clips") or {}
    if not clips:
        sys.exit("no clip versions in state; run `videos` first")
    target = job_dir(hand) / "outputs/maxdesign"
    target.mkdir(parents=True, exist_ok=True)
    for name, entry in sorted(clips.items()):
        version = entry.get("versionId")
        if not version:
            sys.exit(f"clip {name}: no versionId recorded")
        res = mcp.json("get_output", {"versionId": version})
        if "error" in res:
            sys.exit(f"get_output {name}: {res['error']['message']}")
        source = pathlib.Path(res.get("path") or res.get("filePath") or "")
        if not source.is_file():
            sys.exit(f"get_output {name}: no readable path in {json.dumps(res)[:300]}")
        destination = target / f"{name}.mp4"
        shutil.copyfile(source, destination)
        print(f"  {name}  {destination}  {destination.stat().st_size} B")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["plan", "refs", "images", "videos", "fetch"])
    ap.add_argument("episode")
    ap.add_argument("--i-approve-cost", action="store_true",
                    help="required before any generate_* call")
    args = ap.parse_args()
    hand = load(args.episode)
    if args.command == "plan":
        plan(hand)
        return
    if args.command in ("images", "videos") and not args.i_approve_cost:
        sys.exit("refusing to generate without --i-approve-cost")
    mcp = Mcp()
    mcp.connect()
    open_project(hand, mcp)
    state = load_state(hand)
    if args.command == "refs":
        deliver_refs(hand, mcp, state)
    elif args.command == "images":
        submit_images(hand, mcp, state)
    elif args.command == "videos":
        submit_videos(hand, mcp, state)
    else:
        fetch_clips(hand, mcp, state)


if __name__ == "__main__":
    main()
