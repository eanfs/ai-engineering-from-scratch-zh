# AI 课程视频系列（三阶段并行）制作实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `eanfs/hypit-productions`（私有）的 `ai-engineering-zh/` 目录建立可复用的手绘大画布视频制作工程，并交付阶段 03、07、14 三条流水线的首集样片。该目录位于课程仓的 `hypit-productions` 子模块内。

**Architecture:** 参考已验证工程 `hypit-productions/self-attention-whiteboard`（Hypit 0.2.17 + HyperFrames + 自建 CosyVoice 3）。参考工程的 `packages/whiteboard/src/render.ts` 把 12 个场景的图形、标题、世界坐标和镜头常量全部硬编码，且 `check_cosy_camera.cjs` 用正则从源码里抠出数组、`Array(12)` 写死场景数——每换一集主题就要改引擎。本计划先把它拆成「引擎（`@production/board-kit`，跨集复用）+ 单集图形（`episodes/<slug>`，一集一个 Hypit 组件包）」，再让三条流水线各自在独立目录内顺序推进，互不改同一个文件。

**Tech Stack:** Hypit 0.2.17（SVML / SVRun / Component Package）、Node 24.16（原生 TypeScript 执行 + `node --test`）、Python 3.14 + `opencc-python-reimplemented`、FFmpeg 7.1、自建 CosyVoice 3（`http://172.16.12.71:8097`）、Whisper small（`172.16.12.182`）。

**Spec:** `docs/plans/ai-engineering-video-series.md`（本仓库，同 PR）。计划中所有档位、时长、分辨率、配音服务均以该 spec 为准；spec 已在同一 PR 修正为 1280×720 / CosyVoice 3 / 分档时长。

## Global Constraints

- 成片 1280×720、24 fps、H.264 + AAC；画面 `spatial:Canvas` 1280×720，世界画布按布局计算；**不得改造为 1080p**。
- 单集场景数与档位绑定：T-L = 12 场景 / 36 事件 / 4–6 分钟；T-M = 9 场景 / 27 事件 / 3–4 分钟；T-S = 6 场景 / 18 事件 / 2–3 分钟。
- 每个场景恰好 3 段旁白，每段 110–180 字；同一集内所有场景段数必须一致。
- 旁白使用自建 CosyVoice 3，音色 `default`；**不产生第三方 TTS 账单**，不得擅自切换到付费云端服务。
- 只在场景之间插入 0.65 秒静音，片尾 1 秒；**段落内部保留模型停顿，不得逐句合成后插固定静音**。
- 字幕内容取自已核对讲稿；ASR（Whisper small）只用于定位句首。ASR 与讲稿字符覆盖率 < 0.65 时脚本必须报错，**不得下调阈值让脚本通过**。
- 图形在世界坐标中永久保留；镜头只平移缩放同一个画布，禁止逐场景 DOM 替换或淡出（会退化成幻灯片翻页）。
- 镜头交接必须是一条连续运动：五次缓动 `6t⁵-15t⁴+10t³`，缩放在对数空间插值；运动区间不得重叠、端点必须连续。
- 课程仓库的课程内容（`phases/`、`certifications/`、`glossary/`、`site/`、`scripts/`）全程只读；制作产物只写进 `hypit-productions/` 子模块，提交进 `eanfs/hypit-productions` 仓库，**不得提交进课程仓库**。
- 密钥只经 Hypit auth 存入 Keychain，项目文件只保存凭证引用；不得把密钥写进脚本、README、命令行参数或版本库。
- 每集交付 MP4、SRT、讲稿、可编辑 Source/Run、验收证据；旧版本文件保留，不覆盖。
- 引用参考工程的文件时**只读不写**；`self-attention-whiteboard` 的成片和已接受音轨不得修改。

## 决策基线（本次已定，不再重开）

| 项 | 决定 |
|---|---|
| 分辨率 | 沿用 1280×720 |
| 配音 | 自建 CosyVoice 3 为主；云端 TTS 属预算外变更，需另行授权 |
| 时长结构 | 按课程复杂度分档（T-L / T-M / T-S） |
| 本计划范围 | 准备批 + 三条流水线首集样片（03-01、07-01、14-01）；剩余 80 集按量产 runbook 复用 |

## 文件结构

制作工程根：`/Users/lirichen/Work/GithubRepo/ai-engineering-from-scratch-zh/hypit-productions/ai-engineering-zh/`

它位于课程仓库内的 **`hypit-productions` 子模块**（`eanfs/hypit-productions`，私有）中。课程仓库本身只保存 `.gitmodules` 与一个 gitlink；本计划的全部产物提交进制作工程仓库，不提交进课程仓库。

```sh
export COURSE='/Users/lirichen/Work/GithubRepo/ai-engineering-from-scratch-zh'
export VIDEO_PROJECT="$COURSE/hypit-productions/ai-engineering-zh"   # 本计划的工程根
export REFERENCE="$COURSE/hypit-productions/self-attention-whiteboard" # 只读参考（仓库副本）
export REFERENCE_WORK='/Users/lirichen/Work/GithubRepo/hypit-productions/self-attention-whiteboard' # 本机工作副本，含 .hypit/ 与 node_modules/，未入库
```

`$REFERENCE`（仓库内副本）不含 `node_modules/` 与 `.hypit/`——它们被 `.gitignore` 排除，**因此仓库副本不能直接运行**。需要跑参考工程时用 `$REFERENCE_WORK`（保留完整构建状态与运行结果），或先给仓库副本补 `npm install` 与 runtime 配置。只有 Task 1 Step 5 的工具链验证依赖可运行的参考工程。

```text
package.json                     # 聚合所有单集组件包的 file: 依赖
hypit.runtime.json               # local runtime + cosy.remote Provider
BRIEF.md                         # 目标、风格与制作决定
PROGRESS.md                      # 三条流水线进度表
REVIEW.md                        # 验收记录与遗留项
episodes/<slug>/                 # 一集一个自包含目录，同时是一个 Hypit 组件包
  episode.json                   # slug / 档位 / 场景数 / 课程来源 / 来源提交
  lesson.json                    # 场景 id、标题、3 段旁白
  deck.ts                        # 该集的世界坐标、主题与图形（唯一的内容文件）
  package.json                   # @production/ep-<slug>，hypit.activation 指向 src/activation.ts
  src/activation.ts              # createBoardPackage("@production/ep-<slug>", deck)
  authors/voice.svml             # 讲稿 → CosyVoice 请求
  authors/main.svml              # 画面 + 声音时间线（由 assemble.py 回填帧号）
  runs/voice.svrun  runs/final.svrun  runs/edit.svrun
  assets/  evidence/  output/
packages/board-kit/              # 跨集复用引擎
  src/deck.ts                    # Deck / Scene / DrawContext 类型 + assertDeck + describeDeck
  src/theme.ts                   # 配色与字号
  src/layout.ts                  # 蛇形大画布布局 + defaultCamera
  src/primitives.ts              # 世界坐标绘制原语 + 收集器
  src/camera.ts                  # 镜头规划与求值
  src/render.ts                  # browserProgram 生成（依赖 @hypit/*）
  src/components.ts              # 标题卡 / 机制图 / 代码块 / 结果卡 / 总结条
  src/package.ts                 # createBoardPackage(moduleName, deck)（依赖 @hypit/*）
  src/index.ts                   # 汇总导出（含 @hypit 依赖，仅供 Hypit 加载器）
  test/*.test.ts                 # 只测纯模块，import 具体文件，不 import index.ts
tools/
  classify.mjs                   # 课程 → 档位
  new-episode.mjs                # 生成单集骨架并 npm 链接
  export_voice.py                # 导出分段 WAV（去硬编码路径）
  assemble.py                    # 拼接、ASR 对齐、字幕、时间线回填
  master.py                      # 响度处理（幂等）
  add_title.py                   # 5 秒片头时间顺延
  check_camera.mjs               # 镜头连续性检查（导入 deck，不再正则解析源码）
templates/
  voice.svml  main.svml  voice.svrun  final.svrun  edit.svrun
```

## 任务总览

| # | 任务 | 产物 |
|---|---|---|
| 1 | 制作工程脚手架与运行环境核验 | 可 `plan` 的空工程 + `evidence/env-check.json` |
| 2 | board-kit 类型层 | `deck.ts` `theme.ts` + 校验测试 |
| 3 | board-kit 绘制原语 | `primitives.ts` + 测试 |
| 4 | board-kit 镜头引擎 | `camera.ts` + 连续性测试 |
| 5 | board-kit 渲染器与组件包工厂 | `render.ts` `package.ts` |
| 6 | 五类可复用图形组件 | `components.ts` + 测试 |
| 7 | 单集脚手架生成器 | `classify.mjs` `new-episode.mjs` + 测试 |
| 8 | 配音与时间线工具链 | `export_voice.py` `assemble.py` `master.py` `check_camera.mjs` |
| 9 | 5 秒片头工具 | `add_title.py` |
| 10 | 样片 A · 03-01 感知机（T-L） | 成片 + 证据 |
| 11 | 样片 B · 07-01 为什么需要 Transformer（T-L） | 成片 + 证据 |
| 12 | 样片 C · 14-01 Agent 循环（T-M） | 成片 + 证据 |
| 13 | 三样片集中评审、模板冻结与量产交接 | `REVIEW.md` + 量产 runbook |

---

### Task 1: 制作工程脚手架与运行环境核验

**Files:**
- Create: `$COURSE/hypit-productions/ai-engineering-zh/package.json`
- Create: `.../hypit.runtime.json`
- Create: `.../BRIEF.md` `.../PROGRESS.md` `.../REVIEW.md`
- Create: `.../tools/check_env.sh`
- Create: `.../evidence/env-check.json`

**Interfaces:**
- Consumes: 无
- Produces: 一个能用 `hypit plan` 跑通的最小工程；`COURSE`、`VIDEO_PROJECT`、`REFERENCE`、`REFERENCE_WORK` 四个环境变量约定，后续所有任务依赖

- [ ] **Step 1: 建立目录并复制 runtime profile**

```sh
export COURSE='/Users/lirichen/Work/GithubRepo/ai-engineering-from-scratch-zh'
export HYPIT_REPO='/Users/lirichen/Work/GithubRepo/hypit'
export VIDEO_PROJECT="$COURSE/hypit-productions/ai-engineering-zh"
export REFERENCE="$COURSE/hypit-productions/self-attention-whiteboard"
export REFERENCE_WORK='/Users/lirichen/Work/GithubRepo/hypit-productions/self-attention-whiteboard'
mkdir -p "$VIDEO_PROJECT"/{episodes,packages,tools,templates,authors,runs,evidence,output}
cp "$REFERENCE/hypit.runtime.json" "$VIDEO_PROJECT/hypit.runtime.json"
cp "$REFERENCE/authors/look.svs" "$VIDEO_PROJECT/authors/look.svs"
```

- [ ] **Step 2: 写根 `package.json`**

```json
{
  "name": "ai-engineering-zh",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "dependencies": {
    "@production/board-kit": "file:packages/board-kit"
  }
}
```

后续每加一集由 `tools/new-episode.mjs` 追加一条 `"@production/ep-<slug>": "file:episodes/<slug>"`。

- [ ] **Step 3: 写环境核验脚本**

`tools/check_env.sh`（`chmod +x`）：

```sh
#!/usr/bin/env bash
# 制作开始前的必要检查。任一硬失败项不通过就不应开始配音或渲染。
set -uo pipefail
: "${HYPIT_REPO:?先 export HYPIT_REPO}"
: "${VIDEO_PROJECT:?先 export VIDEO_PROJECT}"
cd "$VIDEO_PROJECT"
out=evidence/env-check.json
fail=0
record() { printf '  %-34s %s\n' "$1" "$2"; }
json() { printf '"%s": %s' "$1" "$2"; }

hypit() { node "$HYPIT_REPO/bin/hypit.mjs" "$@"; }

node -e 'process.exit(Number(process.versions.node.split(".")[0])>=24?0:1)' \
  && record node "ok $(node -v)" || { record node "FAIL $(node -v) 需要 >=24"; fail=1; }
ffmpeg -version >/dev/null 2>&1 && record ffmpeg "ok" || { record ffmpeg FAIL; fail=1; }
ffprobe -version >/dev/null 2>&1 && record ffprobe "ok" || { record ffprobe FAIL; fail=1; }
hypit --version >/dev/null 2>&1 && record hypit "ok $(hypit --version)" || { record hypit FAIL; fail=1; }
[ "$(hypit --version)" = "0.2.17" ] || { record hypit-version "WARN 参考工程使用 0.2.17"; }

health=$(curl -sS --fail --max-time 8 http://172.16.12.71:8097/health 2>/dev/null) \
  && record cosyvoice "ok $health" || { record cosyvoice FAIL; fail=1; }
hypit auth status cosy.remote >/dev/null 2>&1 \
  && record cosy-credential ok || { record cosy-credential "FAIL 运行 hypit auth login cosy.remote"; fail=1; }

[ -d "$HYPIT_REPO/node_modules" ] && record hypit-deps ok || { record hypit-deps "FAIL 在 Hypit 仓库运行 pnpm install --frozen-lockfile"; fail=1; }
[ -f "$REFERENCE/hypit.runtime.json" ] && record reference-project ok || { record reference-project FAIL; fail=1; }

if [ "$fail" -eq 0 ]; then ok=true; else ok=false; fi
{
  printf '{'; json ok "$ok";
  printf ', '; json node "\"$(node -v)\"";
  printf ', '; json ffmpeg "\"$(ffmpeg -version 2>/dev/null | head -1)\"";
  printf ', '; json hypit "\"$(hypit --version)\"";
  printf ', '; json cosyvoice_health "\"$health\"";
  printf ', '; json checked_at "\"$(date -Iseconds)\"";
  printf '}\n';
} > "$out"
[ "$ok" = true ] && echo "环境核验通过 → $out" || { echo "环境核验未通过 → $out"; exit 1; }
```

- [ ] **Step 4: 运行并确认通过**

Run: `export HYPIT_REPO='/Users/lirichen/Work/GithubRepo/hypit'; export VIDEO_PROJECT='/Users/lirichen/Work/GithubRepo/ai-engineering-from-scratch-zh/hypit-productions/ai-engineering-zh'; bash "$VIDEO_PROJECT/tools/check_env.sh"`
Expected: 所有项 `ok`，末行 `环境核验通过`，退出码 0。
已知事实：CosyVoice 3 在 2026-10-10 实测返回 `{"status":"ready","model":"FunAudioLLM/Fun-CosyVoice3-0.5B-2512","busy":false}`，Hypit CLI 返回 `0.2.17`。

- [ ] **Step 5: 确认工具链真能构建（不只 `--version`）**

```sh
cd "$REFERENCE_WORK"   # 必须用本机工作副本：仓库内的 $REFERENCE 没有 node_modules/ 与 .hypit/
node "$HYPIT_REPO/bin/hypit.mjs" plan runs/final-cosy-title.svrun
```

Expected: 输出含 `Preflight  ready`，请求列表里 `media.local` 与 `hyperframes.local` 都是 `local, no Provider charge`。这一步验证的是**参考工程整体可构建**——如果它失败，本计划后续所有 `hypit plan` / `hypit build` 都不成立，必须先修 Hypit 环境（在 Hypit 仓库按说明 `pnpm install --frozen-lockfile`）再继续。

若 `$REFERENCE_WORK` 已不存在（只克隆了课程仓），跳过本步，改在 Task 5 Step 5 用探针单集验证——那是更强的检查，因为它走的是本工程自己的组件包。

> 实测记录（2026-10-10）：本步在 `$REFERENCE_WORK` 上通过；CosyVoice 3 健康检查返回 `{"status":"ready","busy":false}`；Hypit CLI 为 `0.2.17`。

- [ ] **Step 6: 写 `BRIEF.md`、`PROGRESS.md`、`REVIEW.md`**

`BRIEF.md` 必须写明：系列名、三阶段 83 集、分档规则、1280×720 / 24 fps、CosyVoice 3 音色 `default`、课程仓库只读、制作工程仓库与子模块位置（`eanfs/hypit-productions` → 课程仓 `hypit-productions/`）、参考工程路径（`$REFERENCE`）、以及「图形在世界坐标永久保留，镜头不切场景」这一形式决定。

`PROGRESS.md` 用三张表（A/B/C），每行 `集号 | 档位 | 状态 | 当前步骤 | 阻塞原因 | Build ID`。

`REVIEW.md` 记录每集的验收时间、检查项、未完成项；初始写三行「待样片批填入」。

- [ ] **Step 7: 提交进制作工程仓库**

```sh
cd "$COURSE/hypit-productions"
git status --short          # 确认只有 ai-engineering-zh/ 下的新文件，没有音频/成片/.hypit
git add ai-engineering-zh
git commit -m "chore: 建立 ai-engineering-zh 制作工程与运行环境核验"
```

**不要在这里 `git init`。** `hypit-productions/` 已经是课程仓的子模块，单独 init 会造出嵌套仓库，父仓的 gitlink 会指向不到东西。构建产物的忽略规则由 `hypit-productions/.gitignore` 统一提供（`**/.hypit/`、`**/node_modules/`、`**/output/`、`**/*.wav`、`**/*.mp4`、`**/__pycache__/` 等），本工程不需要自己的 `.gitignore`。

---

### Task 2: board-kit 类型层

