# video-productions · 手绘笔记讲解视频

用 [dashi-animationstyle](../skills/dashi-animationstyle) skill 的「手绘笔记」风格，把 hypit 的课程讲稿做成手绘讲解视频。
本目录保存**可复现的代码**：通用工具、每集的画面代码、分镜数据。成片、配音、帧序列等构建产物不入库。

## 已制作

| 集 | 主题 | 成片 | 场/句 | 字幕条 | 卡点 |
|---|---|---|---|---|---|
| 07-03 | 多头注意力 | 260.4 秒 / 21.8 MiB | 13 / 39 | 81 | 87 |
| 14-01 | ReAct 与 Agent 循环 | 241.0 秒 / 20.3 MiB | 9 / 27 | 81 | 60 |
| 14-03 | Reflexion | 173.0 秒 / 14.6 MiB | 9 / 27 | 55 | 37 |

成片（1920×1080、30 fps、H.264 + AAC）在制作机上：`~/video-skills/output/dashi-*-handdrawn.mp4`，
不入库；按下面的步骤可以整片重建。

## 目录

```
tools/                       通用工具（与具体集无关）
  prepare.sh                 讲稿 → TTS → 口播.wav（第一步）
  build.sh                   字幕 → 分镜 → 时间线 → index.html（第二步）
  parse_lesson.py            从 hypit episodes/<集>/lesson.json 生成 讲稿.md / scenes.json / 稿子.txt
  tts_par.py                 edge-tts 逐句合成（并发、断点续跑）
  assemble.py                拼接 口播.wav，并写下每句的精确起止 line_times.json
  mksub.py                   由精确句界生成 字幕.json / .srt（token 级均衡切条，不吞 ASCII 标点）
  mkstory.py                 分镜数据 → 分镜.json / .md，并校验每个卡点短语能在单条字幕里按 token 边界找到
  make_page.py               模板底座 + common.js + 场景代码 → index.html
  common.js                  手绘笔记场景公共底座（段落、页眉、网格、箭头、卡片等）
  render_all.sh              分段渲染（断点续跑）+ 拼接混音 → 成片_full.mp4
  compress.sh                两遍编码压到 25 MiB 以下
  verify.sh / verify_thumbs.py   验收：编码/分辨率/时长 + 抽三帧
data/story_<集>.json         每集的分镜数据：标题、高亮、字幕强调、卡点、每场的关键字/要讲清/运动设想/变化
<集>/scenes_*.js             每集的画面代码；最后一段含场景入口 drawScenes 与镜头 CAM
```

## 依赖

- **Node ≥ 22**：skill 的 `render.mjs` 用 Node 自带 WebSocket
- **ffmpeg / ffprobe**、**Google Chrome**（无头逐帧截图）
- **edge-tts**：配音（本机装在 `~/video-skills/venv`，用 `EDGE_TTS` 指定别的路径）
- **skill 本体**：[skills/dashi-animationstyle](../skills/dashi-animationstyle)，可用 `DASHI_SKILL` 指向别处

## 复现一集

```bash
export DASHI_SKILL="$PWD/skills/dashi-animationstyle"
EP=14-01
WORK=~/video-skills/dashi-works/${EP}_重建
SCENES="$PWD/video-productions/14-01_ReAct循环"

# 1. 讲稿 + 配音 + 精确句界（需要网络，27 句约 2 分钟）
bash video-productions/tools/prepare.sh "$EP" "$WORK"

# 2. 字幕 + 分镜 + 时间线 + 页面
bash video-productions/tools/build.sh "$EP" "$WORK" "$SCENES" 2

# 3. 静帧自审（挑每场末尾；看有没有重叠、越界、字没写完）
cd "$WORK"
node "$DASHI_SKILL/pipeline/render.mjs" "$WORK/index.html" --stills 26,52,78 --outdir 静帧 --prefix 调试

# 4. 确定性检查 → 整片渲染 → 压缩 → 验收
node "$DASHI_SKILL/pipeline/render.mjs" "$WORK/index.html" --check-determinism auto
bash video-productions/tools/render_all.sh "$WORK"          # 约 120 毫秒/帧，241 秒的片子约 15 分钟
bash video-productions/tools/compress.sh "$WORK" "dashi-react-agent-loop-handdrawn"
bash video-productions/tools/verify.sh "$WORK" "dashi-react-agent-loop-handdrawn"
```

## 改内容

- **改文案**：改 `data/story_<集>.json`。`marks[].phrase` 必须能在**单条字幕里按 token 边界**整段找到，否则 `mkstory.py` 会报错并指出是哪个卡点、哪一句。
- **改画面**：改 `<集>/scenes_*.js`。每场一个 `scene(i, (sc, t) => { … })`，所有时间从 `MS('卡点名')` 取，**不写死秒数**；画面底部不要超过 `y0 + 857`（字幕带在 y=908，镜头还有 1.06 倍慢推）。
- **换配音**：`DASHI_VOICE=zh-CN-YunxiNeural DASHI_RATE=+20%` 重新跑 `prepare.sh`（删掉作品目录的 `tts/` 会重录），后面所有步骤自动跟随。
- **换风格**：`make_page.py` 目前固定读手绘笔记模板的底座行号与 `drawSections` 入口；换别的风格要换模板并改这两处。

## 约定

- **不引入生成模型**：画面是 HTML/Canvas 代码，由无头 Chrome 逐帧截图。
- **字幕烧进画面**（页面自绘），成片不挂独立字幕轨，避免双字幕。
- 时间轴的唯一来源是字幕的字级时间：页面里只出现 `TL.mark(...)`，没有硬编码秒数。
- 画面数字要用课程实跑值（例：07-03 的 6×6 注意力矩阵取自 `phases/07-transformers-deep-dive/03-multi-head-attention/code/main.py` 的输出），示意值必须在画面上注明「示意」。
- 成片 `.mp4`、`口播.wav`、`tts/`、`aud/`、`seg/`、`静帧/`、`检查/` 都不入库。
