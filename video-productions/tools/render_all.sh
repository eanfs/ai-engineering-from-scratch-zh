#!/bin/bash
# 用法：render_all.sh <作品目录> [每段秒数=43.4]  —— 分段渲染（断点续跑）+ 拼接混音 → 成片_full.mp4
set -u
SKILL="${DASHI_SKILL:-$HOME/video-skills/dashi-animationstyle}"
P="$(cd "$1" && pwd)"
SEG=${2:-43.4}
cd "$P" || exit 1
DUR=$(python3 -c "import json;d=json.load(open('分镜.json'));print(d.get('duration') or json.load(open('字幕.json'))['duration'])")
N=$(python3 -c "import math;print(max(1,math.ceil(float('$DUR')/float('$SEG'))))")
echo "片长 $DUR 秒，切成 $N 段（每段 $SEG 秒）"
mkdir -p seg && : > seg/list.txt
for k in $(seq 0 $((N-1))); do
  f="seg/seg$k.mp4"
  printf "file '%s'\n" "$P/$f" >> seg/list.txt
  if [ -f "$f.done" ] && [ -s "$f" ]; then echo "跳过已完成段 $k"; continue; fi
  a=$(python3 -c "print($k*$SEG)")
  b=$(python3 -c "print(min(float('$DUR'), ($k+1)*$SEG))")
  echo "=== 段 $k: $a - $b ==="
  t0=$(date +%s)
  node "$SKILL/pipeline/render.mjs" "$P/index.html" --format jpeg --no-audio --from "$a" --to "$b" -o "$f" 2>&1 | tail -2
  if [ -s "$f" ]; then touch "$f.done"; echo "段 $k 完成，用时 $(( $(date +%s) - t0 )) 秒"; else echo "段 $k 失败"; exit 1; fi
done
echo "=== 拼接混音 ==="
ffmpeg -y -v error -f concat -safe 0 -i seg/list.txt -i "$P/口播.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k -af apad -shortest "$P/成片_full.mp4"
echo "CONCAT_OK $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$P/成片_full.mp4")"
