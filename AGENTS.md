# AGENTS.md

本文档是贡献者和 AI agent 修改本仓库时的操作手册。开 PR 前必须阅读。

这是一套课程，不是 SaaS 应用。课程内容就是产品。中文翻译以 [TRANSLATION.md](TRANSLATION.md) 为唯一权威契约。

## 定位

核心课程包含 20 个阶段、528 节课。每个算法都先从原始数学构建，再使用生产框架完成同一操作。
你会亲手写出反向传播、分词器、注意力机制和 agent 循环，所以当 PyTorch 或其他库登场时，它们不再是黑盒。

`projects/` 是独立实战层（76 项就绪项目、308 阶段），`manuals/` 是独立技术手册层（2 本）。它们不计入核心 528 课。

`certifications/claude/` 是独立的 Claude 认证备考层，包含 4 条路线、33 节认证课、诊断和原创模拟题。
认证课程单独统计，使用独立的站点构建与学习路径。

## 仓库结构

```text
phases/
  NN-phase-slug/
    NN-lesson-slug/
      docs/zh.md              # 中文课程正文
      code/                   # 实现与测试
      quiz.json               # 6 道题
      outputs/                # 可复用产物
certifications/claude/
  program.json                # 项目声明、核验日期、官方链接
  tracks/*.json               # 考试蓝图、路线和学习计划
  lessons/NN-slug/            # 认证课程
  assessments/<exam-code>/    # 诊断和完整模拟题
projects/                      # 独立实战层（76 项就绪项目、308 阶段）
manuals/                       # 独立技术手册层（2 本）
video-productions/             # 视频剧集源码与制作任务（成片不入库）
skills/                        # 课程配套技能
glossary/terms.md              # 术语表唯一数据源
site/                          # 静态页面与构建器
api/                           # Vercel 只读 REST / MCP 接口
scripts/                       # 审计和构建工具
.github/workflows/build.yml    # 中文站 CI
```

## 强制规则

1. 新增课程时，每个 lesson 目录用一个原子提交。上游同步或批量翻译可按可审查的逻辑批次提交。
2. 提交标题使用约定式前缀且不超过 72 字符；本中文镜像优先使用 `sync(zh):`、`i18n(quiz):`、`feat(site):`、`fix(site):`。
3. 图表只使用 Mermaid、SVG 或站点注册的 `figure` 机制，不用 ASCII/绘图字符假装图表。
4. 所有代码围栏必须带语言标记。
5. 不使用外部 LLM API 做翻译；不提交考题泄露内容、机密题目或包过承诺。
6. 代码保持 stdlib-first，不为满足形式而伪造 provider API 集成。
7. 不直接 push `main`；所有更改走 PR。`gh pr create` 必须显式带 `--repo eanfs/ai-engineering-from-scratch-zh`：本机 `gh` 的默认仓库会解析到 `upstream`（fancyboi999），不指定就会把 PR 建到错误的仓库下。
8. 不提交构建产物 `site/sitemap.xml`、`site/llms.txt`、`site/build-meta.js`、`site/certification-data.js`、`site/lessons/`。
9. 项目、手册、Hub、OG 数据与目录从中文源构建；不提交 `site/projects-data.js`、`site/project-content/`、`site/manuals-data.js`、`site/manuals.html`、`site/manual-*.html`、`site/hubs/`、`site/lesson-terms.json` 或 `site/og-cards.json`。
10. `site/data.js` 是中文仓跟踪的构建产物；课程、术语或站点数据变动后必须重建并与源文件一起提交。
11. 视频成片与中间产物不入库：`video-productions/output/*.mp4`、`handdraw-jobs/*/work/`、`handdraw-jobs/*/outputs/film.mp4`、母带音频与 `handdraw-jobs/*/inputs/narration/master.wav` 均由 `.gitignore` 排除；只提交剧集源码（`lesson.json`、`story_*.json`、`scenes_*.js`）与任务配置（`job.json`、`design.json`、briefs、prompts、输入源图）。

## 依赖约束

| 语言 | 允许的依赖 |
|---|---|
| Python | `numpy`、`torch`、`h5py`、`zstandard`、`safetensors`、标准库 |
| TypeScript | `hono`、`zod`、`ws`（只在需要 WebSocket 时）、`@hono/node-server`、Node 20+ 标准库 |
| Rust | 标准库，单文件 `rustc --edition 2021` |
| Julia | `Random`、`Statistics`、`LinearAlgebra`、`Printf` |

## 课程契约

### `docs/zh.md`

```markdown
# <标题>

> <一句话摘要>

**类型：** <Learn | Build | Reference>
**语言：** <与 code/main.* 匹配的语言>
**前置要求：** <课程链接或“无”>
**预计时间：** <分钟>

## 学习目标
- <4–6 条以动词开头的目标>
```

