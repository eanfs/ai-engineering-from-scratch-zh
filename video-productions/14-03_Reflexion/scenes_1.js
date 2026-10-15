
// ---------------- s01 同一句话，第三次才成功 ----------------
scene(0, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mBase = MS('s01_基线', sc.st + 0.5), m14 = MS('s01_差14', sc.st + 2.5),
        mMem = MS('s01_记忆', sc.st + 5), m3rd = MS('s01_第3次', sc.st + 8),
        mRef = MS('s01_反思', sc.st + 11.5);
  // 上排：基线四次都是 [1,2,3] = 6
  if (t >= mBase - 0.5) {
    label('基线：连试四次', 150, y0 + 190, t, mBase, 40);
    for (let k = 0; k < 4; k++) {
      const x = 150 + k * 250, tk = mBase + k * 0.45;
      if (t < tk - 0.3) continue;
      const S = sc['b' + k] || (sc['b' + k] = new Sk(4101 + k).penOn().rrect(x, y0 + 230, 220, 130, 14, { w: 3.2, col: C.gray }));
      S.at(t, tk, 0.4);
      writeText('[1,2,3]', x + 110, y0 + 282, hand(36, 700), C.gray, t, seq(tk + 0.2, '[1,2,3]', 0.06), 0.1, 'center');
      writeText('= 6', x + 110, y0 + 332, hand(36, 700), C.gray, t, seq(tk + 0.45, '= 6', 0.08), 0.1, 'center');
      const X = sc['bx' + k] || (sc['bx' + k] = new Sk(4121 + k).penOn());
      if (!sc['bx' + k + 'b']) { X.line(x + 20, y0 + 240, x + 200, y0 + 350, { w: 5, col: C.gray2 }); X.line(x + 200, y0 + 240, x + 20, y0 + 350, { w: 5, col: C.gray2 }); sc['bx' + k + 'b'] = 1; }
      X.at(t, tk + 0.5, 0.25);
    }
    if (t >= m14) writeText('离目标 20 差 14 —— 它从不改变', 150, y0 + 400, hand(34, 700), C.gray, t, seq(m14, '离目标 20 差 14', 0.05), 0.1);
  }
  // 下排：打开情景记忆之后
  if (t >= mMem - 0.5) {
    label('打开情景记忆之后', 150, y0 + 470, t, mMem, 40);
    const rows = [['第 1 次', '[1,2,3]', '6', mMem + 0.6, false], ['第 2 次', '[5,6,7]', '18', mMem + 2.0, false], ['第 3 次', '[6,7,7]', '20', m3rd, true]];
    for (let k = 0; k < 3; k++) {
      const [nm, arr, sum, tk, ok] = rows[k];
      const x = 150 + k * 400;
      if (t < tk - 0.4) continue;
      const S = sc['r' + k] || (sc['r' + k] = new Sk(4141 + k).penOn().rrect(x, y0 + 520, 360, 170, 16, { w: 3.6, col: ok ? COL_A : C.ink }));
      S.at(t, tk, 0.45);
      writeText(nm, x + 30, y0 + 560, hand(32, 700), ok ? COL_A : C.ink, t, seq(tk + 0.15, nm, 0.07), 0.1);
      writeText(arr, x + 180, y0 + 615, hand(40, 700), C.ink, t, seq(tk + 0.35, arr, 0.06), 0.1, 'center');
      writeText('和 ' + sum, x + 180, y0 + 665, hand(36, 700), ok ? COL_A : C.ink, t, seq(tk + 0.6, '和 ' + sum, 0.06), 0.1, 'center');
      if (ok) { const CK = sc.tick || (sc.tick = new Sk(4151).penOn().poly([[x + 300, y0 + 560], [x + 322, y0 + 588], [x + 356, y0 + 530]], { w: 9, col: COL_A })); CK.at(t, tk + 0.9, 0.3); }
    }
    if (t >= mRef) writeText('唯一的区别：失败之后，多存了一句自然语言反思', 960, y0 + 790, hand(40, 700), COL_A, t, seq(mRef, '唯一的区别：多存了一句自然语言反思', 0.05), 0.1, 'center');
  }
});

