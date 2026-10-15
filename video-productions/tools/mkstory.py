#!/usr/bin/env python3
# 用法：mkstory.py <作品目录> <数据 JSON>  —— 生成 分镜.json / 分镜.md，并校验每个卡点短语能在单条字幕里按 token 边界找到
import json, os, sys

work, datafile = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
subs = json.load(open(os.path.join(work, "字幕.json"), encoding="utf-8"))
scenes = json.load(open(os.path.join(work, "scenes.json"), encoding="utf-8"))
sc_cues = json.load(open(os.path.join(work, "scene_cues.json"), encoding="utf-8"))
data = json.load(open(datafile, encoding="utf-8"))

cue_by_id = {c["id"]: c for c in subs["cues"]}
tokens_by_cue = {c["id"]: [ch["text"] for ch in subs["chars"] if ch["cue"] == c["id"]] for c in subs["cues"]}

def find_cue(scene, line_idx, phrase):
    sent = [s for s in subs["sentences"] if s["scene"] == scene][line_idx - 1]
    for cid in sent["cues"]:
        toks = tokens_by_cue[cid]
        for i in range(len(toks)):
            s = ""
            for j in range(i, len(toks)):
                s += toks[j]
                if s == phrase:
                    return cid
                if not phrase.startswith(s):
                    break
    return None

marks, missing = [], []
for m in data["marks"]:
    cid = find_cue(m["scene"], m["line"], m["phrase"])
    if cid is None:
        missing.append(m)
    else:
        marks.append({"name": m["name"], "cue": cid, "phrase": m["phrase"]})

shots = []
for i, sc in enumerate(scenes, 1):
    meta = data["shots"].get(str(i), {})
    shots.append({
        "id": i,
        "cues": sc_cues[f"s{i:02d}"],
        "title": sc["title"],
        "关键字": meta.get("关键字", []),
        "时间点": [m["name"] for m in data["marks"] if m["scene"] == i],
        "要讲清": meta.get("要讲清", ""),
        "运动设想": meta.get("运动设想", ""),
        "变化": meta.get("变化", ""),
    })

story = {
    "说明": f"{data['集']} 的分镜：{len(scenes)} 场 = {len(scenes)} 个镜头，每场 3 句。时间单位秒，取自同目录 口播.wav（逐句 TTS 拼接）。高亮 = 全片固定上色的两个词；字幕强调 = 橙色波浪下划线。",
    "duration": round(subs["duration"] + 1.0, 3),
    "fps": 30, "size": [1920, 1080],
    "标题": data["标题"],
    "高亮": data["高亮"],
    "字幕强调": data["字幕强调"],
    "shots": shots,
    "marks": marks,
}
json.dump(story, open(os.path.join(work, "分镜.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

md = [f"# {data['标题']} · 分镜", "",
      f"片长 {story['duration']} 秒，{len(shots)} 个镜头，{len(marks)} 个卡点。",
      "高亮：" + "／".join(f"{h['text']}（{h['role']}）" for h in data["高亮"]) + "；字幕强调：" + "、".join(data["字幕强调"]) + "。", "",
      "| # | 时间 | 标题 | 关键字 | 要讲清 |", "|---|---|---|---|---|"]
for s in shots:
    st, en = cue_by_id[s["cues"][0]]["start"], cue_by_id[s["cues"][-1]]["end"]
    md.append(f"| {s['id']} | {st:.1f}–{en:.1f} | {s['title']} | {'、'.join(s['关键字'])} | {s['要讲清']} |")
md += ["", "## 卡点", "", "| 名字 | 场 | 短语 | 字幕条 |", "|---|---|---|---|"]
for m in marks:
    sc = next(x["scene"] for x in data["marks"] if x["name"] == m["name"])
    md.append(f"| {m['name']} | s{sc:02d} | {m['phrase']} | {m['cue']} |")
open(os.path.join(work, "分镜.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")

print(f"{data['集']}: 镜头 {len(shots)}，卡点 {len(marks)}/{len(data['marks'])}，片长 {story['duration']} 秒")
if missing:
    print("找不到的卡点（短语被字幕切断或写错，需要改）：")
    for m in missing:
        print(f"   {m['name']} s{m['scene']:02d} 句{m['line']} 「{m['phrase']}」")
    sys.exit(1)
