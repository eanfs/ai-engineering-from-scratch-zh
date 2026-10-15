// ---------------- s05 一张不够，就多画几张——别靠翻倍 ----------------
scene(4, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mPar = MS('s05_并行', sc.st + 0.4), mWide = MS('s05_全宽', sc.st + 4.5), mDbl = MS('s05_翻倍', sc.st + 6.5),
        mCost = MS('s05_花钱', sc.st + 8.5), m2017 = MS('s05_2017', sc.st + 10.5);
  // 头卡逐张叠出
  for (let k = 0; k < 3; k++) {
    const x = 180 + k * 290, tk = mPar + k * 0.5;
    if (t < tk - 0.25) continue;
    const S = sc['hd' + k] || (sc['hd' + k] = new Sk(1601 + k).penOn().rrect(x, y0 + 200, 250, 150, 16, { w: 3.4 }));
    S.at(t, tk, 0.4);
    writeText('头 ' + k, x + 125, y0 + 258, hand(46, 700), C.ink, t, seq(tk + 0.25, '头 ' + k, 0.09), 0.1, 'center');
    if (t >= mWide) writeText('全宽 8 维', x + 125, y0 + 318, hand(34, 700), COL_A, t, seq(mWide + k * 0.25, '全宽 8 维', 0.07), 0.1, 'center');
  }
  // 参数量柱 1× → 4×
  if (t >= mDbl - 0.6) {
    const base = y0 + 620;
    const b1 = sc.b1 || (sc.b1 = new Sk(1611).penOn().rrect(1180, base - 110, 96, 110, 8, { w: 3.2 }));
    if (!sc.b1_b) sc.b1_b = 1;
    b1.at(t, mDbl - 0.5, 0.35);
    writeText('1×', 1228, base + 40, hand(42, 700), C.ink, t, seq(mDbl, '1×', 0.1), 0.1, 'center');
    const b2 = sc.b2 || (sc.b2 = new Sk(1621).penOn().rrect(1350, base - 440, 96, 440, 8, { w: 3.2, col: COL_A }));
    if (t >= mDbl + 0.5) { b2.at(t, mDbl + 0.5, 0.5);
      writeText('4×', 1398, base + 40, hand(42, 700), COL_A, t, seq(mDbl + 1.1, '4×', 0.1), 0.1, 'center'); }
    if (t >= mDbl + 0.4) label('头数翻倍 → 参数跟着翻倍', 1180, y0 + 700, t, mDbl + 0.4, 40);
  }
  // 「花钱买表达力」被划掉
  if (t >= mCost - 0.3) {
    const f = hand(50, 700), x = 180, y = y0 + 720, w2 = tw('花钱买表达力 ≠ 设计', f);
    writeText('花钱买表达力 ≠ 设计', x, y, f, C.ink, t, seq(mCost, '花钱买表达力 ≠ 设计', 0.06), 0.09);
    const X = sc.xout || (sc.xout = new Sk(1631).penOn());
    if (!sc.xout_b) { X.line(x - 10, y + 26, x + w2 + 10, y - 26, { w: 7, col: COL_A }); sc.xout_b = 1; }
    X.at(t, mCost + 0.75, 0.35);
  }
  if (t >= m2017) { label('→ 2017 年的关键一步', 180, y0 + 820, t, m2017, 46); }
});