`**语言：**` 必须与 `code/` 中的实际实现文件一致。中文正文保存在 `docs/zh.md`；翻译和章节标题遵循 `TRANSLATION.md`。

### `quiz.json`

```json
{
  "lesson": "<dir-slug>",
  "title": "<标题>",
  "questions": [
    {"stage": "pre", "question": "...", "options": ["a", "b", "c", "d"], "correct": 0, "explanation": "..."}
  ]
}
```

每课恰好 6 题：1 道 `pre`、3 道 `check`、2 道 `post`。`correct` 是从 0 开始的索引，翻译时绝不改动。

## Claude 认证契约

- 每节认证课必须有可运行 `main.*` 和至少 5 个确定性测试。
- 概念课用场景运行器、政策评分器、产物校验器、批准模拟器、威胁模型检查器或证据评分器承载实践。
- 完整课程必须包含 `交互实验`、`实践实验`、`交付产物`、`验证`、`综合项目关联`，并嵌入已注册 figure。
- `program.json` 管理独立性声明、核验日期和官方链接。
- `prerequisites.json` 管理课程依赖图；`tracks/*.json` 管理考试蓝图、权重、路线、评估和学习计划。
- 诊断和模拟题的 `correct` 始终是数组；`single` 只有一个索引，`multiple` 至少两个。
- 题目必须映射到公开 objective，包含实质性解析，且不得复制或推测真实考题。
- 公开页面和课程必须明确声明：这是独立社区课程，不隶属于 Anthropic，不颁发证书，不保证通过。

## AI-native 认证学习模式

当用户要求选择、开始、继续、学习、练习或评估 Claude 认证时，先阅读 `skills/claude-certification/SKILL.md`。

学习模式必须：

- 每次读取当前 track manifest，不凭记忆虚构路线、权重或政策。
- 每次教一课，运行真实实验和测试，要求学习者在 `learning-artifacts/` 产出自己的交付物。
- 进度写入 `CLAUDE-CERTIFICATION.md`，不覆盖仓库内置的 `outputs/` 参考产物。
- 练习百分比不是 Anthropic 官方量表分数。

## 本地验证

提交前按实际改动执行：

```bash
node site/build.js
node site/build.js --check
python3 scripts/audit_certifications.py
python3 scripts/backfill_certification_references.py --check
find certifications/claude/lessons -path '*/code/tests/test_*.py' -print0 | xargs -0 -n1 python3
find certifications/claude/lessons -path '*/code/main.py' -print0 | xargs -0 -n1 python3
node scripts/check_figure_loader.js
node scripts/test_tts.js
```

视频剧集改动还需在对应任务目录运行（技能位于 `~/.hub/skills/handdrawn-explainer-video`）：

```bash
python3 ~/.hub/skills/handdrawn-explainer-video/scripts/handdraw_video.py doctor .
```

项目与手册整合还需运行：

```bash
python3 scripts/project_test.py --all --solution --strict --report /tmp/project-grade.json
node --test site/test*.js lib/test*.js scripts/test_site_integration.js
node scripts/audit_manuals.js --skip-capture
node scripts/check_manual_outputs.js
node scripts/check_hubs.js
node scripts/test_og.js
node scripts/check_og_cards.js --require-manifests
```

图表冻结对等回归需要 `AIFS_FIGURE_FROZEN_ROOT`（组 1/2）与 `AIFS_FIGURES_FROZEN_ROOT`（组 3）指向冻结的 `56c886c8821fc488b6f9608895c983d18f0d1ea3` 源根；CI 显式取得该 oracle，缺源不能跳过。OG 字集在全部元数据生成后由开发机用固定 OFL 字体运行 `scripts/build-og-fonts.js` 重建，CI 和部署只检查，不启动 Chromium。卡片 URL 的内容 hash 同时包括字体与 renderer。

`.github/workflows/build.yml` 定义 CI 检查命令。`audit_certifications.py` 校验认证题的答案位置与分布。课程时长以各课 `docs/zh.md` 为源，ROADMAP 行与阶段汇总随正文更新；专项路径的必修范围和时长以 `learning-paths/*.json` 为源。

交付与验证：

1. 按改动范围运行对应检查；站点改动先构建，再在真实浏览器里验证受影响页面、交互和移动端。预渲染页面用 `python3 -m http.server 8000 --directory site`，打开 `/lessons/<phase>/<lesson>/`。本地课程与认证源文件的联调从仓库根运行 `python3 -m http.server 8001`，打开 `/site/lesson.html?path=phases/...` 或 `/site/certifications.html`。
2. 明确列出执行结果、warning 和验证边界。
3. 通过 PR 合并，再验证 `https://aieng-zh.cn` 的受影响页面。

