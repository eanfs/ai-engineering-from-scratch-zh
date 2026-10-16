// 14-04 Tree of Thoughts 与 LATS —— 场景 5-9 + 场景入口
// 注意：writeText 的第 7 个参数是「每个字的开始时间」，长度必须等于整串字符数（含空格）。

// ---------------- s05 实跑 ToT：这一跑没找到 24 ----------------
scene(4, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m数字 = MS('s05_数字', sc.st + 0.6), m152 = MS('s05_152', sc.st + 5.0),
        m27 = MS('s05_27', sc.st + 8.6), m失败 = MS('s05_失败', sc.st + 10.4);

  // 目标框
  if (t >= m数字 - 0.4) {
    const S = sc.goal || (sc.goal = new Sk(7401).penOn().rrect(170, y0 + 196, 420, 128, 16, { w: 4, col: COL_A }));
    S.at(t, m数字 - 0.35, 0.45);
    const NT = '数字 4、6、4、1';
    writeText(NT, 380, y0 + 238, hand(30, 700), C.gray, t, seq(m数字 - 0.1, NT, 0.05), 0.1, 'center');
    writeText('目标 24', 380, y0 + 288, hand(50, 700), COL_A, t, seq(m数字 + 0.35, '目标 24', 0.07), 0.1, 'center');
  }
  // 152 次展开
  if (t >= m152 - 0.5) {
    const S = sc.grid || (sc.grid = new Sk(7411).penOn().rrect(1130, y0 + 196, 660, 128, 16, { w: 3.2, col: C.gray2 }));
    S.at(t, m152 - 0.55, 0.35);
    const ET = '展开 152 个节点';
    writeText(ET, 1460, y0 + 260, hand(44, 700), C.ink, t, seq(m152 - 0.4, ET, 0.05), 0.1, 'center');
  }
  // 三格轨迹
  const trace = ['6 × 4 = 24', '4 − 1 = 3', '24 + 3 = 27'];
  if (t >= m152 + 0.9) {
    trace.forEach((txt, k) => {
      const x = 190 + k * 520, tk = m152 + 1.0 + k * 0.5;
      if (t < tk - 0.4) return;
      const S = sc['t' + k] || (sc['t' + k] = new Sk(7421 + k).penOn().rrect(x, y0 + 404, 420, 130, 14, { w: 3.4, col: k === 2 ? C.gray : C.ink }));
      S.at(t, tk - 0.35, 0.4);
      writeText(txt, x + 210, y0 + 469, hand(44, 700), k === 2 ? C.gray : C.ink, t, seq(tk + 0.1, txt, 0.06), 0.1, 'center');
      if (k < 2) {
        const A = sc['ta' + k] || (sc['ta' + k] = new Sk(7431 + k).penOn());
        if (!sc['ta' + k + 'b']) { arrowTo(A, x + 428, y0 + 469, x + 500, y0 + 469, { w: 3.2, col: C.gray }); sc['ta' + k + 'b'] = 1; }
        A.at(t, tk + 0.4, 0.25);
      }
    });
  }
  // 终态 + 叉
  if (t >= m27 - 0.4) {
    const S = sc.fin || (sc.fin = new Sk(7441).penOn().rrect(190, y0 + 616, 420, 140, 16, { w: 4, col: C.gray }));
    S.at(t, m27 - 0.35, 0.45);
    writeText('实际终态 27', 400, y0 + 686, hand(46, 700), C.gray, t, seq(m27, '实际终态 27', 0.07), 0.1, 'center');
  }
  if (t >= m失败 - 0.4) {
    const X = sc.cross || (sc.cross = new Sk(7451).penOn());
    if (!sc.cross_b) { X.line(700, y0 + 636, 900, y0 + 736, { w: 7, col: C.gray }); X.line(900, y0 + 636, 700, y0 + 736, { w: 7, col: C.gray }); sc.cross_b = 1; }
    X.at(t, m失败 - 0.35, 0.35);
    const VT = '这次搜索失败了，如实记录';
    writeText(VT, 1280, y0 + 686, hand(46, 700), C.gray, t, seq(m失败 + 0.25, VT, 0.06), 0.1, 'center');
    if (t >= m失败 + 0.7) {
      const NT = 'BFS 带自评，但没有回溯到那一步正确的展开';
      writeText(NT, 1280, y0 + 764, hand(30, 700), C.gray, t, seq(m失败 + 0.75, NT, 0.035), 0.1, 'center');
    }
  }
});

