
// ---------------- s06 工具是循环的手 ----------------
scene(5, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mName = MS('s06_名称参数', sc.st + 0.5), mReg = MS('s06_注册表', sc.st + 2.5),
        mCalc = MS('s06_计算器', sc.st + 5.5), mStore = MS('s06_存储', sc.st + 7.5),
        mErr = MS('s06_错误', sc.st + 9.5), mPre = MS('s06_预设', sc.st + 12);
  // 注册表
  if (t >= mName - 0.5) {
    const S = sc.reg || (sc.reg = new Sk(3601).penOn().rrect(170, y0 + 220, 560, 320, 18, { w: 3.8 }));
    S.at(t, mName - 0.45, 0.5);
    writeText('工具注册表', 220, y0 + 282, hand(44, 700), C.ink, t, seq(mName + 0.2, '工具注册表', 0.08), 0.1);
    if (t >= mReg) {
      writeText('calculate  →  calc()', 220, y0 + 380, hand(34, 700), C.ink, t, seq(mReg, 'calculate', 0.06), 0.1);
      writeText('kv.set     →  store()', 220, y0 + 450, hand(34, 700), C.ink, t, seq(mReg + 0.5, 'kv.set', 0.06), 0.1);
      writeText('名称 + 参数，模型只写名字', 220, y0 + 510, hand(28, 700), C.gray, t, seq(mReg + 1.0, '名称 + 参数', 0.05), 0.1);
    }
  }
  // 两条调用箭头 + 结果
  if (t >= mCalc - 0.5) {
    const A = sc.ar1 || (sc.ar1 = new Sk(3611).penOn());
    if (!sc.ar1_b) { arrowTo(A, 740, y0 + 300, 950, y0 + 300, { w: 3.4 }); sc.ar1_b = 1; }
    A.at(t, mCalc - 0.45, 0.4);
    const R = sc.r1 || (sc.r1 = new Sk(3612).penOn().rrect(970, y0 + 240, 320, 120, 14, { w: 3.4, col: COL_A }));
    R.at(t, mCalc - 0.1, 0.45);
    writeText('计算器 → 18', 1130, y0 + 300, hand(38, 700), COL_A, t, seq(mCalc + 0.2, '计算器 → 18', 0.06), 0.1, 'center');
    label('工具调用 = 名称 + 参数', 800, y0 + 180, t, mName + 0.5, 34);
  }
  if (t >= mStore - 0.5) {
    const A = sc.ar2 || (sc.ar2 = new Sk(3621).penOn());
    if (!sc.ar2_b) { arrowTo(A, 740, y0 + 420, 950, y0 + 420, { w: 3.4 }); sc.ar2_b = 1; }
    A.at(t, mStore - 0.45, 0.4);
    const R = sc.r2 || (sc.r2 = new Sk(3622).penOn().rrect(970, y0 + 360, 320, 120, 14, { w: 3.4 }));
    R.at(t, mStore - 0.1, 0.45);
    writeText('键值存储 → OK', 1130, y0 + 420, hand(38, 700), C.ink, t, seq(mStore + 0.2, '键值存储 → OK', 0.06), 0.1, 'center');
  }
  if (t >= mErr - 0.5) {
    const A = sc.ar3 || (sc.ar3 = new Sk(3631).penOn());
    if (!sc.ar3_b) { A.poly([[740, y0 + 500], [850, y0 + 560], [950, y0 + 560]], { w: 3.4, col: C.gray }); sc.ar3_b = 1; }
    A.at(t, mErr - 0.45, 0.5);
    const R = sc.r3 || (sc.r3 = new Sk(3632).penOn().rrect(970, y0 + 500, 320, 120, 14, { w: 3.4, col: C.gray }));
    R.at(t, mErr - 0.1, 0.45);
    writeText('错误字符串写回历史', 1130, y0 + 560, hand(32, 700), C.gray, t, seq(mErr + 0.2, '错误字符串写回历史', 0.05), 0.1, 'center');
  }
  if (t >= mPre) writeText('演示程序依靠预设脚本继续运行，并没有自主纠错能力', 620, y0 + 780, hand(36, 700), C.gray, t, seq(mPre, '演示程序依靠预设脚本', 0.05), 0.1, 'center');
});