// ---------------- s06 关键：拆开，不是复制 ----------------
scene(5, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mSplit = MS('s06_拆', sc.st + 0.4), mD8 = MS('s06_dmodel8', sc.st + 3.5), mN2 = MS('s06_头数2', sc.st + 5),
        mD4 = MS('s06_dhead4', sc.st + 6.5), mW = MS('s06_投影矩阵', sc.st + 8), m84 = MS('s06_8乘4', sc.st + 10),
        m88 = MS('s06_8乘8', sc.st + 12);
  // d_model = 8：8 格条
  if (t >= mSplit - 0.5) {
    const S = sc.strip || (sc.strip = new Sk(1701).penOn());
    if (!sc.strip_b) { for (let k = 0; k < 8; k++) S.rrect(180 + k * 92, y0 + 180, 84, 84, 8, { w: 2.8 }); sc.strip_b = 1; }
    S.at(t, mSplit - 0.4, 0.6);
    if (t >= mD8) label('d_model = 8', 180, y0 + 310, t, mD8, 46);
    // 拆成两组 4 格
    if (t >= mN2 - 0.4) {
      const A2 = sc.arrow2 || (sc.arrow2 = new Sk(1711).penOn());
      if (!sc.arrow2_b) { arrowTo(A2, 380, y0 + 300, 380, y0 + 360, { w: 3 }); arrowTo(A2, 740, y0 + 300, 740, y0 + 360, { w: 3 }); sc.arrow2_b = 1; }
      A2.at(t, mN2 - 0.35, 0.3);
      for (const [gi, gx] of [[0, 200], [1, 560]]) {
        if (t < mN2 + gi * 0.4) continue;
        const G = sc['g' + gi] || (sc['g' + gi] = new Sk(1721 + gi).penOn());
        if (!sc['g' + gi + '_b']) { for (let k = 0; k < 4; k++) G.rrect(gx + k * 88, y0 + 380, 80, 80, 8, { w: 2.8, col: COL_A }); sc['g' + gi + '_b'] = 1; }
        G.at(t, mN2 + gi * 0.4, 0.5);
        writeText('头 ' + gi, gx + 176, y0 + 500, hand(38, 700), COL_A, t, seq(mN2 + gi * 0.4 + 0.35, '头 ' + gi, 0.09), 0.1, 'center');
      }
    }
    if (t >= mD4) label('d_head = 4', 180, y0 + 540, t, mD4, 46);
  }
  // 8×4 的投影矩阵
  if (t >= mW - 0.4) {
    const x = 420, y = y0 + 570, S = sc.w84 || (sc.w84 = new Sk(1731).penOn());
    if (!sc.w84_b) { gridSk(S, x, y, 230, 230, 4, 8, { w: 2.2 }); sc.w84_b = 1; }
    S.at(t, mW, 0.7);
    if (t >= m84) { writeText('8 × 4', x + 115, y - 36, hand(48, 700), COL_A, t, seq(m84 + 0.1, '8 × 4', 0.08), 0.1, 'center'); label('每个头的 W_Q / W_K / W_V', x + 280, y + 90, t, mW + 0.6, 40); }
  }
  // 8×8 打叉
  if (t >= m88 - 0.5) {
    const x = 1230, y = y0 + 570, S = sc.w88 || (sc.w88 = new Sk(1741).penOn());
    if (!sc.w88_b) { gridSk(S, x, y, 230, 230, 8, 8, { w: 2, col: C.gray }); sc.w88_b = 1; }
    S.at(t, m88 - 0.45, 0.6);
    const X = sc.xx || (sc.xx = new Sk(1751).penOn());
    if (!sc.xx_b) { X.line(x - 16, y - 16, x + 246, y + 246, { w: 9, col: COL_A }); X.line(x + 246, y - 16, x - 16, y + 246, { w: 9, col: COL_A }); sc.xx_b = 1; }
    X.at(t, m88 + 0.2, 0.4);
    label('不是 8 × 8', x, y - 46, t, m88 + 0.6, 46);
  }
});