// ---------------- s06 LATS：MCTS 四步 ----------------
scene(5, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mMCTS = MS('s06_MCTS', sc.st + 0.5), m角色 = MS('s06_三角色', sc.st + 5.6),
        m价值 = MS('s06_价值', sc.st + 8.4), m四步 = MS('s06_四步', sc.st + 11.4);

  if (t >= mMCTS - 0.4) {
    writeText('蒙特卡洛树搜索', 170, y0 + 216, hand(50, 700), C.ink, t, seq(mMCTS, '蒙特卡洛树搜索', 0.06), 0.1);
    const UT = '统一 ToT · ReAct · Reflexion';
    writeText(UT, 1300, y0 + 216, hand(34, 700), C.gray, t, seq(mMCTS + 0.9, UT, 0.045), 0.1, 'center');
  }
  // 三个角色
  const roles = [['策略 Policy', '提候选', 0], ['价值函数', '打分', 1], ['自省器', '写反思', 0]];
  if (t >= m角色 - 0.4) {
    roles.forEach(([nm, sub, hot], k) => {
      const x = 170 + k * 540, tk = m角色 + k * 0.6;
      if (t < tk - 0.45) return;
      const S = sc['r' + k] || (sc['r' + k] = new Sk(7501 + k).penOn().rrect(x, y0 + 290, 480, 150, 16, { w: 3.8, col: hot ? COL_A : C.ink }));
      S.at(t, tk - 0.4, 0.45);
      writeText(nm, x + 240, y0 + 344, hand(42, 700), hot ? COL_A : C.ink, t, seq(tk, nm, 0.07), 0.1, 'center');
      writeText(sub, x + 240, y0 + 400, hand(30, 700), C.gray, t, seq(tk + 0.5, sub, 0.08), 0.1, 'center');
    });
  }
  if (t >= m价值 - 0.3) {
    const VL = '价值函数吃环境反馈，所以搜索被真实工具结果引导';
    writeText(VL, 960, y0 + 490, hand(34, 700), COL_B, t, seq(m价值, VL, 0.032), 0.1, 'center');
  }
  // 四步环
  const steps = [['Select', '选择'], ['Expand', '扩展'], ['Simulate', '模拟'], ['Backprop', '回传']];
  const SX = 200, SY = y0 + 556, SW = 340, SH = 150, GAPX = 60;
  if (t >= m四步 - 0.4) {
    steps.forEach(([en, cn], k) => {
      const x = SX + k * (SW + GAPX), tk = m四步 + k * 0.45;
      if (t < tk - 0.4) return;
      const S = sc['s' + k] || (sc['s' + k] = new Sk(7511 + k).penOn().rrect(x, SY, SW, SH, 16, { w: 3.8, col: k === 3 ? COL_A : C.ink }));
      S.at(t, tk - 0.35, 0.45);
      writeText(en, x + SW / 2, SY + 62, hand(42, 700), k === 3 ? COL_A : C.ink, t, seq(tk + 0.15, en, 0.07), 0.1, 'center');
      writeText(cn, x + SW / 2, SY + 110, hand(30, 700), C.gray, t, seq(tk + 0.5, cn, 0.08), 0.1, 'center');
      if (k < 3) {
        const A = sc['sa' + k] || (sc['sa' + k] = new Sk(7521 + k).penOn());
        if (!sc['sa' + k + 'b']) { arrowTo(A, x + SW + 8, SY + SH / 2, x + SW + GAPX - 8, SY + SH / 2, { w: 3.4 }); sc['sa' + k + 'b'] = 1; }
        A.at(t, tk + 0.35, 0.25);
      }
    });
    if (t >= m四步 + 2.1) {
      const LP = sc.loop || (sc.loop = new Sk(7531).penOn());
      if (!sc.loop_b) { LP.curve([[1800, SY + SH - 4], [1876, y0 + 838], [960, y0 + 836], [244, y0 + 838], [200, SY + SH - 4]], { w: 3.8, col: COL_A }); sc.loop_b = 1; }
      LP.at(t, m四步 + 2.15, 0.6);
      const LT = '每一轮都把价值回传上去';
      writeText(LT, 960, y0 + 778, hand(34, 700), COL_A, t, seq(m四步 + 2.5, LT, 0.05), 0.1, 'center');
    }
  }
});

