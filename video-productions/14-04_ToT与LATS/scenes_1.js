
// ===== 14-04 专用：3D 空间辅助（等距投影，用线稿画体积） =====
// 等距盒子：前面矩形 + 顶面/右侧面平行四边形，给卡片和柱子体积感。
function isoBox(S, x, y, w, h, dep, o = {}) {
  const col = o.col ?? C.ink, w2 = o.w ?? 3;
  // 落影：盒底向右下错开一层淡墨，给体积一个「站在纸上」的接触感
  S.fill([[x + dep * 0.26, y + h + dep * 0.16], [x + w + dep * 0.26, y + h + dep * 0.16],
          [x + w + dep * 0.94, y + h - dep * 0.46], [x + dep * 0.94, y + h - dep * 0.46]],
    'rgba(21,25,45,0.10)', { fade: 30 });
  S.line(x, y, x + dep * 0.72, y - dep * 0.58, { w: w2, col });
  S.line(x + w, y, x + w + dep * 0.72, y - dep * 0.58, { w: w2, col });
  S.line(x, y, x + w, y, { w: w2, col });
  S.line(x + w, y, x + w, y + h, { w: w2, col });
  S.line(x, y, x, y + h, { w: w2, col });
  S.line(x, y + h, x + w, y + h, { w: w2, col });
  S.line(x + dep * 0.72, y - dep * 0.58, x + w + dep * 0.72, y - dep * 0.58, { w: w2, col });
  S.line(x + w + dep * 0.72, y - dep * 0.58, x + w + dep * 0.72, y + h - dep * 0.58, { w: w2, col });
  S.line(x + w, y + h, x + w + dep * 0.72, y + h - dep * 0.58, { w: w2, col });
  return S;
}
// 3D 柱：底面椭圆 + 侧面 + 顶面，高度按值。
function bar3d(S, x, base, w, h, col, o = {}) {
  const ry = w * 0.16;
  S.ellipse(x + w / 2, base, w / 2, ry, { w: 2.6, col, turns: 1.02 });
  S.line(x, base, x, base - h, { w: 2.8, col });
  S.line(x + w, base, x + w, base - h, { w: 2.8, col });
  S.ellipse(x + w / 2, base - h, w / 2, ry, { w: 2.6, col, turns: 1.02 });
  return S;
}
// 节点：等距圆盘 + 分数标签
function node3d(S, cx, cy, r, col) {
  // 节点落影（压扁的椭圆，偏下）
  S.fill(circlePts(cx, cy + r * 0.5, r * 0.9), 'rgba(21,25,45,0.09)', { fade: 30 });
  S.ellipse(cx, cy, r, r * 0.62, { w: 3, col, turns: 1.05 });
  S.ellipse(cx, cy - r * 0.18, r, r * 0.62, { w: 2.2, col, turns: 1.03 });
  return S;
}

// ---------------- s01 封面：为什么 4% 能变成 74% ----------------
scene(0, (sc, t) => {
  const y0 = sc.y0;
  const mCover = MS('s01_封面', sc.st + 0.3), mAsk = MS('s01_提问', sc.st + 3.5), mPre = MS('s01_预告', sc.st + 7);
  // 封面大卡（3D 厚度 + 落影）
  const S = sc.card || (sc.card = new Sk(5001).penOn());
  if (!sc.card_b) { isoBox(S, 240, y0 + 170, 1440, 300, 26, { col: C.ink }); sc.card_b = 1; }
  S.at(t, mCover - 0.3, 0.6);
  writeText('Tree of Thoughts 与 LATS', 960, y0 + 290, hand(64, 700), C.ink, t, seq(mCover, 'Tree of Thoughts 与 LATS', 0.05), 0.08, 'center');
  writeText('单条思维链没有回头路', 960, y0 + 380, hand(40, 700), C.gray, t, seq(mCover + 1.6, '单条思维链没有回头路', 0.06), 0.1, 'center');
  // 页脚分隔线
  const L = sc.line || (sc.line = new Sk(5002).penOn());
  if (!sc.line_b) { L.line(430, y0 + 450, 1490, y0 + 450, { w: 3, col: C.gray2 }); sc.line_b = 1; }
  L.at(t, mAsk - 0.5, 0.4);
  // 提问（钩子）
  if (t >= mAsk - 0.4) writeText('为什么 4% 能变成 74%？', 960, y0 + 560, hand(56, 700), COL_A, t, seq(mAsk, '为什么 4% 能变成 74%？', 0.06), 0.1, 'center');
  // 预告
  if (t >= mPre - 0.4) writeText('两种把推理变成搜索的方法', 960, y0 + 700, hand(38, 700), C.ink, t, seq(mPre, '两种把推理变成搜索的方法', 0.05), 0.1, 'center');
});

