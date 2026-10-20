
// ---------------- s06 MCTS 的四步与 UCT ----------------
scene(6, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mFour = MS('s07_四步', sc.st + 0.5), mUct = MS('s07_uct', sc.st + 4), mC = MS('s07_c', sc.st + 7.5);
  // 四步环形
  const ring = [['Select', 420, y0 + 230], ['Expand', 700, y0 + 230], ['Simulate', 700, y0 + 520], ['Backprop', 420, y0 + 520]];
  ring.forEach(([nm, x, y], k) => {
    const tk = mFour + k * 0.7;
    if (t < tk - 0.35) return;
    const G0 = sc['s' + k] || (sc['s' + k] = new Sk(5601 + k).penOn());
    if (!sc['s' + k + '_b']) { node3d(G0, Number(x), Number(y), 76, k === 0 ? COL_A : C.ink); sc['s' + k + '_b'] = 1; }
    G0.at(t, tk, 0.45);
    writeText(String(nm), Number(x), Number(y) - 4, hand(30, 700), k === 0 ? COL_A : C.ink, t, seq(tk + 0.3, String(nm), 0.06), 0.1, 'center');
  });
  // 环上的箭头（顺时针）
  if (t >= mFour - 0.4) {
    const A = sc.loop || (sc.loop = new Sk(5611).penOn());
    if (!sc.loop_b) {
      arrowTo(A, 500, y0 + 230, 616, y0 + 230, { w: 3, col: C.gray });
      arrowTo(A, 700, y0 + 310, 700, y0 + 438, { w: 3, col: C.gray });
      arrowTo(A, 620, y0 + 520, 500, y0 + 520, { w: 3, col: C.gray });
      arrowTo(A, 420, y0 + 438, 420, y0 + 310, { w: 3, col: C.gray });
      sc.loop_b = 1;
    }
    A.at(t, mFour - 0.35, 0.6);
  }
  // UCT 公式
  if (t >= mUct - 0.4) {
    writeText('UCT', 1080, y0 + 200, hand(46, 700), COL_A, t, seq(mUct, 'UCT', 0.1), 0.1);
    writeText('Q(s,a) + c·√(ln N(s) / N(s,a))', 1080, y0 + 290, hand(36, 700), C.ink, t, seq(mUct + 0.4, 'Q(s,a) + c·√(ln N(s) / N(s,a))', 0.05), 0.1);
    label('前一项：利用；后一项：探索', 1080, y0 + 380, t, mUct + 1.2, 36);
  }
  // 利用/探索两条曲线
  if (t >= mC - 0.4) {
    const G = sc.cur || (sc.cur = new Sk(5621).penOn());
    if (!sc.cur_b) {
      const pts1 = [], pts2 = [];
      for (let i = 0; i <= 20; i++) { const u = i / 20; pts1.push([1080 + u * 560, y0 + 600 - 120 * Math.pow(u, 0.5)]); pts2.push([1080 + u * 560, y0 + 600 - 120 * (1 - Math.exp(-3 * u))]); }
      G.curve(pts1, { w: 3.4, col: COL_A }); G.curve(pts2, { w: 3.4, col: C.ink }); sc.cur_b = 1;
    }
    G.at(t, mC - 0.35, 0.65);
    label('c 小：更贪心', 1080, y0 + 660, t, mC + 0.2, 32);
    label('c 大：更愿意探索', 1440, y0 + 660, t, mC + 0.6, 32);
    writeText('这个旋钮决定搜索的性格', 1080, y0 + 740, hand(36, 700), COL_A, t, seq(mC + 1.2, '这个旋钮决定搜索的性格', 0.05), 0.1);
  }
});

