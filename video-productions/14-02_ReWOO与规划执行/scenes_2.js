// 14-02 ReWOO 与规划执行 —— 场景 6-10 + 场景入口
// writeText 的第 7 个参数是「每个字的开始时间」，长度必须等于整串字符数（含空格）。

// ---------------- s06 先满足依赖，再分派执行 ----------------
scene(5, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m拓扑 = MS('s06_拓扑', sc.st + 0.5), m循环依赖 = MS('s06_循环依赖', sc.st + 7.4),
        m错误串 = MS('s06_错误字符串', sc.st + 15.0), m两层 = MS('s06_两层', sc.st + 18.4);

  // 上：乱序输入 → 拓扑排序
  if (t >= m拓扑 - 0.5) {
    const IN = ['E2', 'E3', 'E1'], OUT = ['E1', 'E2', 'E3'];
    const draw = (arr, x0, tk0, col, broken) => arr.forEach((id, k) => {
      const x = x0 + k * 130, tk = tk0 + k * 0.35;
      if (t < tk - 0.35) return;
      const S = sc['s' + broken + k] || (sc['s' + broken + k] = new Sk(8501 + (broken ? 20 : 0) + k).penOn().rrect(x, y0 + 250, 108, 108, 14, { w: 3.4, col }));
      S.at(t, tk - 0.3, 0.4);
      writeText(id, x + 54, y0 + 304, hand(42, 700), col, t, seq(tk + 0.1, id, 0.08), 0.1, 'center');
    });
    draw(IN, 190, m拓扑 + 0.4, C.gray, 0);
    writeText('输入（乱序）', 190, y0 + 400, hand(30, 700), C.gray, t, seq(m拓扑 + 1.4, '输入（乱序）', 0.05), 0.1);
    const A = sc.tpA || (sc.tpA = new Sk(8531).penOn());
    if (!sc.tpA_b) { arrowTo(A, 620, y0 + 304, 720, y0 + 304, { w: 3.6, col: COL_A }); sc.tpA_b = 1; }
    A.at(t, m拓扑 + 1.8, 0.3);
    draw(OUT, 760, m拓扑 + 2.3, COL_A, 1);
    writeText('拓扑顺序', 760, y0 + 400, hand(30, 700), COL_A, t, seq(m拓扑 + 3.3, '拓扑顺序', 0.05), 0.1);
    const NT = '即使输入顺序反了，也要先执行被依赖的节点';
    writeText(NT, 960, y0 + 470, hand(32, 700), C.ink, t, seq(m拓扑 + 3.8, NT, 0.035), 0.1, 'center');
  }
  // 中：循环依赖 → 打叉
  if (t >= m循环依赖 - 0.5) {
    const loop = [['E1', 720], ['E2', 1140]];
    loop.forEach(([id, x], k) => {
      const S = sc['c' + k] || (sc['c' + k] = new Sk(8551 + k).penOn().rrect(x, y0 + 540, 150, 110, 14, { w: 3.4, col: C.gray }));
      S.at(t, m循环依赖 - 0.4 + k * 0.3, 0.4);
      writeText(id, x + 75, y0 + 595, hand(40, 700), C.gray, t, seq(m循环依赖 + k * 0.3, id, 0.08), 0.1, 'center');
    });
    const A = sc.loopA || (sc.loopA = new Sk(8561).penOn());
    if (!sc.loopA_b) {
      arrowTo(A, 878, y0 + 560, 1132, y0 + 560, { w: 3.2, col: C.gray });
      arrowTo(A, 1132, y0 + 632, 878, y0 + 632, { w: 3.2, col: C.gray });
      A.line(700, y0 + 520, 1330, y0 + 668, { w: 7, col: C.gray });
      sc.loopA_b = 1;
    }
    A.at(t, m循环依赖 + 0.9, 0.7);
    const LT = '循环依赖或缺失引用：一轮检查后没有任何节点能推进';
    writeText(LT, 960, y0 + 700, hand(32, 700), C.gray, t, seq(m循环依赖 + 1.7, LT, 0.032), 0.1, 'center');
  }
  // 下：两类失败在不同层
  if (t >= m错误串 - 0.5) {
    const two = [['计划结构：抛出运行错误', COL_A, 200], ['工具执行：返回错误字符串', C.ink, 1000]];
    two.forEach(([txt, col, x], k) => {
      const tk = m错误串 + k * 1.4;
      if (t < tk - 0.4) return;
      const S = sc['f' + k] || (sc['f' + k] = new Sk(8571 + k).penOn().rrect(x, y0 + 762, 720, 96, 14, { w: 3.4, col }));
      S.at(t, tk - 0.35, 0.42);
      writeText(txt, x + 360, y0 + 810, hand(34, 700), col, t, seq(tk, txt, 0.045), 0.1, 'center');
    });
  }
});