// ---------------- s07 实跑 LATS：收敛到 24 ----------------
scene(6, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mUCT = MS('s07_UCT', sc.st + 0.5), m286 = MS('s07_286', sc.st + 4.6),
        m成功 = MS('s07_成功', sc.st + 9.4), mHE = MS('s07_HE', sc.st + 12.0);

  if (t >= mUCT - 0.4) {
    const UT = 'UCT = Q + c·√(ln N / n)';
    writeText(UT, 170, y0 + 216, hand(42, 700), COL_B, t, seq(mUCT, UT, 0.05), 0.1);
    writeText('利用 + 探索', 1240, y0 + 216, hand(34, 700), C.gray, t, seq(mUCT + 0.8, '利用 + 探索', 0.06), 0.1, 'center');
  }
  if (t >= m286 - 0.5) {
    const S = sc.grid || (sc.grid = new Sk(7601).penOn().rrect(1130, y0 + 280, 660, 128, 16, { w: 3.2, col: COL_A }));
    S.at(t, m286 - 0.55, 0.35);
    const ET = '展开 286 个节点';
    writeText(ET, 1460, y0 + 344, hand(44, 700), COL_A, t, seq(m286 - 0.4, ET, 0.05), 0.1, 'center');
  }
  // 轨迹（与 s05 同构）
  const trace = ['6 × 4 = 24', '24 × 1 = 24'];
  if (t >= m286 + 0.6) {
    trace.forEach((txt, k) => {
      const x = 190 + k * 640, tk = m286 + 0.7 + k * 0.6;
      if (t < tk - 0.4) return;
      const S = sc['t' + k] || (sc['t' + k] = new Sk(7611 + k).penOn().rrect(x, y0 + 452, 540, 130, 14, { w: 3.6, col: COL_A }));
      S.at(t, tk - 0.35, 0.4);
      writeText(txt, x + 270, y0 + 517, hand(46, 700), COL_A, t, seq(tk + 0.1, txt, 0.06), 0.1, 'center');
      if (k === 0) {
        const A = sc.ta || (sc.ta = new Sk(7621).penOn());
        if (!sc.ta_b) { arrowTo(A, x + 548, y0 + 517, x + 620, y0 + 517, { w: 3.4, col: COL_A }); sc.ta_b = 1; }
        A.at(t, tk + 0.45, 0.25);
      }
    });
  }
  // 成功：终态 24 + 对勾
  if (t >= m成功 - 0.4) {
    const S = sc.fin || (sc.fin = new Sk(7631).penOn().rrect(190, y0 + 640, 540, 150, 16, { w: 4.4, col: COL_A }));
    S.at(t, m成功 - 0.35, 0.45);
    writeText('实际终态 24', 460, y0 + 715, hand(48, 700), COL_A, t, seq(m成功, '实际终态 24', 0.07), 0.1, 'center');
    const CK = sc.tick || (sc.tick = new Sk(7641).penOn().poly([[780, y0 + 690], [830, y0 + 748], [920, y0 + 646]], { w: 10, col: COL_A }));
    CK.at(t, m成功 + 0.7, 0.35);
  }
  if (t >= mHE - 0.4) {
    writeText('HumanEval pass@1', 1380, y0 + 686, hand(36, 700), C.ink, t, seq(mHE - 0.3, 'HumanEval pass@1', 0.05), 0.1, 'center');
    writeText('92.7%', 1380, y0 + 758, hand(56, 700), COL_A, t, seq(mHE + 0.3, '92.7%', 0.09), 0.1, 'center');
    const NT = '论文发表时的 SOTA';
    writeText(NT, 1380, y0 + 818, hand(28, 700), C.gray, t, seq(mHE + 1.0, NT, 0.05), 0.1, 'center');
  }
});

