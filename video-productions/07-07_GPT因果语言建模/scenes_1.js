// 07-07 GPT 因果语言建模 —— 场景 1-4
// 时间一律从 MS('卡点名') 取；内容区不越过 y0 + 857（字幕带在 y = 908）。
// 结构按小红书数据调整：第 1 场直接给问题钩子，标题卡在第 2 场。

// 小工具：画一个 n×n 矩阵网格
function matGrid(S, x, y, n, cell, o = {}) {
  for (let i = 0; i <= n; i++) {
    S.line(x + i * cell, y, x + i * cell, y + n * cell, { w: o.w ?? 2.2, col: o.col });
    S.line(x, y + i * cell, x + n * cell, y + i * cell, { w: o.w ?? 2.2, col: o.col });
  }
  return S;
}
// 填一个格子
function cellFill(S, x, y, cell, col, a = 0.85) {
  const p = 3;
  S.fill([[x + p, y + p], [x + cell - p, y + p], [x + cell - p, y + cell - p], [x + p, y + cell - p]], col, { a, fade: 20 });
  return S;
}

// ---------------- s01 钩子：为什么只会往后写 ----------------
scene(0, (sc, t) => {
  const y0 = sc.y0;
  const mAI = MS('h_AI', sc.st + 0.3), m往后 = MS('h_往后写', sc.st + 1.2),
        m锁死 = MS('h_锁死', sc.st + 5.0), m掩码 = MS('h_掩码', sc.st + 8.2);

  // 第 1 帧就写：画面领先旁白，短视频开头才有抓手
  const T0 = sc.st + 0.22;
  if (t >= T0 - 0.1) {
    writeText('AI 聊天模型', 960, y0 + 168, hand(44, 700), C.gray, t, seq(T0, 'AI 聊天模型', 0.045), 0.1, 'center', false);
  }
  if (t >= T0 + 0.18) {
    const Q = '为什么只会往后写？';
    writeText(Q, 960, y0 + 292, hand(88, 700), C.ink, t, seq(T0 + 0.18, Q, 0.045), 0.1, 'center', false);
  }

  // 屏幕 + 三角形 + 划掉的视线
  if (t >= m锁死 - 0.6) {
    const S = sc.lock || (sc.lock = new Sk(7101).penOn());
    if (!sc.lock_b) {
      S.rrect(710, y0 + 386, 500, 292, 16, { w: 4.4 });
      S.line(710, y0 + 434, 1210, y0 + 434, { w: 2.4 });
      S.dot(736, y0 + 410, 6, C.gray2); S.dot(762, y0 + 410, 6, C.gray2); S.dot(788, y0 + 410, 6, C.gray2);
      S.poly([[960, y0 + 476], [1112, y0 + 628], [808, y0 + 628], [960, y0 + 476]], { w: 5.4, col: COL_A });
      S.line(1156, y0 + 566, 1232, y0 + 642, { w: 5.4, col: COL_A });
      S.line(1232, y0 + 566, 1156, y0 + 642, { w: 5.4, col: COL_A });
      sc.lock_b = 1;
    }
    S.at(t, m锁死 - 0.55, 1.0);
  }
  if (t >= m锁死 + 0.9) {
    writeText('视线被一个三角形锁死', 960, y0 + 726, hand(40, 700), C.ink, t, seq(m锁死 + 0.95, '视线被一个三角形锁死', 0.05), 0.1, 'center', false);
  }

  // 落点：橙色块 + 白字「因果掩码」
  if (t >= m掩码 - 0.6) {
    const S2 = sc.block || (sc.block = new Sk(7111).penOn());
    if (!sc.block_b) { S2.fill(rrPts(660, y0 + 790, 600, 108, 18), COL_A, { fade: 1 }); sc.block_b = 1; }
    S2.at(t, m掩码 - 0.55, 0.35);
    writeText('因果掩码', 960, y0 + 846, hand(58, 700), '#ffffff', t, seq(m掩码 - 0.2, '因果掩码', 0.08), 0.1, 'center', false);
  }
});