## 视频制作（默认方案）

课程视频默认用下面这套方案，已跑通 07-07、07-08 两集，不要临时改用 dashi 手绘笔记或 MiniMax 生视频。

| 项 | 默认值 |
|---|---|
| 流水线 | `~/.hub/skills/handdrawn-explainer-video`（逐笔手绘 + 真人手） |
| 画风 | 12 工业设计马克笔手绘 |
| 手部 | teacher-pen（白衬衫中性笔） |
| 画幅 | 16:9 · 1920×1080 · 30 fps |
| 时长 | 约 175 秒（12 页 × 3 句） |
| 插画 | **PIL 本地绘制**（`design/illustration-gen.py`），扁平信息图；不用图像生成 API |
| 配音 | edge-tts **女声** `zh-CN-XiaoxiaoNeural`，整篇一次合成，不逐句拼接 |
| 字幕 | 由 alignment 在本地烧录，单层，字号 42，底部 54px |
| 音乐 | 添加，**动感电子**（节奏型铺底，不与旁白抢中频） |

结构固定为：**钩子前置**（第 1 页直接抛问题，画面领先旁白约 0.2 秒开始写）→ 标题页放到第 2 页 → 正文 → 末页提问并引导评论区留言。小红书数据表明前 5 秒报集号会显著拉低完播率。

**插画用 PIL 本地绘制，不用 AI 生图的 3D 渲染素材。** 实测 07-09/10 的 Grok 3D 插画曝光→观看转化率只有 7.4%，而 PIL 扁平信息图（07-05/07-06）是 29.8%；且信息图上要放中文数据卡片和结论文字，AI 生图做不到。绘制脚本随任务入库，可完全复现。

每页信息密度要够：标题 + 图示 + 数据卡片 + 结论句，12 页约 36 句。

### 关键约束（踩过的坑）

- PIL 绘制的排版是手工坐标：柱子高度、底部结论句、长文本最容易压住别的元素或超出 900 画布。改完必须逐页看图。
- 字体只有 Noto Sans CJK，**没有 ✓ ✗ 等符号字形**（会渲染成方框）；对勾和叉要用 `Sheet.check()` / `Sheet.cross()` 画。
- 插画改动后 `drawing-review.json` 的 `source_sha256` 会失效，verify 报 "Semantic drawing review ... belongs to another image"；重跑 `build_ep.py` 重新生成 art-direction 与 drawing-review 再 build。
- 若确需 AI 生图：凭证在 `~/.grok/auth.json`，沙箱下需 `GROK_HOME` 指向工作区内副本；模型名用 `grok-imagine-image`。但只用它补背景元素，主体信息图仍用 PIL。
- 音乐 `audio.music.gain` 上限 0.3；超过会被 build 拒绝。响度不够时提高音乐源本身或调 `end_hold_seconds`，不要突破 gain 上限。
- 配乐默认用动感电子（节奏型），素材见 `~/Movies/Hub/Projects/handdrawn-explainer-/位置编码轻电子配乐.mp3`；换曲后要重新 build，因为音乐文件参与指纹。
- `ending.fade_seconds` 必须小于 `audio.end_hold_seconds`；尾部静音合计不得超过 1.2 秒。
- 成片响度必须落在 -20 ~ -14 LUFS，true peak < -1 dBTP；渲染管线会把旁白归一化到 -20，所以要靠音乐层补足。
- 每个 drawing part 必须有可描轮廓；纯阴影区域（如“地面”）会报 `Part has no drawable outline`，改用单一主体 part。
- `alignment.json` 的 `script_sha256` 用原文直接拼接（含标点），beat id 必须与 `job.json` 一致。
- 任务目录放 `video-productions/handdraw-jobs/<集>-v2/`；`outputs/film.mp4`、`work/`、`inputs/narration/master.wav` 按 `.gitignore` 不入库。
- 交付前必须写 `review.json`（content/visual/motion/audio/privacy 五项 + limitations）再 `finalize`；verify 会覆盖未填写的 review。

### 交付物

每集产出 `outputs/film.mp4`、`outputs/cover.png`、`outputs/script.txt`、`outputs/editing/captions.srt`、`outputs/verification.json`。成片复制到 `video-productions/output/` 供发布，源文件留在任务目录。

### 发布到小红书

