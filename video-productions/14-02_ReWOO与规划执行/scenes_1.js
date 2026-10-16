// 14-02 ReWOO 与规划执行 —— 场景 1-5
// 时间一律从 MS('卡点名') 取；内容区不越过 y0 + 857（字幕带在 y = 908）。
// writeText 的第 7 个参数是「每个字的开始时间」，长度必须等于整串字符数（含空格）。

// ---------------- s01 封面：ReWOO 与规划执行 ----------------
scene(0, (sc, t) => {
  const y0 = sc.y0, CX = 960;
  const m阶段 = MS('s01_阶段', sc.st + 0.4), m副题 = MS('s01_副题', sc.st + 1.6),
        m规划 = MS('s01_规划', sc.st + 8.0), m代价 = MS('s01_代价', sc.st + 13.0);

  const F = sc.frame || (sc.frame = new Sk(8001).penOn().rrect(150, y0 + 118, 1620, 500, 26, { w: 4.6 }));
  F.at(t, sc.st + 0.15, 0.75);

  if (t >= m阶段 - 0.35) {
    const TAG = '阶段 14 · 02';
    tag(TAG, CX - tagW(TAG, 42) / 2, y0 + 190, 42, P(t, m阶段 - 0.3, 0.32));
  }

  if (t >= m副题 - 0.1) {
    const T1 = 'ReWOO';
    writeText(T1, CX, y0 + 322, hand(112, 700), C.ink, t, seq(m副题, T1, 0.09), 0.1, 'center');
  }
  if (t >= m副题 + 0.75) {
    const T2 = '与 Plan-and-Execute';
    writeText(T2, CX, y0 + 442, hand(66, 700), C.ink, t, seq(m副题 + 0.8, T2, 0.05), 0.1, 'center');
    const wl = tw(T2, hand(66, 700));
    underline(CX - wl / 2 - 14, CX + wl / 2 + 14, y0 + 486, RQ(8011), P(t, m副题 + 1.5, 0.35), 8, COL_A, m副题 + 1.5);
  }

  if (t >= m规划 + 0.4) {
    const SUB = '把规划与执行拆开';
    writeText(SUB, CX, y0 + 552, hand(38, 700), C.gray, t, seq(m规划 + 0.5, SUB, 0.07), 0.1, 'center');
  }

  // 右侧小图：一条竖直的依赖链（本集的图形母题）
  if (t >= m代价 - 0.6) {
    const CH = sc.chainDoodle || (sc.chainDoodle = new Sk(8021).penOn());
    if (!sc.chainDoodle_b) {
      for (let k = 0; k < 3; k++) CH.rrect(1512, y0 + 268 + k * 92, 96, 60, 10, { w: 3, col: k === 2 ? COL_A : C.ink });
      CH.line(1560, y0 + 332, 1560, y0 + 356, { w: 3 }); CH.line(1560, y0 + 424, 1560, y0 + 448, { w: 3 });
      sc.chainDoodle_b = 1;
    }
    CH.at(t, m代价 - 0.55, 0.6);
  }

  // 三件套色块：规划（橙底）/ 执行（墨底）/ 求解（白底）
  const chips = [['规划', COL_A, '#ffffff', m规划 + 0.9], ['执行', COL_B, '#ffffff', m代价], ['求解', null, C.ink, m代价 + 0.7]];
  const CW = 300, CHH = 104, GAP = 70, X0 = CX - (CW * 3 + GAP * 2) / 2, CY = y0 + 660;
  chips.forEach(([txt, bg, fg, tk], k) => {
    if (t < tk - 0.3) return;
    const x = X0 + k * (CW + GAP);
    const S = sc['c' + k] || (sc['c' + k] = new Sk(8031 + k).penOn());
    if (!sc['c' + k + 'b']) {
      if (bg) S.fill(rrPts(x, CY, CW, CHH, 18), bg, { fade: 1 });
      S.rrect(x, CY, CW, CHH, 18, { w: 3.8, col: bg || C.ink });
      sc['c' + k + 'b'] = 1;
    }
    S.at(t, tk - 0.25, 0.42);
    writeText(txt, x + CW / 2, CY + CHH / 2, hand(48, 700), fg, t, seq(tk + 0.15, txt, 0.09), 0.1, 'center');
  });
});

