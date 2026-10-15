#!/usr/bin/env python3
# 由 line_times.json（精确句界）生成 字幕.json / 字幕.srt / scene_cues.json
# 句界零误差；句内按标点均衡分组（视觉宽度 <= 20 字，英文词/数字整体算一个单位，不在词中间断开）；句内按宽度分摊时间。
import json, os, re, math, sys

WORK = os.path.abspath(sys.argv[1])   # 用法：mksub.py <作品目录>
MAXW = 20.0
PUNCT = "，。：；、？！"          # 只做切点的中文标点（ASCII 的 . 和 , 是小数、括号内的分隔，绝不当切点）
TRIM = "，。：；、？！"          # 去首尾只去中文标点：ASCII 的 . 和 , 属于内容（0.389、(N, d_model)）

lt = json.load(open(os.path.join(WORK, "line_times.json"), encoding="utf-8"))
lines = lt["lines"]

def vw(s):
    w = 0.0
    for ch in s:
        w += 0.55 if ord(ch) < 0x2000 else 1.0
    return w

def strip_p(s):
    return re.sub(r"^[\s" + re.escape(TRIM) + r"]+|[\s" + re.escape(TRIM) + r"]+$", "", s)

def tokenize(s):
    """单位：连续 ASCII 字母/数字/._- 算一个；其余每字符一个"""
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if re.match(r"[0-9A-Za-z]", ch):
            j = i
            while j < len(s) and re.match(r"[0-9A-Za-z._\-']", s[j]):
                j += 1
            out.append(s[i:j]); i = j
        else:
            out.append(ch); i += 1
    return out

def hard_split(seg, maxw):
    """超宽段按单位边界均衡切开（每条尽量等宽、且不超过 maxw）"""
    toks = tokenize(seg)
    W = sum(vw(t) for t in toks)
    if W <= maxw:
        return [seg]
    n = max(2, math.ceil(W / maxw))
    target = W / n
    res, cur, acc = [], [], 0.0
    for tk in toks:
        if cur and (acc >= target or acc + vw(tk) > maxw):
            res.append("".join(cur)); cur, acc = [], 0.0
        cur.append(tk); acc += vw(tk)
    if cur:
        res.append("".join(cur))
    return res

def split_line(text, maxw=MAXW):
    """token 级均衡切分：每条宽度尽量接近平均、且不超过 maxw；切点优先落在中文标点后或空格后"""
    toks = tokenize(text)
    if not toks:
        return [text]
    W = sum(vw(t) for t in toks)
    if W <= maxw:
        return [text]
    n = max(2, math.ceil(W / maxw))
    target = W / n
    cum = [0.0]
    for t in toks:
        cum.append(cum[-1] + vw(t))
    cuts = []
    for g in range(1, n):
        ideal = target * g
        k = min(range(1, len(toks) + 1), key=lambda i: abs(cum[i] - ideal))
        best = k
        prev_cut = cuts[-1] if cuts else 0
        for d in range(0, 5):
            found = None
            for cand in ([k + d, k - d] if d else [k]):
                if 1 <= cand < len(toks) and (toks[cand - 1] in PUNCT or toks[cand - 1] == ' '):
                    found = cand; break
            if found is not None:
                if cum[found] - cum[prev_cut] <= maxw:
                    best = found
                break
        if cum[best] - cum[prev_cut] > maxw:
            best = min(range(prev_cut + 1, len(toks) + 1), key=lambda i: abs(cum[i] - (cum[prev_cut] + maxw)))
        cuts.append(best)
    parts, prev = [], 0
    for c in sorted(set(cuts)) + [len(toks)]:
        if c <= prev:
            continue
        parts.append("".join(toks[prev:c])); prev = c
    out = []
    for p in parts:
        p2 = strip_p(p)
        if not p2:
            continue
        out.extend(hard_split(p2, maxw) if vw(p2) > maxw else [p2])
    return out

scenes = json.load(open(os.path.join(WORK, "scenes.json"), encoding="utf-8"))
scene_of = []
for si, sc in enumerate(scenes, 1):
    for _ in sc["lines"]:
        scene_of.append(si)

cues, chars, sentences = [], [], []
cid = 1
for ln in lines:
    i, text, t0, t1 = ln["i"], ln["text"], ln["start"], ln["end"]
    parts = split_line(text)
    clean_parts = [strip_p(p) for p in parts]
    clean_parts = [c for c in clean_parts if c]
    weights = [max(vw(c), 0.5) for c in clean_parts]
    total_w = sum(weights) or 1
    dur = t1 - t0
    ids, cur_t = [], t0
    for c, w in zip(clean_parts, weights):
        d = dur * w / total_w
        st = cur_t; cur_t += d
        cue = {"id": cid, "text": c, "start": round(st, 3), "end": round(cur_t, 3)}
        cues.append(cue); ids.append(cid)
        toks = tokenize(c); n = len(toks) or 1
        for k, tk in enumerate(toks):
            chars.append({"text": tk, "start": round(st + d * k / n, 3), "end": round(st + d * (k + 1) / n, 3), "cue": cid})
        cid += 1
    sentences.append({"id": i, "scene": scene_of[i - 1], "text": text, "start": round(t0, 3),
                      "end": round(t1, 3), "cues": ids})

for c in cues:
    c["show"] = round(max(0.0, c["start"] - 0.05), 3)
for k, c in enumerate(cues):
    nxt = cues[k + 1] if k + 1 < len(cues) else None
    c["hide"] = round(nxt["show"], 3) if nxt else round(c["end"] + 0.25, 3)

duration = round(cues[-1]["hide"], 3)
subs = {
    "说明": "时间单位为秒，都是同目录 口播.wav 里的时间。start/end 是语音起止（39 句逐句 TTS 拼接时的精确时间，零误差）；show/hide 是画面上显示字幕的时间。",
    "duration": duration,
    "text": "".join(l["text"] for l in lines),
    "speech": {"start": cues[0]["start"], "end": round(lines[-1]["end"], 3)},
    "sentences": sentences,
    "cues": cues,
    "chars": chars,
}
json.dump(subs, open(os.path.join(WORK, "字幕.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def ts(s):
    ms = int(round(s * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); sec, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"
with open(os.path.join(WORK, "字幕.srt"), "w", encoding="utf-8") as f:
    for k, c in enumerate(cues, 1):
        f.write(f"{k}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['text']}\n\n")

sc_cues = {}
for s in sentences:
    sc_cues.setdefault(f"s{s['scene']:02d}", []).extend(s["cues"])
json.dump(sc_cues, open(os.path.join(WORK, "scene_cues.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"字幕 {len(cues)} 条，字级 {len(chars)} 个单位，时长 {duration} 秒")
print("每场条数：", {k: len(v) for k, v in sc_cues.items()})
over = [(c["id"], c["text"], round(vw(c["text"]), 1)) for c in cues if vw(c["text"]) > MAXW + 0.01]
print("超宽条：", over)
short = [(c["id"], c["text"]) for c in cues if vw(c["text"]) < 3]
print("过短条：", short)
for c in cues[:6] + cues[-4:]:
    print(f"  {c['id']:3d} {c['start']:7.2f}-{c['end']:7.2f} {c['text']}")