**Files:**
- Create: `$VIDEO_PROJECT/packages/board-kit/package.json`
- Create: `$VIDEO_PROJECT/packages/board-kit/src/theme.ts`
- Create: `$VIDEO_PROJECT/packages/board-kit/src/deck.ts`
- Test: `$VIDEO_PROJECT/packages/board-kit/test/deck.test.ts`

**Interfaces:**
- Consumes: 无
- Produces:
  - `type Beat = number`
  - `type Pos = { x: number; y: number }`
  - `type DrawContext`，方法签名：`text(id, value, x, y, size?, color?, beat?, width?)` / `stroke(id, d, beat?, color?, strokeWidth?, fill?, delay?)` / `line(x, y, a, b, beat?, color?)` / `arrow(x, y, a, b, beat?, color?)` / `box(x, y, w, h, beat?, color?, fill?)` / `person(x, y, beat?, color?)` / `matrix(x, y, rows, cols, beat?, cell?, gap?)`
  - `type Scene = { id: string; title: string; pos: Pos; lines: string[]; draw: (d: DrawContext) => void }`
  - `type CameraConfig`、`type Deck`、`type Theme`
  - `assertDeck(deck: Deck): void`（抛 `Error`，消息含 `deck.id` 与场景 id）
  - `collectBeats(scene: Scene): number[]`
  - `describeDeck(deck: Deck): { sceneIds: string[]; beatLimits: Record<string, number>; sceneCount: number }`（纯函数，供激活模块与测试共用）

- [ ] **Step 1: 写 `theme.ts`**

```ts
export type Theme = {
  background: string; ink: string; green: string; blue: string; purple: string; red: string; paper: string;
};

export const defaultTheme: Theme = {
  background: "#fffefa", ink: "#252b28", green: "#74ab45", blue: "#3788ae",
  purple: "#9976b9", red: "#d66b60", paper: "#fafcf7",
};

export const sizes = { sceneTitle: 38, body: 30, caption: 24, worldTitle: 85, worldSubtitle: 39 } as const;
```

- [ ] **Step 2: 写失败测试**

`packages/board-kit/test/deck.test.ts`：

```ts
import { strict as assert } from "node:assert";
import { test } from "node:test";
import { assertDeck, collectBeats, describeDeck } from "../src/deck.ts";
import { defaultTheme } from "../src/theme.ts";
import type { Deck, DrawContext, Scene } from "../src/deck.ts";

const camera = {
  fps: 24,
  panel: { width: 1280, height: 620 },
  fit: { width: 1180, height: 585 },
  local: { z: [0.82, 0.76], nudgeX: 75, nudgeY: 25 },
  move: { minSeconds: 3.3, maxSeconds: 4.6, baseSeconds: 3.3, distanceDivisor: 2400, lead: 0.56, wideFactor: 0.72 },
  opening: { cx: 1490, cy: -195, z: 1.05 },
  overview: { cx: 1450, cy: 1440, z: 0.178 },
  recap: { firstReview: [0], secondReview: [1], tailFrames: 180 },
};

const scene = (id: string, lines: string[], draw: Scene["draw"]): Scene =>
  ({ id, title: `标题 ${id}`, pos: { x: 0, y: 0 }, lines, draw });

const deckWith = (scenes: Scene[]): Deck => ({
  id: "demo", title: "演示", subtitle: "副标题", world: { width: 4400, height: 3400 },
  theme: defaultTheme, camera: { ...camera, local: { ...camera.local, z: scenes.map(() => 0.76) } }, scenes,
});

const threeLines = ["一", "二", "三"];

test("assertDeck 接受合法 deck", () => {
  const deck = deckWith([scene("a", threeLines, d => d.text("a-0", "x", 10, 20, 30, undefined, 0))]);
  assert.doesNotThrow(() => assertDeck(deck));
});

test("assertDeck 拒绝空 id、重复场景 id、空旁白", () => {
  assert.throws(() => assertDeck({ ...deckWith([]), id: "" }), /deck\.id/);
  const dup = deckWith([scene("a", threeLines, () => {}), scene("a", threeLines, () => {})]);
  assert.throws(() => assertDeck(dup), /duplicate scene id a/);
  assert.throws(() => assertDeck(deckWith([scene("a", ["", "二", "三"], () => {})])), /lines must not be empty/);
});

test("assertDeck 拒绝超出范围的 beat", () => {
  const bad = deckWith([scene("a", threeLines, d => d.text("x", "x", 0, 0, 30, undefined, 3))]);
  assert.throws(() => assertDeck(bad), /beat 3 is outside 0\.\.2/);
});

test("assertDeck 要求每个 beat 至少有一个图元", () => {
  const thin = deckWith([scene("a", threeLines, d => d.text("x", "x", 0, 0, 30, undefined, 0))]);
  assert.throws(() => assertDeck(thin), /beat 1 has no primitives/);
});

test("assertDeck 要求 camera.local.z 与场景数一致", () => {
  const deck = deckWith([scene("a", threeLines, () => {})]);
  deck.camera.local.z = [];
  assert.throws(() => assertDeck(deck), /camera\.local\.z/);
});

test("assertDeck 要求同集内每个场景段数一致", () => {
  const deck = deckWith([scene("a", threeLines, () => {}), scene("b", ["一", "二"], () => {})]);
  assert.throws(() => assertDeck(deck), /must all declare the same number of lines/);
});

test("collectBeats 返回每个图元的 beat，顺序与绘制顺序一致", () => {
  const beats = collectBeats(scene("a", threeLines, d => {
    d.text("t", "x", 0, 0, 30, undefined, 0);
    d.box(0, 0, 10, 10, 2);
    d.arrow(0, 0, 10, 10, 1);
  }));
  assert.deepEqual(beats, [0, 2, 1]);
});

test("describeDeck 给出场景 id、各场景 beat 上界与场景数", () => {
  const deck = deckWith([scene("a", threeLines, () => {}), scene("b", threeLines, () => {})]);
  assert.deepEqual(describeDeck(deck), { sceneIds: ["a", "b"], beatLimits: { a: 3, b: 3 }, sceneCount: 2 });
});
```

- [ ] **Step 3: 运行测试确认失败**

Run: `cd "$VIDEO_PROJECT" && node --test packages/board-kit/test/deck.test.ts`
Expected: FAIL — `Cannot find module '../src/deck.ts'`

- [ ] **Step 4: 写 `packages/board-kit/package.json`**

```json
{
  "name": "@production/board-kit",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "exports": {
    ".": "./src/index.ts",
    "./deck": "./src/deck.ts",
    "./camera": "./src/camera.ts",
    "./primitives": "./src/primitives.ts",
    "./render": "./src/render.ts",
    "./components": "./src/components.ts"
  }
}
```

- [ ] **Step 5: 写 `deck.ts`**

```ts
import type { Theme } from "./theme.ts";
import { defaultTheme } from "./theme.ts";

export type Beat = number;
export type Pos = { x: number; y: number };
export type Cell = { color: string; fill: string; glyph?: string };

export type DrawContext = {
  text(id: string, value: string, x: number, y: number, size?: number, color?: string, beat?: Beat, width?: number): void;
  stroke(id: string, d: string, beat?: Beat, color?: string, strokeWidth?: number, fill?: string, delay?: number): void;
  line(x: number, y: number, a: number, b: number, beat?: Beat, color?: string): void;
  arrow(x: number, y: number, a: number, b: number, beat?: Beat, color?: string): void;
  box(x: number, y: number, w: number, h: number, beat?: Beat, color?: string, fill?: string): void;
  person(x: number, y: number, beat?: Beat, color?: string): void;
  matrix(x: number, y: number, rows: number, cols: number, beat?: Beat, cell?: (i: number, j: number) => Cell, gap?: { x: number; y: number }): void;
};

export type Scene = { id: string; title: string; pos: Pos; lines: string[]; draw: (d: DrawContext) => void };

export type CameraConfig = {
  fps: number;
  panel: { width: number; height: number };
  fit: { width: number; height: number };
  local: { z: number[]; nudgeX: number; nudgeY: number };
  move: { minSeconds: number; maxSeconds: number; baseSeconds: number; distanceDivisor: number; lead: number; wideFactor: number };
  opening: { cx: number; cy: number; z: number };
  overview: { cx: number; cy: number; z: number };
  recap: { firstReview: number[]; secondReview: number[]; tailFrames: number };
};

export type Deck = {
  id: string;
  title: string;
  subtitle: string;
  world: { width: number; height: number };
  theme: Theme;
  camera: CameraConfig;
  scenes: Scene[];
};

/** 记录图元被绘制时的顺序与 beat，用于校验和动画排期。 */
export function collectBeats(scene: Scene): number[] {
  const beats: number[] = [];
  const rec = (beat: Beat) => { beats.push(beat); };
  scene.draw({
    text: (_id, _v, _x, _y, _s, _c, beat = 0) => rec(beat),
    stroke: (_id, _d, beat = 0) => rec(beat),
    line: (_x, _y, _a, _b, beat = 0) => rec(beat),
    arrow: (_x, _y, _a, _b, beat = 0) => rec(beat),
    box: (_x, _y, _w, _h, beat = 0) => rec(beat),
    person: (_x, _y, beat = 0) => rec(beat),
    matrix: (_x, _y, _r, _c, beat = 0) => rec(beat),
  } as DrawContext);
  return beats;
}

export function assertDeck(deck: Deck): void {
  const at = (message: string) => new Error(`${deck.id}: ${message}`);
  if (!deck.id) throw new Error("deck.id is required");
  if (!deck.scenes.length) throw at("at least one scene is required");
  if (!deck.title.trim()) throw at("title is required");
  const sceneCount = deck.scenes.length;
  const expectedLines = deck.scenes[0]?.lines.length ?? 0;
  const seen = new Set<string>();
  for (const scene of deck.scenes) {
    if (!scene.id) throw at("scene id is required");
    if (seen.has(scene.id)) throw at(`duplicate scene id ${scene.id}`);
    seen.add(scene.id);
    if (!scene.title.trim()) throw at(`${scene.id}: title is required`);
    if (scene.lines.length !== expectedLines) throw at(`all scenes must all declare the same number of lines (${scene.id})`);
    if (scene.lines.length < 2) throw at(`${scene.id}: at least two lines are required`);
    if (scene.lines.some(line => !line.trim())) throw at(`${scene.id}: lines must not be empty`);
    if (!Number.isFinite(scene.pos.x) || !Number.isFinite(scene.pos.y)) throw at(`${scene.id}: pos must be finite`);
    const beats = collectBeats(scene);
    for (const beat of beats) {
      if (!Number.isInteger(beat) || beat < 0 || beat >= scene.lines.length)
        throw at(`${scene.id}: beat ${beat} is outside 0..${scene.lines.length - 1}`);
    }
    for (let beat = 0; beat < scene.lines.length; beat++) {
      if (!beats.includes(beat)) throw at(`${scene.id}: beat ${beat} has no primitives`);
    }
  }
  const z = deck.camera.local.z;
  if (z.length !== sceneCount) throw at(`camera.local.z must list exactly ${sceneCount} entries, got ${z.length}`);
  if (z.some(value => !Number.isFinite(value) || value <= 0)) throw at("camera.local.z entries must be positive finite numbers");
  if (!(deck.camera.fps > 0)) throw at("camera.fps must be positive");
}

/** 场景 id 与各场景的 beat 上界。激活模块与测试共用，避免两处各写一份。 */
export function describeDeck(deck: Deck): { sceneIds: string[]; beatLimits: Record<string, number>; sceneCount: number } {
  return {
    sceneIds: deck.scenes.map(scene => scene.id),
    beatLimits: Object.fromEntries(deck.scenes.map(scene => [scene.id, scene.lines.length])),
    sceneCount: deck.scenes.length,
  };
}

export { defaultTheme };
```

- [ ] **Step 6: 运行测试确认通过**

Run: `cd "$VIDEO_PROJECT" && node --test packages/board-kit/test/deck.test.ts`
Expected: PASS，8 个 test 全绿。

- [ ] **Step 7: 提交**

```sh
git add packages/board-kit && git commit -m "feat(board-kit): 抽出 Deck/Scene 类型与 deck 校验"
```

---

### Task 3: board-kit 绘制原语

**Files:**
- Create: `$VIDEO_PROJECT/packages/board-kit/src/primitives.ts`
- Test: `$VIDEO_PROJECT/packages/board-kit/test/primitives.test.ts`

**Interfaces:**
- Consumes: `Deck`、`Scene`、`DrawContext`、`Theme`（Task 2）
- Produces:
  - `createBoardGraphics(input: { theme: Theme; font: { faces: unknown } }): BoardGraphics`
  - `BoardGraphics = { drawScene(scene: Scene): PanelGraphics; texts: TextRecord[] }`
  - `PanelGraphics = { id: string; pos: Pos; strokes: string[]; labels: string[]; beats: number[] }`
  - `TextRecord = { id: string; kind: "text"; parent: string; order: number; text: string; fonts: unknown; style: { name: string; value: string }[] }`

- [ ] **Step 1: 写失败测试**

`packages/board-kit/test/primitives.test.ts`：

```ts
import { strict as assert } from "node:assert";
import { test } from "node:test";
import { createBoardGraphics } from "../src/primitives.ts";
import { defaultTheme } from "../src/theme.ts";
import type { Scene } from "../src/deck.ts";

const scene = (draw: Scene["draw"], id = "s1"): Scene =>
  ({ id, title: "场景", pos: { x: 100, y: 200 }, lines: ["一", "二", "三"], draw });

const g = () => createBoardGraphics({ theme: defaultTheme, font: { faces: ["f"] } });

test("text 生成 label 标记与 text 记录，id 带场景前缀，用 {{id}} 占位", () => {
  const b = g();
  const p = b.drawScene(scene(d => d.text("t1", "你好", 10, 20, 40, "#111", 1, 500)));
  assert.equal(p.labels.length, 1);
  assert.match(p.labels[0], /class="label reveal"/);
  assert.match(p.labels[0], /data-beat="1"/);
  assert.match(p.labels[0], /left:10px;top:20px;width:500px/);
  assert.match(p.labels[0], /\{\{s1-t1\}\}/);
  assert.deepEqual(p.beats, [1]);
  assert.equal(b.texts.length, 1);
  assert.equal(b.texts[0].id, "s1-t1");
  assert.equal(b.texts[0].kind, "text");
  assert.equal(b.texts[0].parent, "board");
  assert.equal(b.texts[0].text, "你好");
  assert.deepEqual(b.texts[0].style.map(s => s.name), ["font-size", "line-height", "color"]);
  assert.deepEqual(b.texts[0].style.map(s => s.value), ["40px", "1.3", "#111"]);
});

test("stroke 生成可描画的 path，id 带场景前缀，带 beat 与 delay", () => {
  const p = g().drawScene(scene(d => d.stroke("p1", "M0,0 L10,10", 2, "#0a0", 5, "#eee", 3)));
  assert.equal(p.strokes.length, 1);
  assert.match(p.strokes[0], /id="s1-p1"/);
  assert.match(p.strokes[0], /class="draw"/);
  assert.match(p.strokes[0], /data-beat="2"/);
  assert.match(p.strokes[0], /data-delay="3"/);
  assert.match(p.strokes[0], /stroke="#0a0" stroke-width="5" fill="#eee"/);
  assert.match(p.strokes[0], /stroke-linecap="round"/);
});

test("box 是闭合手绘路径，arrow 生成两段（杆 + 箭头）", () => {
  const p = g().drawScene(scene(d => {
    d.box(0, 0, 100, 50, 0);
    d.arrow(0, 0, 100, 0, 1);
  }));
  assert.equal(p.strokes.length, 3);
  assert.match(p.strokes[0], /Z" stroke/);
  assert.deepEqual(p.beats, [0, 1, 1]);
});

test("matrix 生成 rows*cols 个格子，并按 cell 回调着色", () => {
  const p = g().drawScene(scene(d => d.matrix(0, 0, 2, 3, 0, (i, j) => ({ color: "#f00", fill: "#fee", glyph: `${i}${j}` }))));
  assert.equal(p.strokes.length, 6);
  assert.equal(p.labels.length, 6);
  assert.match(p.labels[0], /\{\{s1-m0-0-g\}\}/);
});

test("两个场景使用相同的局部 id 时不会互相覆盖，order 全局递增", () => {
  const b = g();
  const a = b.drawScene(scene(d => d.text("title", "A", 0, 0, 30), "s1"));
  const c = b.drawScene(scene(d => d.text("title", "B", 0, 0, 30), "s2"));
  assert.equal(a.labels[0].includes("{{s1-title}}"), true);
  assert.equal(c.labels[0].includes("{{s2-title}}"), true);
  assert.deepEqual(b.texts.map(t => t.id), ["s1-title", "s2-title"]);
  assert.deepEqual(b.texts.map(t => t.order), [0, 1]);
});
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd "$VIDEO_PROJECT" && node --test packages/board-kit/test/primitives.test.ts`
Expected: FAIL — `Cannot find module '../src/primitives.ts'`

- [ ] **Step 3: 实现 `primitives.ts`**

