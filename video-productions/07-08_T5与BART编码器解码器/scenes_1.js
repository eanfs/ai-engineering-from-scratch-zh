// 07-08 T5 与 BART · 编码器-解码器 —— 场景 1-4
// 时间一律从 MS('卡点名') 取；内容区不越过 y0 + 857（字幕带在 y = 908）。

function matGrid(S, x, y, n, cell, o = {}) {
  for (let i = 0; i <= n; i++) {
    S.line(x + i * cell, y, x + i * cell, y + n * cell, { w: o.w ?? 2.2, col: o.col });
    S.line(x, y + i * cell, x + n * cell, y + i * cell, { w: o.w ?? 2.2, col: o.col });
  }
  return S;
}
function cellFill(S, x, y, cell, col, a = 0.85) {
  const p = 3;
  S.fill([[x + p, y + p], [x + cell - p, y + p], [x + cell - p, y + cell - p], [x + p, y + cell - p]], col, { a, fade: 20 });
  return S;
}
// 一个带标签的小方块
function block(sc, key, x, y, w, h, tk, t, label, o = {}) {
  if (t < tk - 0.35) return;
  const S = sc[key] || (sc[key] = new Sk(o.seed ?? 3001).penOn().rrect(x, y, w, h, 14, { w: o.w ?? 3.6, col: o.col ?? C.ink }));
  S.at(t, tk - 0.3, 0.42);
  writeText(label, x + w / 2, y + h / 2, hand(o.size ?? 34, 700), o.tcol ?? C.ink, t, seq(tk + 0.2, label, 0.05), 0.1, 'center', false);
}

// ---------------- s01 钩子：一套架构干三类活 ----------------
scene(0, (sc, t) => {
  const y0 = sc.y0;
  const m三件 = MS('h_三件事', sc.st + 0.35), m一套 = MS('h_一套架构', sc.st + 2.8),
        m两半 = MS('h_两半', sc.st + 6.4), m编解 = MS('h_编码器解码器', sc.st + 10.6);

  // 三个任务标签：画面领先旁白，0.2 秒就开始落
  const T0 = sc.st + 0.2;
  const tags = ['翻译', '长文摘要', '语音转文字'];
  const CW = 300, GAP = 34, X0 = 960 - (CW * 3 + GAP * 2) / 2;
  tags.forEach((w, k) => {
    const tk = T0 + k * 0.38;
    if (t < tk - 0.3) return;
    const x = X0 + k * (CW + GAP);
    block(sc, 'tg' + k, x, y0 + 214, CW, 96, tk, t, w, { size: 36, seed: 7301 + k });
  });

  if (t >= T0 + 1.5) {
    const Q = '为什么共用一套架构？';
    writeText(Q, 960, y0 + 392, hand(62, 700), C.ink, t, seq(T0 + 1.5, Q, 0.05), 0.1, 'center', false);
  }

  // 画面从中间劈成两半
  if (t >= m两半 - 0.6) {
    const S = sc.split || (sc.split = new Sk(7311).penOn());
    if (!sc.split_b) {
      S.line(960, y0 + 452, 960, y0 + 760, { w: 3.4, col: C.gray2 });
      S.line(700, y0 + 470, 700, y0 + 740, { w: 3.6, col: COL_A });
      S.line(1220, y0 + 470, 1220, y0 + 740, { w: 3.6, col: COL_B });
      sc.split_b = 1;
    }
    S.at(t, m两半 - 0.55, 0.7);
    writeText('读懂', 830, y0 + 540, hand(46, 700), COL_A, t, seq(m两半 - 0.2, '读懂', 0.08), 0.1, 'center', false);
    writeText('生成', 1090, y0 + 540, hand(46, 700), COL_B, t, seq(m两半 + 0.3, '生成', 0.08), 0.1, 'center', false);
    writeText('一半负责读懂', 830, y0 + 676, hand(30, 700), C.gray, t, seq(m两半 + 0.9, '一半负责读懂', 0.04), 0.1, 'center', false);
    writeText('一半负责生成', 1090, y0 + 676, hand(30, 700), C.gray, t, seq(m两半 + 1.4, '一半负责生成', 0.04), 0.1, 'center', false);
  }

  // 落点
  if (t >= m编解 - 0.6) {
    const S2 = sc.bar || (sc.bar = new Sk(7321).penOn());
    if (!sc.bar_b) { S2.fill(rrPts(560, y0 + 782, 800, 104, 18), COL_A, { fade: 1 }); sc.bar_b = 1; }
    S2.at(t, m编解 - 0.55, 0.35);
    writeText('编码器-解码器', 960, y0 + 836, hand(56, 700), '#ffffff', t, seq(m编解 - 0.2, '编码器-解码器', 0.06), 0.1, 'center', false);
  }
});

