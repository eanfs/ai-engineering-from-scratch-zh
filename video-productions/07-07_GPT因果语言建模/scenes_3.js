// 07-07 GPT 因果语言建模 —— 场景 8-10 + 场景入口
// 时间一律从 MS('卡点名') 取；内容区不越过 y0 + 857。

// ---------------- s08 GPT 配方为什么有效 ----------------
scene(7, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m纯解码 = MS('s08_纯解码器', sc.st + 0.5), m前馈 = MS('s08_前馈', sc.st + 3.6),
        m六十亿 = MS('s08_六十亿', sc.st + 8.8);

  // 左侧：纯解码器 block 堆叠
  const BX = 210, BW = 420, BH = 96;
  for (let k = 0; k < 3; k++) {
    const tk = m纯解码 - 0.2 + k * 0.55;
    if (t < tk - 0.3) return;
    const y = y0 + 300 + (2 - k) * (BH + 22);
    const S = sc['bl' + k] || (sc['bl' + k] = new Sk(7601 + k).penOn().rrect(BX, y, BW, BH, 14, { w: 3.6, col: k === 0 ? COL_A : C.ink }));
    S.at(t, tk - 0.25, 0.4);
    writeText('masked attention + FFN', BX + BW / 2, y + BH / 2, hand(26, 700), C.ink, t, seq(tk + 0.15, 'masked attention + FFN', 0.02), 0.05, 'center');
  }
  if (t >= m纯解码 - 0.4) {
    const T = '纯解码器：没有编码器开销';
    writeText(T, BX, y0 + 246, hand(34, 700), C.ink, t, seq(m纯解码 - 0.3, T, 0.045), 0.1);
  }
  if (t >= m前馈 - 0.4) {
    const T = '每层：一次注意力 + 一个前馈';
    writeText(T, BX, y0 + 700, hand(30, 700), C.gray, t, seq(m前馈 - 0.3, T, 0.04), 0.1);
  }

  // 右侧：参数规模曲线 + 6B 涌现点
  if (t >= m纯解码 + 1.2) {
    const S = sc.curve || (sc.curve = new Sk(7611).penOn());
    if (!sc.curve_b) {
      S.curve([[980, y0 + 620], [1120, y0 + 588], [1260, y0 + 520], [1400, y0 + 414], [1540, y0 + 318], [1680, y0 + 268]], { w: 4.4, col: C.ink });
      S.line(960, y0 + 640, 1720, y0 + 640, { w: 2.6 });
      S.line(960, y0 + 640, 960, y0 + 250, { w: 2.6 });
      sc.curve_b = 1;
    }
    S.at(t, m纯解码 + 1.15, 0.9);
    writeText('模型规模', 1680, y0 + 682, hand(26, 700), C.gray, t, seq(m纯解码 + 1.6, '模型规模', 0.04), 0.08, 'right');
    writeText('能力', 916, y0 + 258, hand(26, 700), C.gray, t, seq(m纯解码 + 1.8, '能力', 0.04), 0.08, 'right');
  }
  if (t >= m六十亿 - 0.5) {
    const S = sc.dot || (sc.dot = new Sk(7621).penOn());
    if (!sc.dot_b) { S.ellipse(1280, y0 + 486, 34, 34, { w: 4.4, col: COL_A }); sc.dot_b = 1; }
    S.at(t, m六十亿 - 0.45, 0.4);
    writeText('6B 左右涌现', 1280, y0 + 414, hand(30, 700), COL_A, t, seq(m六十亿 + 0.1, '6B 左右涌现', 0.045), 0.1, 'center');
  }

  // 底部三标签
  const chips = [['数据', m六十亿 + 2.6], ['规模', m六十亿 + 3.2], ['后训练', m六十亿 + 3.8]];
  const CW = 250, CH = 84, GAP = 44, X0 = 960 - (CW * 3 + GAP * 2) / 2, CY = y0 + 748;
  chips.forEach(([txt, tk], k) => {
    if (t < tk - 0.3) return;
    const x = X0 + k * (CW + GAP);
    const S = sc['ch' + k] || (sc['ch' + k] = new Sk(7631 + k).penOn());
    if (!sc['ch' + k + 'b']) {
      S.fill(rrPts(x, CY, CW, CH, 16), k === 0 ? COL_A : C.gray3, { fade: 1 });
      S.rrect(x, CY, CW, CH, 16, { w: 3.4, col: k === 0 ? COL_A : C.ink });
      sc['ch' + k + 'b'] = 1;
    }
    S.at(t, tk - 0.25, 0.4);
    writeText(txt, x + CW / 2, CY + CH / 2, hand(40, 700), k === 0 ? '#ffffff' : C.ink, t, seq(tk + 0.15, txt, 0.08), 0.1, 'center');
  });
});

