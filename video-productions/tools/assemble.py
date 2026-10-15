#!/usr/bin/env python3
# 用法：assemble.py <作品目录>  —— 拼接 tts/NN.mp3 为 口播.wav，并写 line_times.json（精确句界）
import json, os, subprocess, sys

work = sys.argv[1]
TTS = os.path.join(work, "tts"); AUD = os.path.join(work, "aud")
os.makedirs(AUD, exist_ok=True)
scenes = json.load(open(os.path.join(work, "scenes.json"), encoding="utf-8"))
scene_of = [si for si, sc in enumerate(scenes, 1) for _ in sc["lines"]]
lines = [l for l in open(os.path.join(work, "稿子.txt"), encoding="utf-8").read().splitlines() if l.strip()]
N = len(lines)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError(" ".join(cmd) + "\n" + r.stderr[-800:])
    return r.stdout
def dur(p): return float(run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).strip())

parts = []
for i in range(1, N + 1):
    n = f"{i:02d}"; mp3 = os.path.join(TTS, n + ".mp3"); wav = os.path.join(AUD, n + ".wav")
    if not os.path.exists(wav) or os.path.getmtime(wav) < os.path.getmtime(mp3):
        run(["ffmpeg","-y","-v","error","-i",mp3,"-ac","1","-ar","24000",wav])
    parts.append(wav)

LEAD, IN_SCENE, BETWEEN = 0.5, 0.45, 0.9
def sil(sec, name):
    p = os.path.join(AUD, name)
    if not os.path.exists(p): run(["ffmpeg","-y","-v","error","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(sec),p])
    return p
s_lead, s_in, s_bet = sil(LEAD,"g_head.wav"), sil(IN_SCENE,"g_line.wav"), sil(BETWEEN,"g_scene.wav")

seq, times, t = [s_lead], [], LEAD
for i, w in enumerate(parts, 1):
    d = dur(w)
    times.append({"i": i, "scene": scene_of[i-1], "text": lines[i-1], "start": round(t,4), "end": round(t+d,4)})
    seq.append(w); t += d
    if i < N:
        g = s_bet if scene_of[i] != scene_of[i-1] else s_in
        seq.append(g); t += dur(g)

lf = os.path.join(AUD, "list.txt")
with open(lf, "w") as f: [f.write("file '%s'\n" % p.replace("'", "'\\''")) for p in seq]
out = os.path.join(work, "口播.wav")
run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",lf,"-ar","48000","-ac","1",out])
real = dur(out)
json.dump({"lines": times, "total": round(real,4)}, open(os.path.join(work,"line_times.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{os.path.basename(work)}: {N} 句，口播 {real:.2f} 秒（累计 {t:.2f}）")
