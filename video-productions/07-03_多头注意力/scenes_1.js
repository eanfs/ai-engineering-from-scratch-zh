// ---------------- s01 回顾：从 RNN 到自注意力 ----------------
scene(0, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mRNN = MS('s01_串行', sc.st + 0.5), mState = MS('s01_状态', sc.st + 2), m1024 = MS('s01_1024', sc.st + 4),
        mWait = MS('s01_连续等', sc.st + 6), mPipe = MS('s01_查询', sc.st + 9), mProj = MS('s01_投影', sc.st + 11),
        mScore = MS('s01_打分', sc.st + 13), mScale = MS('s01_缩放', sc.st + 15), mNorm = MS('s01_归一化', sc.st + 17),
        mMerge = MS('s01_汇合', sc.st + 19), mTwo = MS('s01_两个头', sc.st + 20);
  // RNN 链：h1 → h2 → …（逐个出现）
  for (let k = 0; k < 4; k++) {
    const x = 140 + k * 168, tk = mRNN + k * 0.55;
    if (t < tk) continue;
    const S = sc['rnn' + k] || (sc['rnn' + k] = new Sk(1101 + k).penOn().rrect(x, y0 + 196, 128, 92, 16, { w: 3.6 }));
    S.at(t, tk, 0.45);
    writeText('h' + (k + 1), x + 64, y0 + 244, hand(46, 700), C.ink, t, seq(tk + 0.3, 'h' + (k + 1), 0.08), 0.1, 'center');
    if (k < 3) { const A = sc['rA' + k] || (sc['rA' + k] = new Sk(1121 + k).penOn()); if (!sc['rA' + k + 'b']) { arrowTo(A, x + 136, y0 + 242, x + 160, y0 + 242, { w: 3 }); sc['rA' + k + 'b'] = 1; } A.at(t, tk + 0.4, 0.25); }
  }
  // 1024 的账
  if (t >= mState) label('串行深度', 980, y0 + 216, t, mState + 0.1, 44);
  if (t >= m1024) {
    writeText('1024 个位置', 980, y0 + 286, hand(52, 700), C.ink, t, seq(m1024 + 0.05, '1024 个位置', 0.07), 0.1);
    const S2 = sc.wait || (sc.wait = new Sk(1131).penOn()); S2.at(t, mWait, 0.4);
    writeText('→ 连续等 1024 次', 980, y0 + 356, hand(48, 700), COL_A, t, seq(mWait + 0.15, '→ 连续等 1024 次', 0.06), 0.1);
  }
  // 五步流水线
  const names = ['投影', '打分', '缩放', '归一化', '汇合'];
  const tm = [mProj, mScore, mScale, mNorm, mMerge];
  for (let k = 0; k < 5; k++) {
    const x = 130 + k * 178, tk = tm[k];
    if (t < tk - 0.2) continue;
    const S = sc['pp' + k] || (sc['pp' + k] = new Sk(1201 + k).penOn().rrect(x, y0 + 486, 150, 84, 14, { w: 3.2 }));
    S.at(t, tk, 0.4);
    writeText(names[k], x + 75, y0 + 528, hand(42, 700), C.ink, t, seq(tk + 0.22, names[k], 0.09), 0.1, 'center');
    if (k < 4) { const A = sc['pa' + k] || (sc['pa' + k] = new Sk(1211 + k).penOn()); if (!sc['pa' + k + 'b']) { arrowTo(A, x + 158, y0 + 528, x + 174, y0 + 528, { w: 2.8 }); sc['pa' + k + 'b'] = 1; } A.at(t, tk + 0.35, 0.2); }
  }
  label('@流水线：', 130, y0 + 452, t, mPipe, 40);
  // 上一课结尾试了两个头
  if (t >= mTwo) {
    const S = sc.two || (sc.two = new Sk(1241).penOn());
    if (!sc.two_b) { miniMat(S, 1320, y0 + 400, 110, 4, 1, { w: 2 }); miniMat(S, 1450, y0 + 400, 110, 4, 2, { w: 2 }); sc.two_b = 1; }
    S.at(t, mTwo, 0.5);
    writeText('上一课结尾：试了 2 个头', 1240, y0 + 560, hand(44, 700), C.ink, t, seq(mTwo + 0.3, '上一课结尾：试了 2 个头', 0.07), 0.1);
  }
  const stp = sc.stamp || (sc.stamp = makeStamp('为什么要多头？', 96, COL_A, 1251, 200));
  drawStamp(stp, 960, y0 + 790, t, MS('s01_多头', sc.st + 20) + 0.1, -0.05);
});