// ---------------- s02 片头 ----------------
scene(1, (sc, t) => {
  const y0 = sc.y0;
  const m阶段 = MS('t_阶段', sc.st + 0.4), m课号 = MS('t_课号', sc.st + 1.4),
        m标题 = MS('t_标题', sc.st + 2.6), mBART = MS('t_BART', sc.st + 5.2),
        m理解 = MS('t_理解', sc.st + 6.6), m标准 = MS('t_标准', sc.st + 10.6);

  const F = sc.frame || (sc.frame = new Sk(7401).penOn().rrect(150, y0 + 118, 1620, 520, 28, { w: 4.8 }));
  F.at(t, sc.st + 0.12, 0.8);

  if (t >= m阶段 - 0.35) tag('阶段 7 · 08', 218, y0 + 180, 42, P(t, m阶段 - 0.3, 0.32));
  if (t >= m标题 - 0.3) {
    writeText('T5 与', 222, y0 + 330, hand(90, 700), C.ink, t, seq(m标题 - 0.25, 'T5 与', 0.09), 0.1);
  }
  if (t >= mBART - 0.3) {
    const T2 = 'BART';
    writeText(T2, 222, y0 + 448, hand(90, 700), COL_A, t, seq(mBART - 0.25, T2, 0.1), 0.1);
    const w2 = tw(T2, hand(90, 700));
    underline(212, 222 + w2 + 10, y0 + 500, RQ(7411), P(t, mBART + 0.7, 0.35), 8, COL_A, mBART + 0.7);
    writeText('编码器-解码器', 222 + w2 + 40, y0 + 462, hand(44, 700), C.gray, t, seq(mBART + 1.0, '编码器-解码器', 0.05), 0.1);
  }
  if (t >= m理解 - 0.35) {
    writeText('编码器负责理解  |  解码器负责生成', 224, y0 + 578, hand(36, 700), C.ink, t, seq(m理解 - 0.25, '编码器负责理解  |  解码器负责生成', 0.03), 0.1);
  }
  if (t >= m标准 - 0.6) {
    // 右侧：两个堆叠示意
    const S = sc.stack || (sc.stack = new Sk(7421).penOn());
    if (!sc.stack_b) {
      for (let k = 0; k < 3; k++) S.rrect(1440, y0 + 260 + k * 74, 200, 60, 10, { w: 2.8, col: COL_A });
      for (let k = 0; k < 3; k++) S.rrect(1440, y0 + 520 + k * 74, 200, 60, 10, { w: 2.8, col: COL_B });
      S.line(1540, y0 + 448, 1540, y0 + 512, { w: 3, col: C.gray });
      sc.stack_b = 1;
    }
    S.at(t, m标准 - 0.55, 0.9);
    writeText('编码器', 1540, y0 + 236, hand(28, 700), COL_A, t, seq(m标准 - 0.2, '编码器', 0.06), 0.1, 'center', false);
    writeText('解码器', 1540, y0 + 706, hand(28, 700), COL_B, t, seq(m标准 + 0.3, '解码器', 0.06), 0.1, 'center', false);
  }
});

// ---------------- s03 为什么需要两半 ----------------
scene(2, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m纯解 = MS('w_纯解码', sc.st + 0.5), m精简 = MS('w_精简', sc.st + 3.2),
        m天然 = MS('w_天然', sc.st + 6.4), m契合 = MS('w_契合', sc.st + 14.0);

  // 左：GPT（纯解码器），右：BERT（纯编码器）
  block(sc, 'gpt', 200, y0 + 260, 330, 120, m纯解, t, 'GPT', { size: 44, col: COL_A, tcol: COL_A });
  block(sc, 'bert', 1390, y0 + 260, 330, 120, m纯解 + 0.9, t, 'BERT', { size: 44, col: COL_B, tcol: COL_B, seed: 7501 });
  if (t >= m精简 - 0.4) {
    writeText('纯解码器', 365, y0 + 414, hand(30, 700), C.gray, t, seq(m精简 - 0.3, '纯解码器', 0.04), 0.1, 'center', false);
    writeText('纯编码器', 1555, y0 + 414, hand(30, 700), C.gray, t, seq(m精简 + 0.3, '纯编码器', 0.04), 0.1, 'center', false);
  }

  // 中间：四类任务
  const tasks = ['翻译', '摘要', '语音识别', '结构化抽取'];
  tasks.forEach((w, k) => {
    const tk = m天然 + 0.2 + k * 0.55;
    block(sc, 'tk' + k, 640, y0 + 250 + k * 96, 640, 74, tk, t, '输入 → 输出：' + w, { size: 32, seed: 7511 + k, w: 3.2 });
  });

  // 底部：桥梁
  if (t >= m契合 - 0.6) {
    const S = sc.bridge || (sc.bridge = new Sk(7531).penOn());
    if (!sc.bridge_b) {
      S.line(400, y0 + 700, 1520, y0 + 700, { w: 4, col: COL_A });
      S.line(960, y0 + 640, 960, y0 + 700, { w: 3.4, col: COL_A });
      sc.bridge_b = 1;
    }
    S.at(t, m契合 - 0.55, 0.6);
    writeText('编码器-解码器：最干净的契合', 960, y0 + 790, hand(44, 700), COL_A, t, seq(m契合 - 0.2, '编码器-解码器：最干净的契合', 0.04), 0.1, 'center', false);
  }
});