// ---------------- s01 四个数字，只有一次能到 24 ----------------
scene(1, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mGame = MS('s02_游戏', sc.st + 0.5), m4 = MS('s02_4percent', sc.st + 3),
        m74 = MS('s02_74', sc.st + 6), mBoth = MS('s02_两法', sc.st + 9);
  // 四张数字牌（3D 厚度）
  const nums = ['4', '6', '4', '1'];
  for (let k = 0; k < 4; k++) {
    const x = 140 + k * 170, tk = mGame + k * 0.25;
    if (t < tk - 0.3) continue;
    const G0 = sc['n' + k] || (sc['n' + k] = new Sk(5101 + k).penOn());
    if (!sc['n' + k + '_b']) { isoBox(G0, x, y0 + 220, 120, 150, 18, { col: C.ink }); sc['n' + k + '_b'] = 1; }
    G0.at(t, tk, 0.45);
    writeText(nums[k], x + 60, y0 + 295, hand(64, 700), C.ink, t, seq(tk + 0.35, nums[k], 0.1), 0.1, 'center');
  }
  // 目标 24
  if (t >= m4 - 0.6) {
    label('目标', 880, y0 + 200, t, mGame + 1.2, 38);
    writeText('24', 880, y0 + 300, hand(110, 700), COL_A, t, seq(mGame + 1.4, '24', 0.12), 0.12);
  }
  // 两根 3D 柱：CoT 4% vs ToT 74%
  if (t >= m4 - 0.4) {
    const b1 = sc.b1 || (sc.b1 = new Sk(5111).penOn()); if (!sc.b1_b) { bar3d(b1, 620, y0 + 720, 130, 40, C.gray); sc.b1_b = 1; }
    b1.at(t, m4 - 0.35, 0.4);
    writeText('CoT 4%', 620, y0 + 790, hand(36, 700), C.gray, t, seq(m4 + 0.2, 'CoT 4%', 0.08), 0.1);
  }
  if (t >= m74 - 0.4) {
    const b2 = sc.b2 || (sc.b2 = new Sk(5121).penOn()); if (!sc.b2_b) { bar3d(b2, 860, y0 + 720, 130, 300, COL_A); sc.b2_b = 1; }
    b2.at(t, m74 - 0.35, 0.45);
    writeText('ToT 74%', 860, y0 + 790, hand(40, 700), COL_A, t, seq(m74 + 0.2, 'ToT 74%', 0.08), 0.1);
  }
  if (t >= mBoth) {
    writeText('ToT 与 LATS：把推理变成搜索', 1250, y0 + 300, hand(44, 700), C.ink, t, seq(mBoth, 'ToT 与 LATS：把推理变成搜索', 0.07), 0.1);
    label('同一批数字、同一个模型', 1250, y0 + 380, t, mBoth + 0.8, 36);
  }
});