| 项 | 做法 |
|---|---|
| 标题 | **「手绘讲透 XXX：一句具体的问题」**。问句 + 明确价值承诺，历史爆款都是这个格式 |
| 标题长度 | **硬上限 20 字**，超出会阻止发布且只在标题旁显示红字「22 / 20」，没有别的提示。中文按 1 算、英文按约 0.7 算——「手绘讲透 Transformer：」已占 18，后面只剩 2–3 字。含长英文名的选题改成短结论句式 |
| 标签 | 4 个大词（#AI #大模型 #Transformer #深度学习）+ 2 个具体模型词（#ViT #MoE #Whisper） |
| 时段 | **19:00–21:00**（历史爆款都在这个窗口） |
| 节奏 | 曝光由**互动率**决定，不是发布时间。11-07 同时段连发三条实测：互动 40 → 曝光 3138、互动 29 → 2120、互动 7 → 1282，最晚发的曝光反而最高 |
| 封面 | 用视频第 1 帧（PIL 绘制的信息图），平台会自动截取；网页版的封面编辑器点不开，不要浪费时间 |

标题是唯一的硬约束，其他都能事后补救（正文可编辑、封面可换）。发布后看到「22 / 20」就是没发出去，缩短标题再点一次。

发布 48 小时后看三个指标：**曝光、封面点击率、人均观看时长**。点击率低说明封面/标题不行，人均时长短说明前几秒没留住，曝光低说明互动不够——三者要分开判断，不要混成一个「数据不好」的结论。

**早期时长数据（发布 10 小时内）完全不可信**：同一条笔记 11-06 读到 5 秒，11-07 读到 25 秒。必须等 24 小时以上再判断留人能力。

#### 用 orca computer 发布的操作要点

四个环节都有坑：

**1. 上传文件**

点「上传视频」→ 系统文件对话框（`NSOpenPanel`，orca 的 AX 读不到它，只能靠键盘）：

```bash
# 「前往文件夹」会预填上次用过的路径，必须先 Cmd+A 覆盖
osascript -e 'tell application "System Events" to keystroke "g" using {command down, shift down}'
sleep 3
osascript -e 'tell application "System Events" to keystroke "a" using command down'
printf "%s" "/tmp/v0714.mp4" | pbcopy
osascript -e 'tell application "System Events" to keystroke "v" using command down'
sleep 2
osascript -e 'tell application "System Events" to key code 36'   # 确认路径
sleep 3
osascript -e 'tell application "System Events" to key code 36'   # 打开文件
```

**不要在文件列表里点鼠标**——合成鼠标事件对 `NSOpenPanel` 无效，试过多次完全没有反应。

**2. 填正文**

标题可以直接 `set-value`；正文必须「先清空再剪贴板粘贴」，三条弯路：

- `orca computer paste-text` 会执行**两次**，正文重复一遍
- `set-value` 传真实换行会被**吞成空格**，全文挤成一段
- `Cmd+Z` 撤销一次会**清空整个正文**，不是回退一层

```bash
orca computer click --app com.google.Chrome --element-index <正文索引>
orca computer set-value --app com.google.Chrome --element-index <正文索引> --value ""
sleep 2
cat body.txt | pbcopy
osascript -e 'tell application "System Events" to keystroke "v" using command down'
```

**3. 点发布**

先 dump 整棵树再拿索引，`--query "按钮 发布"` 有时匹配不到：

```bash
orca computer get-app-state --app com.google.Chrome --json > /tmp/state.json
grep -oE "[0-9]+ 按钮 发布" /tmp/state.json | head -1
```

成功标志：URL 变成 `?source=&published=true`。如果还是 `?target=video` 且标题旁有红字，就是标题超限。

**4. 编辑已发布笔记**

笔记管理页点卡片标题直接进编辑页（`publish/update?id=...&noteType=video`），改完点底部「发布」保存，URL 跳到 `note-manager?source=` 即成功。验证：重新打开编辑 URL 读正文内容。

**标签页管理**：Chrome 常开着一堆别的标签，orca 只作用于当前活动标签。切换要按 URL 匹配，不要用索引（新开标签会让索引漂移）：

```applescript
tell application "Google Chrome"
	set tabList to tabs of front window
	repeat with i from 1 to count of tabList
		if URL of item i of tabList contains "creator.xiaohongshu.com/publish" then
			set active tab index of front window to i
			exit repeat
		end if
	end repeat
end tell
```

---

## 同步与冲突

- 只跟踪 `upstream/main`，以 `.sync-upstream-base` 作为已检视基准。同步前读取 `.sync-upstream-pending.json`（若存在），先处理其中未完成的批次；上游新增提交数为 0 不表示这些批次已完成。每项通过对应本地和线上验证后移出 pending 清单。
- 不用上游英文 `build.js`、`lesson.html`、域名、GitHub 链接或营销数据覆盖中文保护层。
- 必须保留 `aieng-zh.cn`、中文仓链接、`docs/zh.md`、`md-render.js` 单一渲染器、静态 `/lessons/` 预渲染和中文 quiz 锚点。
- 冲突时以当前中文实现为基底，语义移植上游变更，不整文件覆盖。

---

最后审校：2026-11-12。