// ---------------- s07 头是免费的 ----------------
scene(6, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mPar = MS('s07_参数量', sc.st + 0.5), mFull = MS('s07_全宽头', sc.st + 2.5), mFree = MS('s07_免费', sc.st + 5),
        mAdd = MS('s07_加头', sc.st + 7), mSub = MS('s07_子空间', sc.st + 9), mSpec = MS('s07_专精', sc.st + 11);
  // 两块 8×4 = 一个 8×8
  if (t >= mPar - 0.5) {
    const A2 = sc.m1 || (sc.m1 = new Sk(1801).penOn()), B2 = sc.m2 || (sc.m2 = new Sk(1802).penOn()), C2 = sc.m3 || (sc.m3 = new Sk(1803).penOn());
    if (!sc.m1_b) { gridSk(A2, 150, y0 + 200, 260, 260, 4, 8, { w: 2 }); gridSk(B2, 470, y0 + 200, 260, 260, 4, 8, { w: 2 }); sc.m1_b = 1; }
    A2.at(t, mPar - 0.4, 0.5); B2.at(t, mPar + 0.1, 0.5);
    writeText('8 × 4', 280, y0 + 168, hand(42, 700), C.ink, t, seq(mPar + 0.4, '8 × 4', 0.08), 0.1, 'center');
    writeText('8 × 4', 600, y0 + 168, hand(42, 700), C.ink, t, seq(mPar + 0.6, '8 × 4', 0.08), 0.1, 'center');
    const PL = sc.plus || (sc.plus = new Sk(1804).penOn());
    if (!sc.plus_b) { PL.line(422, y0 + 300, 458, y0 + 300, { w: 5 }); PL.line(440, y0 + 282, 440, y0 + 318, { w: 5 }); sc.plus_b = 1; }
    PL.at(t, mPar + 0.7, 0.25);
    if (t >= mFull - 0.4) {
      if (!sc.m3_b) { gridSk(C2, 790, y0 + 176, 300, 300, 8, 8, { w: 2.2, col: COL_A }); sc.m3_b = 1; }
      C2.at(t, mFull - 0.35, 0.6);
      writeText('8 × 8', 940, y0 + 146, hand(44, 700), COL_A, t, seq(mFull + 0.3, '8 × 8', 0.08), 0.1, 'center');
      label('（= 两块 8×4 的参数量）', 790, y0 + 520, t, mFull + 0.5, 36);
    }
  }
  // 只加并行 + 子空间
  if (t >= mAdd - 0.4) {
    const AR = sc.ar || (sc.ar = new Sk(1811).penOn());
    if (!sc.ar_b) { arrowTo(AR, 1240, y0 + 250, 1700, y0 + 250, { w: 3.6 }); arrowTo(AR, 1240, y0 + 330, 1700, y0 + 330, { w: 3.6 }); sc.ar_b = 1; }
    AR.at(t, mAdd - 0.35, 0.6);
    label('只加并行，不加参数', 1240, y0 + 180, t, mAdd + 0.2, 42);
  }
  if (t >= mSub - 0.4) {
    const AX = sc.ax || (sc.ax = new Sk(1821).penOn());
    if (!sc.ax_b) { AX.line(1260, y0 + 560, 1700, y0 + 560, { w: 3.4 }); AX.line(1260, y0 + 560, 1260, y0 + 430, { w: 3.4 }); arrowTo(AX, 1260, y0 + 560, 1620, y0 + 440, { w: 3, col: COL_A }); sc.ax_b = 1; }
    AX.at(t, mSub - 0.35, 0.6);
    label('子空间 1', 1280, y0 + 600, t, mSub + 0.2, 38);
    label('子空间 2', 1520, y0 + 600, t, mSub + 0.5, 38);
  }
  if (t >= mSpec) label('各自专精，不抢表示预算', 1240, y0 + 700, t, mSpec, 42);
  const stp = sc.stamp || (sc.stamp = makeStamp('头是免费的', 104, COL_A, 1831, 200));
  drawStamp(stp, 500, y0 + 760, t, mFree + 0.1, -0.04);
});