// ---------------- s04 前向循环 ----------------
scene(3, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m源 = MS('f_源token', sc.st + 0.5), m表示 = MS('f_表示', sc.st + 3.0),
        m交叉 = MS('f_交叉', sc.st + 7.2), m错位 = MS('f_错位', sc.st + 14.6);

  // 编码器栈（左）
  if (t >= m源 - 0.5) {
    for (let k = 0; k < 3; k++) {
      block(sc, 'enc' + k, 200, y0 + 300 + k * 92, 300, 72, m源 + 0.2 + k * 0.4, t, 'encoder block', { size: 26, col: COL_A, seed: 7601 + k, w: 3 });
    }
    writeText('编码器', 350, y0 + 260, hand(34, 700), COL_A, t, seq(m源 + 0.3, '编码器', 0.06), 0.1, 'center', false);
    writeText('只跑一次', 350, y0 + 610, hand(28, 700), C.gray, t, seq(m表示 + 0.5, '只跑一次', 0.05), 0.1, 'center', false);
  }
  // 解码器栈（右）
  if (t >= m交叉 - 0.8) {
    for (let k = 0; k < 3; k++) {
      block(sc, 'dec' + k, 1420, y0 + 300 + k * 92, 300, 72, m交叉 - 0.4 + k * 0.4, t, 'decoder block', { size: 26, col: COL_B, seed: 7611 + k, w: 3 });
    }
    writeText('解码器', 1570, y0 + 260, hand(34, 700), COL_B, t, seq(m交叉 - 0.3, '解码器', 0.06), 0.1, 'center', false);
    writeText('自回归地跑', 1570, y0 + 610, hand(28, 700), C.gray, t, seq(m交叉 + 1.2, '自回归地跑', 0.05), 0.1, 'center', false);
  }
  // 交叉注意力箭头
  if (t >= m交叉 - 0.4) {
    const S = sc.cross || (sc.cross = new Sk(7621).penOn());
    if (!sc.cross_b) { arrowTo(S, 510, y0 + 480, 1410, y0 + 480, { w: 4.4, col: COL_A }); sc.cross_b = 1; }
    S.at(t, m交叉 - 0.35, 0.6);
    writeText('交叉注意力', 960, y0 + 436, hand(36, 700), COL_A, t, seq(m交叉 - 0.1, '交叉注意力', 0.05), 0.1, 'center', false);
  }
  // 错位一格
  if (t >= m错位 - 0.5) {
    const S2 = sc.shift || (sc.shift = new Sk(7631).penOn());
    if (!sc.shift_b) {
      S2.rrect(660, y0 + 700, 240, 66, 10, { w: 2.8 });
      S2.rrect(920, y0 + 700, 240, 66, 10, { w: 2.8, col: COL_A });
      S2.line(880, y0 + 748, 916, y0 + 748, { w: 3, col: COL_A });
      sc.shift_b = 1;
    }
    S2.at(t, m错位 - 0.45, 0.6);
    writeText('输入', 780, y0 + 733, hand(26, 700), C.ink, t, seq(m错位 - 0.2, '输入', 0.06), 0.1, 'center', false);
    writeText('目标', 1040, y0 + 733, hand(26, 700), COL_A, t, seq(m错位 + 0.1, '目标', 0.06), 0.1, 'center', false);
    writeText('错位一格，损失和 GPT 一样', 960, y0 + 800, hand(30, 700), C.gray, t, seq(m错位 + 0.5, '错位一格，损失和 GPT 一样', 0.03), 0.1, 'center', false);
  }
});