// ---------------- s07 省下的是重复上下文 ----------------
scene(6, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m重复 = MS('s07_重复', sc.st + 0.6), m八七三 = MS('s07_八七三', sc.st + 8.6),
        m四九五 = MS('s07_四九五', sc.st + 10.4), m不是 = MS('s07_不是', sc.st + 15.4);

  if (t >= m重复 - 0.5) {
    const RT = '交替式循环把先前轨迹反复带入后续请求';
    writeText(RT, 170, y0 + 232, hand(40, 700), C.ink, t, seq(m重复, RT, 0.045), 0.1);
    if (t >= m重复 + 1.6) {
      const RT2 = '分开规划与执行，工具阶段不必反复携带整段推理';
      writeText(RT2, 170, y0 + 292, hand(32, 700), C.gray, t, seq(m重复 + 1.65, RT2, 0.035), 0.1);
    }
  }
  // 两根横条：873 与 495（条长按数值等比，1 个单位 1.2 像素）
  const SCALE = 1.2, BX = 400;
  if (t >= m八七三 - 0.5) {
    const W1 = 873 * SCALE;
    const S = sc.b1 || (sc.b1 = new Sk(8601).penOn());
    if (!sc.b1_b) { S.fill(rectPts(BX, y0 + 380, W1, 110), C.gray3, { fade: 1 }); S.rrect(BX, y0 + 380, W1, 110, 8, { w: 3.6, col: C.gray }); sc.b1_b = 1; }
    S.at(t, m八七三 - 0.45, 0.6);
    writeText('ReAct', 170, y0 + 436, hand(40, 700), C.gray, t, seq(m八七三 + 0.2, 'ReAct', 0.08), 0.1);
    writeText('873', BX + W1 + 40, y0 + 436, hand(52, 700), C.gray, t, seq(m八七三 + 0.5, '873', 0.09), 0.1);
    writeText('字符数（粗略对照）', BX + 40, y0 + 340, hand(28, 700), C.gray, t, seq(m八七三 + 1.1, '字符数', 0.05), 0.1);
  }
  if (t >= m四九五 - 0.5) {
    const W2 = 495 * SCALE;
    const S = sc.b2 || (sc.b2 = new Sk(8611).penOn());
    if (!sc.b2_b) { S.fill(rectPts(BX, y0 + 530, W2, 110), COL_A, { fade: 1, a: 0.9 }); S.rrect(BX, y0 + 530, W2, 110, 8, { w: 4, col: COL_A }); sc.b2_b = 1; }
    S.at(t, m四九五 - 0.45, 0.6);
    writeText('ReWOO', 170, y0 + 586, hand(40, 700), COL_A, t, seq(m四九五 + 0.2, 'ReWOO', 0.08), 0.1);
    writeText('495', BX + W2 + 40, y0 + 586, hand(52, 700), COL_A, t, seq(m四九五 + 0.5, '495', 0.09), 0.1);
    if (t >= m四九五 + 1.4) {
      const RR = '1.76×';
      writeText(RR, 1340, y0 + 566, hand(70, 700), COL_A, t, seq(m四九五 + 1.45, RR, 0.1), 0.1, 'center');
      const NT = '本次运行的两组计数';
      writeText(NT, 1340, y0 + 640, hand(28, 700), C.gray, t, seq(m四九五 + 1.9, NT, 0.05), 0.1, 'center');
    }
  }
  // 边界
  if (t >= m不是 - 0.5) {
    const S = sc.scope || (sc.scope = new Sk(8621).penOn().rrect(170, y0 + 700, 1580, 130, 16, { w: 3.4, col: C.gray }));
    S.at(t, m不是 - 0.45, 0.45);
    const T1 = '这不是实际计费的词元数，也不是通用加速倍数';
    writeText(T1, 960, y0 + 744, hand(34, 700), C.ink, t, seq(m不是, T1, 0.035), 0.1, 'center');
    if (t >= m不是 + 1.6) {
      const T2 = '是否节省，要在真实任务、接口与相同质量标准下测量';
      writeText(T2, 960, y0 + 796, hand(30, 700), C.gray, t, seq(m不是 + 1.65, T2, 0.032), 0.1, 'center');
    }
  }
});