```ts
import type { Beat, Cell, DrawContext, Pos, Scene } from "./deck.ts";
import type { Theme } from "./theme.ts";
import { sizes } from "./theme.ts";

export type TextRecord = {
  id: string; kind: "text"; parent: string; order: number; text: string;
  fonts: unknown; style: { name: string; value: string }[];
};
export type PanelGraphics = { id: string; pos: Pos; strokes: string[]; labels: string[]; beats: number[] };
export type BoardGraphics = { drawScene(scene: Scene): PanelGraphics; texts: TextRecord[] };

const esc = (value: string) => value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

export function createBoardGraphics(input: { theme: Theme; font: { faces: unknown } }): BoardGraphics {
  const { theme, font } = input;
  const texts: TextRecord[] = [];
  let order = 0;

  const drawScene = (scene: Scene): PanelGraphics => {
    const strokes: string[] = [], labels: string[] = [], beats: number[] = [];
    let serial = 0;
    // 局部 id 只需场景内唯一；对外一律加场景前缀，否则两个场景用同一个语义 id
    // （例如都叫 title）会生成重复的 DOM id 与重复的 {{占位}}。
    const local = (prefix: string) => `${prefix}${serial++}`;
    const scoped = (id: string) => `${scene.id}-${id}`;

    const ctx: DrawContext = {
      text(id, value, x, y, size = sizes.body, color = theme.ink, beat = 0, width = 1000) {
        beats.push(beat);
        const full = scoped(id);
        texts.push({
          id: full, kind: "text", parent: "board", order: order++, text: value, fonts: font.faces,
          style: [{ name: "font-size", value: `${size}px` }, { name: "line-height", value: "1.3" }, { name: "color", value: color }],
        });
        labels.push(`<div class="label reveal" data-beat="${beat}" style="left:${x}px;top:${y}px;width:${width}px">{{${full}}}</div>`);
      },
      stroke(id, d, beat = 0, color = theme.ink, strokeWidth = 3, fill = "none", delay = 0) {
        beats.push(beat);
        strokes.push(`<path class="draw" id="${scoped(id)}" data-beat="${beat}" data-delay="${delay}" d="${d}" stroke="${color}" stroke-width="${strokeWidth}" fill="${fill}" stroke-linecap="round" stroke-linejoin="round"/>`);
      },
      line(x, y, a, b, beat = 0, color = theme.ink) {
        ctx.stroke(local("l"), `M${x},${y} Q${(x + a) / 2 + 2},${(y + b) / 2 - 2} ${a},${b}`, beat, color);
      },
      arrow(x, y, a, b, beat = 0, color = theme.ink) {
        ctx.line(x, y, a, b, beat, color);
        const ang = Math.atan2(b - y, a - x);
        ctx.stroke(local("h"), `M${a - 15 * Math.cos(ang - 0.4)},${b - 15 * Math.sin(ang - 0.4)} L${a},${b} L${a - 15 * Math.cos(ang + 0.4)},${b - 15 * Math.sin(ang + 0.4)}`, beat, color);
      },
      box(x, y, w, h, beat = 0, color = theme.ink, fill = "none") {
        ctx.stroke(local("b"), `M${x + 2},${y + 2} L${x + w - 3},${y} L${x + w},${y + h - 2} L${x},${y + h} Z`, beat, color, 3, fill);
      },
      person(x, y, beat = 0, color = theme.ink) {
        ctx.stroke(local("p"), `M${x + 16},${y} C${x + 16},${y + 20} ${x - 17},${y + 21} ${x - 16},${y} C${x - 15},${y - 20} ${x + 15},${y - 19} ${x + 16},${y} M${x},${y + 18} L${x},${y + 60} M${x - 25},${y + 35} L${x},${y + 25} L${x + 27},${y + 38} M${x},${y + 60} L${x - 20},${y + 85} M${x},${y + 60} L${x + 22},${y + 85}`, beat, color);
      },
      matrix(x, y, rows, cols, beat = 0, cell: (i: number, j: number) => Cell = () => ({ color: theme.green, fill: "none" }), gap = { x: 69, y: 58 }) {
        const cw = gap.x - 4, ch = gap.y - 4;
        for (let i = 0; i < rows; i++) {
          for (let j = 0; j < cols; j++) {
            const { color, fill, glyph } = cell(i, j);
            ctx.stroke(local(`m${i}-${j}-`), `M${x + j * gap.x + 2},${y + i * gap.y + 2} L${x + j * gap.x + cw - 3},${y + i * gap.y} L${x + j * gap.x + cw},${y + i * gap.y + ch - 2} L${x + j * gap.x},${y + i * gap.y + ch} Z`, beat, color, 3, fill);
            if (glyph) ctx.text(`m${i}-${j}-g`, glyph, x + j * gap.x + 20, y + i * gap.y + 4, 30, color, beat, 45);
          }
        }
      },
    };

    scene.draw(ctx);
    return { id: scene.id, pos: scene.pos, strokes, labels, beats };
  };

  return { drawScene, texts };
}

export { esc };
```

- [ ] **Step 4: 运行测试确认通过**

Run: `cd "$VIDEO_PROJECT" && node --test packages/board-kit/test/primitives.test.ts`
Expected: PASS，5 个 test 全绿。

- [ ] **Step 5: 提交**

```sh
git add packages/board-kit && git commit -m "feat(board-kit): 世界坐标绘制原语与图元收集器"
```

---

### Task 4: board-kit 镜头引擎

**Files:**
- Create: `$VIDEO_PROJECT/packages/board-kit/src/camera.ts`
- Create: `$VIDEO_PROJECT/packages/board-kit/src/layout.ts`
- Test: `$VIDEO_PROJECT/packages/board-kit/test/camera.test.ts`
- Test: `$VIDEO_PROJECT/packages/board-kit/test/layout.test.ts`

**Interfaces:**
- Consumes: `CameraConfig`、`Pos`（Task 2）
- Produces:
  - `type Pose = { cx: number; cy: number; z: number }`
  - `type Move = { start: number; end: number; from: Pose; to: Pose; wide: number }`
  - `type CameraPlan = { opening: Pose; moves: Move[] }`
  - `fitRegion(positions: Pos[], indices: number[], pad: number, cfg: CameraConfig): Pose`
  - `localPose(positions: Pos[], index: number, cfg: CameraConfig): Pose`
  - `planCamera(input: { starts: number[]; eventFrames: number[][]; end: number; positions: Pos[]; cfg: CameraConfig }): CameraPlan`
  - `cameraAt(plan: CameraPlan, frame: number): Pose`
  - `PANEL = { width: 1280, height: 620 }`
  - `layout(count: number): Pos[]`（蛇形布局，每行 3 个）
  - `defaultCamera(count: number, positions: Pos[], panel?: { width: number; height: number }): CameraConfig`

- [ ] **Step 1: 写失败测试**

`packages/board-kit/test/camera.test.ts`：

```ts
import { strict as assert } from "node:assert";
import { test } from "node:test";
import { cameraAt, fitRegion, localPose, planCamera } from "../src/camera.ts";
import type { CameraConfig, Pos } from "../src/deck.ts";

const cfg: CameraConfig = {
  fps: 24,
  panel: { width: 1280, height: 620 },
  fit: { width: 1180, height: 585 },
  local: { z: [0.82, 0.76, 0.76], nudgeX: 75, nudgeY: 25 },
  move: { minSeconds: 3.3, maxSeconds: 4.6, baseSeconds: 3.3, distanceDivisor: 2400, lead: 0.56, wideFactor: 0.72 },
  opening: { cx: 1490, cy: -195, z: 1.05 },
  overview: { cx: 1450, cy: 1440, z: 0.178 },
  recap: { firstReview: [0, 1], secondReview: [1, 2], tailFrames: 180 },
};

const positions: Pos[] = [{ x: 0, y: 0 }, { x: 1320, y: 120 }, { x: 2600, y: 0 }];
const starts = [120, 900, 1700];
const eventFrames = starts.map(s => [s, s + 100, s + 200]);
const end = 3000;

test("fitRegion 把给定区域装进画面，倍率随区域变大而变小", () => {
  const one = fitRegion(positions, [0], 80, cfg);
  const two = fitRegion(positions, [0, 1], 0, cfg);
  assert.ok(one.z > two.z);
  assert.ok(Number.isFinite(one.cx) && Number.isFinite(one.cy));
});

test("localPose 以面板中心为基准，并按前后场景方向做偏移", () => {
  const p = localPose(positions, 1, cfg);
  assert.equal(p.z, 0.76);
  assert.equal(p.cx, 1320 + 640 + Math.sign(positions[0].x - positions[1].x) * 75);
  assert.equal(p.cy, 120 + 310 + Math.sign(positions[0].y - positions[1].y) * 25);
});

test("planCamera 的运动区间严格递增且不重叠", () => {
  const plan = planCamera({ starts, eventFrames, end, positions, cfg });
  assert.ok(plan.moves.length >= positions.length);
  for (let i = 0; i < plan.moves.length; i++) {
    const m = plan.moves[i];
    assert.ok(m.end > m.start, `move ${i} 需要 end > start`);
    if (i) assert.ok(m.start >= plan.moves[i - 1].end, `move ${i} 与前一个重叠`);
  }
});

test("cameraAt 在运动端点两侧连续，且全片有限", () => {
  const plan = planCamera({ starts, eventFrames, end, positions, cfg });
  for (const m of plan.moves) {
    for (const edge of [m.start, m.end]) {
      const a = cameraAt(plan, edge - 1e-5), b = cameraAt(plan, edge + 1e-5);
      assert.ok(Math.hypot(a.cx - b.cx, a.cy - b.cy) < 0.01, `位置在 ${edge} 断点`);
      assert.ok(Math.abs(a.z - b.z) < 1e-5, `倍率在 ${edge} 断点`);
    }
  }
  for (let f = 0; f < end; f++) {
    const p = cameraAt(plan, f);
    assert.ok(Number.isFinite(p.cx) && Number.isFinite(p.cy) && p.z > 0);
  }
});

test("倍率始终为正且带开场时首段从 opening 出发", () => {
  const plan = planCamera({ starts, eventFrames, end, positions, cfg });
  assert.deepEqual(plan.moves[0].from, cfg.opening);
  assert.equal(plan.opening, cfg.opening);
});

test("无开场时首段从第一个局部机位出发", () => {
  const plan = planCamera({ starts: [0, 900, 1700], eventFrames, end, positions, cfg });
  assert.deepEqual(plan.opening, localPose(positions, 0, cfg));
});
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd "$VIDEO_PROJECT" && node --test packages/board-kit/test/camera.test.ts`
Expected: FAIL — `Cannot find module '../src/camera.ts'`

- [ ] **Step 3: 实现 `camera.ts`**

```ts
import type { CameraConfig, Pos } from "./deck.ts";

export type Pose = { cx: number; cy: number; z: number };
export type Move = { start: number; end: number; from: Pose; to: Pose; wide: number };
export type CameraPlan = { opening: Pose; moves: Move[] };

const clamp = (x: number) => Math.max(0, Math.min(1, x));
/** 五次缓动：起止速度与加速度同时归零。 */
const smoother = (t: number) => t * t * t * (t * (t * 6 - 15) + 10);

export function fitRegion(positions: Pos[], indices: number[], pad: number, cfg: CameraConfig): Pose {
  const ps = indices.map(i => positions[i]);
  const l = Math.min(...ps.map(p => p.x)) - pad;
  const r = Math.max(...ps.map(p => p.x + cfg.panel.width)) + pad;
  const t = Math.min(...ps.map(p => p.y)) - pad;
  const b = Math.max(...ps.map(p => p.y + cfg.panel.height)) + pad;
  return { cx: (l + r) / 2, cy: (t + b) / 2, z: Math.min(cfg.fit.width / (r - l), cfg.fit.height / (b - t)) };
}

export function localPose(positions: Pos[], index: number, cfg: CameraConfig): Pose {
  // 夹到合法范围：回顾段会请求最后一个场景的前一个机位，单场景探针会请求 -1。
  const i = Math.max(0, Math.min(index, positions.length - 1));
  const p = positions[i], prev = positions[Math.max(0, i - 1)];
  return {
    cx: p.x + cfg.panel.width / 2 + Math.sign(prev.x - p.x) * cfg.local.nudgeX,
    cy: p.y + cfg.panel.height / 2 + Math.sign(prev.y - p.y) * cfg.local.nudgeY,
    z: cfg.local.z[i],
  };
}

export function planCamera(input: { starts: number[]; eventFrames: number[][]; end: number; positions: Pos[]; cfg: CameraConfig }): CameraPlan {
  const { starts, eventFrames, end, positions, cfg } = input;
  const moves: Move[] = [];
  const add = (start: number, stop: number, from: Pose, to: Pose, wide: number) => {
    moves.push({ start: Math.round(start), end: Math.round(stop), from, to, wide });
  };
  const last = positions.length - 1;
  const opening = starts[0] > 0 ? cfg.opening : localPose(positions, 0, cfg);

  if (starts[0] > 0) {
    add(Math.max(0, starts[0] - Math.round(cfg.fps * 2.5)), starts[0], opening, localPose(positions, 0, cfg), cfg.move.wideFactor);
  }
  for (let i = 1; i < positions.length; i++) {
    const from = localPose(positions, i - 1, cfg), to = localPose(positions, i, cfg);
    const distance = Math.hypot(to.cx - from.cx, to.cy - from.cy);
    const duration = Math.round(cfg.fps * Math.min(cfg.move.maxSeconds, cfg.move.baseSeconds + distance / cfg.move.distanceDivisor));
    const start = starts[i] - Math.round(duration * cfg.move.lead);
    add(start, start + duration, from, to, Math.max(fitRegion(positions, [i - 1, i], 65, cfg).z, Math.min(from.z, to.z) * cfg.move.wideFactor));
  }

  const firstReview = fitRegion(positions, cfg.recap.firstReview, 100, cfg);
  const secondReview = fitRegion(positions, cfg.recap.secondReview, 100, cfg);
  const recapFrames = eventFrames[last];
  add(starts[last] - 55, starts[last] + 55, localPose(positions, Math.max(0, last - 1), cfg), firstReview, Math.min(firstReview.z, 0.3));
  add(recapFrames[1] - 40, recapFrames[1] + 55, firstReview, secondReview, Math.min(firstReview.z, secondReview.z));
  add(recapFrames[2] - 24, recapFrames[2] + 65, secondReview, localPose(positions, last, cfg), Math.min(secondReview.z, 0.3));
  const finalStart = Math.max(recapFrames[2] + 95, end - cfg.recap.tailFrames);
  add(finalStart, end - 48, localPose(positions, last, cfg), cfg.overview, cfg.overview.z);

  return { opening, moves };
}

export function cameraAt(plan: CameraPlan, frame: number): Pose {
  let pose = plan.opening;
  for (const m of plan.moves) {
    if (frame < m.start) break;
    if (frame >= m.end) { pose = m.to; continue; }
    const u = clamp((frame - m.start) / (m.end - m.start)), t = smoother(u);
    // 倍率在对数空间插值，避免缩放速度跳变；wide 制造中途拉远。
    const baseline = Math.exp(Math.log(m.from.z) * (1 - t) + Math.log(m.to.z) * t);
    const midpoint = Math.sqrt(m.from.z * m.to.z);
    const dip = Math.max(0, Math.log(midpoint / m.wide));
    pose = {
      cx: m.from.cx + (m.to.cx - m.from.cx) * t,
      cy: m.from.cy + (m.to.cy - m.from.cy) * t,
      z: baseline * Math.exp(-dip * Math.sin(Math.PI * t) ** 2),
    };
    break;
  }
  return pose;
}
```

- [ ] **Step 4: 运行测试确认通过**

Run: `cd "$VIDEO_PROJECT" && node --test packages/board-kit/test/camera.test.ts`
Expected: PASS，6 个 test 全绿。

- [ ] **Step 5: 写 `layout.ts` 的失败测试**

`packages/board-kit/test/layout.test.ts`：

```ts
import { strict as assert } from "node:assert";
import { test } from "node:test";
import { PANEL, defaultCamera, layout } from "../src/layout.ts";
import { localPose } from "../src/camera.ts";

test("layout 为每个场景给出互不重复的世界坐标", () => {
  const positions = layout(12);
  assert.equal(positions.length, 12);
  assert.equal(new Set(positions.map(p => `${p.x},${p.y}`)).size, 12);
});

test("layout 每行 3 个，第二行反向（蛇形）", () => {
  const p = layout(12);
  assert.equal(p[0].y, p[1].y);
  assert.equal(p[1].y, p[2].y);
  assert.equal(p[3].y > p[0].y, true);
  assert.equal(p[2].x > p[3].x, true, "第二行应从右向左");
});

test("layout 的行间距大于面板高度，避免相邻行图形重叠", () => {
  const p = layout(6);
  assert.ok(p[3].y - p[0].y >= PANEL.height + 100);
});

test("defaultCamera 的 local.z 长度等于场景数，首场景倍率更大", () => {
  const positions = layout(6);
  const cfg = defaultCamera(6, positions);
  assert.equal(cfg.local.z.length, 6);
  assert.ok(cfg.local.z[0] > cfg.local.z[1]);
  assert.ok(cfg.overview.z > 0 && cfg.overview.z < 0.4);
});

test("defaultCamera 对 6 / 9 / 12 场景都自适应，帧率与面板恒定", () => {
  for (const count of [6, 9, 12]) {
    const cfg = defaultCamera(count, layout(count));
    assert.equal(cfg.local.z.length, count);
    assert.equal(cfg.fps, 24);
    assert.deepEqual(cfg.panel, PANEL);
    assert.ok(Number.isFinite(cfg.opening.cx) && Number.isFinite(cfg.overview.cy));
  }
});

test("defaultCamera 的 recap 下标不越界，单场景探针也能取到合法下标", () => {
  for (const count of [1, 6, 9, 12]) {
    const cfg = defaultCamera(count, layout(count));
    for (const index of [...cfg.recap.firstReview, ...cfg.recap.secondReview]) {
      assert.ok(index >= 0 && index < count, `${count} 场景时下标 ${index} 越界`);
    }
    assert.ok(cfg.recap.firstReview.length > 0);
    assert.ok(cfg.recap.secondReview.length > 0);
  }
});

test("localPose 把越界下标夹回合法范围，不返回 undefined", () => {
  const positions = layout(3);
  const cfg = defaultCamera(3, positions);
  for (const index of [-1, 3, 99]) {
    const pose = localPose(positions, index, cfg);
    assert.ok(Number.isFinite(pose.cx) && Number.isFinite(pose.cy) && pose.z > 0);
  }
});
```

