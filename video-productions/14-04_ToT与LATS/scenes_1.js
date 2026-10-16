// 14-04 Tree of Thoughts 与 LATS —— 场景 1-4
// 时间一律从 MS('卡点名') 取；内容区不越过 y0 + 857（字幕带在 y = 908）。
// 注意：writeText 的第 7 个参数是「每个字的开始时间」，长度必须等于整串字符数（含空格）。

// ---------------- s01 封面：Tree of Thoughts 与 LATS ----------------
scene(0, (sc, t) => {
  const y0 = sc.y0, CX = 960;
  const m阶段 = MS('s01_阶段', sc.st + 0.4), m副题 = MS('s01_副题', sc.st + 1.5),
        m搜索 = MS('s01_搜索', sc.st + 7.0), m树 = MS('s01_一棵树', sc.st + 9.6);

  // 封面外框
  const F = sc.frame || (sc.frame = new Sk(7001).penOn().rrect(150, y0 + 118, 1620, 500, 26, { w: 4.6 }));
  F.at(t, sc.st + 0.15, 0.75);

  // 集号标签：阶段 14 · 04
  if (t >= m阶段 - 0.35) {
    const TAG = '阶段 14 · 04';
    tag(TAG, CX - tagW(TAG, 42) / 2, y0 + 190, 42, P(t, m阶段 - 0.3, 0.32));
  }

  // 主标题两行
  if (t >= m副题 - 0.1) {
    const T1 = 'Tree of Thoughts';
    writeText(T1, CX, y0 + 320, hand(96, 700), C.ink, t, seq(m副题, T1, 0.055), 0.1, 'center');
  }
  if (t >= m副题 + 0.85) {
    const T2 = '与 LATS';
    writeText(T2, CX, y0 + 438, hand(78, 700), C.ink, t, seq(m副题 + 0.9, T2, 0.08), 0.1, 'center');
    const wl = tw(T2, hand(78, 700));
    underline(CX - wl / 2 - 14, CX + wl / 2 + 14, y0 + 486, RQ(7011), P(t, m副题 + 1.5, 0.35), 8, COL_A, m副题 + 1.5);
  }

  // 封面副标题（不念，只在画面上说清这一课干什么）
  if (t >= m搜索 + 0.4) {
    const SUB = '把推理变成搜索';
    writeText(SUB, CX, y0 + 552, hand(38, 700), C.gray, t, seq(m搜索 + 0.5, SUB, 0.07), 0.1, 'center');
  }

  // 右侧小树：一条主干分三杈，第三杈结出 24
  if (t >= m树 - 0.5) {
    const TR = sc.tree || (sc.tree = new Sk(7021).penOn());
    if (!sc.tree_b) {
      TR.line(1560, y0 + 556, 1560, y0 + 376, { w: 4 });
      TR.line(1560, y0 + 376, 1474, y0 + 296, { w: 3.6 });
      TR.line(1560, y0 + 376, 1560, y0 + 276, { w: 3.6 });
      TR.line(1560, y0 + 376, 1646, y0 + 296, { w: 3.6 });
      TR.dot(1474, y0 + 288, 9, C.gray2); TR.dot(1560, y0 + 268, 9, C.gray2); TR.dot(1646, y0 + 288, 9, COL_A);
      sc.tree_b = 1;
    }
    TR.at(t, m树 - 0.45, 0.6);
    if (t >= m树 + 0.5) writeText('24', 1646, y0 + 246, hand(38, 700), COL_A, t, seq(m树 + 0.55, '24', 0.08), 0.1, 'center');
  }

  // 三件套色块：搜索（橙底）/ 自评（墨底）/ 价值（白底）
  const chips = [['搜索', COL_A, '#ffffff', m搜索 + 0.9], ['自评', COL_B, '#ffffff', m树], ['价值', null, C.ink, m树 + 0.8]];
  const CW = 300, CH = 104, GAP = 70, X0 = CX - (CW * 3 + GAP * 2) / 2, CY = y0 + 660;
  chips.forEach(([txt, bg, fg, tk], k) => {
    if (t < tk - 0.3) return;
    const x = X0 + k * (CW + GAP);
    const S = sc['c' + k] || (sc['c' + k] = new Sk(7031 + k).penOn());
    if (!sc['c' + k + 'b']) {
      if (bg) S.fill(rrPts(x, CY, CW, CH, 18), bg, { fade: 1 });
      S.rrect(x, CY, CW, CH, 18, { w: 3.8, col: bg || C.ink });
      sc['c' + k + 'b'] = 1;
    }
    S.at(t, tk - 0.25, 0.42);
    writeText(txt, x + CW / 2, CY + CH / 2, hand(48, 700), fg, t, seq(tk + 0.15, txt, 0.09), 0.1, 'center');
  });
});

