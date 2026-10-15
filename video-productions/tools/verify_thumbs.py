#!/usr/bin/env python3
# 用法：verify_thumbs.py <作品目录> <成片> <输出目录> <名字> —— 在每 1/3、2/3、末尾的场末抽一帧（精确 seek）
import json, os, subprocess, sys

P, dst, outdir, name = sys.argv[1:5]
subs = json.load(open(os.path.join(P, "字幕.json"), encoding="utf-8"))
story = json.load(open(os.path.join(P, "分镜.json"), encoding="utf-8"))
cue = {c["id"]: c for c in subs["cues"]}
shots = story["shots"]
picks = [shots[len(shots) // 3 - 1], shots[2 * len(shots) // 3 - 1], shots[-1]]
for sh in picks:
    s = round(cue[sh["cues"][-1]]["end"] - 0.25, 2)
    p = os.path.join(outdir, "%s-s%02d-%ss.jpg" % (name, sh["id"], s))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", dst, "-ss", str(s), "-frames:v", "1", "-q:v", "2", p], check=True)
    print("thumb", "s%02d" % sh["id"], s, p)
