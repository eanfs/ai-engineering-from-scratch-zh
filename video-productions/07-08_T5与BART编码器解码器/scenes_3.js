// 07-08 T5 与 BART —— 场景 8-10 + 场景入口

// ---------------- s08 实跑：五种噪声长什么样 ----------------
scene(7, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m差别 = MS('n_差别', sc.st + 0.4), m占位 = MS('n_占位', sc.st + 3.2),
        m填充 = MS('n_填充', sc.st + 7.6), m旋转 = MS('n_旋转', sc.st + 12.4);

  if (t >= m差别 - 0.4) {
    writeText('code/main.py 实跑输出', 150, y0 + 196, hand(26, 700), C.gray, t, seq(m差别 - 0.3, 'code/main.py 实跑输出', 0.025), 0.08);
    writeText('original:', 150, y0 + 254, hand(26, 700), C.gray, t, seq(m差别 - 0.1, 'original:', 0.03), 0.06);
    const ORIG = 'the quick brown fox jumps over the lazy dog a stitch in time saves';
    writeText(ORIG, 330, y0 + 254, hand(26, 700), C.ink, t, seq(m差别 + 0.1, ORIG, 0.012), 0.04);
  }

  const rows = [
    { tk: m差别 + 1.2, label: 'token mask:', text: '<mask> quick brown fox jumps over the lazy <mask> <mask> stitch in time <mask>' },
    { tk: m占位 + 0.4, label: 'token delete:', text: 'the quick jumps over the lazy dog a stitch time saves' },
    { tk: m填充 - 0.4, label: 'text infill:', text: '<mask> brown fox <mask> the lazy dog a stitch in time saves' },
    { tk: m填充 + 2.2, label: 'sentence permute:', text: 'language models learn patterns / a stitch in time / the quick brown fox' },
    { tk: m旋转 - 0.3, label: 'document rotate:', text: 'stitch in time saves the quick brown fox jumps over the lazy dog a' }
  ];
  rows.forEach((r, k) => {
    if (t < r.tk - 0.3) return;
    const y = y0 + 340 + k * 94;
    writeText(r.label, 150, y, hand(24, 700), C.gray, t, seq(r.tk - 0.25, r.label, 0.02), 0.05);
    writeText(r.text, 380, y, hand(24, 700), k === 3 ? COL_A : C.ink, t, seq(r.tk + 0.05, r.text, 0.008), 0.03);
  });

  if (t >= m旋转 + 1.6) {
    writeText('有的留占位，有的真删，有的只留一个掩码让模型猜长度', 960, y0 + 812, hand(32, 700), COL_A, t, seq(m旋转 + 1.65, '有的留占位，有的真删，有的只留一个掩码让模型猜长度', 0.03), 0.08, 'center', false);
  }
});