// ---------------- s08 静态计划遇到意外怎么办 ----------------
scene(7, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m静态 = MS('s08_静态', sc.st + 0.6), m模板 = MS('s08_模板', sc.st + 7.6),
        m重规划 = MS('s08_重规划', sc.st + 14.4), m扩展 = MS('s08_扩展', sc.st + 17.4);

  // 上：静态计划在结果未知处断开
  if (t >= m静态 - 0.5) {
    const steps = [['E1', 190], ['E2', 610], ['E3', 1030]];   // E2 处断开
    steps.forEach(([id, x], k) => {
      const tk = m静态 + 0.4 + k * 0.5;
      if (t < tk - 0.4) return;
      const S = sc['p' + k] || (sc['p' + k] = new Sk(8701 + k).penOn().rrect(x, y0 + 246, 320, 120, 16, { w: 3.6, col: k === 1 ? C.gray : C.ink }));
      S.at(t, tk - 0.35, 0.42);
      writeText(id, x + 160, y0 + 306, hand(44, 700), k === 1 ? C.gray : C.ink, t, seq(tk + 0.1, id, 0.09), 0.1, 'center');
      if (k < 2) {
        const A = sc['pa' + k] || (sc['pa' + k] = new Sk(8711 + k).penOn());
        if (!sc['pa' + k + 'b']) { arrowTo(A, x + 328, y0 + 306, x + 412, y0 + 306, { w: 3.4, col: k === 1 ? C.gray2 : C.ink }); sc['pa' + k + 'b'] = 1; }
        A.at(t, tk + 0.45, 0.25);
      }
    });
    if (t >= m静态 + 2.2) {
      const X = sc.brk || (sc.brk = new Sk(8721).penOn());
      if (!sc.brk_b) { X.line(890, y0 + 268, 960, y0 + 344, { w: 6, col: C.orangeD }); X.line(960, y0 + 268, 890, y0 + 344, { w: 6, col: C.orangeD }); sc.brk_b = 1; }
      X.at(t, m静态 + 2.25, 0.35);
      const BT = '静态计划在看到工具结果之前已经确定，遇到错误不会天然生成新方案';
      writeText(BT, 960, y0 + 418, hand(32, 700), C.orangeD, t, seq(m静态 + 2.6, BT, 0.03), 0.1, 'center');
    }
  }
  // 中：求解器只填模板
  if (t >= m模板 - 0.5) {
    const S = sc.tpl || (sc.tpl = new Sk(8731).penOn().rrect(190, y0 + 490, 700, 140, 16, { w: 3.6, col: C.ink }));
    S.at(t, m模板 - 0.45, 0.45);
    writeText('求解器：把证据填入模板', 540, y0 + 548, hand(38, 700), C.ink, t, seq(m模板, '求解器：把证据填入模板', 0.045), 0.1, 'center');
    const S2 = sc.tpl2 || (sc.tpl2 = new Sk(8741).penOn().rrect(1000, y0 + 490, 750, 140, 16, { w: 3.6, col: C.gray }));
    S2.at(t, m模板 + 0.8, 0.45);
    const T2 = '没有自主降级或补救能力';
    writeText(T2, 1375, y0 + 548, hand(36, 700), C.gray, t, seq(m模板 + 1.2, T2, 0.05), 0.1, 'center');
  }
  // 下：重规划回路（扩展，非已有功能）
  if (t >= m重规划 - 0.5) {
    const L = sc.rp || (sc.rp = new Sk(8751).penOn());
    if (!sc.rp_b) {
      L.curve([[1180, y0 + 716], [1250, y0 + 812], [900, y0 + 840], [550, y0 + 812], [490, y0 + 716]], { w: 4, col: COL_A, seg: 10 });
      L.rrect(880, y0 + 748, 620, 96, 14, { w: 3.8, col: COL_A });
      sc.rp_b = 1;
    }
    L.at(t, m重规划 - 0.45, 0.7);
    writeText('重规划器：修改剩余步骤', 1190, y0 + 796, hand(34, 700), COL_A, t, seq(m重规划 + 0.3, '重规划器：修改剩余步骤', 0.04), 0.1, 'center');
  }
  if (t >= m扩展 - 0.4) {
    const ET = '这是计划后执行的一种扩展，而不是本集代码已有功能';
    writeText(ET, 960, y0 + 678, hand(30, 700), C.gray, t, seq(m扩展, ET, 0.03), 0.1, 'center');
  }
});