// ---------------- s08 头真的会专精吗？会 ----------------
scene(7, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mThink = MS('s08_猜想', sc.st + 0.4), mProbe = MS('s08_探针', sc.st + 2.5), mPos = MS('s08_位置', sc.st + 5),
        mPrev = MS('s08_前一个', sc.st + 6.6), mCopy = MS('s08_复制', sc.st + 8.2), mName = MS('s08_命名实体', sc.st + 9.6),
        mInd = MS('s08_归纳头', sc.st + 11), mCtx = MS('s08_上下文', sc.st + 12.5);
  // 放大镜 + 探针研究
  if (t >= mProbe - 0.5) {
    const MG = sc.mg || (sc.mg = new Sk(1901).penOn().ellipse(700, y0 + 250, 92, 92, { w: 4.5 }).line(766, y0 + 316, 846, y0 + 402, { w: 9 }));
    MG.at(t, mProbe - 0.45, 0.6);
    label('探针研究 2019–2024', 200, y0 + 386, t, mProbe + 0.3, 42);
  }
  if (t >= mThink) label('这不是理论猜想', 200, y0 + 180, t, mThink, 42);
  // 五张标签卡
  const CARD = [['位置头', mPos, false], ['前一个 token 头', mPrev, false], ['复制头', mCopy, false], ['命名实体头', mName, false], ['归纳头', mInd, true]];
  for (let k = 0; k < 5; k++) {
    const x = 200 + k * 320, tk = CARD[k][1], hi = CARD[k][2];
    if (t < tk - 0.35) continue;
    const S = sc['cd' + k] || (sc['cd' + k] = new Sk(1911 + k).penOn().rrect(x, y0 + 460, 290, 140, 18, { w: 3.4, col: hi ? COL_A : C.ink }));
    S.at(t, tk, 0.45);
    const f = hand(hi ? 48 : 42, 700);
    writeText(CARD[k][0], x + 145, y0 + 532, f, hi ? COL_A : C.ink, t, seq(tk + 0.3, CARD[k][0], 0.07), 0.1, 'center');
  }
  if (t >= mCtx) label('→ 上下文学习背后的电路', 200, y0 + 700, t, mCtx, 50);
  if (t >= mInd) { const E = sc.ind || (sc.ind = new Sk(1921).penOn()); if (!sc.ind_b) { E.ellipse(1625, y0 + 530, 168, 92, { w: 4, col: COL_A }); sc.ind_b = 1; } E.at(t, mInd + 0.5, 0.5); }
});

// ---------------- s09 解法第一步：reshape 与 transpose ----------------
scene(8, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mX = MS('s09_X', sc.st + 0.4), mProj = MS('s09_投影', sc.st + 2.5), mRe = MS('s09_reshape', sc.st + 6),
        mTr = MS('s09_transpose', sc.st + 10), mLoop = MS('s09_循环', sc.st + 14), mPT = MS('s09_pytorch', sc.st + 15.5);
  const boxes = [
    ['X', '(N, d_model)', 140, mX, C.ink],
    ['Q / K / V', '投影后同形状', 430, mProj, C.ink],
    ['reshape', '(N, n_heads, d_head)', 740, mRe, COL_A],
    ['transpose', '(n_heads, N, d_head)', 1080, mTr, COL_A],
  ];
  for (let k = 0; k < boxes.length; k++) {
    const [nm, sub, x, tk, col] = boxes[k];
    if (t < tk - 0.4) continue;
    const S = sc['bx' + k] || (sc['bx' + k] = new Sk(2001 + k).penOn().rrect(x, y0 + 280, 280, 140, 16, { w: 3.6, col }));
    S.at(t, tk, 0.5);
    writeText(nm, x + 140, y0 + 330, hand(46, 700), col, t, seq(tk + 0.25, nm, 0.08), 0.1, 'center');
    writeText(sub, x + 140, y0 + 390, hand(34, 700), C.ink, t, seq(tk + 0.55, sub, 0.05), 0.1, 'center');
    if (k < boxes.length - 1) { const A = sc['ar' + k] || (sc['ar' + k] = new Sk(2021 + k).penOn()); if (!sc['ar' + k + 'b']) { arrowTo(A, x + 288, y0 + 350, x + 424, y0 + 350, { w: 3 }); sc['ar' + k + 'b'] = 1; } A.at(t, tk + 0.7, 0.3); }
  }
  const stp = sc.stamp || (sc.stamp = makeStamp('0 个循环', 104, COL_A, 2031, 200));
  drawStamp(stp, 620, y0 + 700, t, mLoop + 0.1, -0.04);
  if (t >= mPT) { label('PyTorch 在', 1100, y0 + 660, t, mPT + 0.1, 42); enText('nn.MultiheadAttention', 1100, y0 + 740, 52, P(t, mPT + 0.4, 0.3)); label('底下做的就是这件事', 1100, y0 + 820, t, mPT + 0.9, 42); }
});