// ---------------- s07 实跑：286 次展开，真的找到 24 ----------------
scene(7, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m286 = MS('s08_286', sc.st + 0.5), m24 = MS('s08_24', sc.st + 4), mStrat = MS('s08_策略', sc.st + 8);
  // 对比柱：ToT 152 vs LATS 286
  if (t >= m286 - 0.5) {
    const b1 = sc.b1 || (sc.b1 = new Sk(5701).penOn()); if (!sc.b1_b) { bar3d(b1, 260, y0 + 620, 140, 150, C.gray); sc.b1_b = 1; }
    b1.at(t, m286 - 0.45, 0.4);
    writeText('152', 330, y0 + 680, hand(40, 700), C.gray, t, seq(m286, '152', 0.1), 0.1, 'center');
    label('ToT', 330, y0 + 740, t, m286 + 0.3, 34);
    const b2 = sc.b2 || (sc.b2 = new Sk(5711).penOn()); if (!sc.b2_b) { bar3d(b2, 520, y0 + 620, 140, 290, COL_A); sc.b2_b = 1; }
    b2.at(t, m286 + 0.2, 0.45);
    writeText('286', 590, y0 + 680, hand(40, 700), COL_A, t, seq(m286 + 0.5, '286', 0.1), 0.1, 'center');
    label('LATS', 590, y0 + 740, t, m286 + 0.8, 34);
  }
  // 轨迹与终点
  if (t >= m24 - 0.5) {
    const steps = ['6×4=24', '24×1=24'], ty = y0 + 220;
    steps.forEach((s, k) => {
      const tk = m24 + k * 0.8, x = 900 + k * 340;
      if (t < tk - 0.3) return;
      const G0 = sc['t' + k] || (sc['t' + k] = new Sk(5721 + k).penOn()); if (!sc['t' + k + '_b']) { isoBox(G0, x, ty, 300, 100, 14, { col: C.ink }); sc['t' + k + '_b'] = 1; }
      G0.at(t, tk, 0.45);
      writeText(s, x + 150, ty + 50, hand(34, 700), C.ink, t, seq(tk + 0.3, s, 0.06), 0.1, 'center');
    });
    writeText('终点 (24, 4)', 1240, y0 + 380, hand(40, 700), COL_A, t, seq(m24 + 1.8, '终点 (24, 4)', 0.08), 0.1);
    const CK = sc.ck || (sc.ck = new Sk(5731).penOn().poly([[1600, y0 + 330], [1652, y0 + 386], [1750, y0 + 266]], { w: 11, col: COL_A }));
    CK.at(t, m24 + 2.2, 0.3);
  }
  // 价值 0.000
  if (t >= m24 + 2.0) {
    writeText('价值 0.000', 900, y0 + 500, hand(44, 700), COL_A, t, seq(m24 + 2.0, '价值 0.000', 0.07), 0.1);
  }
  if (t >= mStrat) {
    writeText('差别不在模型，在搜索策略：预算更多花在有希望的分支上', 300, y0 + 820, hand(38, 700), C.ink, t, seq(mStrat, '差别不在模型，在搜索策略：预算更多花在有希望的分支上', 0.05), 0.1);
  }
});

// ---------------- s08 成本的现实 ----------------
scene(8, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mBang = MS('s09_爆炸', sc.st + 0.5), mKeep = MS('s09_留给', sc.st + 4), mNoise = MS('s09_噪声', sc.st + 9);
  // 倍率堆叠条：100× → 1000×
  if (t >= mBang - 0.5) {
    const G0 = sc.rate || (sc.rate = new Sk(5801).penOn());
    if (!sc.rate_b) { for (let k = 0; k < 5; k++) isoBox(G0, 200 + k * 30, y0 + 300 - k * 26, 320, 70, 12, { col: k === 4 ? COL_A : C.ink }); sc.rate_b = 1; }
    G0.at(t, mBang - 0.45, 0.6);
    writeText('100× → 1000×', 240, y0 + 420, hand(46, 700), COL_A, t, seq(mBang + 0.2, '100× → 1000×', 0.06), 0.1);
    label('同样的任务，token 用量是 CoT 的 100 到 1000 倍', 200, y0 + 510, t, mBang + 0.8, 36);
  }
  // 三条适用条件
  if (t >= mKeep - 0.5) {
    const items = ['单条轨迹明显不够的任务', '墙钟时间没正确性重要', '有廉价、可靠的价值函数'];
    items.forEach((s, k) => {
      const tk = mKeep + k * 0.6, y = y0 + 200 + k * 120;
      if (t < tk - 0.3) return;
      const G0 = sc['k' + k] || (sc['k' + k] = new Sk(5811 + k).penOn()); if (!sc['k' + k + '_b']) { isoBox(G0, 1080, y, 760, 90, 12, { col: C.ink }); sc['k' + k + '_b'] = 1; }
      G0.at(t, tk, 0.45);
      writeText(s, 1120, y + 45, hand(32, 700), C.ink, t, seq(tk + 0.25, s, 0.05), 0.1);
    });
    label('把搜索留给', 1080, y0 + 140, t, mKeep, 38);
  }
  // 噪声警告
  if (t >= mNoise - 0.5) {
    const G0 = sc.warn || (sc.warn = new Sk(5821).penOn());
    if (!sc.warn_b) { isoBox(G0, 200, y0 + 620, 1560, 120, 14, { col: COL_A }); sc.warn_b = 1; }
    G0.at(t, mNoise - 0.45, 0.5);
    writeText('评估器有噪声 → 搜索会找到「评分很高」的错误答案', 260, y0 + 680, hand(38, 700), COL_A, t, seq(mNoise + 0.2, '评估器有噪声 → 搜索会找到「评分很高」的错误答案', 0.05), 0.1);
  }
});