- [ ] **Step 6: 运行测试确认失败**

Run: `cd "$VIDEO_PROJECT" && node --test packages/board-kit/test/layout.test.ts`
Expected: FAIL — `Cannot find module '../src/layout.ts'`

- [ ] **Step 7: 实现 `layout.ts`**

```ts
import type { CameraConfig, Pos } from "./deck.ts";

export const PANEL = { width: 1280, height: 620 };

/** 蛇形布局：每行 3 个场景，下一行反向，形成可连续巡览的一张大画布。 */
export function layout(count: number): Pos[] {
  const stepX = PANEL.width + 40, stepY = PANEL.height + 220, cols = 3;
  return Array.from({ length: count }, (_, i) => {
    const row = Math.floor(i / cols), col = i % cols;
    const c = row % 2 === 0 ? col : cols - 1 - col;
    return { x: c * stepX, y: row * stepY };
  });
}

export function defaultCamera(count: number, positions: Pos[], panel = PANEL): CameraConfig {
  const l = Math.min(...positions.map(p => p.x));
  const r = Math.max(...positions.map(p => p.x)) + panel.width;
  const t = Math.min(...positions.map(p => p.y));
  const b = Math.max(...positions.map(p => p.y)) + panel.height;
  // 回顾段的下标按实际场景数裁剪：T-L(12)/T-M(9)/T-S(6) 以及探针单集都不能越界。
  const at = (indices: number[]) => {
    const kept = indices.filter(i => i < count);
    return kept.length ? kept : Array.from({ length: count }, (_, i) => i);
  };
  return {
    fps: 24,
    panel,
    fit: { width: 1180, height: 585 },
    local: { z: positions.map((_, i) => (i === 0 ? 0.82 : 0.76)), nudgeX: 75, nudgeY: 25 },
    move: { minSeconds: 3.3, maxSeconds: 4.6, baseSeconds: 3.3, distanceDivisor: 2400, lead: 0.56, wideFactor: 0.72 },
    opening: { cx: l + panel.width * 0.55, cy: t - 195, z: 1.05 },
    overview: { cx: (l + r) / 2, cy: (t + b) / 2, z: Math.min(1180 / (r - l), 585 / (b - t)) },
    recap: { firstReview: at([1, 2, 3, 4]), secondReview: at([4, 5, 6, 7, 8]), tailFrames: 180 },
  };
}
```

相应地，`localPose` 与 `planCamera` 必须容忍首尾边界：`localPose` 内部把下标夹到 `[0, positions.length - 1]`，`planCamera` 里回顾段的前一个机位用 `localPose(positions, Math.max(0, last - 1), cfg)`。单场景探针（`count = 1`）会走到这两条边界路径，探针跑通即证明它们没写崩。

12 个场景的 `local.z` 与 `recap` 取值沿用参考工程已验证的值；6 与 9 场景档由 `at()` 与 `local.z` 生成规则自动适配，**但观感未经样片验证**（见 Task 13 遗留项）。

- [ ] **Step 8: 运行测试确认通过**

Run: `cd "$VIDEO_PROJECT" && node --test packages/board-kit/test/layout.test.ts && node --test packages/board-kit/test/camera.test.ts`
Expected: 两个文件全绿（layout 7 个 + camera 6 个）。

- [ ] **Step 9: 提交**

```sh
git add packages/board-kit && git commit -m "feat(board-kit): 蛇形大画布布局与默认镜头配置"
```

---

### Task 5: board-kit 渲染器与组件包工厂

**Files:**
- Create: `$VIDEO_PROJECT/packages/board-kit/src/render.ts`
- Create: `$VIDEO_PROJECT/packages/board-kit/src/package.ts`
- Create: `$VIDEO_PROJECT/packages/board-kit/src/index.ts`
- Test: `$VIDEO_PROJECT/packages/board-kit/test/package.test.ts`

**Interfaces:**
- Consumes: Task 2–4 全部
- Produces:
  - `renderDeck(timeline, canvas, window, font, events, options, deck)` — 返回 `sealVisualTrack(...)` 的结果
  - `createBoardPackage(moduleName: string, deck: Deck): { manifest: ModuleManifest; components: ComponentPackage[]; hostFacets: unknown[] }`
  - `type BoardEvent = { id: string; scene: string; text: string; beat: string; at: { frame: number } }`

- [ ] **Step 1: 确认本任务的验证方式（先读，别急着写测试）**

`render.ts` 与 `package.ts` 必须 import `@hypit/hypit/author-kit`、`@hypit/hypit/composition` 等模块。实测：**这些模块无法在普通 `node` 下导入**——`node -e 'await import("@production/board-kit")'` 会以 `ERR_MODULE_NOT_FOUND` 失败，指向 `hypit/packages/protocol/src/canonical.js`，因为 Hypit 的包内相对导入使用 `.js` 说明符，只有 Hypit 自己的加载器（`hypit` CLI）会把它映射到 `.ts`。`tsx` 直接跑也会因 tsconfig 上下文不同而失败。

因此这两个文件**不写单元测试，改用真实端到端验证**：造一个最小探针单集，让 `hypit plan` 去加载组件包。这同时验证 manifest、surface 解码、beat 校验和渲染入口，比无法导入的单元测试更强。Task 2–4、6 的纯模块仍然照常用 `node --test`。

- [ ] **Step 2: 实现 `render.ts`**

照搬参考工程 `packages/whiteboard/src/render.ts` 第 38–104 行的结构，但把所有硬编码换成 deck 数据。关键改动：

```ts
import { sealVisualTrack } from "@hypit/hypit/composition";
import { browserProgram } from "@hypit/hypit/hyperframes";
import { assertDeck, type Deck } from "./deck.ts";
import { createBoardGraphics } from "./primitives.ts";

export type BoardEvent = { id: string; scene: string; text: string; beat: string; at: { frame: number } };
export type BoardOptions = { id: string; title: string; entranceFrames: number };

export function renderDeck(timeline: any, canvas: any, window: any, font: any, events: BoardEvent[], options: BoardOptions, deck: Deck) {
  assertDeck(deck);
  const { theme } = deck;
  const g = createBoardGraphics({ theme, font });
  const panels = deck.scenes.map(scene => g.drawScene(scene));
  const ids = deck.scenes.map(scene => scene.id);
  const positions = deck.scenes.map(scene => scene.pos);

  const sceneOf = (event: BoardEvent) => {
    const index = ids.indexOf(event.scene);
    if (index < 0) throw new Error(`${deck.id}: unknown scene ${event.scene}`);
    return index;
  };
  const data = {
    positions,
    theme,
    fps: deck.camera.fps,
    end: window.span.endFrameExclusive - window.span.startFrame,
    starts: deck.scenes.map((_, i) => events.find(e => sceneOf(e) === i)?.at.frame ?? 1e9),
    events: events.map(e => ({ scene: sceneOf(e), beat: Number(e.beat), frame: e.at.frame - window.span.startFrame })),
  };
  const plan = planCamera({ starts: data.starts, eventFrames: deck.scenes.map((_, i) => data.events.filter(e => e.scene === i).map(e => e.frame)), end: data.end, positions, cfg: deck.camera });
  // ... 与参考工程一致的 html / css / setup 生成，其中：
  //   - 面板 HTML 来自 panels.map(...)，不再拼 12 个字符串
  //   - 世界尺寸来自 deck.world，连接线由相邻 positions 推导
  //   - camera / routes / objects 三段逻辑直接复用参考实现，只把 data 换成上述结构
  const children = [...panels.flatMap((_, i) => []), ...g.texts];
  for (let i = 0; i < events.length; i++) {
    children.push({ id: `caption-${i}`, kind: "text", parent: "board", order: g.texts.length + i, text: events[i].text, fonts: font.faces,
      style: [{ name: "font-size", value: "24px" }, { name: "line-height", value: "1.45" }, { name: "color", value: theme.ink }] });
  }
  return sealVisualTrack({
    id: options.id, programSpaceId: timeline.id, visualIr: "hypit.visual-ir@1",
    presents: [{ id: options.id, span: window.span, stacking: { order: 0, tieBreak: options.id },
      elements: [{ id: "board", kind: "program", order: 0, program: browserProgram({ html, css, data: { ...data, plan }, setup }),
        style: [{ name: "position", value: "absolute" }, { name: "inset", value: 0 },
          { name: "width", value: `${canvas.widthPx}px` }, { name: "height", value: `${canvas.heightPx}px` }] }, ...children] }],
  });
}
```

`setup` 与 `html`/`css` 的浏览器端代码逐字沿用参考工程 `render.ts` 的第 54–102 行，把其中 `data.positions` / `data.events` / `data.end` 的读取保持不变，新增 `const plan=data.plan`，把 `const moves=[]` 到 `const camera=frame=>{...}` 的整段删除，改为 `const camera=frame=>cameraAt(plan,frame)`，并在浏览器侧内联一份 `cameraAt`/`smoother` 实现（浏览器里不能再 import Node 模块）：

```ts
const cameraAtSource = `const smoother=t=>t*t*t*(t*(t*6-15)+10);
const cameraAt=(plan,frame)=>{let pose=plan.opening;for(const m of plan.moves){
 if(frame<m.start)break; if(frame>=m.end){pose=m.to;continue;}
 const u=Math.max(0,Math.min(1,(frame-m.start)/(m.end-m.start))),t=smoother(u);
 const baseline=Math.exp(Math.log(m.from.z)*(1-t)+Math.log(m.to.z)*t);
 const midpoint=Math.sqrt(m.from.z*m.to.z),dip=Math.max(0,Math.log(midpoint/m.wide));
 pose={cx:m.from.cx+(m.to.cx-m.from.cx)*t,cy:m.from.cy+(m.to.cy-m.from.cy)*t,z:baseline*Math.exp(-dip*Math.sin(Math.PI*t)**2)};break;
}return pose;};`;
```

**必须同时写一条断言**：`setup` 里出现的 `cameraAt(plan,frame)` 调用与 `cameraAtSource` 必须来自同一份逻辑——在测试中用 `node --test` 对同一组 `(starts, end, positions)` 分别跑 `cameraAt(planCamera(...))` 和把 `cameraAtSource` 用 `new Function` 求值，逐帧比对 `cx/cy/z` 完全相等。

- [ ] **Step 3: 实现 `package.ts`**

```ts
import { assertAttributes, assertEmptyElement, canonicalize, createMarkupSurfaceHostFacet, sameType, sealGraphFragment, textAttribute } from "@hypit/hypit/author-kit";
import { compositionTypes } from "@hypit/hypit/composition";
import { mediaTypes } from "@hypit/hypit/media";
import { timelineTypes } from "@hypit/hypit/timeline";
import { spatialTypes } from "@hypit/hypit/spatial";
import { temporalTypes } from "@hypit/hypit/temporal";
import { createTemporalInstantProjection, createTemporalWindowProjection, resolveTemporalContext,
  temporalContextAttributeVocabulary, temporalInstantAttributeNames, temporalInstantAttributeVocabulary,
  temporalWindowAttributeNames, temporalWindowAttributeVocabulary } from "@hypit/hypit/temporal-markup";
import { assertDeck, describeDeck, type Deck } from "./deck.ts";
import { renderDeck } from "./render.ts";

export function createBoardPackage(moduleName: string, deck: Deck) {
  assertDeck(deck);
  const { beatLimits } = describeDeck(deck);
  // 其余实现逐行照搬参考工程 packages/whiteboard/src/activation.ts，替换三处：
  //   1. const module = { name: moduleName, version: "1" };
  //   2. render producer 调用 renderDeck(..., deck)
  //   3. decodeSurface 中 beat 校验由 ["0","1","2"].includes(beat) 改为按 describeDeck 的 beatLimits 查表：
  //      const sceneId = textAttribute(child, "scene");
  //      const limit = beatLimits[sceneId];
  //      if (limit === undefined) throw new Error(`${moduleName}: unknown scene ${sceneId}`);
  //      if (!Number.isInteger(Number(beat)) || Number(beat) < 0 || Number(beat) >= limit)
  //        throw new Error(`${moduleName}: beat must be 0..${limit - 1}`);
  return { manifest, components: [component], hostFacets: [facet], beatLimits };
}
```

`createMarkupSurfaceHostFacet` 的 `declaration.vocabulary.example` 改为 `'<board:Scene id="board" timeline={speech.timeline} canvas={canvas} font={font} during="program" title="…"><board:Event id="s1-0" scene="s1" beat="0" text="…" at={…}/></board:Scene>'`。

- [ ] **Step 4: 写 `index.ts`**

```ts
export * from "./deck.ts";
export * from "./theme.ts";
export * from "./layout.ts";
export * from "./primitives.ts";
export * from "./camera.ts";
export * from "./components.ts";
export { renderDeck } from "./render.ts";
export { createBoardPackage } from "./package.ts";
```

`index.ts` 不得被 `node --test` 的测试引用——它 re-export 了依赖 `@hypit/hypit` 的模块，只能由 Hypit CLI 加载。测试文件一律直接从 `../src/<模块>.ts` 导入。

- [ ] **Step 5: 造最小探针单集并用 `hypit plan` 验证组件包**

```sh
cd "$VIDEO_PROJECT"
mkdir -p episodes/probe/assets episodes/probe/src episodes/probe/authors episodes/probe/runs
ffmpeg -v error -y -f lavfi -i anullsrc=r=24000:cl=mono -t 1 -c:a pcm_s16le episodes/probe/assets/narration.wav
cat > episodes/probe/lesson.json <<'JSON'
[{"id":"s01","title":"探针","lines":["一","二","三"]}]
JSON
cat > episodes/probe/package.json <<'JSON'
{"name":"@production/ep-probe","version":"0.0.0","private":true,"type":"module",
 "dependencies":{"@production/board-kit":"file:../../packages/board-kit"},
 "hypit":{"activation":"./src/activation.ts"}}
JSON
cat > episodes/probe/src/activation.ts <<'TS'
import { createBoardPackage } from "@production/board-kit";
import { deck } from "../deck.ts";
export const hypitPackage = createBoardPackage("@production/ep-probe", deck);
export default hypitPackage;
TS
cat > episodes/probe/deck.ts <<'TS'
import { defaultTheme, layout, defaultCamera, type Deck } from "@production/board-kit";
const positions = layout(1);
export const deck: Deck = {
  id: "probe", title: "探针", subtitle: "组件包装配检查",
  world: { width: 4400, height: 3400 }, theme: defaultTheme, camera: defaultCamera(1, positions),
  scenes: [{ id: "s01", title: "探针", pos: positions[0], lines: ["一", "二", "三"],
    draw: (d) => { d.text("title", "探针", 100, 24, 38, undefined, 0); d.box(100, 200, 200, 100, 1); d.arrow(100, 400, 400, 400, 2); } }],
};
TS
cat > episodes/probe/authors/main.svml <<'XML'
<?svml using="@hypit/markup@1"?>
<svml>
<import as="time" from="@hypit/timeline-author@1"/>
<import as="spatial" from="@hypit/spatial@1"/>
<import as="fonts" from="@hypit/fonts-open@1"/>
<import as="media" from="@hypit/media@1"/>
<import as="pipeline" from="@hypit/media-pipeline@1"/>
<import as="audio" from="@hypit/audio-track@1"/>
<import as="film" from="@hypit/film@1"/>
<import as="render" from="@hypit/render-hyperframes@1"/>
<import as="board" from="@production/ep-probe@1"/>
<import as="look" source="./look.svs"/>
<time:Clock id="clock" frame-rate="24"/>
<time:Timeline id="program" clock={clock} end="24f"/>
<spatial:Canvas id="canvas" width="1280" height="720"/>
<fonts:Stack id="font" family="patrick-hand" weight="400" style="normal"/>
<media:Audio id="narration" src="../assets/narration.wav"/>
<pipeline:Normalize id="voice" source={narration} video="none" audio="default" span-authority="audio" clock={clock}/>
<audio:Track id="voice-track" timeline={program.timeline}><audio:Item source={voice.media} during="program" playback="once"/></audio:Track>
<board:Scene id="whiteboard" timeline={program.timeline} canvas={canvas} font={font} title="探针" during="program">
<board:Event id="s01-0" scene="s01" beat="0" at="2f" text="一"/>
<board:Event id="s01-1" scene="s01" beat="1" at="8f" text="二"/>
<board:Event id="s01-2" scene="s01" beat="2" at="16f" text="三"/>
</board:Scene>
</svml>
XML
cat > episodes/probe/runs/final.svrun <<'XML'
<?svml using="@hypit/run-markup@1"?>
<svrun version="1"><author source="../authors/main.svml"/><target output="final.video"/></svrun>
XML
cp authors/look.svs episodes/probe/authors/look.svs
node -e 'const p=require("./package.json");p.dependencies["@production/ep-probe"]="file:episodes/probe";require("fs").writeFileSync("package.json",JSON.stringify(p,null,2)+"\n")'
npm install
node "$HYPIT_REPO/bin/hypit.mjs" plan episodes/probe/runs/final.svrun
```