// ---------------- s09 BERT 与 GPT，一行对比 ----------------
scene(8, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m被掩 = MS('s09_被掩', sc.st + 1.6), m生成 = MS('s09_生成', sc.st + 4.8), m编码器 = MS('s09_编码器', sc.st + 9.2);

  // 中分线
  const S = sc.mid || (sc.mid = new Sk(7701).penOn().dash(958, y0 + 240, 958, y0 + 760, { w: 2.6, col: C.gray2 }));
  S.at(t, sc.st + 0.3, 0.6);

  // 左栏 GPT
  if (t >= sc.st + 0.4) {
    writeText('GPT', 300, y0 + 300, hand(64, 700), COL_A, t, seq(sc.st + 0.45, 'GPT', 0.1), 0.1, 'center');
    const F1 = 'P(x_t | x_<t)';
    writeText(F1, 300, y0 + 396, hand(36, 700), C.ink, t, seq(sc.st + 1.2, 'P(x_t | x_<t)', 0.05), 0.1, 'center');
    const N1 = '只看过去';
    writeText(N1, 300, y0 + 462, hand(30, 700), C.gray, t, seq(sc.st + 2.2, '只看过去', 0.04), 0.1, 'center');
  }
  // 右栏 BERT
  if (t >= m被掩 - 2.0) {
    writeText('BERT', 1620, y0 + 300, hand(64, 700), COL_B, t, seq(m被掩 - 1.9, 'BERT', 0.1), 0.1, 'center');
    if (t >= m被掩 - 0.5) {
      const F2 = 'P(x_masked | x_unmasked)';
      writeText(F2, 1620, y0 + 396, hand(32, 700), C.ink, t, seq(m被掩 - 0.45, 'P(x_masked | x_unmasked)', 0.03), 0.1, 'center');
    }
    if (t >= m被掩 + 0.3) {
      const N2 = '两边都看';
      writeText(N2, 1620, y0 + 462, hand(30, 700), C.gray, t, seq(m被掩 + 0.35, '两边都看', 0.04), 0.1, 'center');
    }
  }

  // 结论：生成 / 理解
  if (t >= m生成 - 0.4) {
    const T = '损失函数决定模型能不能生成';
    writeText(T, 960, y0 + 590, hand(46, 700), C.ink, t, seq(m生成 - 0.3, T, 0.045), 0.1, 'center');
  }
  if (t >= m生成 + 2.2) {
    const A = 'GPT 能';
    writeText(A, 300, y0 + 690, hand(52, 700), COL_A, t, seq(m生成 + 2.25, 'GPT 能', 0.08), 0.1, 'center');
    const B = 'BERT 不能';
    writeText(B, 1620, y0 + 690, hand(52, 700), COL_B, t, seq(m生成 + 2.7, 'BERT 不能', 0.06), 0.1, 'center');
  }
  if (t >= m编码器 - 0.4) {
    const T = '理解用编码器，生成用解码器';
    writeText(T, 960, y0 + 790, hand(40, 700), COL_A, t, seq(m编码器 - 0.3, T, 0.04), 0.1, 'center');
  }
});

// ---------------- s10 结尾：来说说你的看法 ----------------
scene(9, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m提问 = MS('s10_提问', sc.st + 0.5), m评论 = MS('s10_评论区', sc.st + 4.2), m关注 = MS('s10_关注', sc.st + 9.4);

  // 提问卡
  if (t >= m提问 - 0.5) {
    const S = sc.card || (sc.card = new Sk(7801).penOn().rrect(300, y0 + 240, 1320, 200, 24, { w: 4.4, col: COL_A }));
    S.at(t, m提问 - 0.45, 0.7);
    const T = '如果做聊天应用：采样参数重要，还是数据重要？';
    writeText(T, 960, y0 + 340, hand(44, 700), C.ink, t, seq(m提问 - 0.2, T, 0.045), 0.1, 'center');
  }

  // 评论框示意
  if (t >= m评论 - 0.5) {
    const S = sc.box || (sc.box = new Sk(7811).penOn().rrect(420, y0 + 496, 1080, 132, 20, { w: 3.8, col: C.ink }));
    S.at(t, m评论 - 0.45, 0.6);
    const PH = '写下你的答案…';
    writeText(PH, 470, y0 + 562, hand(36, 700), C.gray, t, seq(m评论 + 0.2, PH, 0.05), 0.1);
    // 光标
    const cp = P(t, m评论 + 1.2, 1.2);
    if (cp > 0 && Math.floor(t * 2) % 2 === 0) {
      const S2 = sc.cur || (sc.cur = new Sk(7821).penOn());
      S2.draw(cp);
      if (!sc.cur_b) { S2.line(470 + tw(PH, hand(36, 700)) + 12, y0 + 532, 470 + tw(PH, hand(36, 700)) + 12, y0 + 592, { w: 3.4, col: COL_A }); sc.cur_b = 1; }
      S2.at(t, m评论 + 1.2, 0.2);
    }
    // 评论图标
    if (t >= m评论 + 2.0) {
      const C1 = sc.cm || (sc.cm = new Sk(7831).penOn());
      if (!sc.cm_b) {
        C1.rrect(1240, y0 + 530, 200, 68, 16, { w: 3.2, col: COL_A });
        C1.line(1290, y0 + 598, 1272, y0 + 622, { w: 3.2, col: COL_A });
        sc.cm_b = 1;
      }
      C1.at(t, m评论 + 1.95, 0.4);
      writeText('发评论', 1340, y0 + 564, hand(30, 700), COL_A, t, seq(m评论 + 2.2, '发评论', 0.06), 0.1, 'center');
    }
  }

  // 关注提示
  if (t >= m关注 - 0.5) {
    const S = sc.fol || (sc.fol = new Sk(7841).penOn());
    if (!sc.fol_b) {
      S.line(700, y0 + 726, 1220, y0 + 726, { w: 3.4, col: COL_A });
      sc.fol_b = 1;
    }
    S.at(t, m关注 - 0.45, 0.5);
    const T = '关注这个系列 · 下一集：T5 与 BART';
    writeText(T, 960, y0 + 790, hand(40, 700), COL_A, t, seq(m关注 - 0.1, T, 0.045), 0.1, 'center');
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
