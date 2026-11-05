// 07-07 GPT 因果语言建模 —— 场景 5-7
// 时间一律从 MS('卡点名') 取；内容区不越过 y0 + 857。

// ---------------- s05 三角形从何而来 ----------------
scene(4, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m前缀 = MS('s05_前缀平均', sc.st + 0.5), m均值 = MS('s05_均值', sc.st + 3.4),
        m下三角 = MS('s05_下三角', sc.st + 6.0), m因果性 = MS('s05_因果性', sc.st + 9.6);

  // 三个阶段：均匀平均 → 学习权重 → 依赖内容
  const N = 4, CELL = 40, SZ = N * CELL;
  const stages = [
    { x: 200, y: y0 + 320, tag: '前缀平均', sub: '每一行都填 1', tk: m前缀 },
    { x: 790, y: y0 + 320, tag: '学习权重', sub: 'softmax 之后', tk: m下三角 },
    { x: 1380, y: y0 + 320, tag: '依赖内容', sub: 'Q·K 决定', tk: m因果性 }
  ];

  stages.forEach((st, k) => {
    if (t < st.tk - 0.6) return;
    const S = sc['st' + k] || (sc['st' + k] = new Sk(7301 + k * 7).penOn());
    if (!sc['st' + k + 'b']) {
      matGrid(S, st.x, st.y, N, CELL, { w: 2.2 });
      for (let i = 0; i < N; i++) for (let j = 0; j <= i; j++) cellFill(S, st.x + j * CELL, st.y + i * CELL, CELL, k === 2 ? COL_A : C.gray3, k === 2 ? 0.6 : 0.9);
      sc['st' + k + 'b'] = 1;
    }
    S.at(t, st.tk - 0.55, 0.7);
    writeText(st.tag, st.x + SZ / 2, st.y - 46, hand(38, 700), k === 2 ? COL_A : C.ink, t, seq(st.tk - 0.4, st.tag, 0.06), 0.1, 'center');
    if (t >= st.tk + 0.7) writeText(st.sub, st.x + SZ / 2, st.y + SZ + 42, hand(30, 700), C.gray, t, seq(st.tk + 0.75, st.sub, 0.04), 0.1, 'center');
    // 阶段之间的箭头
    if (k < 2) {
      const AX = st.x + SZ + 40, AY = st.y + SZ / 2;
      const AR = sc['ar' + k] || (sc['ar' + k] = new Sk(7311 + k).penOn());
      if (!sc['ar' + k + 'b']) { arrowTo(AR, AX, AY, AX + 250, AY, { w: 4 }); sc['ar' + k + 'b'] = 1; }
      AR.at(t, st.tk + 0.5, 0.4);
    }
  });

  // 均值说明
  if (t >= m均值 - 0.4) {
    const A = '位置 i 取 0 到 i 的均值';
    writeText(A, 960, y0 + 214, hand(42, 700), C.ink, t, seq(m均值 - 0.25, A, 0.05), 0.1, 'center');
  }

  // 底部不变量
  if (t >= m因果性 + 1.2) {
    const S = sc.line || (sc.line = new Sk(7321).penOn());
    if (!sc.line_b) { S.line(170, y0 + 620, 1750, y0 + 620, { w: 3, col: COL_A }); sc.line_b = 1; }
    S.at(t, m因果性 + 1.15, 0.5);
    const T = '不变量：一直是用下三角行随机矩阵乘序列';
    writeText(T, 960, y0 + 688, hand(40, 700), COL_A, t, seq(m因果性 + 1.6, T, 0.04), 0.1, 'center');
  }
});

