
// ---------------- s05 实跑：反思怎么改写下一轮 ----------------
scene(4, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m1 = MS('s05_第1次', sc.st + 0.5), mR1 = MS('s05_反思1', sc.st + 2),
        m2 = MS('s05_第2次', sc.st + 4.5), m3 = MS('s05_第3次', sc.st + 8),
        mW = MS('s05_权重', sc.st + 10);
  const rows = [
    ['第 1 次', '[1,2,3]', '和 6', '差了 14，要挑更大的值', m1, mR1, false],
    ['第 2 次', '[5,6,7]', '和 18', '还差 2，再调大一点', m2, m2 + 1.2, false],
    ['第 3 次', '[6,7,7]', '和 20', '成功', m3, m3 + 1.2, true],
  ];
  for (let k = 0; k < 3; k++) {
    const [nm, arr, sum, ref, tk, tkr, ok] = rows[k];
    const y = y0 + 220 + k * 180;
    if (t < tk - 0.4) continue;
    const S = sc['row' + k] || (sc['row' + k] = new Sk(4501 + k).penOn().rrect(170, y, 1050, 140, 16, { w: 3.4, col: ok ? COL_A : C.ink }));
    S.at(t, tk, 0.45);
    writeText(nm, 220, y + 70, hand(36, 700), ok ? COL_A : C.ink, t, seq(tk + 0.2, nm, 0.07), 0.1);
    writeText(arr, 500, y + 70, hand(42, 700), C.ink, t, seq(tk + 0.4, arr, 0.06), 0.1, 'center');
    writeText(sum, 800, y + 70, hand(40, 700), ok ? COL_A : C.ink, t, seq(tk + 0.7, sum, 0.06), 0.1, 'center');
    if (ok) { const CK = sc.tick2 || (sc.tick2 = new Sk(4511).penOn().poly([[900, y + 50], [925, y + 80], [965, y + 20]], { w: 9, col: COL_A })); CK.at(t, tk + 1.0, 0.3); }
  }
  // 右侧反思气泡
  if (t >= mR1 - 0.4) {
    const S = sc.rf || (sc.rf = new Sk(4521).penOn().rrect(1280, y0 + 220, 460, 140, 60, { w: 3.4, col: COL_A }));
    S.at(t, mR1 - 0.35, 0.5);
    writeText('反思', 1330, y0 + 268, hand(34, 700), COL_A, t, seq(mR1, '反思', 0.08), 0.1);
    writeText('差了 14，要挑更大的值', 1330, y0 + 322, hand(30, 700), C.ink, t, seq(mR1 + 0.35, '差了 14，要挑更大的值', 0.045), 0.1);
  }
  if (t >= m2 + 1.2) {
    const S = sc.rf2 || (sc.rf2 = new Sk(4531).penOn().rrect(1280, y0 + 400, 460, 140, 60, { w: 3.4, col: COL_A }));
    S.at(t, m2 + 1.2, 0.5);
    writeText('反思', 1330, y0 + 448, hand(34, 700), COL_A, t, seq(m2 + 1.5, '反思', 0.08), 0.1);
    writeText('还差 2，再调大一点', 1330, y0 + 502, hand(30, 700), C.ink, t, seq(m2 + 1.8, '还差 2，再调大一点', 0.045), 0.1);
  }
  if (t >= m3 + 1.2) {
    writeText('权重一个都没动', 1280, y0 + 600, hand(38, 700), C.ink, t, seq(m3 + 1.2, '权重一个都没动', 0.06), 0.1);
  }
  const stp = sc.stamp || (sc.stamp = makeStamp('权重更新 0 次', 88, COL_A, 4541, 200));
  drawStamp(stp, 620, y0 + 820, t, mW + 0.15, -0.04);
});

