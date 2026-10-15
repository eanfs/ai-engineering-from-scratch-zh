// ---------------- s10 解法第二步：一次批量 matmul ----------------
scene(9, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mNo = MS('s10_互不', sc.st + 0.5), mBatch = MS('s10_批量', sc.st + 7), mScale = MS('s10_平方根', sc.st + 10.5), mSat = MS('s10_饱和', sc.st + 12.5);
  // 两条通道 + 虚线墙
  if (t >= mNo - 0.5) {
    const A2 = sc.ch1 || (sc.ch1 = new Sk(2101).penOn().rrect(170, y0 + 240, 330, 120, 14, { w: 3.4 })), B2 = sc.ch2 || (sc.ch2 = new Sk(2102).penOn().rrect(170, y0 + 420, 330, 120, 14, { w: 3.4 }));
    A2.at(t, mNo - 0.45, 0.45); B2.at(t, mNo + 0.05, 0.45);
    writeText('头 0：Q₀ · K₀ᵀ', 335, y0 + 300, hand(44, 700), COL_A, t, seq(mNo + 0.2, '头 0：Q₀ · K₀ᵀ', 0.06), 0.1, 'center');
    writeText('头 1：Q₁ · K₁ᵀ', 335, y0 + 480, hand(44, 700), COL_A, t, seq(mNo + 0.7, '头 1：Q₁ · K₁ᵀ', 0.06), 0.1, 'center');
    const W2 = sc.wall || (sc.wall = new Sk(2111).penOn());
    if (!sc.wall_b) { W2.dash(560, y0 + 200, 560, y0 + 580, { w: 3.4, d: 22, gp: 14 }); sc.wall_b = 1; }
    W2.at(t, mNo + 1.2, 0.5);
    writeText('互不通信', 620, y0 + 390, hand(42, 700), C.gray, t, seq(mNo + 1.6, '互不通信', 0.09), 0.1, 'center');
  }
  // 叠层块（heads 层）+ 批量 matmul
  if (t >= mBatch - 0.6) {
    for (let k = 2; k >= 0; k--) {
      const S = sc['st' + k] || (sc['st' + k] = new Sk(2121 + k).penOn().rrect(880 + k * 16, y0 + 300 - k * 16, 320, 300, 16, { w: k ? 2.6 : 3.6, col: k ? C.gray2 : C.ink }));
      S.at(t, mBatch - 0.5 + (2 - k) * 0.18, 0.5);
    }
    writeText('(heads, N, d_head)', 1060, y0 + 440, hand(38, 700), C.ink, t, seq(mBatch + 0.3, '(heads, N, d_head)', 0.05), 0.1, 'center');
    label('一次批量 matmul', 880, y0 + 660, t, mBatch + 0.7, 44);
  }
  // 公式 + 饱和曲线
  if (t >= mScale - 0.4) {
    label('缩放因子 = √d_head', 1480, y0 + 250, t, mScale, 40);
    const F = sc.fx || (sc.fx = new Sk(2131).penOn());
    if (!sc.fx_b) {
      F.rect(1460, y0 + 300, 380, 96, { w: 3 });
      sc.fx_b = 1;
    }
    F.at(t, mScale + 0.2, 0.5);
    writeText('softmax( QKᵀ / √d_head )', 1650, y0 + 350, hand(38, 700), C.ink, t, seq(mScale + 0.5, 'softmax( QKᵀ / √d_head )', 0.04), 0.1, 'center');
  }
  if (t >= mSat - 0.4) {
    const C2 = sc.cv || (sc.cv = new Sk(2141).penOn());
    if (!sc.cv_b) {
      const pts = [];
      for (let i = 0; i <= 24; i++) { const u = i / 24, x = 1480 + u * 380, y = y0 + 620 - 120 * (1 - Math.exp(-3.2 * u)) / (1 - Math.exp(-3.2)); pts.push([x, y]); }
      C2.curve(pts, { w: 3.6, col: COL_A }); C2.line(1460, y0 + 620, 1880, y0 + 620, { w: 2.6, col: C.gray }); C2.line(1460, y0 + 620, 1460, y0 + 460, { w: 2.6, col: C.gray });
      sc.cv_b = 1;
    }
    C2.at(t, mSat - 0.35, 0.7);
    label('点积太大会让 softmax 提前饱和', 1480, y0 + 680, t, mSat - 0.15, 36);
  }
});