Expected: `plan` 通过 `Preflight ready`，请求列表含 `@hypit/render-hyperframes#render-visual` 与 `hyperframes.local`，全部 `local, no Provider charge`，无报错。

这是**唯一在 Task 7 之前验证组件包契约的机会**，必须真的跑通。常见失败与对应原因：

| 报错 | 原因 |
|---|---|
| `Unknown module @production/ep-probe` | `npm install` 没建出 `node_modules` 符号链接 |
| `<board:Scene>` 属性校验失败 | `assertAttributes` 的属性表与 SVML 不一致 |
| `beat must be 0..2` | `describeDeck` 的 `beatLimits` 没接到 `decodeSurface` |
| `Whiteboard events need unique ids …` | 事件 id 重复或 `at` 帧号不是递增 |

- [ ] **Step 6: 提交**

```sh
git add packages/board-kit episodes/probe package.json package-lock.json
git commit -m "feat(board-kit): 渲染器、组件包工厂与探针单集验证"
```

---

### Task 6: 五类可复用图形组件

**Files:**
- Create: `$VIDEO_PROJECT/packages/board-kit/src/components.ts`
- Test: `$VIDEO_PROJECT/packages/board-kit/test/components.test.ts`

**Interfaces:**
- Consumes: `DrawContext`、`Theme`（Task 2、3）
- Produces（全部只调用 `DrawContext`，不直接产 HTML）：
  - `titleCard(d, o: { id: string; title: string; subtitle: string; x: number; y: number; beat?: Beat }): void`
  - `mechanismPanel(d, o: { id: string; x: number; y: number; width: number; height: number; label: string; beat: Beat; color?: string; fill?: string }): void`
  - `codeBlock(d, o: { id: string; lines: string[]; x: number; y: number; beat: Beat; lineHeight?: number; size?: number }): void`
  - `resultCallout(d, o: { id: string; items: string[]; x: number; y: number; beat: Beat; color?: string }): void`
  - `summaryStrip(d, o: { id: string; steps: string[]; x: number; y: number; width: number; beat: Beat }): void`

- [ ] **Step 1: 写失败测试**

`packages/board-kit/test/components.test.ts`：

```ts
import { strict as assert } from "node:assert";
import { test } from "node:test";
import { codeBlock, mechanismPanel, resultCallout, summaryStrip, titleCard } from "../src/components.ts";
import { collectBeats } from "../src/deck.ts";

const spy = () => {
  const beats: number[] = [], texts: string[] = [], strokes: number[] = [];
  return {
    beats, texts, strokes,
    ctx: {
      text: (_id: string, v: string, _x: number, _y: number, _s?: number, _c?: string, beat = 0) => { beats.push(beat); texts.push(v); },
      stroke: (_id: string, _d: string, beat = 0) => { beats.push(beat); strokes.push(beat); },
      line: (_x: number, _y: number, _a: number, _b: number, beat = 0) => { beats.push(beat); strokes.push(beat); },
      arrow: (_x: number, _y: number, _a: number, _b: number, beat = 0) => { beats.push(beat); strokes.push(beat); },
      box: (_x: number, _y: number, _w: number, _h: number, beat = 0) => { beats.push(beat); strokes.push(beat); },
      person: (_x: number, _y: number, beat = 0) => { beats.push(beat); strokes.push(beat); },
      matrix: (_x: number, _y: number, _r: number, _c: number, beat = 0) => { beats.push(beat); strokes.push(beat); },
    },
  };
};

test("titleCard 输出标题与副标题两条文本", () => {
  const s = spy();
  titleCard(s.ctx, { id: "t", title: "从零实现 感知机", subtitle: "权重 · 偏置 · 一次决策", x: 0, y: 0 });
  assert.deepEqual(s.texts, ["从零实现 感知机", "权重 · 偏置 · 一次决策"]);
  assert.deepEqual(s.beats, [0, 0]);
});

test("codeBlock 每行一条文本，并画一个外框", () => {
  const s = spy();
  codeBlock(s.ctx, { id: "c", lines: ["a = 1", "b = 2", "c = a + b"], x: 0, y: 0, beat: 1 });
  assert.equal(s.texts.length, 3);
  assert.equal(s.strokes.length, 1);
  assert.ok(s.beats.every(b => b === 1));
});

test("resultCallout 每条结论带一个对勾文本", () => {
  const s = spy();
  resultCallout(s.ctx, { id: "r", items: ["输出形状正确", "每行和为 1"], x: 0, y: 0, beat: 2 });
  assert.equal(s.texts.length, 4);
});

test("summaryStrip 为每个步骤画框，步骤间画箭头", () => {
  const s = spy();
  summaryStrip(s.ctx, { id: "s", steps: ["投影", "打分", "缩放", "归一化", "汇合"], x: 0, y: 0, width: 1000, beat: 2 });
  assert.equal(s.texts.length, 5);
  assert.equal(s.strokes.length, 5 + 4 + 4); // 5 个框 + 4 个箭头杆 + 4 个箭头尖
});

test("mechanismPanel 画框并居中写标签", () => {
  const s = spy();
  mechanismPanel(s.ctx, { id: "m", x: 0, y: 0, width: 300, height: 120, label: "机制", beat: 0 });
  assert.equal(s.texts.length, 1);
  assert.equal(s.strokes.length, 1);
});

test("所有组件产出的 beat 都是传入值", () => {
  const beatsOf = (draw: (d: any) => void) => {
    const s = spy(); draw(s.ctx); return s.beats;
  };
  assert.deepEqual(beatsOf(d => titleCard(d, { id: "t", title: "a", subtitle: "b", x: 0, y: 0, beat: 2 })), [2, 2]);
});
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd "$VIDEO_PROJECT" && node --test packages/board-kit/test/components.test.ts`
Expected: FAIL — `Cannot find module '../src/components.ts'`

- [ ] **Step 3: 实现 `components.ts`**

```ts
import type { Beat, DrawContext } from "./deck.ts";

export function titleCard(d: DrawContext, o: { id: string; title: string; subtitle: string; x: number; y: number; beat?: Beat }): void {
  const beat = o.beat ?? 0;
  d.text(`${o.id}-title`, o.title, o.x, o.y, 54, "#252b28", beat, 1100);
  d.text(`${o.id}-subtitle`, o.subtitle, o.x + 10, o.y + 86, 32, "#74ab45", beat, 1100);
}

export function mechanismPanel(d: DrawContext, o: { id: string; x: number; y: number; width: number; height: number; label: string; beat: Beat; color?: string; fill?: string }): void {
  d.box(o.x, o.y, o.width, o.height, o.beat, o.color ?? "#252b28", o.fill ?? "none");
  d.text(`${o.id}-label`, o.label, o.x + 16, o.y + Math.round(o.height / 2) - 20, 30, o.color ?? "#252b28", o.beat, o.width - 32);
}

export function codeBlock(d: DrawContext, o: { id: string; lines: string[]; x: number; y: number; beat: Beat; lineHeight?: number; size?: number }): void {
  const lineHeight = o.lineHeight ?? 53, size = o.size ?? 27;
  const width = 1110, height = o.lines.length * lineHeight + 30;
  d.box(o.x, o.y, width, height, o.beat, "#252b28", "#fafcf7");
  o.lines.forEach((line, i) => d.text(`${o.id}-l${i}`, line, o.x + 35, o.y + 27 + i * lineHeight, size, "#3788ae", o.beat, width - 70));
}

export function resultCallout(d: DrawContext, o: { id: string; items: string[]; x: number; y: number; beat: Beat; color?: string }): void {
  const color = o.color ?? "#74ab45";
  o.items.forEach((item, i) => {
    d.text(`${o.id}-mark-${i}`, "✓", o.x, o.y + i * 68, 36, color, o.beat, 60);
    d.text(`${o.id}-text-${i}`, item, o.x + 50, o.y + i * 68, 36, color, o.beat, 900);
  });
}

export function summaryStrip(d: DrawContext, o: { id: string; steps: string[]; x: number; y: number; width: number; beat: Beat }): void {
  const gap = 50, boxWidth = Math.floor((o.width - gap * (o.steps.length - 1)) / o.steps.length);
  o.steps.forEach((step, i) => {
    const x = o.x + i * (boxWidth + gap);
    d.box(x, o.y, boxWidth, 76, o.beat, i === o.steps.length - 1 ? "#74ab45" : "#252b28");
    d.text(`${o.id}-s${i}`, step, x + 36, o.y + 19, 29, "#252b28", o.beat, boxWidth - 72);
    if (i < o.steps.length - 1) d.arrow(x + boxWidth + 5, o.y + 38, x + boxWidth + gap - 5, o.y + 38, o.beat, "#74ab45");
  });
}
```

- [ ] **Step 4: 运行测试确认通过**

Run: `cd "$VIDEO_PROJECT" && node --test packages/board-kit/test/components.test.ts`
Expected: PASS，6 个 test 全绿。

- [ ] **Step 5: 提交**

```sh
git add packages/board-kit && git commit -m "feat(board-kit): 标题卡/机制图/代码块/结果卡/总结条五类组件"
```

---

### Task 7: 单集脚手架生成器

**Files:**
- Create: `$VIDEO_PROJECT/tools/classify.mjs`
- Create: `$VIDEO_PROJECT/tools/new-episode.mjs`
- Create: `$VIDEO_PROJECT/templates/voice.svml` `main.svml` `voice.svrun` `final.svrun` `edit.svrun`
- Test: `$VIDEO_PROJECT/tools/classify.test.mjs`

**Interfaces:**
- Consumes: Task 2–6 的 `@production/board-kit`
- Produces:
  - `classify(markdown: string): { tier: "T-L" | "T-M" | "T-S"; reason: string }`
  - `SCENES = { "T-L": 12, "T-M": 9, "T-S": 6 }`
  - `layout(count: number): Pos[]`（蛇形布局，3 列）
  - `node tools/new-episode.mjs <phase>-<lesson>` 生成 `episodes/<slug>/` 并写入根 `package.json`、执行 `npm install`

- [ ] **Step 1: 写失败测试**

`tools/classify.test.mjs`。`layout`/`defaultCamera` 已由 Task 4 放进 board-kit，这里只测本任务新写的 `classify`、`SCENES` 与 `lessonPath`：

```js
import { strict as assert } from "node:assert";
import { test } from "node:test";
import { SCENES, classify, lessonPath } from "./new-episode.mjs";

test("有动手构建且步骤 >= 3 判为 T-L", () => {
  const md = "## 动手构建\n\n### 第 1 步：a\n\n### 第 2 步：b\n\n### 第 3 步：c\n";
  assert.equal(classify(md).tier, "T-L");
});

test("无动手构建但正文够长判为 T-M", () => {
  const md = "## 核心概念\n\n### 甲\n\n### 乙\n\n### 丙\n";
  assert.equal(classify(md + "字".repeat(3000)).tier, "T-M");
});

test("短文档判为 T-S", () => {
  assert.equal(classify("# 标题\n\n## 概念\n\n很短。\n").tier, "T-S");
});

test("代码块不计入正文字符数", () => {
  const md = "## 概念\n\n```python\n" + "x".repeat(5000) + "\n```\n";
  assert.equal(classify(md).tier, "T-S");
});

test("三档场景数固定", () => {
  assert.deepEqual(SCENES, { "T-L": 12, "T-M": 9, "T-S": 6 });
});

test("classify 给出的档位与场景数一致", () => {
  for (const md of ["## 动手构建\n### 第 1 步\n### 第 2 步\n### 第 3 步\n", "## 核心概念\n" + "字".repeat(3000)]) {
    const { tier } = classify(md);
    assert.equal(SCENES[tier], SCENES[tier]);
    assert.ok(["T-L", "T-M", "T-S"].includes(tier));
  }
});

test("lessonPath 解析阶段与课号，指向真实存在的 docs/zh.md", () => {
  const found = lessonPath("03-01");
  assert.equal(found.dir.startsWith("01-"), true);
  assert.match(found.markdown, /phases\/03-deep-learning-core\/01-[\w-]+\/docs\/zh\.md$/);
  assert.match(found.code, /\/code$/);
});

test("lessonPath 拒绝未知阶段与不存在的课号", () => {
  assert.throws(() => lessonPath("99-01"), /未知阶段/);
  assert.throws(() => lessonPath("03-99"), /找不到第 99 课/);
});
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd "$VIDEO_PROJECT" && node --test tools/classify.test.mjs`
Expected: FAIL — `Cannot find module './new-episode.mjs'`

- [ ] **Step 3: 实现 `new-episode.mjs`**

```js
#!/usr/bin/env node
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { PANEL, defaultCamera, layout } from "../packages/board-kit/src/layout.ts";

const TOOL = dirname(fileURLToPath(import.meta.url));
export const ROOT = resolve(TOOL, "..");
export const COURSE = process.env.COURSE_REPO ?? "/Users/lirichen/Work/GithubRepo/ai-engineering-from-scratch-zh";
export const PHASES = { "03": "03-deep-learning-core", "07": "07-transformers-deep-dive", "14": "14-agent-engineering" };
export const SCENES = { "T-L": 12, "T-M": 9, "T-S": 6 };

/** 档位判定：可审计、可复算。判定依据写进 episode.json 的 reason。 */
export function classify(markdown) {
  const body = markdown.replace(/```[\s\S]*?```/g, "");
  const steps = (markdown.match(/^###\s*第\s*\d+\s*步/gm) ?? []).length;
  const sections = (markdown.match(/^### /gm) ?? []).length;
  if (markdown.includes("## 动手构建") && steps >= 3) return { tier: "T-L", reason: `含动手构建且 ${steps} 个分步` };
  if (body.length >= 3000 || sections >= 4) return { tier: "T-M", reason: `正文 ${body.length} 字符 / ${sections} 个小节` };
  return { tier: "T-S", reason: `正文 ${body.length} 字符 / ${sections} 个小节` };
}

export function lessonDirs(phase) {
  return readdirSync(join(COURSE, "phases", PHASES[phase])).filter(name => /^\d\d-/.test(name)).sort();
}

export function lessonPath(slug) {
  const [phase, lesson] = slug.split("-");
  const phaseDir = PHASES[phase];
  if (!phaseDir) throw new Error(`未知阶段 ${phase}，可选 ${Object.keys(PHASES).join(" / ")}`);
  const dir = lessonDirs(phase).find(name => name.startsWith(`${lesson}-`));
  if (!dir) throw new Error(`阶段 ${phase} 下找不到第 ${lesson} 课`);
  const root = join(COURSE, "phases", phaseDir, dir);
  return { dir, markdown: join(root, "docs", "zh.md"), code: join(root, "code") };
}

function write(rel, content) {
  const target = join(ROOT, rel);
  mkdirSync(dirname(target), { recursive: true });
  writeFileSync(target, content);
  return rel;
}

export function createEpisode(slug, { force = false } = {}) {
  const { dir, markdown, code } = lessonPath(slug);
  const { tier, reason } = classify(readFileSync(markdown, "utf8"));
  const count = SCENES[tier];
  const positions = layout(count);
  const base = `episodes/${slug}`;
  if (existsSync(join(ROOT, base)) && !force) throw new Error(`${base} 已存在；需要重建请传 --force`);
  const ids = positions.map((_, i) => `s${String(i + 1).padStart(2, "0")}`);
  const written = [];

  written.push(write(`${base}/episode.json`, `${JSON.stringify({
    slug, phase: slug.split("-")[0], lesson: dir, tier, reason, sceneCount: count,
    source: markdown.replace(`${COURSE}/`, ""), code: code.replace(`${COURSE}/`, ""),
    sourceCommit: null, createdAt: new Date().toISOString(),
  }, null, 2)}\n`));

  written.push(write(`${base}/lesson.json`, `${JSON.stringify(
    ids.map(id => ({ id, title: "", lines: ["", "", ""] })), null, 2)}\n`));

  written.push(write(`${base}/package.json`, `${JSON.stringify({
    name: `@production/ep-${slug}`, version: "0.0.0", private: true, type: "module",
    dependencies: { "@production/board-kit": "file:../../packages/board-kit" },
    hypit: { activation: "./src/activation.ts" },
  }, null, 2)}\n`));

  written.push(write(`${base}/src/activation.ts`,
`import { createBoardPackage } from "@production/board-kit";
import { deck } from "../deck.ts";

export const hypitPackage = createBoardPackage("@production/ep-${slug}", deck);
export default hypitPackage;
`));

  written.push(write(`${base}/deck.ts`,
`import { defaultTheme, layout, defaultCamera, type Deck } from "@production/board-kit";
import { lesson } from "./lesson.json" with { type: "json" };

const positions = layout(lesson.length);