// ---------------- s09 什么时候还选编码器-解码器 ----------------
scene(8, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m翻译 = MS('s_翻译', sc.st + 0.5), mWhisper = MS('s_whisper', sc.st + 4.2), m纯解 = MS('s_纯解码', sc.st + 10.2);

  (sc.mid || (sc.mid = new Sk(8001).penOn().dash(958, y0 + 230, 958, y0 + 720, { w: 2.6, col: C.gray2 }))).at(t, sc.st + 0.25, 0.6);

  // 左：仍然首选
  if (t >= m翻译 - 0.4) {
    writeText('仍然首选', 480, y0 + 268, hand(40, 700), COL_A, t, seq(m翻译 - 0.3, '仍然首选', 0.06), 0.1, 'center', false);
    writeText('翻译', 480, y0 + 366, hand(42, 700), C.ink, t, seq(m翻译 + 0.1, '翻译', 0.08), 0.1, 'center', false);
    writeText('语音转文本', 480, y0 + 452, hand(42, 700), C.ink, t, seq(mWhisper - 0.2, '语音转文本', 0.06), 0.1, 'center', false);
    writeText('Whisper 就是这一类', 480, y0 + 528, hand(28, 700), C.gray, t, seq(mWhisper + 0.4, 'Whisper 就是这一类', 0.04), 0.08, 'center', false);
    const S = sc.tick1 || (sc.tick1 = new Sk(8011).penOn().poly([[300, y0 + 352], [318, y0 + 372], [352, y0 + 330]], { w: 6, col: COL_A }));
    S.at(t, m翻译 + 0.5, 0.3);
    const S2 = sc.tick2 || (sc.tick2 = new Sk(8012).penOn().poly([[300, y0 + 438], [318, y0 + 458], [352, y0 + 416]], { w: 6, col: COL_A }));
    S2.at(t, mWhisper + 0.2, 0.3);
  }

  // 右：更适合纯解码器
  if (t >= m纯解 - 0.4) {
    writeText('更适合纯解码器', 1440, y0 + 268, hand(40, 700), COL_B, t, seq(m纯解 - 0.3, '更适合纯解码器', 0.05), 0.1, 'center', false);
    writeText('聊天', 1440, y0 + 366, hand(42, 700), C.ink, t, seq(m纯解 + 0.2, '聊天', 0.08), 0.1, 'center', false);
    writeText('代码补全', 1440, y0 + 452, hand(42, 700), C.ink, t, seq(m纯解 + 0.8, '代码补全', 0.06), 0.1, 'center', false);
    const S3 = sc.cross1 || (sc.cross1 = new Sk(8013).penOn());
    if (!sc.cross1_b) { S3.line(1250, y0 + 340, 1300, y0 + 390, { w: 6, col: COL_B }); S3.line(1300, y0 + 340, 1250, y0 + 390, { w: 6, col: COL_B }); sc.cross1_b = 1; }
    S3.at(t, m纯解 + 0.5, 0.3);
    const S4 = sc.cross2 || (sc.cross2 = new Sk(8014).penOn());
    if (!sc.cross2_b) { S4.line(1250, y0 + 426, 1300, y0 + 476, { w: 6, col: COL_B }); S4.line(1300, y0 + 426, 1250, y0 + 476, { w: 6, col: COL_B }); sc.cross2_b = 1; }
    S4.at(t, m纯解 + 1.1, 0.3);
  }

  if (t >= m纯解 + 3.4) {
    writeText('摘要、结构化抽取：两种都能做，看延迟与质量', 960, y0 + 790, hand(34, 700), C.gray, t, seq(m纯解 + 3.45, '摘要、结构化抽取：两种都能做，看延迟与质量', 0.03), 0.08, 'center', false);
  }
});

// ---------------- s10 结尾：说说你的选择 ----------------
scene(9, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const m提问 = MS('e_提问', sc.st + 0.4), m评论 = MS('e_评论区', sc.st + 4.0), m关注 = MS('e_关注', sc.st + 8.6);

  if (t >= m提问 - 0.5) {
    const S = sc.card || (sc.card = new Sk(8101).penOn().rrect(300, y0 + 240, 1320, 200, 24, { w: 4.4, col: COL_A }));
    S.at(t, m提问 - 0.45, 0.7);
    writeText('翻译/摘要产品：选 T5，还是直接用大模型？', 960, y0 + 340, hand(44, 700), C.ink, t, seq(m提问 - 0.2, '翻译/摘要产品：选 T5，还是直接用大模型？', 0.04), 0.1, 'center', false);
  }

  if (t >= m评论 - 0.5) {
    const S = sc.box || (sc.box = new Sk(8111).penOn().rrect(420, y0 + 496, 1080, 132, 20, { w: 3.8, col: C.ink }));
    S.at(t, m评论 - 0.45, 0.6);
    const PH = '把你的理由写在评论区…';
    writeText(PH, 470, y0 + 562, hand(34, 700), C.gray, t, seq(m评论 + 0.2, PH, 0.045), 0.1, 'left', false);
    if (t >= m评论 + 1.4) {
      const C1 = sc.cm || (sc.cm = new Sk(8121).penOn());
      if (!sc.cm_b) { C1.rrect(1240, y0 + 530, 200, 68, 16, { w: 3.2, col: COL_A }); C1.line(1290, y0 + 598, 1272, y0 + 622, { w: 3.2, col: COL_A }); sc.cm_b = 1; }
      C1.at(t, m评论 + 1.35, 0.4);
      writeText('发评论', 1340, y0 + 564, hand(30, 700), COL_A, t, seq(m评论 + 1.6, '发评论', 0.06), 0.1, 'center', false);
    }
  }

  if (t >= m关注 - 0.5) {
    const S = sc.fol || (sc.fol = new Sk(8131).penOn());
    if (!sc.fol_b) { S.line(700, y0 + 726, 1220, y0 + 726, { w: 3.4, col: COL_A }); sc.fol_b = 1; }
    S.at(t, m关注 - 0.45, 0.5);
    writeText('关注这个系列 · 下一集：Vision Transformer', 960, y0 + 790, hand(38, 700), COL_A, t, seq(m关注 - 0.1, '关注这个系列 · 下一集：Vision Transformer', 0.04), 0.1, 'center', false);
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