// ---------------- s02 标量强化学习的账单 ----------------
scene(1, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mTrials = MS('s02_上千次', sc.st + 0.5), mGrad = MS('s02_梯度', sc.st + 2.5), mBud = MS('s02_预算', sc.st + 5.5),
        mThink = MS('s02_想一想', sc.st + 8.5);
  // 左：账单纸
  if (t >= mTrials - 0.6) {
    const P = sc.paper || (sc.paper = new Sk(4201).penOn());
    if (!sc.paper_b) { P.fill(rectPts(180, y0 + 220, 560, 400), C.white, { fade: 1 }); P.rrect(180, y0 + 220, 560, 400, 18, { w: 3.6 }); sc.paper_b = 1; }
    P.at(t, mTrials - 0.5, 0.5);
    writeText('标准强化学习的账单', 460, y0 + 285, hand(40, 700), C.ink, t, seq(mTrials, '标准强化学习的账单', 0.06), 0.1, 'center');
    writeText('上千次试验', 240, y0 + 380, hand(38, 700), C.ink, t, seq(mTrials + 0.5, '上千次试验', 0.07), 0.1);
    if (t >= mGrad) writeText('算梯度、更新权重', 240, y0 + 460, hand(38, 700), C.ink, t, seq(mGrad, '算梯度、更新权重', 0.07), 0.1);
    if (t >= mGrad) writeText('（每修一个失败模式）', 240, y0 + 530, hand(30, 700), C.gray, t, seq(mGrad + 0.4, '每修一个失败模式', 0.05), 0.1);
  }
  // 中间分叉
  if (t >= mBud - 0.5) {
    const A = sc.ar || (sc.ar = new Sk(4211).penOn());
    if (!sc.ar_b) { arrowTo(A, 760, y0 + 420, 1000, y0 + 420, { w: 3.6, col: COL_A }); sc.ar_b = 1; }
    A.at(t, mBud - 0.45, 0.4);
    writeText('生产环境没有这份预算', 800, y0 + 360, hand(32, 700), C.gray, t, seq(mBud, '生产环境没有这份预算', 0.05), 0.1);
  }
  // 右：替代方案
  if (t >= mThink - 0.6) {
    const S = sc.alt || (sc.alt = new Sk(4221).penOn().rrect(1050, y0 + 300, 680, 240, 20, { w: 3.8, col: COL_A }));
    S.at(t, mThink - 0.5, 0.55);
    writeText('Reflexion', 1120, y0 + 372, hand(44, 700), COL_A, t, seq(mThink - 0.2, 'Reflexion', 0.08), 0.1);
    writeText('要是 agent 只是想一想', 1120, y0 + 448, hand(34, 700), C.ink, t, seq(mThink + 0.2, '要是 agent 只是想一想', 0.05), 0.1);
    writeText('为什么失败，再试一次呢？', 1120, y0 + 500, hand(34, 700), C.ink, t, seq(mThink + 0.7, '为什么失败，再试一次呢', 0.05), 0.1);
  }
});

// ---------------- s03 三个组件加一个缓冲区 ----------------
scene(2, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mActor = MS('s03_actor', sc.st + 0.5), mEval = MS('s03_eval', sc.st + 1.8),
        mRef = MS('s03_reflect', sc.st + 4), mMem = MS('s03_记忆', sc.st + 7), mPre = MS('s03_前置', sc.st + 9);
  const comp = [['Actor', '按 ReAct 产出轨迹', 160, mActor], ['Evaluator', '给轨迹打分', 700, mEval], ['Self-Reflector', '写自然语言反思', 1240, mRef]];
  for (let k = 0; k < 3; k++) {
    const [nm, sub, x, tk] = comp[k];
    if (t < tk - 0.4) continue;
    const S = sc['c' + k] || (sc['c' + k] = new Sk(4301 + k).penOn().rrect(x, y0 + 220, 460, 160, 18, { w: 3.6, col: k === 2 ? COL_A : C.ink }));
    S.at(t, tk, 0.5);
    writeText(nm, x + 230, y0 + 285, hand(44, 700), k === 2 ? COL_A : C.ink, t, seq(tk + 0.25, nm, 0.07), 0.1, 'center');
    writeText(sub, x + 230, y0 + 345, hand(30, 700), C.ink, t, seq(tk + 0.65, sub, 0.05), 0.1, 'center');
    if (k < 2) { const A = sc['a' + k] || (sc['a' + k] = new Sk(4311 + k).penOn()); if (!sc['a' + k + 'b']) { arrowTo(A, x + 468, y0 + 300, x + 532, y0 + 300, { w: 3.2 }); sc['a' + k + 'b'] = 1; } A.at(t, tk + 0.5, 0.28); }
  }
  // 情景记忆缓冲区
  if (t >= mMem - 0.6) {
    const S = sc.mem || (sc.mem = new Sk(4321).penOn().rrect(430, y0 + 500, 1060, 200, 18, { w: 3.8, col: COL_B }));
    S.at(t, mMem - 0.5, 0.55);
    writeText('情景记忆（缓冲区）', 960, y0 + 560, hand(42, 700), COL_B, t, seq(mMem, '情景记忆', 0.07), 0.1, 'center');
    for (let k = 0; k < 4; k++) {
      const tk = mMem + 0.5 + k * 0.2;
      if (t < tk) continue;
      const B = sc['mb' + k] || (sc['mb' + k] = new Sk(4331 + k).penOn().rrect(500 + k * 240, y0 + 600, 200, 70, 10, { w: 2.6, col: C.gray2 }));
      B.at(t, tk, 0.35);
    }
  }
  if (t >= mPre - 0.5) {
    const A = sc.pre || (sc.pre = new Sk(4341).penOn());
    if (!sc.pre_b) { A.curve([[1500, y0 + 420], [1560, y0 + 640], [960, y0 + 740], [380, y0 + 640], [380, y0 + 400]], { w: 3.6, col: COL_A }); sc.pre_b = 1; }
    A.at(t, mPre - 0.45, 0.6);
    writeText('反思被前置到下一次试验的提示里', 960, y0 + 800, hand(40, 700), COL_A, t, seq(mPre + 0.2, '反思被前置到下一次试验的提示里', 0.05), 0.1, 'center');
  }
});

