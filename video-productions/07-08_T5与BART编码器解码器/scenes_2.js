// 07-08 T5 与 BART —— 场景 5-7

// ---------------- s05 T5：一切皆文本到文本 ----------------
scene(4, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mT5 = MS('g_T5', sc.st + 0.5), m重构 = MS('g_重构', sc.st + 3.2),
        mSpan = MS('g_span', sc.st + 7.4), m统一 = MS('g_统一', sc.st + 12.6);

  // T5 徽章
  if (t >= mT5 - 0.4) {
    const S = sc.badge || (sc.badge = new Sk(7701).penOn().rrect(180, y0 + 236, 210, 96, 16, { w: 4, col: COL_A }));
    S.at(t, mT5 - 0.35, 0.4);
    writeText('T5', 285, y0 + 284, hand(52, 700), COL_A, t, seq(mT5 - 0.1, 'T5', 0.1), 0.1, 'center', false);
    writeText('2019 · 一切皆文本到文本', 430, y0 + 284, hand(38, 700), C.ink, t, seq(mT5 + 0.4, '2019 · 一切皆文本到文本', 0.04), 0.1);
  }

  // 源句 → 被破坏 → 目标
  const SRC = 'the quick brown fox jumps over the lazy dog';
  if (t >= m重构 - 0.4) {
    writeText('源句', 180, y0 + 386, hand(28, 700), C.gray, t, seq(m重构 - 0.3, '源句', 0.05), 0.1);
    writeText(SRC, 280, y0 + 386, hand(32, 700), C.ink, t, seq(m重构 - 0.2, SRC, 0.018), 0.04);
  }

  // span 破坏：第二行用哨兵替换两个片段
  if (t >= mSpan - 0.5) {
    const f32 = hand(32, 700);
    writeText('破坏后', 180, y0 + 470, hand(28, 700), C.gray, t, seq(mSpan - 0.45, '破坏后', 0.04), 0.08);
    let x = 280;
    const segs = [
      ['the quick ', C.ink, 0],
      ['<extra_id_0>', COL_A, 0.5],
      [' fox jumps over the ', C.ink, 0.8],
      ['<extra_id_1>', COL_A, 1.3],
      [' dog', C.ink, 1.6]
    ];
    for (const [seg, col, dt] of segs) {
      writeText(seg, x, y0 + 470, f32, col, t, seq(mSpan + dt, seg, 0.02), 0.04, 'left', false);
      x += tw(seg, f32);
    }
  }

  // 目标行
  if (t >= mSpan + 1.4) {
    writeText('目标', 180, y0 + 566, hand(28, 700), C.gray, t, seq(mSpan + 2.2, '目标', 0.05), 0.1);
    const TGT = '<extra_id_0> brown <extra_id_1> stitch in';
    writeText(TGT, 280, y0 + 566, hand(30, 700), COL_B, t, seq(mSpan + 2.35, TGT, 0.02), 0.04);
  }

  // 统一
  if (t >= m统一 - 0.6) {
    const S2 = sc.unify || (sc.unify = new Sk(7721).penOn());
    if (!sc.unify_b) {
      S2.line(180, y0 + 600, 1740, y0 + 600, { w: 3, col: COL_A });
      sc.unify_b = 1;
    }
    S2.at(t, m统一 - 0.55, 0.5);
    writeText('单一架构 · 单一词表 · 单一损失', 960, y0 + 680, hand(44, 700), COL_A, t, seq(m统一 - 0.2, '单一架构 · 单一词表 · 单一损失', 0.05), 0.1, 'center', false);
  }
});