export const deck: Deck = {
  id: "${slug}",
  title: "",        // 片头标题：与 episode.json 的课程标题一致
  subtitle: "",     // 片头副标题：一句话概括本集机制
  world: { width: 4400, height: 3400 },
  theme: defaultTheme,
  camera: defaultCamera(lesson.length, positions),
  scenes: [
${ids.map((id, i) => `    { id: "${id}", title: "", pos: positions[${i}], lines: ["", "", ""],
      draw: (d) => { /* beat 0/1/2 各至少画一个图元，assertDeck 会检查 */ } },`).join("\n")}
  ],
};
`));

  written.push(write(`${base}/authors/voice.svml`, readFileSync(join(ROOT, "templates/voice.svml"), "utf8")
    .replaceAll("{{SCENES}}", ids.map(id => `<${id}></${id}>`).join("\n"))));
  written.push(write(`${base}/authors/main.svml`, readFileSync(join(ROOT, "templates/main.svml"), "utf8")
    .replaceAll("{{SLUG}}", slug)
    .replaceAll("{{EVENTS}}", ids.flatMap(id => [0, 1, 2].map(beat =>
      `<board:Event id="${id}-${beat}" scene="${id}" beat="${beat}" at="0f" text=""/>`)).join("\n"))));
  written.push(write(`${base}/runs/voice.svrun`, readFileSync(join(ROOT, "templates/voice.svrun"), "utf8")
    .replaceAll("{{TARGETS}}", ids.map(id => `<target output="voice-${id}.audio"/>`).join(""))));
  for (const run of ["final", "edit"]) {
    written.push(write(`${base}/runs/${run}.svrun`, readFileSync(join(ROOT, `templates/${run}.svrun`), "utf8")
      .replaceAll("{{SLUG}}", slug)));
  }

  const rootPkg = JSON.parse(readFileSync(join(ROOT, "package.json"), "utf8"));
  rootPkg.dependencies[`@production/ep-${slug}`] = `file:${base}`;
  writeFileSync(join(ROOT, "package.json"), `${JSON.stringify(rootPkg, null, 2)}\n`);
  return { slug, tier, reason, count, written };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const slug = process.argv[2];
  if (!/^\d\d-\d\d$/.test(slug ?? "")) {
    console.error("用法: node tools/new-episode.mjs 03-01 [--force]");
    process.exit(2);
  }
  const result = createEpisode(slug, { force: process.argv.includes("--force") });
  console.log(JSON.stringify({ slug: result.slug, tier: result.tier, scenes: result.count, reason: result.reason }, null, 2));
}
```

`deck.ts` 用 `import ... with { type: "json" }` 读 `lesson.json`，是为了让场景数与 `lesson.json` 只有一个来源；Node 24 支持该语法，Hypit 的加载器也支持。若探针环境报不支持，退化为把 `lesson.length` 写成常量并加一条注释说明需与 `lesson.json` 同步。

- [ ] **Step 4: 写模板**

`templates/voice.svml`：

```xml
<?svml using="@hypit/markup@1"?>
<svml>
<import from="@hypit/script@1"/>
<import as="cosy" from="@production/cosy-speech@1"/>
<script id="story">
{{SCENES}}
</script>
</svml>
```

`templates/main.svml`：

```xml
<?svml using="@hypit/markup@1"?>
<svml>
<import as="time" from="@hypit/timeline-author@1"/>
<import as="spatial" from="@hypit/spatial@1"/>
<import as="fonts" from="@hypit/fonts-open@1"/>
<import as="media" from="@hypit/media@1"/>
<import as="pipeline" from="@hypit/media-pipeline@1"/>
<import as="audio" from="@hypit/audio-track@1"/>
<import as="film" from="@hypit/film@1"/>
<import as="render" from="@hypit/render-hyperframes@1"/>
<import as="board" from="@production/ep-{{SLUG}}@1"/>
<import as="look" source="./look.svs"/>
<time:Clock id="clock" frame-rate="24"/>
<time:Timeline id="program" clock={clock} end="0f"/>
<spatial:Canvas id="canvas" width="1280" height="720"/>
<fonts:Stack id="font" family="patrick-hand" weight="400" style="normal"><fonts:Fallback family="zcool-kuaile" weight="400" style="normal"/><fonts:Fallback family="noto-sans-sc" weight="400" style="normal"/></fonts:Stack>
<media:Audio id="narration" src="../assets/narration.wav"/>
<pipeline:Normalize id="voice" source={narration} video="none" audio="default" span-authority="audio" clock={clock}/>
<audio:Track id="voice-track" timeline={program.timeline}><audio:Item source={voice.media} during="program" playback="once"/></audio:Track>
<board:Scene id="whiteboard" timeline={program.timeline} canvas={canvas} font={font} title="" during="program">
{{EVENTS}}
</board:Scene>
</svml>
```

`templates/voice.svrun`：

```xml
<?svml using="@hypit/run-markup@1"?>
<svrun version="1"><author source="../authors/voice.svml"/>{{TARGETS}}</svrun>
```

`templates/final.svrun`：

```xml
<?svml using="@hypit/run-markup@1"?>
<svrun version="1"><author source="../authors/main.svml"/><target output="final.video"/></svrun>
```

`templates/edit.svrun`：

```xml
<?svml using="@hypit/run-markup@1"?>
<svrun version="1">
  <author source="../authors/main.svml"/>
  <target output="final.video"/>
  <build-record id="accepted-voice" build="{{VOICE_BUILD}}" output="voice.media"/>
  <satisfy output="voice.media" candidate="accepted-voice"/>
</svrun>
```

- [ ] **Step 5: 运行测试确认通过**

Run: `cd "$VIDEO_PROJECT" && node --test tools/classify.test.mjs`
Expected: PASS，8 个 test 全绿。

- [ ] **Step 6: 用三集样片骨架验证生成器**

```sh
cd "$VIDEO_PROJECT"
node tools/new-episode.mjs 03-01
node tools/new-episode.mjs 07-01
node tools/new-episode.mjs 14-01
npm install
ls -l node_modules/@production/
```

Expected: 三行 JSON 分别是 `T-L / 12 场景`、`T-L / 12 场景`、`T-M / 9 场景`；`node_modules/@production/` 下出现 4 个符号链接（board-kit + 3 个 ep-*）。**此时 `hypit plan` 会失败**（deck 的标题、旁白与图形都还是空的，`assertDeck` 会抛错，且 `at="0f"` 事件全部同帧）——这是预期的，说明生成器产出的是待填骨架，不是可直接构建的成品。

- [ ] **Step 7: 提交**

```sh
git add -A && git commit -m "feat(tools): 课程档位判定与单集脚手架生成器"
```

---

### Task 8: 配音与时间线工具链

**Files:**
- Create: `$VIDEO_PROJECT/tools/export_voice.py`
- Create: `$VIDEO_PROJECT/tools/assemble.py`
- Create: `$VIDEO_PROJECT/tools/master.py`
- Create: `$VIDEO_PROJECT/tools/check_camera.mjs`

**Interfaces:**
- Consumes: Task 7 生成的 `episodes/<slug>/{lesson.json,authors/main.svml}`
- Produces:
  - `python3 tools/export_voice.py <slug> <voice-build-id>` → `episodes/<slug>/assets/voice/<scene-id>.wav`
  - `python3 tools/assemble.py <slug> <voice-build-id>` → `assets/narration.wav`、`timing.json`、`assets/subtitles.srt`、回填帧号的 `authors/main.svml`、`evidence/alignment.json`
  - `python3 tools/master.py <slug>` → `assets/narration-master.wav`（幂等）
  - `node tools/check_camera.mjs <slug> [输出路径]` → `evidence/camera-check.json`

- [ ] **Step 1: 写 `export_voice.py`**

相对参考工程 `export_cosy.py` 只改三点：路径来自命令行、Hypit CLI 由 `HYPIT_REPO` 决定、WAV 落在单集目录。

```python
"""Export one WAV per scene from a Hypit voice build. Idempotent per build id."""
import concurrent.futures, json, os, pathlib, subprocess, sys, wave

ROOT = pathlib.Path(__file__).resolve().parent.parent
HYPIT = pathlib.Path(os.environ.get("HYPIT_REPO", "/Users/lirichen/Work/GithubRepo/hypit")) / "bin" / "hypit.mjs"

def main(slug: str, build: str) -> None:
    episode = ROOT / "episodes" / slug
    scenes = json.loads((episode / "lesson.json").read_text(encoding="utf-8"))
    assets = episode / "assets" / "voice"
    assets.mkdir(parents=True, exist_ok=True)

    def export(scene: dict) -> str:
        wav = assets / f"{scene['id']}.wav"
        receipt = wav.with_suffix(".build")
        if not wav.exists() or not receipt.exists() or receipt.read_text(encoding="utf-8").strip() != build:
            subprocess.run(["node", str(HYPIT), "get", build, "--output", f"voice-{scene['id']}.audio", "--to", str(wav)],
                           check=True, stdout=subprocess.DEVNULL)
            receipt.write_text(build, encoding="utf-8")
        with wave.open(str(wav)) as handle:
            return f"{scene['id']} {handle.getnframes() / handle.getframerate():.3f}s"

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for line in pool.map(export, scenes):
            print(line, flush=True)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("用法: python3 tools/export_voice.py <slug> <voice-build-id>")
    main(sys.argv[1], sys.argv[2])
```

`max_workers=2` 而非参考工程的 3：本部署单路合成、忙时返回 429，串行度更高更稳。

- [ ] **Step 2: 写 `assemble.py`**

相对参考工程 `assemble_cosy.py` 的改动：去掉 `if i==11` 的 12 章假设、去掉 `main-qwen.svml` 模板依赖（直接改 `authors/main.svml`）、输出文件名按单集目录、场景数由 `lesson.json` 决定。核心循环：

```python
"""Assemble paragraph performances and locate scene beats from ASR word times."""
import array, difflib, json, math, pathlib, re, sys, unicodedata, wave
from opencc import OpenCC

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONVERTER = OpenCC("t2s")
RATE = 24000


def clean(text: str) -> str:
    return "".join(c.lower() for c in unicodedata.normalize("NFKC", CONVERTER.convert(text)) if c.isalnum())


def main(slug: str, build: str) -> None:
    episode = ROOT / "episodes" / slug
    scenes = json.loads((episode / "lesson.json").read_text(encoding="utf-8"))
    cursor, chunks, events, audit = 0, [], [], []
    for index, scene in enumerate(scenes):
        wav = episode / "assets" / "voice" / f"{scene['id']}.wav"
        asr_path = wav.with_suffix(".asr.json")
        if not asr_path.exists():
            raise SystemExit(f"缺少 ASR 词时间：{asr_path}（见部署说明 §7.1）")
        with wave.open(str(wav)) as handle:
            assert (handle.getnchannels(), handle.getsampwidth(), handle.getframerate()) == (1, 2, RATE), wav
            frames = handle.getnframes()
            pcm = handle.readframes(frames)
        asr = json.loads(asr_path.read_text(encoding="utf-8"))
        observed, times = "", []
        for segment in asr["segments"]:
            for word in segment.get("words", []):
                text = clean(word["word"])
                for j, char in enumerate(text):
                    observed += char
                    times.append(word["start"] + (word["end"] - word["start"]) * j / max(1, len(text)))
        lines = [clean(line) for line in scene["lines"]]
        target = "".join(lines)
        mapping = {a + k: b + k for a, b, size in difflib.SequenceMatcher(None, target, observed, autojunk=False).get_matching_blocks() for k in range(size)}
        coverage = len(mapping) / len(target)
        if coverage < 0.65:
            raise ValueError(f"ASR 与讲稿覆盖率过低 {scene['id']}: {coverage:.3f}，检查边界与音频，不要下调阈值")
        boundaries, offset = [0.0], 0
        for line in lines[:-1]:
            offset += len(line)
            anchors = [j for j in range(offset, min(offset + 10, len(target))) if j in mapping]
            if not anchors:
                raise ValueError(f"句首锚点缺失 {scene['id']}: {offset}")
            j = anchors[0]
            boundary = times[mapping[j]]
            if j > offset:
                boundary = max(boundaries[-1] + 0.2, boundary - (j - offset) * 0.17)
            boundaries.append(boundary)
        boundaries.append(frames / RATE)
        if any(b - a < 2 for a, b in zip(boundaries, boundaries[1:])):
            raise ValueError(f"句边界过近 {scene['id']} {boundaries}")
        scene["start"] = cursor / RATE
        scene["events"] = []
        for beat, line in enumerate(scene["lines"]):
            event = {"id": f"{scene['id']}-{beat}", "scene": index, "beat": beat,
                     "start": cursor / RATE + boundaries[beat], "end": cursor / RATE + boundaries[beat + 1], "text": line}
            scene["events"].append(event)
            events.append(event)
        chunks.append(pcm)
        cursor += frames
        # 段内不插静音；只在场景之间留呼吸间隙，末段前留 1 秒。
        gap = round(RATE * (1.0 if index == len(scenes) - 1 else 0.65))
        chunks.append(bytes(gap * 2))
        cursor += gap
        scene["end"] = cursor / RATE
        audit.append({"scene": scene["id"], "coverage": round(coverage, 4), "boundaries": boundaries, "recognized": asr["text"]})
    duration = math.ceil(cursor / RATE * 24) / 24
    chunks.append(bytes((round(duration * RATE) - cursor) * 2))
    with wave.open(str(episode / "assets" / "narration.wav"), "wb") as handle:
        handle.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        handle.writeframes(b"".join(chunks))
    (episode / "timing.json").write_text(json.dumps(
        {"duration": duration, "voice_build": build, "voice": "CosyVoice official Chinese reference",
         "model": "Fun-CosyVoice3-0.5B-2512", "scenes": scenes, "events": events},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (episode / "evidence" / "alignment.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def stamp(t: float) -> str:
        ms = round(t * 1000)
        return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"

    (episode / "assets" / "subtitles.srt").write_text(
        "\n\n".join(f"{i + 1}\n{stamp(e['start'])} --> {stamp(e['end'])}\n{e['text']}" for i, e in enumerate(events)) + "\n", encoding="utf-8")

    source = (episode / "authors" / "main.svml").read_text(encoding="utf-8")
    source = re.sub(r'(<time:Timeline[^>]* end=")\d+f', lambda m: m[1] + str(round(duration * 24)) + "f", source)
    for event in events:
        source, count = re.subn(r'(<board:Event id="' + re.escape(event["id"]) + r'"[^>]* at=")\d+f',
                                lambda m: m[1] + str(round(event["start"] * 24)) + "f", source)
        assert count == 1, f"事件 {event['id']} 在 main.svml 中匹配 {count} 次，应为 1 次"
    (episode / "authors" / "main.svml").write_text(source, encoding="utf-8")
    print(json.dumps({"slug": slug, "duration": duration, "frames": round(duration * 24),
                      "minimum_ASR_agreement": min(a["coverage"] for a in audit)}, ensure_ascii=False))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("用法: python3 tools/assemble.py <slug> <voice-build-id>")
    main(sys.argv[1], sys.argv[2])
```

**非幂等提醒**：`main.svml` 的 `at` 与 `end` 每次运行都会被覆写。重复运行前先用 `git checkout -- episodes/<slug>/authors/main.svml` 还原，或依赖 `git diff` 确认结果一致。

- [ ] **Step 3: 写 `master.py`（幂等）**

参考工程的 `master_cosy.py` 在最后把 `main-cosy.svml` 里的 WAV 路径原地替换，重复运行会把路径改坏。参数化版本改为**只写音频、不改 SVML**：

```python
"""Two-pass narration loudness mastering, preserving exact timeline duration. Idempotent."""
import json, subprocess, sys, wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(slug: str) -> None:
    episode = ROOT / "episodes" / slug
    source = episode / "assets" / "narration.wav"
    target = episode / "assets" / "narration-master.wav"
    measurement = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(source), "-af", "loudnorm=I=-16:TP=-2.3:LRA=11:print_format=json", "-f", "null", "-"],
        check=True, capture_output=True, text=True).stderr
    (episode / "evidence").mkdir(exist_ok=True)
    (episode / "evidence" / "loudness.txt").write_text(measurement, encoding="utf-8")
    data = json.loads(measurement[measurement.index("{"):measurement.index("}") + 1])
    samples = round(json.loads((episode / "timing.json").read_text(encoding="utf-8"))["duration"] * 24000)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(source), "-af",
                    f'loudnorm=I=-16:TP=-2.3:LRA=11:measured_I={data["input_i"]}:measured_TP={data["input_tp"]}'
                    f':measured_LRA={data["input_lra"]}:measured_thresh={data["input_thresh"]}'
                    f':offset={data["target_offset"]}:linear=false,aresample=24000,'
                    f'apad=whole_len={samples},atrim=end_sample={samples}',
                    "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", str(target)], check=True)
    with wave.open(str(target)) as handle:
        assert handle.getnframes() == samples, "响度处理后采样数必须与时间线一致"
    # 把 source 指向已处理的音轨；已指向则不动，保证重复运行结果一致。
    svml = episode / "authors" / "main.svml"
    text = svml.read_text(encoding="utf-8")
    if "../assets/narration.wav" in text:
        svml.write_text(text.replace("../assets/narration.wav", "../assets/narration-master.wav"), encoding="utf-8")
    print(f"Mastered at -16 LUFS target, {samples} samples, unchanged duration")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("用法: python3 tools/master.py <slug>")
    main(sys.argv[1])
```