// ---------------- s09 按任务的不确定性选择模式 ----------------
scene(8, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m看结果 = MS('s09_看结果', sc.st + 0.6), m事先 = MS('s09_事先', sc.st + 3.4),
        m网页 = MS('s09_网页', sc.st + 9.4), m简单 = MS('s09_简单', sc.st + 17.0);

  // 两条岔路
  const ways = [['下一步必须看刚发生的结果', '交替式循环更容易表达', C.ink, m看结果],
                ['工具与依赖事先清楚', '优先考虑显式计划', COL_A, m事先]];
  ways.forEach(([cond, pick, col, tk], k) => {
    const x = 170 + k * 810;
    if (t < tk - 0.5) return;
    const S = sc['w' + k] || (sc['w' + k] = new Sk(8801 + k).penOn().rrect(x, y0 + 240, 770, 150, 16, { w: 3.8, col }));
    S.at(t, tk - 0.45, 0.45);
    writeText(cond, x + 385, y0 + 292, hand(34, 700), col, t, seq(tk, cond, 0.04), 0.1, 'center');
    writeText('→ ' + pick, x + 385, y0 + 348, hand(34, 700), col, t, seq(tk + 0.9, '→ ' + pick, 0.05), 0.1, 'center');
  });
  // 中：网页长任务 + 重规划
  if (t >= m网页 - 0.5) {
    const S = sc.web || (sc.web = new Sk(8811).penOn().rrect(170, y0 + 450, 1580, 120, 16, { w: 3.4, col: C.gray }));
    S.at(t, m网页 - 0.45, 0.45);
    const WT = '网页长任务还涉及计划训练与环境反馈，不能只增加步骤数';
    writeText(WT, 960, y0 + 510, hand(34, 700), C.ink, t, seq(m网页, WT, 0.035), 0.1, 'center');
  }
  // 下：从简单结构开始的升级阶梯
  if (t >= m简单 - 0.5) {
    const rungs = [['能完成任务的简单结构', 190, C.ink], ['错误记录', 700, C.gray], ['质量', 1000, C.gray], ['开销', 1300, C.gray]];
    rungs.forEach(([nm, x, col], k) => {
      const tk = m简单 + 0.4 + k * 0.45;
      if (t < tk - 0.35) return;
      const w0 = k === 0 ? 460 : 240;
      const S = sc['g' + k] || (sc['g' + k] = new Sk(8821 + k).penOn().rrect(x, y0 + 640, w0, 110, 14, { w: 3.6, col }));
      S.at(t, tk - 0.3, 0.42);
      writeText(nm, x + w0 / 2, y0 + 695, hand(k === 0 ? 34 : 38, 700), col, t, seq(tk + 0.1, nm, 0.045), 0.1, 'center');
    });
    if (t >= m简单 + 2.4) {
      const ST = '再用这三样决定是否升级，避免为了模式名称增加复杂度';
      writeText(ST, 960, y0 + 812, hand(30, 700), C.gray, t, seq(m简单 + 2.45, ST, 0.03), 0.1, 'center');
    }
  }
});