// ---------------- s02 4% 到 74% ----------------
scene(1, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mG24 = MS('s02_G24', sc.st + 0.5), m凑 = MS('s02_凑出', sc.st + 1.9),
        m4 = MS('s02_4', sc.st + 5.6), m74 = MS('s02_74', sc.st + 11.0);

  // 上排：Game of 24 的四个数字 → 24
  if (t >= mG24 - 0.4) {
    writeText('Game of 24', 150, y0 + 232, hand(46, 700), C.ink, t, seq(mG24, 'Game of 24', 0.06), 0.1);
    const nums = ['4', '6', '4', '1'];
    nums.forEach((n, k) => {
      const x = 150 + k * 118, tk = mG24 + 0.5 + k * 0.22;
      if (t < tk - 0.3) return;
      const S = sc['n' + k] || (sc['n' + k] = new Sk(7101 + k).penOn().rrect(x, y0 + 292, 100, 110, 14, { w: 3.4 }));
      S.at(t, tk - 0.25, 0.4);
      writeText(n, x + 50, y0 + 347, hand(52, 700), C.ink, t, seq(tk + 0.1, n, 0.08), 0.1, 'center');
    });
    if (t >= m凑 - 0.3) {
      writeText('→', 640, y0 + 347, hand(52, 700), C.gray, t, seq(m凑 - 0.2, '→', 0.1), 0.1, 'center');
      const S = sc.sum || (sc.sum = new Sk(7111).penOn().rrect(700, y0 + 292, 150, 110, 14, { w: 4, col: COL_A }));
      S.at(t, m凑 - 0.15, 0.4);
      writeText('24', 775, y0 + 347, hand(56, 700), COL_A, t, seq(m凑 + 0.15, '24', 0.08), 0.1, 'center');
    }
  }
  // 下排：两根柱子（高度按百分比等比，8 像素 = 1 个百分点）
  const BASE = y0 + 792, SCALE = 8;
  if (t >= m4 - 0.5) {
    const H = 4 * SCALE, x = 940, w = 220;
    const S = sc.b4 || (sc.b4 = new Sk(7121).penOn());
    if (!sc.b4_b) { S.fill(rectPts(x, BASE - H, w, H), C.gray3, { fade: 1 }); S.rrect(x, BASE - H, w, H, 6, { w: 3.6, col: C.gray }); sc.b4_b = 1; }
    S.at(t, m4 - 0.45, 0.5);
    writeText('CoT', x + w / 2, BASE + 46, hand(40, 700), C.gray, t, seq(m4 + 0.1, 'CoT', 0.08), 0.1, 'center');
    writeText('4%', x + w / 2, BASE - H - 44, hand(46, 700), C.gray, t, seq(m4 + 0.4, '4%', 0.1), 0.1, 'center');
  }
  if (t >= m74 - 0.5) {
    const H = 74 * SCALE, x = 1240, w = 220;
    const S = sc.b74 || (sc.b74 = new Sk(7131).penOn());
    if (!sc.b74_b) { S.fill(rectPts(x, BASE - H, w, H), COL_A, { fade: 1, a: 0.9 }); S.rrect(x, BASE - H, w, H, 6, { w: 4, col: COL_A }); sc.b74_b = 1; }
    S.at(t, m74 - 0.45, 0.55);
    writeText('ToT', x + w / 2, BASE + 46, hand(40, 700), COL_A, t, seq(m74 + 0.1, 'ToT', 0.08), 0.1, 'center');
    writeText('74%', x + w / 2, BASE - H - 44, hand(50, 700), COL_A, t, seq(m74 + 0.45, '74%', 0.1), 0.1, 'center');
  }
  if (t >= m74 + 1.0) {
    const END = '同一个模型，差别只在有没有搜索';
    writeText(END, 940, y0 + 852, hand(34, 700), C.ink, t, seq(m74 + 1.1, END, 0.04), 0.1, 'center');
  }
});