// ---------------- s02 一句话里，四件事同时在做 ----------------
scene(1, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mEx = MS('s02_例句', sc.st + 0.4), m4 = MS('s02_四件事', sc.st + 4),
        mSub = MS('s02_主谓', sc.st + 5), mRef = MS('s02_指代', sc.st + 7), mChunk = MS('s02_句法分块', sc.st + 9),
        mDisc = MS('s02_语篇关系', sc.st + 11), mAll = MS('s02_一次全答', sc.st + 13);
  const words = ['the', 'cat', 'sat', 'on', 'the', 'mat'];
  const xs = words.map((_, k) => 150 + k * 252);
  for (let k = 0; k < 6; k++) {
    const tk = mEx + k * 0.14;
    if (t < tk - 0.15) continue;
    const S = sc['w' + k] || (sc['w' + k] = new Sk(1301 + k).penOn().rrect(xs[k], y0 + 226, 216, 96, 14, { w: 3.2 }));
    S.at(t, tk, 0.35);
    writeText(words[k], xs[k] + 108, y0 + 276, hand(48, 700), C.ink, t, seq(tk + 0.18, words[k], 0.09), 0.1, 'center');
  }
  // 主谓弧线 cat → sat
  if (t >= mSub) { const S = sc.arc || (sc.arc = new Sk(1331).penOn()); if (!sc.arc_b) { S.curve([[xs[1] + 108, y0 + 216], [xs[1] + 180, y0 + 140], [xs[2] + 40, y0 + 140], [xs[2] + 108, y0 + 216]], { w: 3.4, col: COL_A }); sc.arc_b = 1; } S.at(t, mSub, 0.45); label('主谓', xs[1] + 156, y0 + 128, t, mSub + 0.35, 38); }
  // 指代箭头 the → cat
  if (t >= mRef) { const S = sc.ref || (sc.ref = new Sk(1341).penOn()); if (!sc.ref_b) { S.curve([[xs[0] + 108, y0 + 340], [xs[0] + 120, y0 + 430], [xs[1] + 90, y0 + 430], [xs[1] + 90, y0 + 340]], { w: 3.2, col: COL_B }); sc.ref_b = 1; } S.at(t, mRef, 0.45); label('指代', xs[0] + 60, y0 + 462, t, mRef + 0.3, 38); }
  // 句法分块 on the mat
  if (t >= mChunk) { const S = sc.chunk || (sc.chunk = new Sk(1351).penOn()); if (!sc.chunk_b) { S.curve([[xs[3] + 10, y0 + 350], [xs[3] + 30, y0 + 402], [xs[5] + 190, y0 + 402], [xs[5] + 206, y0 + 350]], { w: 3.2, col: C.ink }); sc.chunk_b = 1; } S.at(t, mChunk, 0.4); label('句法分块', xs[4] - 60, y0 + 440, t, mChunk + 0.3, 38); }
  // 语篇关系（指向上一句）
  if (t >= mDisc) { const S = sc.disc || (sc.disc = new Sk(1361).penOn()); if (!sc.disc_b) { arrowTo(S, xs[0] + 20, y0 + 216, xs[0] - 60, y0 + 150, { w: 3, col: C.ink }); sc.disc_b = 1; } S.at(t, mDisc, 0.35); label('↑ 上一句', xs[0] - 130, y0 + 128, t, mDisc + 0.25, 36); }
  // 四张卡
  const cards = [['主谓', mSub], ['指代', mRef], ['句法分块', mChunk], ['语篇关系', mDisc]];
  for (let k = 0; k < 4; k++) {
    const x = 200 + k * 390, tk = cards[k][1] + 0.45;
    if (t < tk - 0.3) continue;
    const S = sc['c' + k] || (sc['c' + k] = new Sk(1371 + k).penOn().rrect(x, y0 + 556, 330, 168, 18, { w: 3.4 }));
    S.at(t, tk, 0.5);
    writeText(cards[k][0], x + 165, y0 + 640, hand(56, 700), k === 3 ? COL_A : C.ink, t, seq(tk + 0.3, cards[k][0], 0.09), 0.1, 'center');
  }
  if (t >= m4) label('一句话里有四件事', 1450, y0 + 190, t, m4 + 0.1, 44);
  const stp = sc.stamp || (sc.stamp = makeStamp('一次全答', 104, COL_A, 1391, 200));
  drawStamp(stp, 960, y0 + 820, t, mAll + 0.1, -0.04);
});

