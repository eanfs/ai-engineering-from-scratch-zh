#!/bin/bash
# 用法：compress.sh <作品目录> <输出文件名>  —— 两遍编码压到 25 MB 以下
set -eu
P="$(cd "$1" && pwd)"
NAME="$2"
OUT="${DASHI_OUT:-$(cd "$(dirname "$0")/.." && pwd)/output}"
mkdir -p "$OUT"
DST="$OUT/$NAME.mp4"
rm -f "$DST"
ffmpeg -y -v error -i "$P/成片_full.mp4" -c:v libx264 -preset slow -tune animation -b:v 640k -pass 1 -passlogfile /tmp/dashi2p -an -f null /dev/null
ffmpeg -y -v error -i "$P/成片_full.mp4" -c:v libx264 -preset slow -tune animation -b:v 640k -pass 2 -passlogfile /tmp/dashi2p -c:a aac -b:a 64k -movflags +faststart "$DST"
echo "COMPRESS_OK $(ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate:format=duration,size -of compact "$DST")"