// ---------------- s02 每一步都重新思考，代价是什么？ ----------------
scene(1, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m循环 = MS('s02_循环', sc.st + 0.5), m不必 = MS('s02_不必', sc.st + 8.0),
        m先画 = MS('s02_先画', sc.st + 13.5), m本集 = MS('s02_本集', sc.st + 20.5);

  // 上：交替循环（思考 → 行动 → 观察 → 回头）
  const loop = [['思考', 220], ['行动', 740], ['观察', 1260]];
  if (t >= m循环 - 0.5) {
    const A = sc.loopAr || (sc.loopAr = new Sk(8101).penOn());
    if (!sc.loopAr_b) { A.curve([[420, y0 + 300], [760, y0 + 210], [1100, y0 + 210], [1440, y0 + 300], [1440, y0 + 560], [960, y0 + 618], [480, y0 + 560], [480, y0 + 300]], { w: 3.4, col: C.gray, seg: 12 }); sc.loopAr_b = 1; }
    A.at(t, m循环 + 0.1, 1.2);
    loop.forEach(([nm, x], k) => {
      const tk = m循环 + 0.5 + k * 0.5;
      if (t < tk - 0.4) return;
      const S = sc['l' + k] || (sc['l' + k] = new Sk(8111 + k).penOn().rrect(x, y0 + 250, 340, 120, 16, { w: 3.6, col: C.gray }));
      S.at(t, tk - 0.35, 0.42);
      writeText(nm, x + 170, y0 + 310, hand(44, 700), C.gray, t, seq(tk + 0.15, nm, 0.09), 0.1, 'center');
    });
    const LT = '上一集的循环：每一步都重新思考';
    writeText(LT, 960, y0 + 174, hand(34, 700), C.gray, t, seq(m循环 + 1.4, LT, 0.035), 0.1, 'center');
    if (t >= m不必 - 0.3) {
      const NT = '工具和依赖常常已经明确，不必每次都重新安排';
      writeText(NT, 960, y0 + 668, hand(34, 700), C.gray, t, seq(m不必, NT, 0.032), 0.1, 'center');
    }
  }
  // 下：先规划、再执行（一条直线，没有回头）
  if (t >= m先画 - 0.5) {
    const bt = [['先画好计划', 200], ['按依赖执行', 740], ['组合答案', 1280]];
    bt.forEach(([nm, x], k) => {
      const tk = m先画 + 0.3 + k * 0.5;
      if (t < tk - 0.4) return;
      const S = sc['b' + k] || (sc['b' + k] = new Sk(8121 + k).penOn().rrect(x, y0 + 712, 420, 118, 16, { w: 3.8, col: k === 1 ? COL_B : C.ink }));
      S.at(t, tk - 0.35, 0.42);
      writeText(nm, x + 210, y0 + 771, hand(42, 700), k === 1 ? COL_B : C.ink, t, seq(tk + 0.15, nm, 0.075), 0.1, 'center');
      if (k < 2) {
        const A = sc['ba' + k] || (sc['ba' + k] = new Sk(8131 + k).penOn());
        if (!sc['ba' + k + 'b']) { arrowTo(A, x + 428, y0 + 771, x + 532, y0 + 771, { w: 3.4 }); sc['ba' + k + 'b'] = 1; }
        A.at(t, tk + 0.4, 0.25);
      }
    });
  }
});

// ---------------- s03 三个角色：规划、执行、求解 ----------------
scene(2, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m规划器 = MS('s03_规划器', sc.st + 0.5), m执行器 = MS('s03_执行器', sc.st + 3.6),
        m三模型 = MS('s03_三模型', sc.st + 9.4), m脚本 = MS('s03_脚本', sc.st + 15.0);

  // 问题 → 规划器 → 计划 → 执行器 → 证据 → 求解器 → 答案
  const boxes = [['规划器', '问题 → 计划', 170, COL_A], ['执行器', '计划 → 证据', 720, COL_B], ['求解器', '证据 → 答案', 1270, C.ink]];
  boxes.forEach(([nm, sub, x, col], k) => {
    const tk = [m规划器, m执行器, m执行器 + 1.6][k];
    if (t < tk - 0.45) return;
    const S = sc['r' + k] || (sc['r' + k] = new Sk(8201 + k).penOn().rrect(x, y0 + 250, 480, 160, 16, { w: 4, col }));
    S.at(t, tk - 0.4, 0.45);
    writeText(nm, x + 240, y0 + 312, hand(48, 700), col, t, seq(tk, nm, 0.09), 0.1, 'center');
    writeText(sub, x + 240, y0 + 372, hand(30, 700), C.gray, t, seq(tk + 0.5, sub, 0.05), 0.1, 'center');
    if (k < 2) {
      const A = sc['ra' + k] || (sc['ra' + k] = new Sk(8211 + k).penOn());
      if (!sc['ra' + k + 'b']) { arrowTo(A, x + 488, y0 + 330, x + 632, y0 + 330, { w: 3.4 }); sc['ra' + k + 'b'] = 1; }
      A.at(t, tk + 0.5, 0.25);
    }
  });
  // 职责拆分 ≠ 三个模型
  if (t >= m三模型 - 0.5) {
    const S = sc.roles || (sc.roles = new Sk(8221).penOn().rrect(170, y0 + 480, 1580, 130, 16, { w: 3.6, col: C.gray }));
    S.at(t, m三模型 - 0.45, 0.45);
    const R1 = '这是职责拆分，不意味着必须调用三个模型';
    writeText(R1, 960, y0 + 524, hand(40, 700), C.ink, t, seq(m三模型, R1, 0.045), 0.1, 'center');
    if (t >= m三模型 + 1.6) {
      const R2 = '工具执行本身也不一定需要模型参与';
      writeText(R2, 960, y0 + 578, hand(32, 700), C.gray, t, seq(m三模型 + 1.65, R2, 0.04), 0.1, 'center');
    }
  }
  // 本集用的是什么
  if (t >= m脚本 - 0.5) {
    writeText('本集代码：', 170, y0 + 686, hand(40, 700), C.ink, t, seq(m脚本 - 0.4, '本集代码：', 0.07), 0.1);
    const impl = [['脚本规划器', 470], ['普通函数', 900], ['模板求解器', 1300]];
    impl.forEach(([nm, x], k) => {
      const tk = m脚本 + 0.3 + k * 0.5;
      if (t < tk - 0.3) return;
      writeText(nm, x, y0 + 686, hand(40, 700), COL_A, t, seq(tk, nm, 0.075), 0.1);
    });
    if (t >= m脚本 + 2.0) {
      const VT = '验证的是数据如何流动，没有真实模型请求';
      writeText(VT, 960, y0 + 792, hand(32, 700), C.gray, t, seq(m脚本 + 2.05, VT, 0.035), 0.1, 'center');
    }
  }
});