// ---------------- s08 成本账：100 到 1000 倍 token ----------------
scene(7, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m倍数 = MS('s08_倍数', sc.st + 0.5), m三个 = MS('s08_三个', sc.st + 6.0),
        m噪声 = MS('s08_噪声', sc.st + 12.0), m错误 = MS('s08_错误', sc.st + 15.0);

  // 左：token 账单
  if (t >= m倍数 - 0.5) {
    const B = sc.bill || (sc.bill = new Sk(7701).penOn());
    if (!sc.bill_b) {
      B.fill(rectPts(170, y0 + 250, 560, 420), C.white, { fade: 1 });
      B.rrect(170, y0 + 250, 560, 420, 18, { w: 3.8 });
      for (let k = 0; k < 5; k++) B.line(220, y0 + 350 + k * 62, 680, y0 + 350 + k * 62, { w: 2.4, col: C.gray3 });
      sc.bill_b = 1;
    }
    B.at(t, m倍数 - 0.45, 0.6);
    writeText('token 账单', 450, y0 + 300, hand(40, 700), C.ink, t, seq(m倍数, 'token 账单', 0.07), 0.1, 'center');
    if (t >= m倍数 + 0.9) writeText('100 ×', 450, y0 + 470, hand(62, 700), C.ink, t, seq(m倍数 + 0.95, '100 ×', 0.08), 0.1, 'center');
    if (t >= m倍数 + 1.6) {
      writeText('到', 450, y0 + 556, hand(36, 700), C.gray, t, seq(m倍数 + 1.6, '到', 0.1), 0.1, 'center');
      writeText('1000 ×', 450, y0 + 632, hand(62, 700), COL_A, t, seq(m倍数 + 1.85, '1000 ×', 0.08), 0.1, 'center');
    }
  }
  // 右：三条判据
  const crit = [['单条轨迹明显不够', 'Game of 24、复杂代码'], ['墙钟时间没正确性重要', '慢一点换对'], ['价值函数廉价又可靠', '单元测试、显式目标']];
  if (t >= m三个 - 0.4) {
    writeText('值得花的三个场合', 1290, y0 + 300, hand(42, 700), C.ink, t, seq(m三个, '值得花的三个场合', 0.06), 0.1, 'center');
    crit.forEach(([a, b], k) => {
      const y = y0 + 356 + k * 116, tk = m三个 + 0.5 + k * 0.7;
      if (t < tk - 0.45) return;
      const S = sc['cr' + k] || (sc['cr' + k] = new Sk(7711 + k).penOn().rrect(830, y, 920, 96, 14, { w: 3.4 }));
      S.at(t, tk - 0.4, 0.4);
      writeText(a, 870, y + 38, hand(38, 700), C.ink, t, seq(tk, a, 0.055), 0.1);
      writeText(b, 870, y + 74, hand(26, 700), C.gray, t, seq(tk + 0.5, b, 0.05), 0.1);
    });
  }
  // 底部警告带
  if (t >= m噪声 - 0.5) {
    const WB = sc.warn || (sc.warn = new Sk(7721).penOn());
    if (!sc.warn_b) { WB.fill(rectPts(170, y0 + 720, 1580, 110), C.orangeL, { fade: 1 }); WB.rrect(170, y0 + 720, 1580, 110, 16, { w: 3.6, col: COL_A }); sc.warn_b = 1; }
    WB.at(t, m噪声 - 0.45, 0.45);
    const WT = '评估器有噪声时，搜索会把事情弄得更糟';
    writeText(WT, 220, y0 + 775, hand(38, 700), C.orangeD, t, seq(m噪声, WT, 0.04), 0.1);
    if (t >= m错误 - 0.5) {
      const ET = '它会找到一个评分很高的错误答案';
      writeText(ET, 1740, y0 + 775, hand(36, 700), C.orangeD, t, seq(m错误 - 0.45, ET, 0.04), 0.1, 'right');
    }
  }
});