// ---------------- s06 为什么它能泛化 ----------------
scene(5, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mMed = MS('s06_媒介', sc.st + 0.5), mLetta = MS('s06_letta', sc.st + 4),
        mClaude = MS('s06_claude', sc.st + 5.5), mExt = MS('s06_外化', sc.st + 8);
  // 左上：Letta
  if (t >= mLetta - 0.5) {
    const S = sc.lt || (sc.lt = new Sk(4601).penOn().rrect(170, y0 + 230, 620, 200, 18, { w: 3.4 }));
    S.at(t, mLetta - 0.45, 0.5);
    writeText('Letta', 210, y0 + 300, hand(40, 700), C.ink, t, seq(mLetta, 'Letta', 0.08), 0.1);
    writeText('sleep-time compute', 210, y0 + 372, hand(34, 700), COL_A, t, seq(mLetta + 0.4, 'sleep-time compute', 0.05), 0.1);
  }
  // 右上：Claude Code
  if (t >= mClaude - 0.5) {
    const S = sc.cc || (sc.cc = new Sk(4611).penOn().rrect(1130, y0 + 230, 620, 200, 18, { w: 3.4 }));
    S.at(t, mClaude - 0.45, 0.5);
    writeText('Claude Code', 1170, y0 + 300, hand(40, 700), C.ink, t, seq(mClaude, 'Claude Code', 0.08), 0.1);
    writeText('CLAUDE.md learnings', 1170, y0 + 372, hand(32, 700), COL_A, t, seq(mClaude + 0.4, 'CLAUDE.md learnings', 0.05), 0.1);
  }
  // 中间通道
  if (t >= mMed - 0.4) {
    writeText('自然语言是足够丰富的媒介', 960, y0 + 160, hand(38, 700), C.ink, t, seq(mMed, '自然语言是足够丰富的媒介', 0.05), 0.1, 'center');
    const A = sc.ch || (sc.ch = new Sk(4621).penOn());
    if (!sc.ch_b) { A.line(790, y0 + 330, 1130, y0 + 330, { w: 3.4, col: COL_B }); A.line(960, y0 + 190, 960, y0 + 330, { w: 3, col: COL_B }); sc.ch_b = 1; }
    A.at(t, mMed + 0.4, 0.6);
  }
  // 底部：反思外化
  if (t >= mExt - 0.5) {
    const S = sc.ex || (sc.ex = new Sk(4631).penOn().rrect(400, y0 + 540, 1120, 200, 20, { w: 3.8, col: COL_A }));
    S.at(t, mExt - 0.45, 0.55);
    writeText('反思被外化成可复用的上下文', 960, y0 + 610, hand(42, 700), COL_A, t, seq(mExt, '反思被外化成可复用的上下文', 0.055), 0.1, 'center');
    writeText('于是可持续地改进下一次尝试', 960, y0 + 680, hand(32, 700), C.ink, t, seq(mExt + 0.7, '于是可持续地改进下一次尝试', 0.05), 0.1, 'center');
  }
});

// ---------------- s07 什么时候它没有用 ----------------
scene(6, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mFirst = MS('s07_第一次', sc.st + 0.5), mExt = MS('s07_外部', sc.st + 2),
        mSup = MS('s07_迷信', sc.st + 5), mStd = MS('s07_标准', sc.st + 8);
  // 两张「帮不上忙」
  const no = [['第一次就成功', '没有失败信号可学', 170, mFirst], ['失败来自外部', '网络挂了、工具坏了', 690, mExt]];
  for (let k = 0; k < 2; k++) {
    const [nm, sub, x, tk] = no[k];
    if (t < tk - 0.4) continue;
    const S = sc['n' + k] || (sc['n' + k] = new Sk(4701 + k).penOn().rrect(x, y0 + 230, 480, 220, 18, { w: 3.4, col: C.gray }));
    S.at(t, tk, 0.5);
    writeText(nm, x + 240, y0 + 310, hand(40, 700), C.ink, t, seq(tk + 0.25, nm, 0.07), 0.1, 'center');
    writeText(sub, x + 240, y0 + 390, hand(30, 700), C.gray, t, seq(tk + 0.65, sub, 0.05), 0.1, 'center');
  }
  // 警告卡
  if (t >= mSup - 0.5) {
    const S = sc.warn || (sc.warn = new Sk(4711).penOn().rrect(1210, y0 + 230, 540, 220, 18, { w: 3.8, col: COL_A }));
    S.at(t, mSup - 0.45, 0.5);
    writeText('最危险：反思变成迷信', 1480, y0 + 310, hand(38, 700), COL_A, t, seq(mSup, '最危险：反思变成迷信', 0.06), 0.1, 'center');
    writeText('为一次偶发的不稳定运行存一套叙事', 1480, y0 + 390, hand(28, 700), C.ink, t, seq(mSup + 0.6, '为一次偶发的不稳定运行存一套叙事', 0.045), 0.1, 'center');
  }
  // 三条判断标准
  if (t >= mStd - 0.5) {
    const S = sc.std || (sc.std = new Sk(4721).penOn().rrect(170, y0 + 530, 1580, 240, 18, { w: 3.6, col: COL_B }));
    S.at(t, mStd - 0.45, 0.5);
    writeText('判断标准', 220, y0 + 600, hand(38, 700), COL_B, t, seq(mStd, '判断标准', 0.08), 0.1);
    writeText('清晰的失败信号　·　可复现的任务类别　·　够用的动作预算', 960, y0 + 690, hand(32, 700), C.ink, t, seq(mStd + 0.4, '清晰的失败信号', 0.03), 0.1, 'center');
  }
});