// ---------------- s02 单条思维链没有回头路 ----------------
scene(2, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mLin = MS('s03_线性', sc.st + 0.5), mBad = MS('s03_坏前提', sc.st + 3.5), mBack = MS('s03_回溯', sc.st + 8);
  // 直线路径：三个步骤节点
  const pts = [[260, y0 + 260], [660, y0 + 260], [1060, y0 + 260]];
  for (let k = 0; k < 3; k++) {
    const tk = mLin + k * 0.6, [x, y] = pts[k];
    if (t < tk - 0.3) continue;
    const G0 = sc['p' + k] || (sc['p' + k] = new Sk(5201 + k).penOn()); if (!sc['p' + k + '_b']) { node3d(G0, x, y, 82, C.ink); sc['p' + k + '_b'] = 1; }
    G0.at(t, tk, 0.45);
    writeText(['第一步', '第二步', '第三步'][k], x, y + 120, hand(34, 700), C.ink, t, seq(tk + 0.3, ['第一步', '第二步', '第三步'][k], 0.07), 0.1, 'center');
    if (k < 2) { const A = sc['a' + k] || (sc['a' + k] = new Sk(5211 + k).penOn()); if (!sc['a' + k + '_b']) { arrowTo(A, x + 96, y, pts[k + 1][0] - 96, pts[k + 1][1], { w: 3.4 }); sc['a' + k + '_b'] = 1; } A.at(t, tk + 0.4, 0.3); }
  }
  // 分叉打叉
  if (t >= mBad - 0.4) {
    const X = sc.branch || (sc.branch = new Sk(5221).penOn());
    if (!sc.branch_b) { X.dash(660, y0 + 340, 660, y0 + 470, { w: 2.4, d: 18, gp: 10 }); X.line(620, y0 + 500, 730, y0 + 570, { w: 8, col: COL_A }); X.line(730, y0 + 500, 620, y0 + 570, { w: 8, col: COL_A }); sc.branch_b = 1; }
    X.at(t, mBad - 0.35, 0.5);
    label('这条分支不再考虑', 760, y0 + 530, t, mBad + 0.3, 36);
  }
  // 回溯箭头
  if (t >= mBack - 0.4) {
    const R = sc.ret || (sc.ret = new Sk(5231).penOn());
    if (!sc.ret_b) { R.curve([[1060, y0 + 340], [1060, y0 + 440], [260, y0 + 440], [260, y0 + 340]], { w: 3.6, col: COL_A }); sc.ret_b = 1; }
    R.at(t, mBack - 0.35, 0.55);
    const items = ['提出多个候选', '给它们打分', '遇到死路就回溯'];
    items.forEach((s, k) => { const tk = mBack + 0.3 + k * 0.5; if (t >= tk) writeText(s, 340 + k * 420, y0 + 640, hand(38, 700), C.ink, t, seq(tk, s, 0.05), 0.1, 'center'); });
  }
});