// ---------------- s04 把计划变成依赖图 ----------------
scene(3, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m三节点 = MS('s04_三节点', sc.st + 0.6), m首都 = MS('s04_首都', sc.st + 2.2),
        m引用 = MS('s04_引用', sc.st + 8.6), m并行 = MS('s04_并行', sc.st + 16.6);

  // 三个节点纵向串成一条链
  const nodes = [['E1', 'search 首都', '#E1'], ['E2', 'search 人口', '#E2'], ['E3', 'round_million', null]];
  if (t >= m三节点 - 0.5) {
    nodes.forEach(([id, op, ref], k) => {
      const y = y0 + 230 + k * 170, tk = m三节点 + 0.5 + k * 0.8;
      if (t < tk - 0.5) return;
      const S = sc['n' + k] || (sc['n' + k] = new Sk(8301 + k).penOn().rrect(200, y, 620, 130, 16, { w: 3.8, col: k === 2 ? COL_A : C.ink }));
      S.at(t, tk - 0.45, 0.45);
      writeText(id + '  ' + op, 240, y + 66, hand(42, 700), k === 2 ? COL_A : C.ink, t, seq(tk, id + '  ' + op, 0.055), 0.1);
      if (ref) writeText(ref, 740, y + 66, hand(38, 700), COL_B, t, seq(tk + 0.6, ref, 0.07), 0.1, 'center');
      if (k < 2) {
        const A = sc['na' + k] || (sc['na' + k] = new Sk(8311 + k).penOn());
        if (!sc['na' + k + 'b']) { arrowTo(A, 510, y + 138, 510, y + 162, { w: 3.4 }); sc['na' + k + 'b'] = 1; }
        A.at(t, tk + 0.7, 0.25);
      }
    });
  }
  // 首都那句：E1 的具体内容
  if (t >= m首都 - 0.4) {
    const S = sc.cap || (sc.cap = new Sk(8321).penOn().rrect(900, y0 + 230, 850, 130, 16, { w: 3.4, col: C.gray }));
    S.at(t, m首都 - 0.35, 0.45);
    writeText('capital of France', 1325, y0 + 296, hand(40, 700), C.ink, t, seq(m首都, 'capital of France', 0.05), 0.1, 'center');
  }
  // 引用：箭头表示必须先获得什么
  if (t >= m引用 - 0.5) {
    const A = sc.refA || (sc.refA = new Sk(8331).penOn());
    if (!sc.refA_b) { A.curve([[826, y0 + 296], [880, y0 + 340], [880, y0 + 470], [826, y0 + 470]], { w: 3.2, col: COL_B, seg: 8 }); sc.refA_b = 1; }
    A.at(t, m引用 - 0.45, 0.7);
    const RT = '第二步引用第一份证据，第三步引用第二份';
    writeText(RT, 1370, y0 + 566, hand(34, 700), COL_B, t, seq(m引用, RT, 0.04), 0.1, 'center');
    if (t >= m引用 + 1.8) {
      const RT2 = '箭头表示必须先获得什么，不能任意交换顺序';
      writeText(RT2, 1370, y0 + 630, hand(30, 700), C.gray, t, seq(m引用 + 1.85, RT2, 0.035), 0.1, 'center');
    }
  }
  // 没有并行
  if (t >= m并行 - 0.5) {
    const S = sc.par || (sc.par = new Sk(8341).penOn().rrect(170, y0 + 742, 1580, 106, 16, { w: 3.4, col: C.gray }));
    S.at(t, m并行 - 0.45, 0.45);
    const PT = '无依赖的节点才有并行机会；本例是一条链，执行器逐个运行';
    writeText(PT, 960, y0 + 795, hand(34, 700), C.gray, t, seq(m并行, PT, 0.032), 0.1, 'center');
  }
});

