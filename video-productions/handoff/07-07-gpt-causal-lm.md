# 07-07 GPT 因果语言建模 — MiniMax Design handoff

- Source job: `video-productions/handdraw-jobs/07-07-gpt-causal-lm`
- Project: `07-07 GPT 因果语言建模` (projectId `p_7668f8b12a93c0f6dba9cde7`)
- Canvas: 1920x1080, 16:9, 30 fps; images 2K, clips MiniMax H3 2K, audio off, one per `clip_plan` entry (15 s max each).
- Style references: `style/anchors/1.jpg`, `style/anchors/5.jpg`, `inputs/cover.png`.

## Pages

### p01 · 预测下一个词 (15.11 s, clip 15 s)

Narration:
- 阶段 7，第 7 课：GPT 与因果语言建模。
- 预测下一个词，是今天所有大模型共用的训练信号。
- 要并行训练整段序列，每个位置就只能看前面。

Image prompt:

```text
industrial marker sketch, warm off-white paper, dark grey marker outline, warm yellow fill, brown streaks, metal grey accents. 左侧卡片标 GPT，三个词块「今天 天气 很」后接暖黄块「好」；右侧卡片写「整段一次前向 → N 个位置的损失」；底部方框写「每个位置只能看前面」。 Visible: 左侧暖黄块标出要预测的下一个词；右侧强调一次前向并行算出 N 个损失。. No people, no photorealism, no dark background, no watermark.
```

Video prompt:

```text
Animate the supplied hand-drawn marker diagram for page p01 (预测下一个词). Slow push-in with slight parallax; ink lines settle and warm-yellow fills stay put. No new objects, no text changes, no label morphing, no camera cuts. Keep the warm off-white paper background.
```

### p02 · 三角掩码 (16.25 s, clips [9, 8])

Narration:
- 给注意力分数加上三角掩码，未来位置全部填负无穷。
- softmax 之后，未来的权重恰好变成零。
- 所以第一行只能看自己，最后一行能看到全部六个位置。

Image prompt:

```text
industrial marker sketch, warm off-white paper, dark grey marker outline, warm yellow fill, brown streaks, metal grey accents. 六乘六网格，上三角填金属灰写 -∞，对角线暖黄；右侧写 mask[i,j]=-∞、exp(-∞)=0、未来权重=0。 Visible: 上三角全为 -∞，下三角与对角线才有概率；第一行只看自己，最后一行看满六格。. No people, no photorealism, no dark background, no watermark.
```

Video prompt:

```text
Animate the supplied hand-drawn marker diagram for page p02 (三角掩码). Slow push-in with slight parallax; ink lines settle and warm-yellow fills stay put. No new objects, no text changes, no label morphing, no camera cuts. Keep the warm off-white paper background.
```

### p03 · 实跑：6 × 6 (20.15 s, clips [11, 10])

Narration:
- 实跑一个六乘六的注意力矩阵，最后一行是 0.327、0.041，一直到 0.444。
- 每一行只在当前位置和更早的列上有概率，加起来正好是一。
- 整个机制就是一行代码：下三角，加负无穷。

Image prompt:

```text
industrial marker sketch, warm off-white paper, dark grey marker outline, warm yellow fill, brown streaks, metal grey accents. 六行六列数字矩阵，上三角灰色 0.000，最后一行用暖棕框圈出 0.327、0.041、0.013、0.101、0.074、0.444。 Visible: 最后一行六个数字完整可见；上三角全部为 0.000；每行和等于 1.000。. No people, no photorealism, no dark background, no watermark.
```

Video prompt:

```text
Animate the supplied hand-drawn marker diagram for page p03 (实跑：6 × 6). Slow push-in with slight parallax; ink lines settle and warm-yellow fills stay put. No new objects, no text changes, no label morphing, no camera cuts. Keep the warm off-white paper background.
```

### p04 · 三角从哪来 (15.04 s, clips [15])

Narration:
- 这个三角不是事后补丁，它来自前缀平均。
- 先做均匀平均，再换成学到的权重，最后换成查询和键的点积。
- 三步都只是用下三角矩阵乘序列。

Image prompt:

```text
industrial marker sketch, warm off-white paper, dark grey marker outline, warm yellow fill, brown streaks, metal grey accents. 三个并排面板：均匀平均、学到权重、Q·K 转置，各画一个 4×4 下三角小矩阵；下方写「三步都只是用下三角矩阵乘序列」。 Visible: 三个面板都保留下三角形状；文字点明换掉的只是权重来源。. No people, no photorealism, no dark background, no watermark.
```

Video prompt:

```text
Animate the supplied hand-drawn marker diagram for page p04 (三角从哪来). Slow push-in with slight parallax; ink lines settle and warm-yellow fills stay put. No new objects, no text changes, no label morphing, no camera cuts. Keep the warm off-white paper background.
```

### p05 · 并行训练，串行推理 (15.01 s, clips [15])

Narration:
- 训练时整段序列一次前向，一次算出 N 个损失。
- 推理时只能一个 token 一个 token 地生成。
- KV 缓存省掉重复计算，但串行长度就是输出长度。

Image prompt:

```text
industrial marker sketch, warm off-white paper, dark grey marker outline, warm yellow fill, brown streaks, metal grey accents. 左侧卡片训练：整段序列条向下分出四个损失框；右侧卡片推理：t1→t2→t3 串成链，箭头折下接到暖黄 t4，并标注 KV 缓存。 Visible: 训练侧四个损失同时在；推理侧链条明显是串行，t4 在链条末端。. No people, no photorealism, no dark background, no watermark.
```

Video prompt:

```text
Animate the supplied hand-drawn marker diagram for page p05 (并行训练，串行推理). Slow push-in with slight parallax; ink lines settle and warm-yellow fills stay put. No new objects, no text changes, no label morphing, no camera cuts. Keep the warm off-white paper background.
```

### p06 · 错位一格 (18.28 s, clip 15 s)

Narration:
- 损失错位一格：输入前三个词，目标就是后三个词。
- 实跑：偏置过的 logits 损失是 1.145，随机 logits 是 2.418。
- 随机基线正好是 ln 十，也就是 2.303。

Image prompt:

```text
industrial marker sketch, warm off-white paper, dark grey marker outline, warm yellow fill, brown streaks, metal grey accents. 上一行输入 t1 t2 t3，下一行暖黄目标 t2 t3 t4，斜箭头逐位连接；右侧三张数字卡：1.145 偏置 logits、2.418 随机 logits、2.303 ln 10 基线。 Visible: 错位关系清楚；三个数字完整可读，2.303 标为基线。. No people, no photorealism, no dark background, no watermark.
```

Video prompt:

```text
Animate the supplied hand-drawn marker diagram for page p06 (错位一格). Slow push-in with slight parallax; ink lines settle and warm-yellow fills stay put. No new objects, no text changes, no label morphing, no camera cuts. Keep the warm off-white paper background.
```

### p07 · 六种取法 (14.41 s, clip 14 s)

Narration:
- 同一组 logits，换一种采样就换出一个词。
- 贪心取 the，温度 0.7 取 jumped，温度 2.0 取 mat。
- top-k 和 top-p 都回到 the，min-p 取 dog。

Image prompt:

```text
industrial marker sketch, warm off-white paper, dark grey marker outline, warm yellow fill, brown streaks, metal grey accents. 左侧六根概率柱：the 0.380、dog 0.255、mat 0.127、jump 0.069、cat 0.047、ran 0.038；右侧六行结果：贪心 the、温度 0.7 jumped、温度 2.0 mat、top-k=3 the、top-p=0.9 the、min-p=0.1 dog。 Visible: 六个结果与课程脚本输出一致；min-p 一行用暖黄强调。. No people, no photorealism, no dark background, no watermark.
```

Video prompt:

```text
Animate the supplied hand-drawn marker diagram for page p07 (六种取法). Slow push-in with slight parallax; ink lines settle and warm-yellow fills stay put. No new objects, no text changes, no label morphing, no camera cuts. Keep the warm off-white paper background.
```

### p08 · GPT 配方 (17.91 s, clips [9, 9])

Narration:
- GPT 的配方很朴素：纯解码器，每层一次注意力加一次前馈。
- 从一亿两千万到一千七百五十亿，核心架构几乎没变。
- 真正拉开差距的，是数据、规模和 RLHF 后训练。

Image prompt:

```text
industrial marker sketch, warm off-white paper, dark grey marker outline, warm yellow fill, brown streaks, metal grey accents. 左侧参数量纵轴：124M、1.5B、175B、数万亿；右侧 2×2 四张卡片：纯解码器、扩展、上下文学习、RLHF；底部写 pre-norm + RoPE + SwiGLU。 Visible: 四个里程碑与四张配方卡一一可见；底部点出真正拉开差距的因素。. No people, no photorealism, no dark background, no watermark.
```

Video prompt:

```text
Animate the supplied hand-drawn marker diagram for page p08 (GPT 配方). Slow push-in with slight parallax; ink lines settle and warm-yellow fills stay put. No new objects, no text changes, no label morphing, no camera cuts. Keep the warm off-white paper background.
```

### p09 · GPT vs BERT (12.43 s, clip 12 s)

Narration:
- GPT 建模的是给定前缀下一个词的概率。
- BERT 建模的是给定其余位置被遮词的概率。
- 损失决定了一个模型能不能生成。

Image prompt:

```text
industrial marker sketch, warm off-white paper, dark grey marker outline, warm yellow fill, brown streaks, metal grey accents. 两张卡片：GPT 写 P(x_t | x_<t)，打勾「能自回归生成」；BERT 写 P(x_masked | 其余)，打叉「不能自回归输出」；底部写「同一个 Transformer，换一个损失，就换一种能力」。 Visible: 勾与叉对照清楚；两张卡片都写出概率形式。. No people, no photorealism, no dark background, no watermark.
```

Video prompt:

```text
Animate the supplied hand-drawn marker diagram for page p09 (GPT vs BERT). Slow push-in with slight parallax; ink lines settle and warm-yellow fills stay put. No new objects, no text changes, no label morphing, no camera cuts. Keep the warm off-white paper background.
```

## Acceptance

- All 9 pages keep the exact Chinese labels shown in the reference images; no garbled or invented characters.
- Warm off-white paper, dark marker outline, warm-yellow fill, brown streaks; no photoreal elements, no people, no watermark.
- Each clip contains no camera cuts and no text animation; labels stay static and legible.
- Final 1920x1080, 30 fps, H.264; narration matches the provided master.wav sample for sample.

## Local assembly

All of this is scripted; see RUNBOOK.md for the full work order.

1. `python3 video-productions/handoff/handoff_maxdesign.py fetch <episode>` downloads every clip into outputs/maxdesign/ as pXXa.mp4, pXXb.mp4.
2. `~/.cache/sweety-handdraw-video/venv/bin/python video-productions/handoff/handoff_assemble.py <episode>` cross-fades multi-clip pages, retimes each page onto its window, insets the picture on the same paper margins as the local renderer, burns the captions from alignment.json, muxes master.wav, and writes verification.json/.txt.
3. Rehearse the whole chain at zero cost with `--preview`, which animates the local page images instead of the app clips.