// ---------------- s03 但一个头，只有一张图 ----------------
scene(2, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mHead = MS('s03_一个头', sc.st + 0.4), mMat = MS('s03_矩阵', sc.st + 2), mSoft = MS('s03_softmax', sc.st + 6),
        mOne = MS('s03_等于1', sc.st + 8), mZero = MS('s03_零和', sc.st + 9), mPress = MS('s03_压低', sc.st + 11);
  // 一个头
  if (t >= mHead - 0.3) {
    const S = sc.hd || (sc.hd = new Sk(1401).penOn());
    if (!sc.hd_b) { S.ellipse(210, y0 + 250, 76, 76, { w: 3.6 }); S.dot(210, y0 + 250, 10, COL_A); sc.hd_b = 1; }
    S.at(t, mHead, 0.45);
    writeText('一个头', 210, y0 + 370, hand(44, 700), C.ink, t, seq(mHead + 0.3, '一个头', 0.09), 0.1, 'center');
  }
  // 6×6 矩阵
  if (t >= mMat - 0.3) {
    const x = 560, y = y0 + 180, sz = 540, S = sc.mtx || (sc.mtx = new Sk(1411).penOn());
    if (!sc.mtx_b) { gridSk(S, x, y, sz, sz, 6, 6, { w: 2.4 }); sc.mtx_b = 1; }
    S.at(t, mMat, 0.75);
    writeText('一张 N × N 注意力矩阵', x + sz / 2, y + sz + 62, hand(46, 700), COL_B, t, seq(mMat + 0.5, '一张 N × N 注意力矩阵', 0.06), 0.1, 'center');
    // 圈出一行（第 5 行）＋ softmax 标注
    if (t >= mSoft - 0.2) {
      const E = sc.row || (sc.row = new Sk(1421).penOn());
      if (!sc.row_b) { E.ellipse(x + sz / 2, y + sz * 4.5 / 6, sz * 0.56, sz / 12 + 8, { w: 3.6, col: COL_A }); sc.row_b = 1; }
      E.at(t, mSoft, 0.6);
      label('每行过 softmax', x + sz + 60, y + sz * 4.5 / 6 - 26, t, mSoft + 0.25, 42);
      if (t >= mOne) label('→ 加起来 = 1', x + sz + 60, y + sz * 4.5 / 6 + 34, t, mOne + 0.15, 42);
    }
  }
  // 四根柱子（示意）
  if (t >= mZero - 0.5) {
    const base = y0 + 760, names = ['主谓', '指代', '句法', '语篇'];
    const hi = [0.32, 0.94, 0.24, 0.20];   // 一根抬高、其余压低
    for (let k = 0; k < 4; k++) {
      const x = 1300 + k * 140, hgt = 300 * hi[k], tk = mZero + k * 0.16;
      if (t < tk - 0.25) continue;
      const S = sc['bar' + k] || (sc['bar' + k] = (() => {
        const s2 = new Sk(1431 + k).penOn();
        s2.fill(rectPts(x + 6, base - hgt + 6, 92, Math.max(6, hgt - 10)), k === 1 ? COL_A : C.gray2, { fade: 40, a: k === 1 ? 0.4 : 0.22 });
        s2.rrect(x, base - hgt, 104, hgt, 10, { w: 3.4, col: k === 1 ? COL_A : C.ink });
        return s2;
      })());
      S.at(t, tk, 0.4);
      writeText(names[k], x + 52, base + 40, hand(38, 700), C.ink, t, seq(tk + 0.2, names[k], 0.09), 0.1, 'center');
    }
    const G = sc.ground || (sc.ground = new Sk(1441).penOn().ground(1280, 1850, base, { w: 3, a: 0.9 }));
    G.at(t, mZero - 0.5, 0.6);
    label('（一行里的分配，示意）', 1300, base + 92, t, mZero + 1.4, 34);
  }
  const stp = sc.stamp || (sc.stamp = makeStamp('零和', 112, COL_A, 1451, 200));
  drawStamp(stp, 320, y0 + 640, t, mZero + 1.1, -0.05);
});