// ---------------- s10 一张图，检查计划到答案 ----------------
scene(9, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m回看 = MS('s10_回看', sc.st + 0.6), m离线 = MS('s10_离线', sc.st + 7.4),
        m乱序 = MS('s10_乱序', sc.st + 11.0), m下一步 = MS('s10_下一步', sc.st + 17.0);

  // 横向汇总链
  const chain = [['计划', 130, COL_A], ['依赖', 500, COL_B], ['证据', 870, C.ink], ['答案', 1240, COL_A]];
  if (t >= m回看 - 0.5) {
    chain.forEach(([nm, x, col], k) => {
      const tk = m回看 + 0.4 + k * 0.6;
      if (t < tk - 0.4) return;
      const S = sc['k' + k] || (sc['k' + k] = new Sk(8901 + k).penOn().rrect(x, y0 + 280, 320, 150, 16, { w: 4, col }));
      S.at(t, tk - 0.35, 0.45);
      writeText(nm, x + 160, y0 + 355, hand(52, 700), col, t, seq(tk + 0.1, nm, 0.09), 0.1, 'center');
      if (k < 3) {
        const A = sc['ka' + k] || (sc['ka' + k] = new Sk(8911 + k).penOn());
        if (!sc['ka' + k + 'b']) { arrowTo(A, x + 328, y0 + 355, x + 362, y0 + 355, { w: 3.6 }); sc['ka' + k + 'b'] = 1; }
        A.at(t, tk + 0.5, 0.25);
      }
    });
  }
  // 离线实验验证了什么
  if (t >= m离线 - 0.5) {
    const S = sc.check || (sc.check = new Sk(8921).penOn().rrect(170, y0 + 490, 1580, 150, 16, { w: 3.4, col: C.gray }));
    S.at(t, m离线 - 0.45, 0.45);
    const T1 = '离线实验验证了三步依赖链';
    writeText(T1, 960, y0 + 540, hand(36, 700), C.ink, t, seq(m离线, T1, 0.045), 0.1, 'center');
    if (t >= m乱序 - 0.4) {
      const T2 = '乱序输入能排序；循环与缺失引用会失败——边界是清楚的';
      writeText(T2, 960, y0 + 596, hand(32, 700), C.gray, t, seq(m乱序, T2, 0.032), 0.1, 'center');
    }
  }
  // 下一步
  if (t >= m下一步 - 0.5) {
    const NT = '下一步：运行课程代码，加入独立节点或错误工具，先观察执行轨迹';
    writeText(NT, 960, y0 + 760, hand(38, 700), COL_B, t, seq(m下一步, NT, 0.032), 0.1, 'center');
    if (t >= m下一步 + 2.4) {
      const NT2 = '再决定是否需要并行或重规划';
      writeText(NT2, 960, y0 + 824, hand(30, 700), C.gray, t, seq(m下一步 + 2.45, NT2, 0.04), 0.1, 'center');
    }
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