// ---------------- s06 实跑：注意力矩阵是下三角 ----------------
scene(5, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m跑 = MS('s06_跑代码', sc.st + 0.5), m矩阵 = MS('s06_矩阵', sc.st + 2.8),
        m第一 = MS('s06_第一行', sc.st + 5.0), m第二 = MS('s06_第二行', sc.st + 7.6);

  const rows = [
    [1.000, 0, 0, 0, 0, 0],
    [0.646, 0.354, 0, 0, 0, 0],
    [0.547, 0.317, 0.136, 0, 0, 0],
    [0.269, 0.232, 0.439, 0.060, 0, 0],
    [0.295, 0.097, 0.180, 0.158, 0.270, 0],
    [0.327, 0.041, 0.013, 0.101, 0.074, 0.444]
  ];
  const N = 6, CELL = 74, SZ = N * CELL, MX = 190, MY = y0 + 268;

  // 矩阵网格（实跑数据）
  if (t >= m矩阵 - 0.5) {
    const S = sc.mat || (sc.mat = new Sk(7401).penOn());
    if (!sc.mat_b) {
      matGrid(S, MX, MY, N, CELL, { w: 2.4 });
      for (let i = 0; i < N; i++) for (let j = 0; j <= i; j++) cellFill(S, MX + j * CELL, MY + i * CELL, CELL, COL_A, 0.16 + 0.6 * rows[i][j]);
      sc.mat_b = 1;
    }
    S.at(t, m矩阵 - 0.45, 0.9);
    // 数值
    rows.forEach((row, i) => {
      row.forEach((v, j) => {
        if (!v) return;
        const tk = m矩阵 + 0.4 + (i * N + j) * 0.02;
        if (t < tk) return;
        writeText(v.toFixed(3), MX + j * CELL + CELL / 2, MY + i * CELL + CELL / 2, hand(21, 700), v > 0.4 ? '#ffffff' : C.ink, t, seq(tk, v.toFixed(3), 0.015), 0.05, 'center');
      });
    });
  }

  // 逐行高亮
  const hiRows = [
    { tk: m第一, i: 0, note: '第 1 行：只有 1 个有效列' },
    { tk: m第二, i: 1, note: '第 2 行：前 2 列有权重' }
  ];
  hiRows.forEach((h, k) => {
    if (t < h.tk - 0.3) return;
    const S = sc['hi' + k] || (sc['hi' + k] = new Sk(7411 + k).penOn().rrect(MX - 10, MY + h.i * CELL - 6, SZ + 20, CELL + 12, 8, { w: 4.4, col: COL_A }));
    S.at(t, h.tk - 0.25, 0.35);
    writeText(h.note, 1060, MY + h.i * CELL + CELL / 2, hand(34, 700), COL_A, t, seq(h.tk + 0.2, h.note, 0.045), 0.1);
  });

  // 结论
  if (t >= m第二 + 3.0) {
    const T = '每一行都是一个只覆盖更早位置的概率分布';
    writeText(T, 960, y0 + 790, hand(42, 700), C.ink, t, seq(m第二 + 3.05, T, 0.04), 0.1, 'center');
  }
  // 实跑标注
  if (t >= m跑 - 0.3) {
    const T = 'code/main.py 实跑输出';
    writeText(T, 1400, y0 + 200, hand(28, 700), C.gray, t, seq(m跑 - 0.2, T, 0.03), 0.1);
  }
});

// ---------------- s07 解码：从分布里挑一个词 ----------------
scene(6, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m采样 = MS('s07_采样', sc.st + 0.5), m贪心 = MS('s07_贪心', sc.st + 3.8),
        mJumped = MS('s07_jumped', sc.st + 7.2), m截断 = MS('s07_截断', sc.st + 10.6);

  const dist = [
    ['the', 0.380], ['dog', 0.255], ['mat', 0.127], ['jumped', 0.069], ['cat', 0.047],
    ['ran', 0.038], ['floor', 0.031], ['sat', 0.023], ['.', 0.017], ['on', 0.013]
  ];
  const BX = 190, BY = y0 + 300, BH = 40, GAP = 12, MAXW = 560;

  // 概率条
  if (t >= m采样 - 0.4) {
    dist.forEach(([w, p], k) => {
      const tk = m采样 + 0.2 + k * 0.16;
      if (t < tk - 0.25) return;
      const y = BY + k * (BH + GAP);
      writeText(w, BX, y + BH / 2, hand(30, 700), C.ink, t, seq(tk - 0.1, w, 0.03), 0.06, 'left', false);
      const S = sc['b' + k] || (sc['b' + k] = new Sk(7501 + k).penOn());
      if (!sc['b' + k + 'b']) {
        const ww = MAXW * p / 0.38;
        S.fill([[BX + 150, y + 4], [BX + 150 + ww, y + 4], [BX + 150 + ww, y + BH - 4], [BX + 150, y + BH - 4]], k < 3 ? COL_A : C.gray3, { a: k < 3 ? 0.75 : 0.9, fade: 20 });
        sc['b' + k + 'b'] = 1;
      }
      S.at(t, tk, 0.3);
      if (t >= tk + 0.2) writeText(p.toFixed(3), BX + 150 + 8, y + BH / 2, hand(22, 700), C.gray, t, seq(tk + 0.2, p.toFixed(3), 0.02), 0.05, 'left', false);
    });
  }

  // 右侧：策略 → 选中的词
  const picks = [
    { tk: m贪心, name: '贪心', pick: 'the', note: '每步取 argmax' },
    { tk: m贪心 + 2.2, name: '温度 0.7', pick: 'jumped', note: 'logits 除以 T 再采样' },
    { tk: mJumped + 0.9, name: '温度 2.0', pick: 'mat', note: '分布更平，更多样' },
    { tk: m截断, name: 'Top-k = 3', pick: 'the', note: '只留前 3 个' },
    { tk: m截断 + 1.6, name: 'Top-p = 0.9', pick: 'the', note: '累积概率到 0.9' },
    { tk: m截断 + 2.4, name: 'Min-p = 0.1', pick: 'dog', note: '低于 0.1×max 的全砍' }
  ];
  picks.forEach((p, k) => {
    if (t < p.tk - 0.35) return;
    const y = y0 + 238 + k * 90;
    writeText(p.name, 1090, y, hand(36, 700), C.ink, t, seq(p.tk - 0.25, p.name, 0.05), 0.1, 'left', false);
    if (t >= p.tk + 0.45) {
      writeText('→  ' + p.pick, 1400, y, hand(36, 700), COL_A, t, seq(p.tk + 0.5, '→  ' + p.pick, 0.05), 0.1, 'left', false);
      writeText(p.note, 1400, y + 38, hand(24, 700), C.gray, t, seq(p.tk + 0.9, p.note, 0.025), 0.06, 'left', false);
    }
  });
});