// ---------------- s08 2026 年的坑：记忆腐烂 ----------------
scene(7, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mPile = MS('s08_攒', sc.st + 0.5), mSlow = MS('s08_变慢', sc.st + 2.5),
        mPress = MS('s08_压实', sc.st + 5), mBound = MS('s08_有界', sc.st + 8);
  // 左：缓冲区越堆越多
  if (t >= mPile - 0.5) {
    const S = sc.buf || (sc.buf = new Sk(4801).penOn());
    if (!sc.buf_b) { S.rrect(170, y0 + 240, 560, 340, 18, { w: 3.6 }); sc.buf_b = 1; }
    S.at(t, mPile - 0.45, 0.5);
    for (let k = 0; k < 6; k++) {
      const x = 210 + (k % 2) * 270, y = y0 + 290 + Math.floor(k / 2) * 90, tk = mPile + k * 0.18;
      if (t < tk) continue;
      const B = sc['bb' + k] || (sc['bb' + k] = new Sk(4811 + k).penOn().rrect(x, y, 240, 70, 10, { w: 2.6, col: k > 4 ? C.gray2 : C.ink }));
      B.at(t, tk, 0.35);
    }
    writeText('反思越攒越多', 450, y0 + 620, hand(36, 700), C.ink, t, seq(mPile + 1.6, '反思越攒越多', 0.06), 0.1, 'center');
    if (t >= mSlow) { const X = sc.old || (sc.old = new Sk(4841).penOn()); if (!sc.old_b) { X.line(240, y0 + 320, 480, y0 + 560, { w: 5, col: COL_A, a: 0.5 }); sc.old_b = 1; } X.at(t, mSlow, 0.4);
      writeText('有些已过时甚至错误', 450, y0 + 668, hand(30, 700), COL_A, t, seq(mSlow + 0.3, '有些已过时甚至错误', 0.05), 0.1, 'center'); }
  }
  // 右：三种缓解
  if (t >= mPress - 0.5) {
    const items = ['周期性压实', '给反思加生存时间', '交给独立的清理 agent'];
    for (let k = 0; k < 3; k++) {
      const tk = mPress + k * 0.7, y = y0 + 270 + k * 130;
      if (t < tk - 0.3) continue;
      const S = sc['ms' + k] || (sc['ms' + k] = new Sk(4851 + k).penOn().rrect(830, y, 900, 110, 14, { w: 3.2, col: COL_A }));
      S.at(t, tk, 0.45);
      writeText(items[k], 900, y + 56, hand(36, 700), C.ink, t, seq(tk + 0.2, items[k], 0.06), 0.1);
    }
    label('缓解办法', 830, y0 + 220, t, mPress, 38);
  }
  // 底部：有界列表
  if (t >= mBound - 0.5) {
    const S = sc.cap || (sc.cap = new Sk(4861).penOn().rrect(170, y0 + 720, 1560, 130, 16, { w: 3.4, col: COL_B }));
    S.at(t, mBound - 0.45, 0.5);
    writeText('实跑里的情景缓冲区是有界列表：装满了就淘汰最老的条目', 950, y0 + 785, hand(34, 700), COL_B, t, seq(mBound + 0.3, '实跑里的情景缓冲区是有界列表', 0.05), 0.1, 'center');
  }
});