// ---------------- s09 把搜索当预算来花 ----------------
scene(8, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m2026 = MS('s09_2026', sc.st + 0.5), mReAct = MS('s09_ReAct', sc.st + 3.2),
        m阈值 = MS('s09_阈值', sc.st + 6.6), m预算 = MS('s09_预算', sc.st + 12.6);

  if (t >= m2026 - 0.4) {
    writeText('2026 年', 170, y0 + 214, hand(46, 700), C.ink, t, seq(m2026, '2026 年', 0.07), 0.1);
    const AT = '大多数生产 agent 跑的不是 LATS';
    writeText(AT, 400, y0 + 214, hand(36, 700), C.gray, t, seq(m2026 + 0.6, AT, 0.04), 0.1);
  }
  if (t >= mReAct - 0.4) {
    const S = sc.react || (sc.react = new Sk(7801).penOn().rrect(170, y0 + 288, 700, 130, 16, { w: 4, col: C.ink }));
    S.at(t, mReAct - 0.35, 0.45);
    writeText('带工具验证的 ReAct', 520, y0 + 353, hand(46, 700), C.ink, t, seq(mReAct, '带工具验证的 ReAct', 0.05), 0.1, 'center');
    const CT = '编码 agent 把单元测试当价值函数';
    writeText(CT, 1500, y0 + 353, hand(32, 700), C.gray, t, seq(mReAct + 1.1, CT, 0.04), 0.1, 'center');
  }
  // 门（阈值），门后透出搜索的树
  if (t >= m阈值 - 0.5) {
    const D = sc.door || (sc.door = new Sk(7811).penOn());
    if (!sc.door_b) {
      D.curve([[800, y0 + 704], [800, y0 + 556], [880, y0 + 486], [960, y0 + 484], [1040, y0 + 486], [1120, y0 + 556], [1120, y0 + 704]], { w: 4.4 });
      D.line(792, y0 + 704, 1128, y0 + 704, { w: 4.4 });
      sc.door_b = 1;
    }
    D.at(t, m阈值 - 0.45, 0.65);
    const DT = '任务复杂度 > 阈值';
    writeText(DT, 960, y0 + 596, hand(40, 700), C.ink, t, seq(m阈值, DT, 0.055), 0.1, 'center');
    if (t >= m阈值 + 1.1) {
      const TR = sc.dtree || (sc.dtree = new Sk(7821).penOn());
      if (!sc.dtree_b) {
        TR.line(960, y0 + 480, 960, y0 + 362, { w: 3.4, col: COL_A });
        TR.line(960, y0 + 430, 890, y0 + 372, { w: 3, col: COL_A });
        TR.line(960, y0 + 430, 1032, y0 + 372, { w: 3, col: COL_A });
        sc.dtree_b = 1;
      }
      TR.at(t, m阈值 + 1.15, 0.5);
      writeText('搜索', 960, y0 + 326, hand(34, 700), COL_A, t, seq(m阈值 + 1.6, '搜索', 0.09), 0.1, 'center');
    }
  }
  // 收尾问句
  if (t >= m预算 - 0.5) {
    const QT = '留一个问题给你：值不值得为一次推理付 100 倍 token？';
    writeText(QT, 960, y0 + 806, hand(40, 700), COL_B, t, seq(m预算, QT, 0.04), 0.1, 'center');
  }
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