// ---------------- s03 ToT：把推理变成一棵树 ----------------
scene(3, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mNode = MS('s04_节点', sc.st + 0.5), mScore = MS('s04_自评', sc.st + 4), mBfs = MS('s04_bfs', sc.st + 8);
  // 等距 3D 树：根 → 3 子 → 6 叶
  const root = [960, y0 + 190], kids = [[760, y0 + 380], [960, y0 + 400], [1160, y0 + 380]];
  const leaves = [[640, y0 + 560], [820, y0 + 580], [920, y0 + 590], [1000, y0 + 590], [1100, y0 + 580], [1280, y0 + 560]];
  if (t >= mNode - 0.5) {
    const G0 = sc.tree || (sc.tree = new Sk(5301).penOn());
    if (!sc.tree_b) {
      node3d(G0, root[0], root[1], 92, C.ink);
      kids.forEach(([x, y]) => { G0.curve([[root[0], root[1] + 40], [(root[0] + x) / 2, (root[1] + y) / 2 + 30], [x, y - 30]], { w: 3, col: C.ink }); node3d(G0, x, y, 70, C.ink); });
      kids.forEach(([kx, ky], i) => { const ls = leaves.slice(i * 2, i * 2 + 2); ls.forEach(([x, y]) => { G0.curve([[kx, ky + 28], [(kx + x) / 2, (ky + y) / 2 + 20], [x, y - 20]], { w: 2.6, col: C.gray }); node3d(G0, x, y, 48, C.gray); }); });
      sc.tree_b = 1;
    }
    // 地面透视网格：树站在一张斜投影的地面上，给 3D 树一个空间参照
    if (!sc.tree_floor) {
      const F = new Sk(5302);
      for (let i = -3; i <= 6; i++) F.line(380 + i * 120, y0 + 700, 620 + i * 120, y0 + 560, { w: 1.6, col: C.gray3, a: 0.55 });
      for (let i = 0; i < 4; i++) F.line(340 + i * 40, y0 + 660 - i * 20, 1500 - i * 40, y0 + 660 - i * 20, { w: 1.4, col: C.gray3, a: 0.5 });
      sc.tree_floor = F;
    }
    sc.tree_floor.at(t, mNode - 0.6, 0.5);
    G0.at(t, mNode - 0.45, 0.75);
    writeText('根：找出 24', root[0], root[1] - 4, hand(26, 700), C.ink, t, seq(mNode + 0.4, '根：找出 24', 0.07), 0.1, 'center');
  }
  // 自评分数
  if (t >= mScore - 0.4) {
    const scores = [['HIGH', 760, y0 + 380, COL_A], ['LIKELY', 960, y0 + 400, C.ink], ['IMPOSSIBLE', 1160, y0 + 380, C.gray]];
    scores.forEach(([s, x, y, col], k) => { const tk = mScore + k * 0.4; if (t >= tk) writeText(String(s), Number(x), Number(y) + 72, hand(28, 700), String(col), t, seq(tk, String(s), 0.06), 0.1, 'center'); });
    label('每个节点自评：sure / likely / impossible', 300, y0 + 700, t, mScore + 1.2, 38);
  }
  if (t >= mBfs) {
    writeText('BFS · DFS · beam', 1300, y0 + 700, hand(40, 700), C.ink, t, seq(mBfs, 'BFS · DFS · beam', 0.07), 0.1);
    writeText('承重部件是自评，不是搜索本身', 640, y0 + 800, hand(40, 700), COL_A, t, seq(mBfs + 0.6, '承重部件是自评，不是搜索本身', 0.06), 0.1, 'center');
  }
});

// ---------------- s04 ToT 实跑：152 次展开 ----------------
scene(4, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m152 = MS('s05_152', sc.st + 0.5), mTrace = MS('s05_轨迹', sc.st + 2.5),
        m27 = MS('s05_27', sc.st + 5), mVal = MS('s05_价值', sc.st + 7);
  if (t >= m152 - 0.4) {
    writeText('152', 150, y0 + 280, hand(130, 700), COL_A, t, seq(m152, '152', 0.15), 0.14);
    label('次节点展开', 160, y0 + 380, t, m152 + 0.5, 38);
    label('输入 [4, 6, 4, 1]，目标 24', 160, y0 + 460, t, m152 + 1.0, 36);
  }
  // 三张轨迹卡（3D）
  const steps = [['6×4=24', mTrace], ['4−1=3', mTrace + 1.2], ['24+3=27', m27]];
  for (let k = 0; k < 3; k++) {
    const [txt, tk] = steps[k], x = 560 + k * 420;
    if (t < tk - 0.35) continue;
    const G0 = sc['c' + k] || (sc['c' + k] = new Sk(5401 + k).penOn());
    if (!sc['c' + k + '_b']) { isoBox(G0, x, y0 + 230, 340, 120, 16, { col: k === 2 ? COL_A : C.ink }); sc['c' + k + '_b'] = 1; }
    G0.at(t, tk, 0.45);
    writeText(txt, x + 170, y0 + 290, hand(42, 700), k === 2 ? COL_A : C.ink, t, seq(tk + 0.3, txt, 0.07), 0.1, 'center');
  }
  // 价值条：0 → −0.030
  if (t >= mVal - 0.4) {
    const G = sc.val || (sc.val = new Sk(5411).penOn());
    if (!sc.val_b) { G.line(560, y0 + 520, 1780, y0 + 520, { w: 3, col: C.ink }); G.line(1170, y0 + 470, 1170, y0 + 570, { w: 3, col: C.gray }); G.line(1300, y0 + 505, 1300, y0 + 535, { w: 2.4, col: COL_A }); sc.val_b = 1; }
    G.at(t, mVal - 0.35, 0.5);
    writeText('0', 1140, y0 + 610, hand(32, 700), C.ink, t, seq(mVal + 0.2, '0', 0.1), 0.1);
    writeText('−0.030', 1250, y0 + 610, hand(38, 700), COL_A, t, seq(mVal + 0.5, '−0.030', 0.07), 0.1);
    writeText('没到 24：预算花在广度上，评分也不够准', 560, y0 + 700, hand(38, 700), COL_A, t, seq(mVal + 1.2, '没到 24：预算花在广度上，评分也不够准', 0.05), 0.1);
  }
});

