#!/bin/bash
# 用法：prepare.sh <集号如 14-01> <作品目录>  —— 讲稿 → 逐句 TTS → 拼接口播.wav + 精确句界
set -eu
T="$(cd "$(dirname "$0")" && pwd)"
EP="$1"; WORK="$2"
mkdir -p "$WORK"
python3 "$T/parse_lesson.py" "$EP" "$WORK"
python3 "$T/tts_par.py" "$WORK"
python3 "$T/assemble.py" "$WORK"
echo "PREPARE_OK $WORK"