// ---------------- s03 把推理框成搜索 ----------------
scene(2, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m三件套 = MS('s03_三件套', sc.st + 0.5), m节点 = MS('s03_节点', sc.st + 2.2),
        m根 = MS('s03_根节点', sc.st + 5.4), m自评 = MS('s03_自评', sc.st + 11.0);

  // 根节点
  if (t >= m节点 - 0.4) {
    const S = sc.root || (sc.root = new Sk(7201).penOn().rrect(700, y0 + 196, 520, 122, 16, { w: 4, col: C.ink }));
    S.at(t, m节点 - 0.35, 0.5);
    const RT = '4 6 4 1 → 24';
    writeText(RT, 960, y0 + 258, hand(46, 700), C.ink, t, seq(m节点 + 0.2, RT, 0.05), 0.1, 'center');
  }
  // 三个子节点 + 连线
  const kids = [['6 − 4 = 2', 0.2], ['4 + 1 = 5', 0.3], ['4 × 6 = 24', 0.9]];
  if (t >= m根 - 0.4) {
    kids.forEach(([txt, val], k) => {
      const x = 170 + k * 560, tk = m根 + k * 0.55;
      if (t < tk - 0.45) return;
      const A = sc['a' + k] || (sc['a' + k] = new Sk(7211 + k).penOn());
      if (!sc['a' + k + 'b']) { arrowTo(A, 960 + (k - 1) * 120, y0 + 322, x + 260, y0 + 452, { w: 3.4, col: k === 2 ? COL_A : C.ink }); sc['a' + k + 'b'] = 1; }
      A.at(t, tk - 0.4, 0.35);
      const S = sc['k' + k] || (sc['k' + k] = new Sk(7221 + k).penOn().rrect(x, y0 + 456, 520, 140, 16, { w: 3.8, col: k === 2 ? COL_A : C.ink }));
      S.at(t, tk - 0.2, 0.45);
      writeText(txt, x + 260, y0 + 526, hand(46, 700), k === 2 ? COL_A : C.ink, t, seq(tk + 0.1, txt, 0.06), 0.1, 'center');
    });
  }
  // 自评分数（承重部件）
  if (t >= m自评 - 0.4) {
    writeText('自评打分', 170, y0 + 652, hand(40, 700), COL_B, t, seq(m自评 - 0.3, '自评打分', 0.08), 0.1);
    kids.forEach(([txt, val], k) => {
      const x = 170 + k * 560, tk = m自评 + k * 0.4;
      if (t < tk - 0.3) return;
      const S = sc['v' + k] || (sc['v' + k] = new Sk(7231 + k).penOn().rrect(x + 400, y0 + 624, 120, 72, 12, { w: 3.2, col: k === 2 ? COL_A : C.gray }));
      S.at(t, tk - 0.25, 0.35);
      writeText(String(val), x + 460, y0 + 661, hand(40, 700), k === 2 ? COL_A : C.gray, t, seq(tk + 0.1, String(val), 0.08), 0.1, 'center');
    });
  }
  // 三件套注解
  if (t >= m三件套 - 0.4) {
    const LG = '节点 = 一个思考　　边 = 展开　　价值 = 有多大希望';
    writeText(LG, 960, y0 + 806, hand(38, 700), C.ink, t, seq(m三件套, LG, 0.035), 0.1, 'center');
  }
});