// ---------------- s05 证据引用如何落到工具参数 ----------------
scene(4, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m占位 = MS('s05_占位符', sc.st + 0.5), m巴黎 = MS('s05_巴黎', sc.st + 5.2),
        m一千一百 = MS('s05_一千一百万', sc.st + 10.0), m模拟表 = MS('s05_模拟表', sc.st + 17.0);

  // 上：占位符在执行时被替换成真实值
  if (t >= m占位 - 0.5) {
    const S = sc.ph || (sc.ph = new Sk(8401).penOn().rrect(200, y0 + 240, 560, 130, 16, { w: 3.8, col: COL_B }));
    S.at(t, m占位 - 0.45, 0.45);
    writeText('#E1', 480, y0 + 305, hand(52, 700), COL_B, t, seq(m占位, '#E1', 0.09), 0.1, 'center');
    const PL = '占位符：执行时才绑定真实返回值';
    writeText(PL, 480, y0 + 410, hand(32, 700), C.gray, t, seq(m占位 + 0.7, PL, 0.035), 0.1, 'center');
  }
  if (t >= m巴黎 - 0.5) {
    const A = sc.phA || (sc.phA = new Sk(8411).penOn());
    if (!sc.phA_b) { arrowTo(A, 772, y0 + 305, 900, y0 + 305, { w: 3.6, col: COL_A }); sc.phA_b = 1; }
    A.at(t, m巴黎 - 0.45, 0.3);
    const S = sc.paris || (sc.paris = new Sk(8421).penOn().rrect(910, y0 + 240, 560, 130, 16, { w: 4, col: COL_A }));
    S.at(t, m巴黎 - 0.4, 0.45);
    writeText('Paris', 1190, y0 + 305, hand(52, 700), COL_A, t, seq(m巴黎, 'Paris', 0.08), 0.1, 'center');
    const PL = '第一份证据被替换为巴黎';
    writeText(PL, 1190, y0 + 410, hand(32, 700), C.gray, t, seq(m巴黎 + 0.7, PL, 0.035), 0.1, 'center');
  }
  // 下：11.2 → 11 的取整
  if (t >= m一千一百 - 0.5) {
    const chain = [['11.2 million metro', 200, C.ink], ['round_million', 740, COL_B], ['11 million', 1280, COL_A]];
    chain.forEach(([txt, x, col], k) => {
      const tk = m一千一百 + 0.3 + k * 0.8;
      if (t < tk - 0.4) return;
      const S = sc['e' + k] || (sc['e' + k] = new Sk(8431 + k).penOn().rrect(x, y0 + 520, 420, 120, 16, { w: 3.6, col }));
      S.at(t, tk - 0.35, 0.42);
      writeText(txt, x + 210, y0 + 580, hand(38, 700), col, t, seq(tk + 0.1, txt, 0.05), 0.1, 'center');
      if (k < 2) {
        const A = sc['ea' + k] || (sc['ea' + k] = new Sk(8441 + k).penOn());
        if (!sc['ea' + k + 'b']) { arrowTo(A, x + 428, y0 + 580, x + 532, y0 + 580, { w: 3.4 }); sc['ea' + k + 'b'] = 1; }
        A.at(t, tk + 0.45, 0.25);
      }
    });
  }
  // 边界说明
  if (t >= m模拟表 - 0.5) {
    const S = sc.sim || (sc.sim = new Sk(8451).penOn().rrect(170, y0 + 700, 1580, 120, 16, { w: 3.4, col: C.orangeL }));
    S.at(t, m模拟表 - 0.45, 0.45);
    const T1 = '数字来自固定的模拟表，只用于检查引用解析与数据传递';
    writeText(T1, 960, y0 + 742, hand(34, 700), C.orangeD, t, seq(m模拟表, T1, 0.032), 0.1, 'center');
    if (t >= m模拟表 + 1.8) {
      const T2 = '既不是在线检索，也不是当前人口结论';
      writeText(T2, 960, y0 + 792, hand(30, 700), C.orangeD, t, seq(m模拟表 + 1.85, T2, 0.035), 0.1, 'center');
    }
  }
});