// ---------------- s11 解法第三步：拼回来，用 W_o 混合 ----------------
scene(10, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mOut = MS('s11_输出', sc.st + 0.5), mBack = MS('s11_堆回', sc.st + 2.5), mWo = MS('s11_Wo', sc.st + 8),
        mTalk = MS('s11_交流', sc.st + 9.5), mApi = MS('s11_接口', sc.st + 17);
  // 两个 (N, d_head)
  if (t >= mOut - 0.5) {
    const A2 = sc.a1 || (sc.a1 = new Sk(2201).penOn().rrect(150, y0 + 230, 220, 150, 14, { w: 3.4 })), B2 = sc.a2 || (sc.a2 = new Sk(2202).penOn().rrect(150, y0 + 420, 220, 150, 14, { w: 3.4 }));
    A2.at(t, mOut - 0.45, 0.5); B2.at(t, mOut + 0.05, 0.5);
    writeText('(N, d_head)', 260, y0 + 308, hand(38, 700), C.ink, t, seq(mOut + 0.2, '(N, d_head)', 0.06), 0.1, 'center');
    writeText('(N, d_head)', 260, y0 + 498, hand(38, 700), C.ink, t, seq(mOut + 0.6, '(N, d_head)', 0.06), 0.1, 'center');
    const A = sc.ar1 || (sc.ar1 = new Sk(2211).penOn());
    if (!sc.ar1_b) { arrowTo(A, 378, y0 + 305, 520, y0 + 380, { w: 3 }); arrowTo(A, 378, y0 + 495, 520, y0 + 420, { w: 3 }); sc.ar1_b = 1; }
    A.at(t, mOut + 1.0, 0.4);
  }
  // 堆回 (N, d_model)
  if (t >= mBack - 0.5) {
    const S = sc.cat || (sc.cat = new Sk(2221).penOn().rrect(540, y0 + 300, 280, 200, 16, { w: 3.6 }));
    S.at(t, mBack - 0.45, 0.5);
    writeText('(N, d_model)', 680, y0 + 400, hand(40, 700), C.ink, t, seq(mBack + 0.25, '(N, d_model)', 0.055), 0.1, 'center');
    const A = sc.ar2 || (sc.ar2 = new Sk(2231).penOn());
    if (!sc.ar2_b) { arrowTo(A, 828, y0 + 400, 960, y0 + 400, { w: 3.4 }); sc.ar2_b = 1; }
    A.at(t, mBack + 1.2, 0.35);
  }
  // W_o 方块 + 圈出「唯一的交流」
  if (t >= mWo - 0.5) {
    const S = sc.wo || (sc.wo = new Sk(2241).penOn().rrect(980, y0 + 320, 220, 160, 14, { w: 3.8, col: COL_A }));
    S.at(t, mWo - 0.45, 0.5);
    writeText('W_o', 1090, y0 + 400, hand(56, 700), COL_A, t, seq(mWo + 0.25, 'W_o', 0.1), 0.1, 'center');
    writeText('(d_model, d_model)', 1090, y0 + 452, hand(30, 700), C.ink, t, seq(mWo + 0.55, '(d_model, d_model)', 0.04), 0.1, 'center');
    const A = sc.ar3 || (sc.ar3 = new Sk(2251).penOn());
    if (!sc.ar3_b) { arrowTo(A, 1208, y0 + 400, 1340, y0 + 400, { w: 3.4 }); sc.ar3_b = 1; }
    A.at(t, mWo + 0.8, 0.35);
    const O = sc.out || (sc.out = new Sk(2261).penOn().rrect(1360, y0 + 320, 220, 160, 14, { w: 3.4 }));
    O.at(t, mWo + 1.1, 0.5);
    writeText('输出', 1470, y0 + 400, hand(46, 700), C.ink, t, seq(mWo + 1.4, '输出', 0.09), 0.1, 'center');
  }
  if (t >= mTalk - 0.4) {
    const E = sc.ring || (sc.ring = new Sk(2271).penOn());
    if (!sc.ring_b) { E.ellipse(1090, y0 + 400, 168, 122, { w: 4.5, col: COL_A }); sc.ring_b = 1; }
    E.at(t, mTalk - 0.35, 0.6);
    label('头之间唯一的交流', 900, y0 + 590, t, mTalk + 0.3, 44);
  }
  // 实跑接口没变 + 勾
  if (t >= mApi - 0.5) {
    label('实跑：输入 (6, 8) → 输出还是 (6, 8)', 900, y0 + 700, t, mApi, 44);
    const CK = sc.ck || (sc.ck = new Sk(2281).penOn().poly([[1640, y0 + 700], [1692, y0 + 756], [1790, y0 + 636]], { w: 11, col: COL_A }));
    CK.at(t, mApi + 0.9, 0.3);
    label('接口没变', 1400, y0 + 800, t, mApi + 1.3, 42);
  }
});