// ---------------- s02 片头：GPT 与因果语言建模 ----------------
scene(1, (sc, t) => {
  const y0 = sc.y0;
  const m阶段 = MS('t_阶段', sc.st + 0.4), m课号 = MS('t_课号', sc.st + 1.6),
        m标题 = MS('t_标题', sc.st + 3.0), mBERT = MS('t_BERT', sc.st + 6.0),
        m只看过去 = MS('t_只看过去', sc.st + 8.2), m掩码 = MS('t_掩码', sc.st + 10.6);

  const F = sc.frame || (sc.frame = new Sk(7201).penOn().rrect(150, y0 + 118, 1620, 520, 28, { w: 4.8 }));
  F.at(t, sc.st + 0.12, 0.8);

  if (t >= m阶段 - 0.35) {
    const TAG = '阶段 7 · 07';
    tag(TAG, 218, y0 + 180, 42, P(t, m阶段 - 0.3, 0.32));
  }
  if (t >= m标题 - 0.25) {
    writeText('GPT', 222, y0 + 330, hand(102, 700), C.ink, t, seq(m标题 - 0.1, 'GPT', 0.13), 0.1);
  }
  if (t >= m标题 + 0.5) {
    const T2 = '因果语言建模';
    writeText(T2, 222, y0 + 448, hand(72, 700), C.ink, t, seq(m标题 + 0.55, T2, 0.075), 0.1);
    const w2 = tw(T2, hand(72, 700));
    underline(212, 222 + w2 + 10, y0 + 496, RQ(7011), P(t, m标题 + 1.35, 0.35), 8, COL_A, m标题 + 1.35);
  }
  if (t >= mBERT - 0.35) {
    const A = 'BERT 看两边';
    writeText(A, 224, y0 + 570, hand(38, 700), C.gray, t, seq(mBERT - 0.25, A, 0.05), 0.1);
  }
  if (t >= m只看过去 - 0.35) {
    const B = '|  GPT 只看过去';
    writeText(B, 224 + tw('BERT 看两边', hand(38, 700)) + 24, y0 + 570, hand(38, 700), COL_B, t, seq(m只看过去 - 0.25, B, 0.05), 0.1);
  }
  if (t >= m掩码 - 0.7) {
    const MX = 1432, MY = y0 + 250, SZ = 208, N = 5, CW = SZ / N;
    const S = sc.tri || (sc.tri = new Sk(7211).penOn());
    if (!sc.tri_b) {
      for (let i = 0; i <= N; i++) {
        S.line(MX + i * CW, MY, MX + i * CW, MY + SZ, { w: 2.2 });
        S.line(MX, MY + i * CW, MX + SZ, MY + i * CW, { w: 2.2 });
      }
      for (let i = 0; i < N; i++) for (let j = 0; j <= i; j++) cellFill(S, MX + j * CW, MY + i * CW, CW, COL_A, 0.8);
      for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) {
        S.line(MX + j * CW + 9, MY + i * CW + 9, MX + (j + 1) * CW - 9, MY + (i + 1) * CW - 9, { w: 2.4, col: C.gray });
        S.line(MX + (j + 1) * CW - 9, MY + i * CW + 9, MX + j * CW + 9, MY + (i + 1) * CW - 9, { w: 2.4, col: C.gray });
      }
      sc.tri_b = 1;
    }
    S.at(t, m掩码 - 0.6, 1.0);
    writeText('因果掩码', MX + SZ / 2, MY + SZ + 48, hand(34, 700), COL_A, t, seq(m掩码 + 0.5, '因果掩码', 0.08), 0.1, 'center');
  }
});

// ---------------- s03 语言模型在学什么 ----------------
scene(2, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m概率 = MS('s03_概率', sc.st + 0.5), m生成 = MS('s03_生成', sc.st + 6.2), m作弊 = MS('s03_作弊', sc.st + 14.4);

  // 一排 token 方块，最后一个待预测
  const toks = ['token1', 'token2', 'token3', 'token4', 'token5', '?'];
  const BX = 180, BY = y0 + 296, BW = 176, BH = 118, GAP = 26;
  toks.forEach((w, k) => {
    const tk = m概率 + 0.2 + k * 0.3;
    if (t < tk - 0.3) return;
    const x = BX + k * (BW + GAP);
    const last = k === toks.length - 1;
    const S = sc['t' + k] || (sc['t' + k] = new Sk(7211 + k).penOn().rrect(x, BY, BW, BH, 14, { w: 3.6, col: last ? COL_A : C.ink }));
    S.at(t, tk - 0.25, 0.4);
    writeText(w, x + BW / 2, BY + BH / 2, hand(38, 700), last ? COL_A : C.ink, t, seq(tk + 0.1, w, 0.06), 0.1, 'center');
  });

  // 最后一个位置上方的概率条
  if (t >= m概率 + 1.9) {
    const x = BX + 5 * (BW + GAP) + BW / 2;
    const S = sc.bar || (sc.bar = new Sk(7221).penOn().rrect(x - 46, y0 + 196, 92, 62, 10, { w: 3.2, col: COL_A }));
    S.at(t, m概率 + 1.9, 0.4);
    writeText('P', x, y0 + 227, hand(34, 700), COL_A, t, seq(m概率 + 2.0, 'P', 0.1), 0.1, 'center');
    if (t >= m概率 + 2.5) {
      const T = '给定前文，下一个 token 的概率';
      writeText(T, 960, y0 + 168, hand(36, 700), C.gray, t, seq(m概率 + 2.55, T, 0.04), 0.1, 'center');
    }
  }

  // 一次生成一个 token
  if (t >= m生成 - 0.4) {
    const A = '训练时整段并行，生成时一次一个';
    writeText(A, 960, y0 + 500, hand(46, 700), C.ink, t, seq(m生成 - 0.25, A, 0.055), 0.1, 'center');
  }
  if (t >= m生成 + 3.0) {
    const B = '自回归：把输出喂回输入';
    writeText(B, 960, y0 + 582, hand(38, 700), C.gray, t, seq(m生成 + 3.05, B, 0.045), 0.1, 'center');
  }

  // 否则会作弊：右侧画一条禁止斜线
  if (t >= m作弊 - 0.5) {
    const S = sc.ban || (sc.ban = new Sk(7231).penOn());
    if (!sc.ban_b) {
      S.ellipse(1560, y0 + 420, 116, 116, { w: 5.2, col: COL_A });
      S.line(1478, y0 + 502, 1642, y0 + 338, { w: 6.2, col: COL_A });
      sc.ban_b = 1;
    }
    S.at(t, m作弊 - 0.45, 0.8);
    const CT = '不能偷看后面';
    writeText(CT, 1560, y0 + 648, hand(34, 700), COL_A, t, seq(m作弊 + 0.8, CT, 0.05), 0.1, 'center', false);
  }
});