// ---------------- s05 LATS：用 MCTS 统一三件事 ----------------
scene(5, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mUni = MS('s06_统一', sc.st + 0.5), mRoles = MS('s06_三角色', sc.st + 3), mFeed = MS('s06_反馈', sc.st + 8);
  // 中心 MCTS 圆盘
  if (t >= mUni - 0.5) {
    const G0 = sc.disk || (sc.disk = new Sk(5501).penOn());
    if (!sc.disk_b) { G0.ellipse(960, y0 + 420, 150, 92, { w: 4, col: COL_A }); G0.ellipse(960, y0 + 400, 150, 92, { w: 2.4, col: COL_A }); sc.disk_b = 1; }
    G0.at(t, mUni - 0.45, 0.55);
    writeText('MCTS', 960, y0 + 415, hand(48, 700), COL_A, t, seq(mUni + 0.3, 'MCTS', 0.08), 0.1, 'center');
  }
  // 三个角色框（三角）
  const roles = [['Policy', '提出下一步动作', 300, y0 + 200], ['Value', '给部分轨迹打分', 300, y0 + 560], ['Self-Reflector', '失败后写反思', 1300, y0 + 380]];
  roles.forEach(([nm, sub, x, y], k) => {
    const tk = mRoles + k * 0.5;
    if (t < tk - 0.35) return;
    const G0 = sc['r' + k] || (sc['r' + k] = new Sk(5511 + k).penOn()); if (!sc['r' + k + '_b']) { isoBox(G0, Number(x), Number(y), 300, 110, 14, { col: C.ink }); sc['r' + k + '_b'] = 1; }
    G0.at(t, tk, 0.45);
    writeText(String(nm), Number(x) + 150, Number(y) + 40, hand(36, 700), C.ink, t, seq(tk + 0.25, String(nm), 0.06), 0.1, 'center');
    writeText(String(sub), Number(x) + 150, Number(y) + 86, hand(26, 700), C.gray, t, seq(tk + 0.5, String(sub), 0.04), 0.1, 'center');
  });
  // 环境反馈箭头
  if (t >= mFeed - 0.5) {
    const A = sc.fb || (sc.fb = new Sk(5521).penOn());
    if (!sc.fb_b) { arrowTo(A, 1700, y0 + 300, 1120, y0 + 380, { w: 3.6, col: COL_A }); sc.fb_b = 1; }
    A.at(t, mFeed - 0.45, 0.5);
    writeText('环境反馈', 1560, y0 + 240, hand(34, 700), COL_A, t, seq(mFeed + 0.2, '环境反馈', 0.06), 0.1);
    writeText('搜索被真实工具结果引导，不只是模型的意见', 500, y0 + 800, hand(38, 700), COL_A, t, seq(mFeed + 0.8, '搜索被真实工具结果引导，不只是模型的意见', 0.05), 0.1, 'center');
  }
});