// ---------------- s09 2026 年的定位 ----------------
scene(9, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mProd = MS('s10_生产', sc.st + 0.5), mScene = MS('s10_场景', sc.st + 4), mStd = MS('s10_标准', sc.st + 8);
  // 两个阵营
  if (t >= mProd - 0.5) {
    const A = sc.campA || (sc.campA = new Sk(5901).penOn()); if (!sc.campA_b) { isoBox(A, 180, y0 + 220, 700, 200, 16, { col: C.ink }); sc.campA_b = 1; }
    A.at(t, mProd - 0.45, 0.5);
    writeText('ReAct + 验证', 220, y0 + 290, hand(42, 700), C.ink, t, seq(mProd + 0.2, 'ReAct + 验证', 0.07), 0.1);
    label('多数生产 agent 跑这个', 220, y0 + 370, t, mProd + 0.8, 34);
    const B = sc.campB || (sc.campB = new Sk(5911).penOn()); if (!sc.campB_b) { isoBox(B, 1040, y0 + 220, 700, 200, 16, { col: COL_A }); sc.campB_b = 1; }
    B.at(t, mProd + 0.4, 0.5);
    writeText('LATS / 搜索', 1080, y0 + 290, hand(42, 700), COL_A, t, seq(mProd + 0.6, 'LATS / 搜索', 0.07), 0.1);
    label('留在细分场景里', 1080, y0 + 370, t, mProd + 1.2, 34);
  }
  // 细分场景
  if (t >= mScene - 0.5) {
    ['编码 agent：单元测试当价值函数', '深度研究：探索多条查询路径', '规划密集的图工作流'].forEach((s, k) => {
      const tk = mScene + k * 0.5;
      if (t >= tk) writeText(s, 1040, y0 + 460 + k * 60, hand(28, 700), C.ink, t, seq(tk, s, 0.05), 0.1);
    });
  }
  // 三条判断标准
  if (t >= mStd - 0.5) {
    const G0 = sc.std || (sc.std = new Sk(5921).penOn()); if (!sc.std_b) { isoBox(G0, 180, y0 + 620, 1560, 150, 16, { col: COL_B }); sc.std_b = 1; }
    G0.at(t, mStd - 0.45, 0.5);
    writeText('任务够难　·　评估器够可靠　·　预算够宽', 340, y0 + 690, hand(36, 700), COL_B, t, seq(mStd + 0.2, '任务够难　·　评估器够可靠　·　预算够宽', 0.05), 0.1);
    writeText('三条都满足，搜索才值得', 680, y0 + 810, hand(40, 700), COL_A, t, seq(mStd + 1.0, '三条都满足，搜索才值得', 0.06), 0.1, 'center');
  }
});

// ---------------- 场景入口：镜头与转场 ----------------
function drawScenes(t, v) {
  for (const sc of SCENES) {
    if (!seen(v, sc.y0 - 60, sc.y0 + SEC_H + 60)) continue;
    const f = D[sc.i]; if (f) f(sc, t, v);
  }
}
CAM0 = { x: 960, y: SCENES[0].y0 + 430, z: 0.95 };
CAM = [];
// 每场一个基础机位；再给几场加「场内推拉」——树展开时推近、对比数字时拉远看全、结尾收束。
SCENES.forEach((sc) => {
  const y = sc.y0 + 430;
  if (sc.i > 0) {
    const cu = FX_CUTS[sc.i - 1], jump = FX_DEFAULT && cu && (cu.kind === 'curl' || cu.kind === 'erase');
    CAM.push(jump ? [cu.t0, cu.tj, 960, y, 0.95, 'cut'] : [sc.s.start - 0.2, sc.s.start + 0.5, 960, y, 0.95]);
  }
  const st = sc.st, en = sc.en;
  // 场内镜头只做「推近/拉回」，机位中心保持在 (960, y0+430)：横移会把标题和左侧内容切出画面。
  // 每个推近段都跟一段回中，保证场末构图与基础机位一致，切场时不跳。
  if (sc.i === 3) CAM.push([st + 2.5, st + 5.5, 960, y, 1.10, 'sine'], [en - 2.5, en, 960, y, 0.95, 'sine']);
  if (sc.i === 4) CAM.push([st + 1.5, st + 4, 960, y, 1.07, 'sine'], [st + 6, st + 9, 960, y, 0.98, 'sine']);
  if (sc.i === 7) CAM.push([st + 1.5, st + 4, 960, y, 1.06, 'sine'], [st + 6, st + 9, 960, y, 0.98, 'sine']);
  if (sc.i === 5) CAM.push([st + 3, st + 6.5, 960, y, 1.09, 'sine'], [en - 2.5, en, 960, y, 0.95, 'sine']);
  if (sc.i === 8) CAM.push([st + 2, st + 6, 960, y, 1.05, 'sine'], [en - 2, en, 960, y, 0.95, 'sine']);
  if (sc.i === 9) CAM.push([st + 1.5, st + 4.5, 960, y, 1.04, 'sine'], [st + 6, st + 9, 960, y, 0.97, 'sine'], [en - 3, en, 960, y, 0.93, 'sine']);
});