// ---------------- s04 因果掩码：一个三角形 ----------------
scene(3, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m上三角 = MS('s04_上三角', sc.st + 0.4), m负无穷 = MS('s04_负无穷', sc.st + 2.6),
        mSoftmax = MS('s04_softmax', sc.st + 5.2), m只关注 = MS('s04_只关注', sc.st + 10.0);

  const N = 6, CELL = 46, SZ = N * CELL;
  const LX = 190, LY = y0 + 300, RX = 830, RY = y0 + 300;

  // 左矩阵：上三角填 -inf
  if (t >= m上三角 - 0.45) {
    const S = sc.LM || (sc.LM = new Sk(7241).penOn());
    if (!sc.LM_b) {
      matGrid(S, LX, LY, N, CELL);
      for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) cellFill(S, LX + j * CELL, LY + i * CELL, CELL, C.gray3, 0.95);
      sc.LM_b = 1;
    }
    S.at(t, m上三角 - 0.4, 0.7);
    writeText('注意力分数 + M', LX + SZ / 2, LY - 40, hand(34, 700), C.ink, t, seq(m上三角, '注意力分数 + M', 0.05), 0.1, 'center');
  }
  if (t >= m负无穷 - 0.35) {
    // 上三角里写 -inf
    for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) {
      const tk = m负无穷 + 0.1 + (i * N + j) * 0.05;
      if (t < tk) continue;
      writeText('-inf', LX + j * CELL + CELL / 2, LY + i * CELL + CELL / 2, hand(19, 700), C.ink, t, seq(tk, '-inf', 0.02), 0.06, 'center');
    }
  }

  // 中间箭头 + softmax
  if (t >= mSoftmax - 0.9) {
    const S = sc.arrow || (sc.arrow = new Sk(7251).penOn());
    if (!sc.arrow_b) { arrowTo(S, LX + SZ + 36, LY + SZ / 2, RX - 36, RY + SZ / 2, { w: 4.2 }); sc.arrow_b = 1; }
    S.at(t, mSoftmax - 0.85, 0.5);
    writeText('softmax', (LX + SZ + RX) / 2, LY + SZ / 2 - 40, hand(38, 700), COL_A, t, seq(mSoftmax - 0.5, 'softmax', 0.06), 0.1, 'center');
  }

  // 右矩阵：下三角是概率分布
  if (t >= mSoftmax - 0.2) {
    const S = sc.RM || (sc.RM = new Sk(7261).penOn());
    if (!sc.RM_b) {
      matGrid(S, RX, RY, N, CELL, { col: C.ink });
      for (let i = 0; i < N; i++) for (let j = 0; j <= i; j++) cellFill(S, RX + j * CELL, RY + i * CELL, CELL, COL_A, 0.55);
      sc.RM_b = 1;
    }
    S.at(t, mSoftmax - 0.15, 0.7);
    writeText('每行和为 1', RX + SZ / 2, RY - 40, hand(34, 700), COL_A, t, seq(mSoftmax + 0.5, '每行和为 1', 0.05), 0.1, 'center');
  }

  // 右侧说明
  if (t >= m只关注 - 0.4) {
    const A = '每个位置只关注自己';
    writeText(A, 1240, y0 + 330, hand(46, 700), C.ink, t, seq(m只关注 - 0.25, A, 0.05), 0.1);
  }
  if (t >= m只关注 + 1.4) {
    const B = '和更早的位置';
    writeText(B, 1240, y0 + 404, hand(46, 700), COL_A, t, seq(m只关注 + 1.45, B, 0.06), 0.1);
  }
  if (t >= m只关注 + 2.6) {
    const CT = '一次前向 = 全部预测';
    writeText(CT, 1240, y0 + 502, hand(36, 700), C.gray, t, seq(m只关注 + 2.65, CT, 0.045), 0.1);
  }
});