// ---------------- s07 为什么这个循环无处不在 ----------------
scene(6, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mChk = MS('s07_检查点', sc.st + 0.5), mRole = MS('s07_角色', sc.st + 2), mTrace = MS('s07_追踪', sc.st + 3.5),
        mRestore = MS('s07_恢复', sc.st + 6), mDispatch = MS('s07_分派', sc.st + 8), mLog = MS('s07_记录', sc.st + 10),
        mMin = MS('s07_最小', sc.st + 12);
  // 中心：工具循环
  if (t >= mChk - 0.8) {
    const S = sc.core || (sc.core = new Sk(3701).penOn());
    if (!sc.core_b) {
      S.rrect(200, y0 + 320, 420, 200, 20, { w: 3.8 });
      S.ellipse(410, y0 + 420, 150, 62, { w: 3.2, col: COL_A });
      sc.core_b = 1;
    }
    S.at(t, mChk - 0.7, 0.6);
    writeText('工具循环', 410, y0 + 420, hand(46, 700), COL_A, t, seq(mChk + 0.2, '工具循环', 0.08), 0.1, 'center');
    writeText('最小可运行单元', 410, y0 + 570, hand(32, 700), C.gray, t, seq(mChk + 0.6, '最小可运行单元', 0.05), 0.1, 'center');
  }
  // 三个外围能力
  const caps = [['保存检查点', mChk], ['角色分工', mRole], ['运行追踪', mTrace]];
  for (let k = 0; k < 3; k++) {
    const x = 900, y = y0 + 200 + k * 180, tk = caps[k][1];
    if (t < tk - 0.35) continue;
    const S = sc['cp' + k] || (sc['cp' + k] = new Sk(3711 + k).penOn().rrect(x, y, 400, 140, 16, { w: 3.4 }));
    S.at(t, tk, 0.45);
    writeText(caps[k][0], x + 200, y + 70, hand(42, 700), C.ink, t, seq(tk + 0.25, caps[k][0], 0.08), 0.1, 'center');
    const A = sc['ca' + k] || (sc['ca' + k] = new Sk(3721 + k).penOn());
    if (!sc['ca' + k + 'b']) { A.dash(630, k === 0 ? y0 + 380 : k === 1 ? y0 + 420 : y0 + 460, x - 10, y + 70, { w: 2.6, d: 18, gp: 12 }); sc['ca' + k + 'b'] = 1; }
    A.at(t, tk + 0.2, 0.5);
  }
  // 三个检查问题
  if (t >= mRestore - 0.4) {
    const S = sc.qs || (sc.qs = new Sk(3741).penOn().rrect(1450, y0 + 240, 350, 420, 18, { w: 3.4, col: COL_A }));
    S.at(t, mRestore - 0.35, 0.5);
    writeText('选框架先问', 1625, y0 + 300, hand(38, 700), COL_A, t, seq(mRestore, '选框架先问', 0.08), 0.1, 'center');
    if (t >= mDispatch) writeText('状态如何恢复', 1625, y0 + 400, hand(32, 700), C.ink, t, seq(mDispatch, '状态如何恢复', 0.06), 0.1, 'center');
    if (t >= mLog) writeText('工具如何分派', 1625, y0 + 490, hand(32, 700), C.ink, t, seq(mLog, '工具如何分派', 0.06), 0.1, 'center');
    if (t >= mLog + 1.2) writeText('执行如何记录', 1625, y0 + 580, hand(32, 700), C.ink, t, seq(mLog + 1.2, '执行如何记录', 0.06), 0.1, 'center');
  }
  if (t >= mMin) writeText('先把最小循环跑通，再增加需要的外围能力', 700, y0 + 740, hand(40, 700), COL_A, t, seq(mMin, '先把最小循环跑通', 0.05), 0.1, 'center');
});