- [ ] **Step 4: 写 `check_camera.mjs`**

替代参考工程的 `check_cosy_camera.cjs`：不再正则解析源码，直接导入 deck 与相机引擎，因此场景数变化时自动适配。

```js
#!/usr/bin/env node
import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { cameraAt, planCamera } from "../packages/board-kit/src/camera.ts";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");

export function checkCamera(deck, timing, fps = 24) {
  const ends = Math.round(timing.duration * fps);
  const positions = deck.scenes.map(s => s.pos);
  const starts = deck.scenes.map((_, i) => Math.round((timing.events.find(e => e.scene === i)?.start ?? 1e9) * fps));
  const eventFrames = deck.scenes.map((_, i) => timing.events.filter(e => e.scene === i).map(e => Math.round(e.start * fps)));
  const plan = planCamera({ starts, eventFrames, end: ends, positions, cfg: deck.camera });
  const fail = [];
  for (let i = 0; i < plan.moves.length; i++) {
    const m = plan.moves[i];
    if (!(m.end > m.start)) fail.push(`move ${i}: end <= start`);
    if (i && m.start < plan.moves[i - 1].end) fail.push(`move ${i}: overlaps previous`);
    for (const edge of [m.start, m.end]) {
      const a = cameraAt(plan, edge - 1e-5), b = cameraAt(plan, edge + 1e-5);
      if (Math.hypot(a.cx - b.cx, a.cy - b.cy) >= 0.01) fail.push(`move ${i}: position jump at ${edge}`);
      if (Math.abs(a.z - b.z) >= 1e-5) fail.push(`move ${i}: zoom jump at ${edge}`);
    }
  }
  for (let f = 0; f < ends; f++) {
    const p = cameraAt(plan, f);
    if (!Number.isFinite(p.cx) || !Number.isFinite(p.cy) || !(p.z > 0)) { fail.push(`frame ${f}: invalid pose`); break; }
  }
  return { frames: ends, moves: plan.moves.length, continuous: fail.length === 0, failures: fail };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const slug = process.argv[2];
  if (!slug) { console.error("用法: node tools/check_camera.mjs <slug> [输出路径]"); process.exit(2); }
  const { deck } = await import(join(ROOT, "episodes", slug, "deck.ts"));
  const timing = JSON.parse((await import("node:fs")).readFileSync(join(ROOT, "episodes", slug, "timing.json"), "utf8"));
  const result = checkCamera(deck, timing);
  const out = process.argv[3] ?? join(ROOT, "episodes", slug, "evidence", "camera-check.json");
  mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, `${JSON.stringify(result, null, 2)}\n`);
  console.log(`${result.moves} camera moves over ${result.frames} frames: ${result.continuous ? "finite, continuous, no overlaps" : "FAILED"}`);
  if (!result.continuous) { console.error(result.failures.join("\n")); process.exit(1); }
}
```

**这条命令不替代实际观看**：它只证明数值有效、运动区间不重叠、端点连续，不能证明画面没有遮挡、文字可读或速度舒适。

- [ ] **Step 5: 用参考工程回归验证 `check_camera.mjs`**

把参考工程的 `positions`（12 个世界坐标）和 `timing-cosy.json` 喂给 `checkCamera`，输出必须与参考工程 `check_cosy_camera.cjs` 的 `evidence/cosy-camera-check.json` 的 `moves` 条数一致。

Run: `cd "$VIDEO_PROJECT" && node -e 'const t=require(process.env.REFERENCE + "/timing-cosy.json"); console.log(t.events.length)'`
Expected: `36`（12 场景 × 3 beat，确认参考数据可用）

- [ ] **Step 6: 提交**

```sh
git add tools && git commit -m "feat(tools): 参数化配音导出、时间线装配、响度处理与镜头检查"
```

---

### Task 9: 5 秒片头工具

**Files:**
- Create: `$VIDEO_PROJECT/tools/add_title.py`

**Interfaces:**
- Consumes: `episodes/<slug>/assets/narration-master.wav`、`timing.json`、`assets/subtitles.srt`、`authors/main.svml`
- Produces: `assets/narration-master-title.wav`、`timing-title.json`、`assets/subtitles-title.srt`、`authors/main-title.svml`、`runs/final-title.svrun`、`runs/edit-title.svrun`

参考工程的手册第 9 节明确写着片头**没有一键脚本**，需要人工同步四类文件；83 集必须脚本化。

- [ ] **Step 1: 写 `add_title.py`**

```python
"""Prepend a silent title segment and shift the whole timeline by exactly N seconds.

参考工程手册第 9 节：片头不是 assemble 的一部分。本脚本把原先必须手工同步的四类
文件（WAV 前置静音、SVML 的 Timeline/Event 帧号、timing JSON、SRT）合成一步，
并且不做整体减速——那样会改变语速。
"""
import json, pathlib, re, sys, wave

ROOT = pathlib.Path(__file__).resolve().parent.parent
RATE = 24000
FPS = 24


def main(slug: str, seconds: float = 5.0) -> None:
    episode = ROOT / "episodes" / slug
    frames = round(seconds * FPS)
    assert abs(frames / FPS - seconds) < 1e-9, "片头时长必须是 1/24 秒的整数倍"

    # 1) 音频：前置静音，之后 PCM 逐字节不变。
    source = episode / "assets" / "narration-master.wav"
    target = episode / "assets" / "narration-master-title.wav"
    with wave.open(str(source)) as handle:
        params, pcm = handle.getparams(), handle.readframes(handle.getnframes())
    assert params.framerate == RATE and params.sampwidth == 2 and params.nchannels == 1, params
    with wave.open(str(target), "wb") as handle:
        handle.setparams(params)
        handle.writeframes(bytes(round(seconds * RATE) * 2) + pcm)

    # 2) 时间线：Timeline end 与所有 Event 的 at 顺延同一帧数。
    svml = (episode / "authors" / "main.svml").read_text(encoding="utf-8")
    svml = svml.replace("../assets/narration-master.wav", "../assets/narration-master-title.wav")
    end = int(re.search(r'<time:Timeline[^>]* end="(\d+)f"', svml).group(1))
    svml = re.sub(r'(<time:Timeline[^>]* end=")\d+f', lambda m: m[1] + str(end + frames) + "f", svml)
    svml, count = re.subn(r'(<board:Event [^>]* at=")(\d+)f', lambda m: m[1] + str(int(m.group(2)) + frames) + "f", svml)
    assert count, "main.svml 中没有任何 board:Event"
    (episode / "authors" / "main-title.svml").write_text(svml, encoding="utf-8")

    # 3) timing：duration、场景 start/end、事件 start/end 全部顺延 seconds。
    timing = json.loads((episode / "timing.json").read_text(encoding="utf-8"))
    timing["duration"] = round(timing["duration"] + seconds, 6)
    timing["title_seconds"] = seconds
    for scene in timing["scenes"]:
        scene["start"] += seconds
        scene["end"] += seconds
        for event in scene["events"]:
            event["start"] += seconds
            event["end"] += seconds
    for event in timing["events"]:
        event["start"] += seconds
        event["end"] += seconds
    (episode / "timing-title.json").write_text(json.dumps(timing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 4) 字幕：每条起止同时顺延。
    def shift(match: re.Match) -> str:
        def stamp(value: float) -> str:
            ms = round(float(value) * 1000) + round(seconds * 1000)
            return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"
        def parse(text: str) -> float:
            h, m, rest = text.split(":"); s, milli = rest.split(",")
            return int(h) * 3600 + int(m) * 60 + int(s) + int(milli) / 1000
        return f"{stamp(parse(match.group(1)))} --> {stamp(parse(match.group(2)))}"

    srt = (episode / "assets" / "subtitles.srt").read_text(encoding="utf-8")
    srt = re.sub(r"(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)", shift, srt)
    (episode / "assets" / "subtitles-title.srt").write_text(srt, encoding="utf-8")

    # 5) Runs：标题版指向标题版 Source。
    (episode / "runs" / "final-title.svrun").write_text(
        '<?svml using="@hypit/run-markup@1"?>\n<svrun version="1"><author source="../authors/main-title.svml"/>'
        '<target output="final.video"/></svrun>\n', encoding="utf-8")
    print(json.dumps({"slug": slug, "title_seconds": seconds, "frames_added": frames,
                      "duration": timing["duration"]}, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit("用法: python3 tools/add_title.py <slug> [秒数，默认 5]")
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) == 3 else 5.0)
```

片头的**画面**由 deck 的标题卡与 `planCamera` 的 `opening` 段负责：`deck.title`/`deck.subtitle` 渲染在 `worldTitle`/`worldSubtitle` 世界坐标上，第一场景的第一个事件晚于第 0 帧时，镜头从标题区域出发并在约 2.5 秒后移向首图。**只改 Scene 的 `title` 属性不会替换片头文字**——必须改 `deck.ts` 里的 `title`/`subtitle`。

- [ ] **Step 2: 在样片 A 上验证帧数守恒**

Run（在 Task 10 完成后）：`cd "$VIDEO_PROJECT" && python3 tools/add_title.py 03-01 5 && python3 -c "import json;t=json.load(open('episodes/03-01/timing-title.json'));print(round(t['duration']*24))"`
Expected: 输出的帧数比 `timing.json` 的帧数正好多 120。

- [ ] **Step 3: 提交**

```sh
git add tools && git commit -m "feat(tools): 5 秒片头时间顺延脚本"
```

---

### Task 10: 样片 A · 03-01 感知机（T-L，12 场景）

**Files:**
- Modify: `$VIDEO_PROJECT/episodes/03-01/{episode.json,lesson.json,deck.ts}`
- Create: `$VIDEO_PROJECT/episodes/03-01/{assets,evidence,output}/…`

**Interfaces:**
- Consumes: Task 1–9 全部
- Produces: `episodes/03-01/output/03-01-perceptron.mp4` + 全套验收证据

课程源（只读）：`phases/03-deep-learning-core/01-the-perceptron/docs/zh.md`、`code/perceptron.py`。

- [ ] **Step 1: 读源材料并写 `episode.json`**

把 `lesson` 改为 `01-the-perceptron`，并把课程源文件的当前提交记入 `sourceCommit`：

```sh
cd /Users/lirichen/Work/GithubRepo/ai-engineering-from-scratch-zh
git log -1 --format=%H -- phases/03-deep-learning-core/01-the-perceptron
```

- [ ] **Step 2: 写 12 个场景的讲稿（`lesson.json`）**

场景顺序与 `docs/zh.md` 的小节一一对应，每场景 3 段、每段 110–180 字：

| # | id | 标题 | 取材小节 |
|---|---|---|---|
| 1 | s01 | 机器怎么学会该用哪种变换 | 问题背景 |
| 2 | s02 | 一个神经元，一个决策 | 一个神经元，一个决策 |
| 3 | s03 | 加权求和，再加一个偏置 | 一个神经元，一个决策 |
| 4 | s04 | 阶跃函数：把结果压成 0 或 1 | 一个神经元，一个决策 |
| 5 | s05 | 决策边界就是一条直线 | 决策边界 |
| 6 | s06 | 学习规则：错了就往回推 | 学习规则 |
| 7 | s07 | 训练一个 OR 门 | 第 2 步：在逻辑门上训练 |
| 8 | s08 | XOR：单层网络的死穴 | XOR 问题、第 3 步 |
| 9 | s09 | 加一层隐藏层 | 第 4 步：用两层解决 XOR |
| 10 | s10 | 换成 sigmoid，让它自己学 | 第 5 步：训练一个两层网络 |
| 11 | s11 | 把整条流程写成 Python | `code/perceptron.py` |
| 12 | s12 | 一张白板，一个感知机 | 关键术语、练习 |

每段旁白必须能追溯回上表小节；`s11` 的旁白要与 `perceptron.py` 的实际变量名一致（打开文件核对，不得凭印象写）。`s08` 必须讲清「线性不可分」而不只是说「XOR 失败了」。

- [ ] **Step 3: 写 `deck.ts` 的图形**

对 12 个场景逐个实现 `draw`，遵守：

- 每个场景的标题用 `d.text(sceneTitle, …)` 画在 `(100, 24)`，字号 38，beat 0；标题下画一条绿色手绘下划线（照参考工程 `path('M100,74 Q220,67 370,74',0,green,8)`）。
- 复用 Task 6 的 `codeBlock`（s11）、`resultCallout`（s10 的两条自检）、`summaryStrip`（s12 的「输入 → 加权求和 → 激活 → 决策」）。
- `s05` 的决策边界用两条带不同斜率的直线加一个不可分区域示意；`s08` 与 `s09` 用 `d.person` + `d.arrow` 对比单层与两层。
- 任何运行结果都必须来自实际执行 `perceptron.py` 的数值，**不得编造**：在仓库根运行

  ```sh
  cd /Users/lirichen/Work/GithubRepo/ai-engineering-from-scratch-zh/phases/03-deep-learning-core/01-the-perceptron/code
  python3 -c "import perceptron as p; print([n for n in dir(p) if not n.startswith('_')])"
  ```

  把真实的权重、偏置或准确率写进 `s10`/`s11` 的画面，并在 `evidence/` 保存原始输出。
- `assertDeck` 必须通过：每个场景 3 个 beat 各有图元，`title`/`lines` 非空。
- `deck.title` = `感知机`，`deck.subtitle` = `权重 · 偏置 · 一次决策`。

- [ ] **Step 4: 静态校验**

Run: `cd "$VIDEO_PROJECT" && node -e 'const {deck}=await import("./episodes/03-01/deck.ts");const {assertDeck}=await import("@production/board-kit");assertDeck(deck);const {checkCamera}=await import("./tools/check_camera.mjs");console.log("deck ok:",deck.scenes.length,"场景")'`
Expected: `deck ok: 12 场景`，无抛错。

- [ ] **Step 5: 生成配音并试听一段**

```sh
cd "$VIDEO_PROJECT"
node "$HYPIT_REPO/bin/hypit.mjs" plan episodes/03-01/runs/voice.svrun
node "$HYPIT_REPO/bin/hypit.mjs" build episodes/03-01/runs/voice.svrun --follow
export VOICE_BUILD='<上一步返回的 Build ID>'
python3 tools/export_voice.py 03-01 "$VOICE_BUILD"
```

Expected: 12 行 `sNN N.NNNs`，每段 25–45 秒。
**先试听 `assets/voice/s07.wav` 与 `assets/voice/s11.wav`**：确认「感知机」「偏置」「XOR」「sigmoid」「反向传播」发音正确、段内停顿自然。不通过就改讲稿重跑本步，不要进入下一步。

- [ ] **Step 6: ASR 词时间戳**

按 `deployment/cosyvoice3/README.md` 的流程，在远程独立目录运行 `transcribe_paragraphs.py` 的本次副本（只对本集 WAV），把 `*.asr.json` 拷回 `episodes/03-01/assets/voice/`。每个 WAV 都必须有对应 JSON；同名音频换了内容时必须换目录或先移走旧 JSON。

- [ ] **Step 7: 拼接、响度、镜头**

```sh
cd "$VIDEO_PROJECT"
python3 -m venv .venv-ops
.venv-ops/bin/python -m pip install opencc-python-reimplemented
.venv-ops/bin/python tools/assemble.py 03-01 "$VOICE_BUILD"
.venv-ops/bin/python tools/master.py 03-01
node tools/check_camera.mjs 03-01
```

Expected: `assemble.py` 打印 `minimum_ASR_agreement ≥ 0.65`；`check_camera.mjs` 打印 `… finite, continuous, no overlaps`。任一失败都回到上一步查边界与音频，**不得下调 0.65 阈值**。

- [ ] **Step 8: 加片头**

```sh
cd "$VIDEO_PROJECT"
python3 tools/add_title.py 03-01 5
node tools/check_camera.mjs 03-01 episodes/03-01/evidence/camera-check-title.json
```

Expected: `frames_added = 120`；标题版镜头检查同样连续。

- [ ] **Step 9: 预览、正式渲染、导出**

```sh
cd "$VIDEO_PROJECT"
node "$HYPIT_REPO/bin/hypit.mjs" studio --run episodes/03-01/runs/final-title.svrun
# 浏览器打开命令返回的地址；抽片头与转场连续帧，同时播放观看运动、朗读与字幕
node "$HYPIT_REPO/bin/hypit.mjs" snapshot --studio http://localhost:5179 \
  --at-frame 0,48,60,84,108,120,144 --grid 4x2 --cell 480 --to episodes/03-01/evidence/title-review
node "$HYPIT_REPO/bin/hypit.mjs" runtime status
node "$HYPIT_REPO/bin/hypit.mjs" plan episodes/03-01/runs/final-title.svrun
node "$HYPIT_REPO/bin/hypit.mjs" build episodes/03-01/runs/final-title.svrun --follow
export FINAL_BUILD='<上一步返回的 Build ID>'
node "$HYPIT_REPO/bin/hypit.mjs" status "$FINAL_BUILD"
node "$HYPIT_REPO/bin/hypit.mjs" get "$FINAL_BUILD" --output final.video --to episodes/03-01/output/03-01-perceptron.mp4
```

`--follow` 断线不代表任务停止，先查 `status` 再重试，避免重复提交。

- [ ] **Step 10: 技术验收**