// ---------------- s06 实跑：span 破坏 ----------------
scene(5, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m跑 = MS('r_跑代码', sc.st + 0.5), mId = MS('r_extraid', sc.st + 3.4),
        mBrown = MS('r_brown', sc.st + 8.8), m一致 = MS('r_一致', sc.st + 14.4);

  // 实跑标注
  if (t >= m跑 - 0.4) {
    writeText('code/main.py 实跑输出', 150, y0 + 200, hand(26, 700), C.gray, t, seq(m跑 - 0.3, 'code/main.py 实跑输出', 0.025), 0.08);
  }

  // 源行（含哨兵）
  if (t >= m跑 + 0.4) {
    writeText('corrupted source', 150, y0 + 268, hand(26, 700), C.gray, t, seq(m跑 + 0.35, 'corrupted source', 0.03), 0.06);
    const L1 = 'the quick <extra_id_0> fox jumps';
    writeText(L1, 150, y0 + 322, hand(30, 700), C.ink, t, seq(m跑 + 0.6, L1, 0.02), 0.04);
    const L2 = 'over the lazy dog a <extra_id_1> time saves';
    writeText(L2, 150, y0 + 372, hand(30, 700), C.ink, t, seq(m跑 + 1.4, L2, 0.02), 0.04);
  }

  // 哨兵高亮
  if (t >= mId - 0.5) {
    const S = sc.hl || (sc.hl = new Sk(7801).penOn());
    if (!sc.hl_b) {
      S.fill(rrPts(390, y0 + 292, 210, 48, 8), COL_A, { a: 0.18, fade: 1 });
      S.fill(rrPts(500, y0 + 342, 210, 48, 8), COL_A, { a: 0.18, fade: 1 });
      sc.hl_b = 1;
    }
    S.at(t, mId - 0.45, 0.5);
  }

  // 目标行
  if (t >= mBrown - 0.5) {
    writeText('decoder target', 150, y0 + 470, hand(26, 700), C.gray, t, seq(mBrown - 0.45, 'decoder target', 0.03), 0.06);
    const T1 = '<extra_id_0> brown <extra_id_1> stitch in <extra_id_2>';
    writeText(T1, 150, y0 + 524, hand(30, 700), COL_B, t, seq(mBrown - 0.2, T1, 0.018), 0.04);
    writeText('brown、stitch in 就是被挖掉的词', 150, y0 + 590, hand(28, 700), C.gray, t, seq(mBrown + 1.6, 'brown、stitch in 就是被挖掉的词', 0.03), 0.08);
  }

  // 打勾 + 一致
  if (t >= m一致 - 0.6) {
    const S2 = sc.check || (sc.check = new Sk(7811).penOn().poly([[1560, y0 + 700], [1610, y0 + 752], [1720, y0 + 636]], { w: 9, col: COL_A }));
    S2.at(t, m一致 - 0.55, 0.35);
    writeText('reconstruction matches original: YES', 150, y0 + 700, hand(34, 700), COL_A, t, seq(m一致 - 0.2, 'reconstruction matches original: YES', 0.025), 0.06);
  }
});

// ---------------- s07 BART：五种加噪 ----------------
scene(6, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m去噪 = MS('b_去噪', sc.st + 0.5), m五种 = MS('b_五种', sc.st + 4.6), m组合 = MS('b_组合', sc.st + 11.0);

  if (t >= m去噪 - 0.4) {
    writeText('BART = 去噪自编码器', 180, y0 + 218, hand(44, 700), C.ink, t, seq(m去噪 - 0.3, 'BART = 去噪自编码器', 0.05), 0.1);
    writeText('对输入加噪，再让解码器重建原文', 180, y0 + 282, hand(30, 700), C.gray, t, seq(m去噪 + 1.2, '对输入加噪，再让解码器重建原文', 0.035), 0.08);
  }

  const noises = ['token 掩码', 'token 删除', '文本填充', '句子打乱', '文档旋转'];
  const BW = 300, BH = 96, GAP = 30, COLS = 3;
  noises.forEach((w, k) => {
    const tk = m五种 + 0.3 + k * 0.5;
    if (t < tk - 0.3) return;
    const col = k % COLS, row = Math.floor(k / COLS);
    const x = 180 + col * (BW + GAP);
    const y = y0 + 380 + row * (BH + 34);
    const hot = (k === 2 || k === 3);
    block(sc, 'nz' + k, x, y, BW, BH, tk, t, w, { size: 34, col: hot ? COL_A : C.ink, tcol: hot ? COL_A : C.ink, seed: 7901 + k });
  });

  if (t >= m组合 - 0.6) {
    const S = sc.pick || (sc.pick = new Sk(7911).penOn());
    if (!sc.pick_b) {
      S.line(930, y0 + 640, 1520, y0 + 640, { w: 3.4, col: COL_A });
      sc.pick_b = 1;
    }
    S.at(t, m组合 - 0.55, 0.5);
    writeText('文本填充 + 句子打乱：下游效果最好', 960, y0 + 716, hand(40, 700), COL_A, t, seq(m组合 - 0.2, '文本填充 + 句子打乱：下游效果最好', 0.035), 0.1, 'center', false);
    writeText('代价：预训练算力比 T5 更高', 960, y0 + 784, hand(32, 700), C.gray, t, seq(m组合 + 1.8, '代价：预训练算力比 T5 更高', 0.035), 0.1, 'center', false);
  }
});