// ---------------- s04 实跑：两张图，真的不一样 ----------------
// 真实权重：课程 main.py 的前向输出（2 头、d_model=8、6 个 token、未训练权重）
const W0 = [[0.147, 0.214, 0.262, 0.154, 0.121, 0.102], [0.113, 0.230, 0.217, 0.156, 0.219, 0.065], [0.125, 0.158, 0.092, 0.132, 0.352, 0.142], [0.103, 0.245, 0.346, 0.154, 0.103, 0.048], [0.132, 0.238, 0.389, 0.112, 0.053, 0.077], [0.177, 0.177, 0.228, 0.161, 0.111, 0.146]];
const W1 = [[0.180, 0.161, 0.136, 0.217, 0.167, 0.139], [0.141, 0.167, 0.109, 0.210, 0.257, 0.116], [0.186, 0.171, 0.141, 0.166, 0.116, 0.219], [0.140, 0.179, 0.143, 0.297, 0.119, 0.121], [0.153, 0.095, 0.153, 0.222, 0.339, 0.039], [0.144, 0.171, 0.209, 0.157, 0.157, 0.163]];
const TOK = ['the', 'cat', 'sat', 'on', 'the', 'mat'];
function heatMat(sc, key, x, y, sz, Wt, t, t0, col) {
  const cw = sz / 6;
  for (let r = 0; r < 6; r++) for (let c = 0; c < 6; c++) {
    const p = P(t, t0 + (r * 6 + c) * 0.006, 0.3);
    if (p <= 0) continue;
    g.save(); g.globalAlpha *= p * Math.min(0.82, Wt[r][c] * 2.2); g.fillStyle = col;
    g.fillRect(x + c * cw + 1.5, y + r * cw + 1.5, cw - 3, cw - 3); g.restore();
  }
}
function matSk(sc, key, x, y, sz, seed) {
  const S = sc[key] || (sc[key] = new Sk(seed).penOn());
  if (!sc[key + '_b']) { gridSk(S, x, y, sz, sz, 6, 6, { w: 2 }); sc[key + '_b'] = 1; }
  return S;
}
scene(3, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mRun = MS('s04_实跑', sc.st + 0.4), mBoth = MS('s04_两张矩阵', sc.st + 2.6), mTheRow = MS('s04_the行', sc.st + 5),
        mP1 = MS('s04_0389', sc.st + 7), mSat = MS('s04_sat', sc.st + 8.5), mP2 = MS('s04_0339', sc.st + 9.5),
        mThe = MS('s04_the', sc.st + 11), mTwo = MS('s04_两张图', sc.st + 12.5);
  const A = { x: 170, y: y0 + 230, sz: 420 }, B2 = { x: 680, y: y0 + 230, sz: 420 }, cw = 420 / 6;
  if (t >= mRun - 0.4) {
    for (const [k, M] of [[0, A], [1, B2]]) {
      const S = matSk(sc, 'm' + k, M.x, M.y, M.sz, 1501 + k * 7);
      S.at(t, mRun + k * 0.25, 0.7);
      writeText('头 ' + k, M.x + M.sz / 2, M.y - 46, hand(48, 700), k === 0 ? COL_A : COL_B, t, seq(mRun + k * 0.25 + 0.3, '头 ' + k, 0.1), 0.1, 'center');
      if (t >= mBoth) for (let j = 0; j < 6; j++) {
        writeText(TOK[j], M.x - 34, M.y + cw * (j + 0.5), hand(30, 700), C.ink, t, seq(mBoth + j * 0.07, TOK[j], 0.05), 0.08, 'center');
        writeText(TOK[j], M.x + cw * (j + 0.5), M.y - 14, hand(30, 700), C.ink, t, seq(mBoth + j * 0.07, TOK[j], 0.05), 0.08, 'center');
      }
    }
    heatMat(sc, 'h0', A.x, A.y, A.sz, W0, t, mRun + 0.4, COL_B);
    heatMat(sc, 'h1', B2.x, B2.y, B2.sz, W1, t, mRun + 0.65, COL_B);
  }
  // 圈出 the 行（第 5 行）
  if (t >= mTheRow - 0.3) {
    const E = sc.er || (sc.er = new Sk(1521).penOn());
    if (!sc.er_b) { E.ellipse(A.x + A.sz / 2, A.y + cw * 4.5, A.sz * 0.56, cw * 0.62, { w: 3.4, col: COL_A }); E.ellipse(B2.x + B2.sz / 2, B2.y + cw * 4.5, B2.sz * 0.56, cw * 0.62, { w: 3.4, col: COL_A }); sc.er_b = 1; }
    E.at(t, mTheRow, 0.6);
  }
  // 两个峰值格 + 标注
  if (t >= mP1 - 0.3) {
    const c1 = sc.c1 || (sc.c1 = new Sk(1531).penOn());
    if (!sc.c1_b) { c1.rrect(A.x + 2 * cw + 2, A.y + 4 * cw + 2, cw - 4, cw - 4, 6, { w: 4, col: COL_A }); sc.c1_b = 1; }
    c1.at(t, mP1, 0.4);
    writeText('0.389 → sat', A.x, y0 + 720, hand(44, 700), COL_A, t, seq(mP1 + 0.25, '0.389 → sat', 0.07), 0.1);
  }
  if (t >= mP2 - 0.3) {
    const c2 = sc.c2 || (sc.c2 = new Sk(1541).penOn());
    if (!sc.c2_b) { c2.rrect(B2.x + 4 * cw + 2, B2.y + 4 * cw + 2, cw - 4, cw - 4, 6, { w: 4, col: COL_A }); sc.c2_b = 1; }
    c2.at(t, mP2, 0.4);
    writeText('0.339 → the', B2.x, y0 + 720, hand(44, 700), COL_A, t, seq(mP2 + 0.25, '0.339 → the', 0.07), 0.1);
  }
  if (t >= mThe) label('同一行输入：', 1230, y0 + 300, t, mThe + 0.05, 44);
  if (t >= mBoth) {
    blockWord('注意力矩阵', 1230, y0 + 400, 46, COL_B, t, seq(mTwo + 0.05, '注意力矩阵', 0.07));
    label('两张不同的图', 1230, y0 + 500, t, mTwo + 0.5, 48);
  }
  label('（格子的深浅 = 实测权重；未训练权重的前向结果）', 170, y0 + 830, t, mBoth + 0.5, 34);
});