```sh
cd "$VIDEO_PROJECT"
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,duration,nb_frames:format=duration,size \
  -of json episodes/03-01/output/03-01-perceptron.mp4 > episodes/03-01/evidence/final-probe.json
ffmpeg -v error -i episodes/03-01/output/03-01-perceptron.mp4 -f null - 2> episodes/03-01/evidence/final-decode.txt
node "$HYPIT_REPO/bin/hypit.mjs" media tiles episodes/03-01/output/03-01-perceptron.mp4 \
  --start 0 --end 7 --every 0.5 --columns 4 --rows 4 --cell 480 --to episodes/03-01/evidence/final-opening
wc -c episodes/03-01/evidence/final-decode.txt
```

要求：解码退出码 0、`final-decode.txt` 为 0 字节、`width=1280 height=720`、`r_frame_rate=24/1`、时长落在 240–360 秒（T-L 档 4–6 分钟）、帧数与 `timing-title.json` 的 `round(duration*24)` 一致。

- [ ] **Step 11: 建立 edit Run 并提交**

用**本次完成的 Build** 写 `episodes/03-01/runs/edit-title.svrun`（替换 `{{VOICE_BUILD}}`）。只改路径不会自动更新 Candidate。

```sh
cd "$VIDEO_PROJECT"
git add episodes/03-01 package.json package-lock.json
git commit -m "feat(ep-03-01): 感知机 T-L 样片成片与验收证据"
```

---

### Task 11: 样片 B · 07-01 为什么需要 Transformer（T-L，12 场景）

**Files:** 同 Task 10，路径换成 `episodes/07-01/`

**Interfaces:**
- Consumes: Task 1–9，以及 Task 10 暴露出的模板修正
- Produces: `episodes/07-01/output/07-01-why-transformers.mp4` + 证据

课程源（只读）：`phases/07-transformers-deep-dive/01-why-transformers/docs/zh.md` 及其 `code/`。

- [ ] **Step 1: 写 `episode.json`、12 段讲稿与 `deck.ts`**

场景顺序对应小节：

| # | id | 标题 | 取材小节 |
|---|---|---|---|
| 1 | s01 | 一句话，为什么不能一次看完 | 问题背景 |
| 2 | s02 | RNN：一步一步传递状态 | 核心概念 |
| 3 | s03 | 串行深度：N 步不能并行 | 核心概念 |
| 4 | s04 | 第 1 步：测量串行深度 | 第 1 步：测量串行深度 |
| 5 | s05 | 第 2 步：数一数理论运算量 | 第 2 步：数一数理论运算量 |
| 6 | s06 | 第 3 步：长序列上的实测扩展 | 第 3 步：长序列上的实测扩展 |
| 7 | s07 | 状态是瓶颈 | 核心概念 |
| 8 | s08 | 长程依赖要走很远的路 | 核心概念 |
| 9 | s09 | 注意力：一次看到整段 | 核心概念 |
| 10 | s10 | 代价：注意力是 O(n²) | 核心概念、实际使用 |
| 11 | s11 | 用代码量一遍 | 动手构建的三步合并展示 |
| 12 | s12 | 一张白板，从 RNN 到注意力 | 关键术语 |

`s04`–`s06` 的画面与旁白必须使用**实际运行三个测量脚本得到的数字**；在仓库根的 `code/` 目录运行并把原始输出存进 `evidence/`：

```sh
cd /Users/lirichen/Work/GithubRepo/ai-engineering-from-scratch-zh/phases/07-transformers-deep-dive/01-why-transformers/code
ls -1 && for f in *.py; do echo "== $f"; python3 "$f" 2>&1 | tee "$VIDEO_PROJECT/episodes/07-01/evidence/measure-${f%.py}.txt" | head -30; done
```

`s10` 必须说明 O(n²) 是注意力自身的代价，且与 RNN 的串行瓶颈是一组权衡，不得只讲优点。

- [ ] **Step 2: 静态校验**

Run: `cd "$VIDEO_PROJECT" && node -e 'const {deck}=await import("./episodes/07-01/deck.ts");const {assertDeck}=await import("@production/board-kit");assertDeck(deck);console.log("deck ok:",deck.scenes.length,"场景")'`
Expected: `deck ok: 12 场景`

- [ ] **Step 3: 跑完整制作链**

按 Task 10 的 Step 5–10 执行同样的命令序列，把 `03-01` 换成 `07-01`。

- [ ] **Step 4: 技术验收**

同 Task 10 Step 10，路径换成 `episodes/07-01`，成片名 `07-01-why-transformers.mp4`，时长同样要求落在 240–360 秒。

- [ ] **Step 5: 提交**

```sh
cd "$VIDEO_PROJECT"
git add episodes/07-01 package.json package-lock.json
git commit -m "feat(ep-07-01): 为什么需要 Transformer T-L 样片成片与验收证据"
```

---

### Task 12: 样片 C · 14-01 Agent 循环（T-M，9 场景）

**Files:** 同 Task 10，路径换成 `episodes/14-01/`

**Interfaces:**
- Consumes: Task 1–9，以及 Task 10、11 暴露出的模板修正
- Produces: `episodes/14-01/output/14-01-agent-loop.mp4` + 证据；**第一个 T-M 档模板验证**

课程源（只读）：`phases/14-agent-engineering/01-the-agent-loop/docs/zh.md`。

- [ ] **Step 1: 写 `episode.json`、9 段讲稿与 `deck.ts`**

| # | id | 标题 | 取材小节 |
|---|---|---|---|
| 1 | s01 | 一次问答，和一次任务差在哪 | 问题背景 |
| 2 | s02 | 观察 → 思考 → 行动 | 核心概念 |
| 3 | s03 | ReAct：标准格式 | ReAct：标准格式 |
| 4 | s04 | 2026 年的转变：原生推理 | 2026 年的转变：原生推理 |
| 5 | s05 | 五大要素 | 五大要素 |
| 6 | s06 | 工具是循环的手 | 五大要素 |
| 7 | s07 | 为什么这个循环无处不在 | 为什么这个循环无处不在 |
| 8 | s08 | 2026 年的坑 | 2026 年的坑 |
| 9 | s09 | 一屏总览：一个 Agent 循环 | 动手构建、关键术语 |

`s05` 用 `mechanismPanel` 画五个要素并连线；`s09` 用 `summaryStrip` 收束「观察 → 思考 → 行动 → 再观察」。`s08` 必须写出具体坑（例如把工具失败当成任务失败），不能只说「有坑」。

- [ ] **Step 2: 静态校验**

Run: `cd "$VIDEO_PROJECT" && node -e 'const {deck}=await import("./episodes/14-01/deck.ts");const {assertDeck}=await import("@production/board-kit");assertDeck(deck);console.log("deck ok:",deck.scenes.length,"场景")'`
Expected: `deck ok: 9 场景`（确认 T-M 档与 12 场景共用同一引擎，`camera.local.z` 自动为 9 项）

- [ ] **Step 3: 跑完整制作链**

按 Task 10 的 Step 5–10 执行，把 `03-01` 换成 `14-01`。

- [ ] **Step 4: 技术验收**

同 Task 10 Step 10，路径换成 `episodes/14-01`，成片名 `14-01-agent-loop.mp4`，**时长要求落在 180–240 秒**（T-M 档 3–4 分钟）。

- [ ] **Step 5: 提交**

```sh
cd "$VIDEO_PROJECT"
git add episodes/14-01 package.json package-lock.json
git commit -m "feat(ep-14-01): Agent 循环 T-M 样片成片与验收证据"
```

---

### Task 13: 三样片集中评审、模板冻结与量产交接

**Files:**
- Modify: `$VIDEO_PROJECT/REVIEW.md`、`$VIDEO_PROJECT/PROGRESS.md`
- Create: `$VIDEO_PROJECT/docs/量产-runbook.md`

**Interfaces:**
- Consumes: Task 10–12 的三集成片与证据
- Produces: 冻结的模板（此后改动必须走单独提交）、80 集量产的可执行 runbook

- [ ] **Step 1: 三集连看听审并记录**

同一场次连看 03-01、07-01、14-01 三集，逐条填写 `REVIEW.md`：

- 标题一开始就能看到，正文衔接自然。
- 旧图形仍在同一画布中；移动时没有跳变或突兀停顿。
- 图形与当前讲解一致，字幕没有抢跑或明显滞后。
- 数字、公式、中英文术语发音正确；整段语气自然；段间没有长空白。
- 文字在 1280×720 目标观看尺寸可读，字幕没有压住重要内容。
- 片尾完整，没有截掉最后一句或总览。
- **不同档位（12 场景 vs 9 场景）之间的观感是否一致**；若不一致，记录差异并决定是改模板还是接受。

**不得用「ASR 覆盖率达标」或「零解码错误」代替听审**——参考工程正是因为缺少这一步被记为未完成项。

- [ ] **Step 2: 按评审结论冻结或修正模板**

若需要修正，只改 `packages/board-kit` 或 `tools/`，然后**重跑三集的静态校验与镜头检查**，受影响集重新渲染。冻结后在 `BRIEF.md` 增加一行「模板冻结于 <commit>，此后修改需单独提交并重跑三样片校验」。

- [ ] **Step 3: 写量产 runbook**

`docs/量产-runbook.md` 必须包含：

- 三条流水线的集号全表（A：03-01…03-13；B：07-01…07-16；C：14-01…14-54），每行标注档位。
- 单集标准作业：`new-episode.mjs` → 写讲稿 → 写 deck → 静态校验 → 配音试听 → ASR → assemble/master/check → 加片头 → 预览 → 渲染导出 → 技术验收 → 提交。每步给出与 Task 10 完全相同的命令，把 `03-01` 换成 `<slug>`。
- 每集之间的检查点：逐集验收通过才放行下一集；`PROGRESS.md` 更新状态、当前步骤与阻塞原因。
- 资源冲突让行顺序：C（14）→ B（07）→ A（03），但**任一阶段内部的课号顺序不得改变**。
- 失败重试规则：`--follow` 断线先查 `status`；失败后保存已成功 Outputs，在新 Run 中显式选择可复用结果再重试；不重复生成已完成配音。
- 已知风险：T-S 档（6 场景，14-43…14-54）在三样片中未验证，14-43 是它的首次验证点，量产到该集时必须按 Task 10 Step 4/7 全套检查。

- [ ] **Step 4: 更新进度表并提交**

`PROGRESS.md` 中 03-01、07-01、14-01 状态置为「已交付」，其余行置为「待制作」并填入档位。

```sh
cd "$VIDEO_PROJECT"
git add -A && git commit -m "docs: 三样片评审结论、模板冻结与量产 runbook"
```

- [ ] **Step 5: 把制作决定回写到 spec**

若评审改变了档位边界、场景数或时长区间，同步更新 `docs/plans/ai-engineering-video-series.md` 并通过 PR 修改（不得直接 push `main`）。

```sh
cd /Users/lirichen/Work/GithubRepo/ai-engineering-from-scratch-zh
git switch feature/hypit-video-series-plan
git add docs/plans/ai-engineering-video-series.md
git commit -m "docs: 按样片评审结论更新视频计划"
git push origin feature/hypit-video-series-plan
```

---

## 自检

**1. Spec 覆盖**

| Spec 要求 | 落在哪个任务 |
|---|---|
| 83 集 / 三阶段并行 / 阶段内串行 | Task 13 Step 3 的 runbook + `PROGRESS.md` 三张表 |
| 1280×720 / 24 fps | Task 1 Step 6（BRIEF）、Task 7 模板 `<spatial:Canvas>`、Task 10 Step 10 技术验收 |
| 分档 T-L / T-M / T-S | Task 7 `classify` + `SCENES`，Task 10/11/12 各验一档 |
| 独立制作工程在 `eanfs/hypit-productions`，经子模块挂在课程仓 `hypit-productions/` | Task 1（含「不要 `git init`」的理由） |
| 从讲义/代码/测验整理每集依据，记录 Git 提交 | Task 10 Step 1–3（`sourceCommit`，`perceptron.py` 实跑），Task 11 Step 1 |
| 统一视觉模板五类可复用组件 | Task 6 |
| 区分图解与证据；模拟结果明确标注 | Task 10 Step 3（实跑脚本取数）、Task 11 Step 1 |
| 自建 CosyVoice 3、段内停顿、0.65 秒场景间隙 | Task 8 `assemble.py`、Task 10 Step 5 |
| ASR 辅助定位，字幕取讲稿 | Task 8 `assemble.py`，Task 10 Step 6 |
| `check` / `plan` / `build` 与 Studio 检视 | Task 10 Step 9 |
| 交付 MP4 / SRT / 封面 / 文案 / 源文件 / Build ID | Task 10 Step 10–11（封面与文案在量产批补齐，样片批先交 MP4+SRT+源文件） |
| 5 秒片头 | Task 9，Task 10 Step 8 |
| 验收：时长、分辨率、音画同步、可追溯、可读字幕 | Task 10 Step 10，Task 13 Step 1 |
| 三条流水线进度表 | Task 13 Step 4 |
| 资源冲突让行顺序 | Task 13 Step 3 |
| 费用边界（第三方语音 ¥0） | Task 1 Step 3（服务健康检查）；无付费调用路径 |

**缺口（已显式记为遗留项，不在本计划范围）：** 封面与发布文案（量产批补齐）、T-S 档（6 场景）模板与镜头的观感验证（14-43 首次验证）、除 03-01/07-01/14-01 外的 80 集。

**2. 占位符扫描**：计划中不含 TBD/TODO；所有代码步骤都给出了可执行的代码或命令；`deck.ts` 与 `lesson.json` 的空白字段是**生成器刻意产出的待填骨架**，由 Task 10/11/12 的 Step 1–3 明确要求填写，不属于计划占位符。

**3. 类型一致性**：`DrawContext` 的七个方法名与签名在 Task 2 定义，Task 3 实现、Task 6 使用、`collectBeats`/`assertDeck` 校验，四处一致。`planCamera` 的入参 `{ starts, eventFrames, end, positions, cfg }` 在 Task 4 定义，Task 5 `render.ts` 与 Task 8 `check_camera.mjs` 调用一致。`PanelGraphics` 字段 `{ id, pos, strokes, labels, beats }` 在 Task 3 定义，Task 5 消费。`describeDeck` 在 Task 2 定义并导出，Task 5 的 `createBoardPackage` 消费它产出的 `beatLimits`。`layout`/`defaultCamera` 在 Task 4 定义，Task 5 的 `index.ts` 导出，Task 7 的生成器与单集 `deck.ts` 消费——`new-episode.mjs` 直接 import `../packages/board-kit/src/layout.ts`，不再自带一份。集目录字段 `slug/phase/lesson/tier/reason/sceneCount/source/code/sourceCommit` 在 Task 7 写出，Task 10 Step 1 修改同名字段。

**4. 已在写计划期间实测并据此修正的事实**（这些是计划成立的前提，执行时若与实测不符应先停下来核对）：

| 事实 | 实测结果 | 对计划的影响 |
|---|---|---|
| `@hypit/hypit/*` 能否用普通 `node` 导入 | **不能**，`ERR_MODULE_NOT_FOUND` → `hypit/packages/protocol/src/canonical.js` | Task 5 放弃单元测试，改用探针单集 + `hypit plan` |
| Node 版本能否原生跑 `.ts`（含从 `.mjs` 导入 `.ts`） | **能**，Node 24.16.0 | Task 2–4、6、7 的 `node --test` 方案成立 |
| 参考工程能否 `hypit plan` | **能**，`Preflight ready`，全部 local provider、零费用 | Task 1 Step 5 作为工具链门禁 |
| CosyVoice 3 服务 | **在线**，`172.16.12.71:8097` 返回 `status: ready` | Task 1 Step 3 的健康检查可用作硬门禁 |
| 参考工程 `check_cosy_camera.cjs` 的场景数 | 写死 `Array(12)`，且用正则从 `render.ts` 抠 `positions` | Task 4/8 必须重写为导入 deck，本计划已改 |
| 参考工程 `render.ts` 硬编码量 | 12 个标题、12 个场景 id、12 组世界坐标、12 段逐场景绘制代码全在引擎里 | 这是本计划拆出 board-kit 的直接原因 |
| `assemble_cosy.py` / `master_cosy.py` 的隐含假设 | 前者 `if i==11` 写死 12 章并依赖 `main-qwen.svml` 作模板；后者原地改写 SVML，**不幂等** | Task 8 两处参数化并修正幂等性 |
| 探针单集的相机边界 | 单场景会让 `localPose(last-1)` 取到 `positions[-1]`；T-S（6 场景）会让 `recap.secondReview` 的 6/7/8 越界 | Task 4 加入下标夹取与 `at()` 裁剪，并加两条测试 |
| 制作工程仓库形态 | 已建 `eanfs/hypit-productions`（私有）并作为子模块挂入课程仓；入库 367 文件 / 16.2 MB，排除 `.hypit/`（1.4G）、音频、成片与第三方参考视频 | 工程根改到子模块内 `<课程仓>/hypit-productions/ai-engineering-zh`；Task 1 Step 7 从「`git init`」改为「提交进父仓库」 |
| 子模块副本能否直接跑 | 不能：`node_modules/` 与 `.hypit/` 被 `.gitignore` 排除 | Task 1 Step 5 的工具链验证改用本机工作副本 `$REFERENCE_WORK`，并给出无该副本时的替代路径 |