// ---------------- s08 三个具体的坑 ----------------
scene(7, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mOut = MS('s08_外部数据', sc.st + 0.5), mAuth = MS('s08_授权', sc.st + 2), mBound = MS('s08_边界', sc.st + 4),
        mErr = MS('s08_错误', sc.st + 6), mVerify = MS('s08_核验', sc.st + 8),
        mBud = MS('s08_预算', sc.st + 10), mRound = MS('s08_轮数', sc.st + 11.5), mFake = MS('s08_伪造', sc.st + 13);
  const cards = [
    ['01 信任边界', '工具结果里的新指令 ≠ 用户授权', mOut, C.ink],
    ['02 错误 ≠ 成功', '要核验结果，再决定恢复或退出', mErr, C.ink],
    ['03 预算耗尽', '最大轮数改成二，明确返回耗尽', mBud, COL_A],
  ];
  for (let k = 0; k < 3; k++) {
    const x = 150 + k * 570, tk = cards[k][2];
    if (t < tk - 0.4) continue;
    const S = sc['cd' + k] || (sc['cd' + k] = new Sk(3801 + k).penOn().rrect(x, y0 + 230, 520, 340, 18, { w: 3.6, col: cards[k][3] }));
    S.at(t, tk, 0.5);
    writeText(cards[k][0], x + 260, y0 + 320, hand(42, 700), cards[k][3], t, seq(tk + 0.25, cards[k][0], 0.06), 0.1, 'center');
    writeText(cards[k][1], x + 260, y0 + 420, hand(30, 700), C.ink, t, seq(tk + 0.7, cards[k][1], 0.04), 0.1, 'center');
  }
  // 各自的小图示
  if (t >= mBound) { const X = sc.x1 || (sc.x1 = new Sk(3811).penOn()); if (!sc.x1_b) { X.rect(300, y0 + 460, 220, 60, { w: 2.6, col: C.gray }); X.line(300, y0 + 460, 520, y0 + 520, { w: 5, col: COL_A }); sc.x1_b = 1; } X.at(t, mBound, 0.4); }
  if (t >= mVerify) { const X = sc.x2 || (sc.x2 = new Sk(3812).penOn()); if (!sc.x2_b) { X.poly([[920, y0 + 490], [960, y0 + 530], [1020, y0 + 450]], { w: 8, col: COL_A }); sc.x2_b = 1; } X.at(t, mVerify, 0.35); }
  if (t >= mRound) {
    const X = sc.x3 || (sc.x3 = new Sk(3813).penOn());
    if (!sc.x3_b) { for (let j = 0; j < 2; j++) X.rrect(1500 + j * 70, y0 + 470, 56, 56, 6, { w: 2.6, col: COL_A }); X.rrect(1640, y0 + 470, 56, 56, 6, { w: 2.6, col: C.gray }); sc.x3_b = 1; }
    X.at(t, mRound, 0.45);
  }
  if (t >= mFake) writeText('预算耗尽就明确返回，不伪造最终答案', 960, y0 + 700, hand(42, 700), COL_A, t, seq(mFake, '预算耗尽就明确返回', 0.05), 0.1, 'center');
});

