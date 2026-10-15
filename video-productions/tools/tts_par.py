#!/usr/bin/env python3
# 用法：tts_par.py <作品目录>  —— 并发逐句 TTS（断点续跑），输出 <作品目录>/tts/NN.mp3
import os, subprocess, sys, concurrent.futures as cf

work = sys.argv[1]
EDGE = os.environ.get("EDGE_TTS", os.path.expanduser("~/video-skills/venv/bin/edge-tts"))
VOICE = os.environ.get("DASHI_VOICE", "zh-CN-XiaoxiaoNeural")
RATE = os.environ.get("DASHI_RATE", "+15%")
TTS = os.path.join(work, "tts"); os.makedirs(TTS, exist_ok=True)
lines = [l for l in open(os.path.join(work, "稿子.txt"), encoding="utf-8").read().splitlines() if l.strip()]

def ok(p):
    if not os.path.exists(p) or os.path.getsize(p) < 1500: return False
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p], capture_output=True, text=True)
    try: return float(r.stdout.strip()) > 0.3
    except Exception: return False

def gen(i):
    n = f"{i:02d}"; out = os.path.join(TTS, n + ".mp3")
    if ok(out): return (i, "skip")
    for _ in range(5):
        subprocess.run([EDGE, "--voice", VOICE, "--rate", RATE, "--text", lines[i-1], "--write-media", out], capture_output=True, text=True)
        if ok(out): return (i, "ok")
    return (i, "FAIL")

with cf.ThreadPoolExecutor(max_workers=6) as ex:
    res = list(ex.map(gen, range(1, len(lines) + 1)))
bad = [i for i, s in res if s == "FAIL"]
print(f"{os.path.basename(work)}: 共 {len(lines)} 句，完成 {len(res)-len(bad)}，失败 {bad}")
sys.exit(1 if bad else 0)