// ---------------- s12 代价不在参数，在推理的 KV 缓存 ----------------
scene(11, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mCache = MS('s12_缓存', sc.st + 0.5), m96 = MS('s12_96', sc.st + 5), m2x = MS('s12_2倍', sc.st + 6.5),
        mLlama = MS('s12_llama', sc.st + 7.5), m8x = MS('s12_8倍', sc.st + 12), mGqa = MS('s12_GQA', sc.st + 13.5);
  // 每个 token 一列 K、V 小格
  if (t >= mCache - 0.5) {
    const S = sc.kv || (sc.kv = new Sk(2301).penOn());
    if (!sc.kv_b) {
      for (let c = 0; c < 6; c++) for (let r = 0; r < 2; r++) S.rrect(160 + c * 62, y0 + 240 + r * 62, 54, 54, 6, { w: 2.2 });
      sc.kv_b = 1;
    }
    S.at(t, mCache - 0.45, 0.6);
    label('K', 130, y0 + 268, t, mCache + 0.1, 34);
    label('V', 130, y0 + 330, t, mCache + 0.3, 34);
    label('每个 token 的 K、V 都要缓存', 160, y0 + 400, t, mCache + 0.6, 42);
  }
  // MHA 4Q·4KV 与 GQA 4Q·2KV
  if (t >= m96 - 0.6) {
    const MHA = sc.mha || (sc.mha = new Sk(2311).penOn()), GQA = sc.gqa || (sc.gqa = new Sk(2312).penOn());
    if (!sc.mha_b) {
      for (let k = 0; k < 4; k++) { MHA.rrect(700 + k * 70, y0 + 210, 56, 56, 6, { w: 2.6 }); MHA.rrect(700 + k * 70, y0 + 330, 56, 56, 6, { w: 2.6, col: C.gray }); MHA.line(728 + k * 70, y0 + 270, 728 + k * 70, y0 + 326, { w: 2 }); }
      for (let k = 0; k < 4; k++) { GQA.rrect(700 + k * 70, y0 + 480, 56, 56, 6, { w: 2.6 }); }
      for (let k = 0; k < 2; k++) { GQA.rrect(728 + k * 140, y0 + 600, 56, 56, 6, { w: 2.6, col: C.gray }); }
      GQA.line(728, y0 + 540, 728, y0 + 596, { w: 2 }); GQA.line(728, y0 + 540, 868, y0 + 596, { w: 2 }); GQA.line(868, y0 + 540, 868, y0 + 596, { w: 2 });
      GQA.line(938, y0 + 540, 938, y0 + 596, { w: 2 });
      sc.mha_b = 1;
    }
    MHA.at(t, m96 - 0.5, 0.7); GQA.at(t, m96 + 0.3, 0.7);
    writeText('MHA · 4 Q · 4 KV', 620, y0 + 180, hand(40, 700), C.ink, t, seq(m96, 'MHA · 4 Q · 4 KV', 0.06), 0.1);
    writeText('GQA · 4 Q · 2 KV', 620, y0 + 450, hand(40, 700), C.ink, t, seq(m96 + 0.8, 'GQA · 4 Q · 2 KV', 0.06), 0.1);
  }
  if (t >= m2x - 0.3) {
    label('缓存元素 96 → 48', 1150, y0 + 240, t, m96 + 0.5, 44);
    label('÷ 2', 1520, y0 + 320, t, m2x, 50);
  }
  if (t >= mLlama) label('Llama 3 70B：64 Q · 8 KV', 1150, y0 + 480, t, mLlama, 42);
  if (t >= m8x) label('缓存缩小 8 倍', 1150, y0 + 570, t, m8x, 46);
  const stp = sc.stamp || (sc.stamp = makeStamp('GQA', 120, COL_A, 2321, 200));
  drawStamp(stp, 1500, y0 + 720, t, m8x + 0.35, -0.04);
});