// ---------------- s09 一屏总览：一个 Agent 循环 ----------------
scene(8, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mGoal = MS('s09_目标', sc.st + 0.5), mDec = MS('s09_决策', sc.st + 2), mBack = MS('s09_回流', sc.st + 3.5),
        mFive = MS('s09_五次', sc.st + 6), m138 = MS('s09_138', sc.st + 8.5),
        mOut = MS('s09_耗尽', sc.st + 10), mRun = MS('s09_运行', sc.st + 12.5);
  // 上排：用户目标 → 历史 → 决策
  const top = [['用户目标', 180, mGoal], ['消息历史', 620, mGoal + 0.9], ['决策器', 1060, mDec]];
  for (let k = 0; k < 3; k++) {
    const [nm, x, tk] = top[k];
    if (t < tk - 0.4) continue;
    const S = sc['t' + k] || (sc['t' + k] = new Sk(3901 + k).penOn().rrect(x, y0 + 210, 360, 130, 16, { w: 3.4 }));
    S.at(t, tk, 0.45);
    writeText(nm, x + 180, y0 + 275, hand(40, 700), C.ink, t, seq(tk + 0.25, nm, 0.08), 0.1, 'center');
    if (k < 2) { const A = sc['ta' + k] || (sc['ta' + k] = new Sk(3911 + k).penOn()); if (!sc['ta' + k + 'b']) { arrowTo(A, x + 368, y0 + 275, x + 432, y0 + 275, { w: 3 }); sc['ta' + k + 'b'] = 1; } A.at(t, tk + 0.4, 0.22); }
  }
  // 下排：观察 ← 运行时 ← 工具请求
  const bot = [['工具请求', 1060, mDec + 1.2], ['运行时执行', 620, mDec + 2.2], ['观察结果', 180, mBack]];
  for (let k = 0; k < 3; k++) {
    const [nm, x, tk] = bot[k];
    if (t < tk - 0.4) continue;
    const S = sc['b' + k] || (sc['b' + k] = new Sk(3921 + k).penOn().rrect(x, y0 + 430, 360, 130, 16, { w: 3.4, col: k === 2 ? COL_A : C.ink }));
    S.at(t, tk, 0.45);
    writeText(nm, x + 180, y0 + 495, hand(40, 700), k === 2 ? COL_A : C.ink, t, seq(tk + 0.25, nm, 0.08), 0.1, 'center');
    if (k < 2) { const A = sc['ba' + k] || (sc['ba' + k] = new Sk(3931 + k).penOn()); if (!sc['ba' + k + 'b']) { arrowTo(A, x - 8, y0 + 495, x - 72, y0 + 495, { w: 3 }); sc['ba' + k + 'b'] = 1; } A.at(t, tk + 0.4, 0.22); }
  }
  // 回流环
  if (t >= mBack - 0.5) {
    const A = sc.loop || (sc.loop = new Sk(3941).penOn());
    if (!sc.loop_b) { arrowTo(A, 1428, y0 + 340, 1428, y0 + 430, { w: 3 }); A.curve([[180, y0 + 430], [90, y0 + 410], [90, y0 + 300], [180, y0 + 275]], { w: 3.2, col: COL_A }); sc.loop_b = 1; }
    A.at(t, mBack - 0.45, 0.5);
  }
  // 两条停止路径
  if (t >= mFive - 0.5) {
    const S = sc.end1 || (sc.end1 = new Sk(3951).penOn().rrect(1450, y0 + 220, 350, 120, 14, { w: 3.4, col: COL_A }));
    S.at(t, mFive - 0.45, 0.45);
    writeText('结束标记', 1625, y0 + 280, hand(36, 700), COL_A, t, seq(mFive + 0.2, '结束标记', 0.07), 0.1, 'center');
  }
  if (t >= mOut - 0.5) {
    const S = sc.end2 || (sc.end2 = new Sk(3952).penOn().rrect(1450, y0 + 430, 350, 130, 14, { w: 3.4 }));
    S.at(t, mOut - 0.45, 0.45);
    writeText('预算耗尽', 1625, y0 + 495, hand(36, 700), C.ink, t, seq(mOut + 0.2, '预算耗尽', 0.07), 0.1, 'center');
    label('两条停止路径', 1625, y0 + 610, t, mOut + 0.8, 32);
  }
  if (t >= m138) {
    writeText('五次工具调用 → 含税总价 138', 620, y0 + 640, hand(42, 700), COL_A, t, seq(m138, '五次工具调用 → 含税总价 138', 0.05), 0.1);
  }
  if (t >= mRun) writeText('会做事和会停下，同样重要', 960, y0 + 780, hand(46, 700), COL_A, t, seq(mRun, '会做事和会停下', 0.07), 0.1, 'center');
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
