#!/bin/bash
# 用法：verify.sh <作品目录> <输出文件名>  —— 验收：编码/分辨率/帧率/时长 + 抽三帧（每 1/3、2/3、末尾场末，精确 seek）
set -eu
P="$(cd "$1" && pwd)"
NAME="$2"
T="${DASHI_TOOLS:-$(cd "$(dirname "$0")" && pwd)}"
OUT="${DASHI_OUT:-$(cd "$(dirname "$0")/.." && pwd)/output}"
DST="$OUT/$NAME.mp4"
echo "=== 成片 ==="
ffprobe -v error -show_entries stream=index,codec_type,codec_name,width,height,r_frame_rate:format=duration,size -of compact "$DST"
echo "=== 母版 ==="
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate:format=duration,size -of compact "$P/成片_full.mp4"
mkdir -p "$OUT/thumbs"
python3 "$T/verify_thumbs.py" "$P" "$DST" "$OUT/thumbs" "$NAME"