// ---------------- s09 一屏总览：Reflexion ----------------
scene(8, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mFour = MS('s09_四步', sc.st + 0.5), mNo = MS('s09_无梯度', sc.st + 5), mProd = MS('s09_生产', sc.st + 8);
  // 四步环
  const steps = [['失败', 220, mFour], ['评估', 620, mFour + 0.8], ['反思', 1020, mFour + 1.6], ['情景记忆', 1420, mFour + 2.4]];
  for (let k = 0; k < 4; k++) {
    const [nm, x, tk] = steps[k];
    if (t < tk - 0.4) continue;
    const S = sc['s' + k] || (sc['s' + k] = new Sk(4901 + k).penOn().rrect(x, y0 + 230, 320, 150, 16, { w: 3.6, col: k === 2 ? COL_A : C.ink }));
    S.at(t, tk, 0.45);
    writeText(nm, x + 160, y0 + 305, hand(42, 700), k === 2 ? COL_A : C.ink, t, seq(tk + 0.25, nm, 0.08), 0.1, 'center');
    if (k < 3) { const A = sc['sa' + k] || (sc['sa' + k] = new Sk(4911 + k).penOn()); if (!sc['sa' + k + 'b']) { arrowTo(A, x + 328, y0 + 305, x + 392, y0 + 305, { w: 3.2 }); sc['sa' + k + 'b'] = 1; } A.at(t, tk + 0.5, 0.25); }
  }
  // 回流：情景记忆 → 失败（重试）
  if (t >= mFour + 2.6) {
    const A = sc.loop2 || (sc.loop2 = new Sk(4921).penOn());
    if (!sc.loop2_b) { A.curve([[1580, y0 + 400], [1650, y0 + 640], [960, y0 + 700], [300, y0 + 640], [380, y0 + 404]], { w: 3.8, col: COL_A }); sc.loop2_b = 1; }
    A.at(t, mFour + 2.6, 0.6);
    writeText('下一次带着它重试', 960, y0 + 660, hand(36, 700), COL_A, t, seq(mFour + 3.0, '下一次带着它重试', 0.06), 0.1, 'center');
  }
  if (t >= mNo) {
    writeText('没有梯度', 620, y0 + 520, hand(42, 700), C.ink, t, seq(mNo, '没有梯度', 0.07), 0.1);
    if (t >= mNo + 0.8) writeText('没有权重更新', 1000, y0 + 520, hand(42, 700), C.ink, t, seq(mNo + 0.8, '没有权重更新', 0.07), 0.1);
    if (t >= mNo + 1.6) writeText('只有一段自然语言在试验之间流动', 620, y0 + 590, hand(34, 700), COL_A, t, seq(mNo + 1.6, '只有一段自然语言在试验之间流动', 0.045), 0.1);
  }
  if (t >= mProd) writeText('配合验证器与记忆压实，这个模式就能进生产', 960, y0 + 810, hand(38, 700), C.ink, t, seq(mProd, '配合验证器与记忆压实', 0.05), 0.1, 'center');
});

// ---------------- 场景入口 ----------------
function drawScenes(t, v) {
  for (const sc of SCENES) {
    if (!seen(v, sc.y0 - 60, sc.y0 + SEC_H + 60)) continue;
    const f = D[sc.i]; if (f) f(sc, t, v);
  }
}
CAM0 = { x: 960, y: SCENES[0].y0 + 430, z: 0.95 };
CAM = [];
SCENES.forEach((sc) => {
  if (sc.i > 0) {
    const cu = FX_CUTS[sc.i - 1], jump = FX_DEFAULT && cu && (cu.kind === 'curl' || cu.kind === 'erase');
    CAM.push(jump ? [cu.t0, cu.tj, 960, sc.y0 + 430, 0.95, 'cut'] : [sc.s.start - 0.2, sc.s.start + 0.5, 960, sc.y0 + 430, 0.95]);
  }
});