// ---------------- s13 回到开头那句话 ----------------
scene(12, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mOne = MS('s13_一张图', sc.st + 0.5), mFour = MS('s13_四步', sc.st + 4), mPar = MS('s13_参数不变', sc.st + 9.5), mNext = MS('s13_位置编码', sc.st + 15);
  // 一个小矩阵 + 一句话
  if (t >= mOne - 0.5) {
    const S = sc.mm || (sc.mm = new Sk(2401).penOn());
    if (!sc.mm_b) { gridSk(S, 190, y0 + 220, 260, 260, 6, 6, { w: 2.2 }); S.ellipse(320, y0 + 350, 168, 168, { w: 4, col: COL_A }); sc.mm_b = 1; }
    S.at(t, mOne - 0.45, 0.7);
    label('一个头 = 一张图 = 一种关系', 190, y0 + 550, t, mOne + 0.4, 42);
  }
  // 四步
  const STEPS = ['拆开', '并行', '拼接', 'W_o 混合'];
  for (let k = 0; k < 4; k++) {
    const x = 760 + k * 280, tk = mFour + k * 0.55;
    if (t < tk - 0.4) continue;
    const S = sc['s' + k] || (sc['s' + k] = new Sk(2411 + k).penOn().rrect(x, y0 + 240, 230, 140, 14, { w: 3.4, col: k === 3 ? COL_A : C.ink }));
    S.at(t, tk, 0.45);
    writeText(STEPS[k], x + 115, y0 + 310, hand(44, 700), k === 3 ? COL_A : C.ink, t, seq(tk + 0.25, STEPS[k], 0.08), 0.1, 'center');
    if (k < 3) { const A = sc['sa' + k] || (sc['sa' + k] = new Sk(2431 + k).penOn()); if (!sc['sa' + k + 'b']) { arrowTo(A, x + 238, y0 + 310, x + 272, y0 + 310, { w: 3 }); sc['sa' + k + 'b'] = 1; } A.at(t, tk + 0.3, 0.22); }
  }
  if (t >= mPar) {
    label('参数不变 · 头数随你调', 760, y0 + 470, t, mPar, 46);
    label('（拆开 → 并行 → 拼接 → W_o 混合）', 760, y0 + 550, t, mPar + 0.5, 36);
  }
  const stp = sc.stamp || (sc.stamp = makeStamp('下一课：位置编码', 96, COL_A, 2441, 200));
  drawStamp(stp, 960, y0 + 800, t, mNext + 0.1, -0.04);
});

// ---------------- 场景入口 ----------------
function drawScenes(t, v) {
  for (const sc of SCENES) {
    if (!seen(v, sc.y0 - 60, sc.y0 + SEC_H + 60)) continue;
    const f = D[sc.i]; if (f) f(sc, t, v);
  }
}
// 镜头：开场看第一场，之后每场一个镜头；卷角/橡皮擦的交界等盖成空白纸再跳（'cut'）
CAM0 = { x: 960, y: SCENES[0].y0 + 430, z: 0.95 };
CAM = [];
SCENES.forEach((sc) => {
  if (sc.i > 0) {
    const cu = FX_CUTS[sc.i - 1], jump = FX_DEFAULT && cu && (cu.kind === 'curl' || cu.kind === 'erase');
    CAM.push(jump ? [cu.t0, cu.tj, 960, sc.y0 + 430, 0.95, 'cut'] : [sc.s.start - 0.2, sc.s.start + 0.5, 960, sc.y0 + 430, 0.95]);
  }
});