// ---------------- s04 三种评估器 ----------------
scene(3, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mS = MS('s04_标量', sc.st + 0.5), mH = MS('s04_启发', sc.st + 3.2), mE = MS('s04_自评', sc.st + 6.2);
  const cards = [['标量评估器', '外部二值信号：测试通过或失败', '最简单也最强', 170, mS, C.ink],
                 ['启发式评估器', '预定义的失败特征', '连续两次同一动作 → 卡住', 690, mH, C.ink],
                 ['自评评估器', '让模型给自己的轨迹打分', '没有标准答案时才用', 1210, mE, COL_A]];
  for (let k = 0; k < 3; k++) {
    const [nm, l1, l2, x, tk, col] = cards[k];
    if (t < tk - 0.4) continue;
    const S = sc['e' + k] || (sc['e' + k] = new Sk(4401 + k).penOn().rrect(x, y0 + 250, 500, 300, 18, { w: 3.6, col }));
    S.at(t, tk, 0.5);
    writeText(nm, x + 250, y0 + 330, hand(42, 700), col, t, seq(tk + 0.25, nm, 0.07), 0.1, 'center');
    writeText(l1, x + 250, y0 + 420, hand(30, 700), C.ink, t, seq(tk + 0.7, l1, 0.045), 0.1, 'center');
    writeText(l2, x + 250, y0 + 480, hand(30, 700), C.gray, t, seq(tk + 1.1, l2, 0.045), 0.1, 'center');
  }
  // 小图示
  if (t >= mS + 1.6) { const X = sc.g1 || (sc.g1 = new Sk(4411).penOn()); if (!sc.g1_b) { X.poly([[250, y0 + 360], [272, y0 + 388], [312, y0 + 330]], { w: 8, col: COL_A }); X.line(360, y0 + 350, 400, y0 + 380, { w: 5, col: C.gray2 }); sc.g1_b = 1; } X.at(t, mS + 1.6, 0.3); }
  if (t >= mH + 1.6) { const X = sc.g2 || (sc.g2 = new Sk(4412).penOn()); if (!sc.g2_b) { for (let j = 0; j < 2; j++) X.rrect(780 + j * 70, y0 + 340, 56, 56, 6, { w: 2.6 }); X.line(860, y0 + 368, 940, y0 + 368, { w: 5, col: COL_A }); sc.g2_b = 1; } X.at(t, mH + 1.6, 0.4); }
  if (t >= mE + 1.6) { const X = sc.g3 || (sc.g3 = new Sk(4413).penOn()); if (!sc.g3_b) { X.ellipse(1460, y0 + 368, 46, 46, { w: 3.2, col: COL_A }); X.line(1440, y0 + 368, 1460, y0 + 388, { w: 4, col: COL_A }); sc.g3_b = 1; } X.at(t, mE + 1.6, 0.4); }
});