// ---------------- s04 ToT：每个节点上的自评 ----------------
scene(3, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mYao = MS('s04_Yao', sc.st + 0.5), m提示词 = MS('s04_提示词', sc.st + 5.4),
        mDFS = MS('s04_DFS', sc.st + 10.2), mBFS = MS('s04_BFS', sc.st + 12.4);

  // 一棵三层小树：根 → 三子 → 每子两个孙
  const L1 = [[430, y0 + 400], [960, y0 + 400], [1490, y0 + 400]];
  const L2 = [[300, y0 + 590], [560, y0 + 590], [830, y0 + 590], [1090, y0 + 590], [1330, y0 + 590], [1590, y0 + 590]];
  if (t >= mYao - 0.4) {
    L1.forEach(([x, y], k) => {
      const tk = mYao + 0.4 + k * 0.4;
      if (t < tk - 0.45) return;
      const A = sc['e' + k] || (sc['e' + k] = new Sk(7301 + k).penOn());
      if (!sc['e' + k + 'b']) { A.line(960, y0 + 240, x, y - 26, { w: 3 }); sc['e' + k + 'b'] = 1; }
      A.at(t, tk - 0.4, 0.3);
      const S = sc['d' + k] || (sc['d' + k] = new Sk(7311 + k).penOn().rrect(x - 90, y, 180, 66, 12, { w: 3.4 }));
      S.at(t, tk - 0.25, 0.4);
    });
    if (t >= mYao + 1.6) L2.forEach(([x, y], k) => {
      const tk = mYao + 1.7 + k * 0.2;
      if (t < tk - 0.4) return;
      const A = sc['f' + k] || (sc['f' + k] = new Sk(7321 + k).penOn());
      const px = L1[Math.floor(k / 2)][0];
      if (!sc['f' + k + 'b']) { A.line(px, y0 + 440, x, y - 20, { w: 2.6, col: C.gray }); sc['f' + k + 'b'] = 1; }
      A.at(t, tk - 0.35, 0.3);
      const S = sc['g' + k] || (sc['g' + k] = new Sk(7331 + k).penOn().rrect(x - 70, y - 20, 140, 54, 10, { w: 2.8, col: C.gray }));
      S.at(t, tk - 0.2, 0.35);
    });
    const YL = 'Yao 等，2023';
    writeText(YL, 1500, y0 + 190, hand(34, 700), C.gray, t, seq(mYao + 1.2, YL, 0.06), 0.1, 'center');
  }
  // 打分提示词：给一个节点贴上自评
  if (t >= m提示词 - 0.4) {
    const S = sc.sc_card || (sc.sc_card = new Sk(7341).penOn().rrect(1120, y0 + 656, 650, 150, 16, { w: 3.8, col: COL_B }));
    S.at(t, m提示词 - 0.35, 0.45);
    const PT = '打分提示词：这个思考有多大希望？';
    writeText(PT, 1445, y0 + 706, hand(34, 700), COL_B, t, seq(m提示词, PT, 0.05), 0.1, 'center');
    if (t >= m提示词 + 1.0) {
      const V = sc.val || (sc.val = new Sk(7351).penOn());
      if (!sc.val_b) { V.line(1445, y0 + 736, 1445, y0 + 756, { w: 2.6, col: C.gray }); sc.val_b = 1; }
      V.at(t, m提示词 + 1.0, 0.3);
      const VT = 'high / likely / impossible';
      writeText(VT, 1445, y0 + 782, hand(30, 700), C.gray, t, seq(m提示词 + 1.2, VT, 0.04), 0.1, 'center');
    }
  }
  // 三种遍历：BFS / DFS / beam，BFS 圈出来
  if (t >= mDFS - 0.4) {
    const ways = [['BFS', 360], ['DFS', 640], ['beam', 920]];
    writeText('遍历：', 170, y0 + 700, hand(40, 700), C.ink, t, seq(mDFS - 0.3, '遍历：', 0.08), 0.1);
    ways.forEach(([w0, x], k) => {
      const tk = mDFS + 0.3 + k * 0.45;
      if (t < tk - 0.25) return;
      writeText(w0, x, y0 + 700, hand(44, 700), k === 0 ? COL_A : C.ink, t, seq(tk, w0, 0.08), 0.1);
    });
    if (t >= mBFS - 0.3) {
      const CIR = sc.cir || (sc.cir = new Sk(7361).penOn().ellipse(400, y0 + 700, 112, 46, { w: 4.6, col: COL_A, turns: 1.12 }));
      CIR.at(t, mBFS - 0.25, 0.42);
    }
  }
});
