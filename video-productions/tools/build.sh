#!/bin/bash
# 用法：build.sh <集号> <作品目录> <场景代码目录> [场景文件数=2]
# 前提：作品目录里已有 口播.wav / scenes.json / 稿子.txt（先跑 prepare.sh）
# 分镜数据默认取 ../data/story_<集号>.json（data/ 不入库）；
# 分镜跟着剧集代码一起入库时，用 DASHI_STORY 指定到剧集目录里。
set -eu
T="$(cd "$(dirname "$0")" && pwd)"
SKILL="${DASHI_SKILL:-$T/../../skills/dashi-animationstyle}"
EP="$1"; WORK="$2"; SRCDIR="$3"; NFILES="${4:-2}"
DATA="${DASHI_STORY:-$T/../data/story_$EP.json}"
[ -f "$DATA" ] || { echo "缺分镜数据 $DATA"; exit 1; }
mkdir -p "$WORK"
node "$SKILL/pipeline/新建作品.mjs" "$WORK" --style 手绘笔记 --audio "$WORK/口播.wav" --script "$WORK/稿子.txt" 2>&1 | tail -2
cd "$WORK"
node "$SKILL/pipeline/字幕.mjs" "$WORK" --no-whisper >/dev/null 2>&1 || true
[ -f 字幕.json ] && mv -f 字幕.json 字幕_工具版.json || true
[ -f 字幕.srt ] && mv -f 字幕.srt 字幕_工具版.srt || true
python3 "$T/mksub.py" "$WORK"
python3 "$T/mkstory.py" "$WORK" "$DATA"
node "$SKILL/pipeline/生成timeline.mjs" "$WORK"
python3 "$T/make_page.py" "$WORK" "$SRCDIR" "$NFILES"
echo "BUILD_OK $WORK/index.html"
