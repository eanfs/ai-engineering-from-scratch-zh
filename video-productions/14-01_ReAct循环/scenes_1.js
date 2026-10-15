
// ---------------- s01 一次问答，和一次任务差在哪 ----------------
scene(0, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mAns = MS('s01_回答', sc.st + 2), mSave = MS('s01_保存', sc.st + 3.2),
        mRead = MS('s01_读回', sc.st + 8), mCheck = MS('s01_可检查', sc.st + 10.5),
        mLoop = MS('s01_循环', sc.st + 13), mEnd = MS('s01_结束', sc.st + 15);
  // 左：一句回答 + 打叉
  if (t >= mAns - 0.5) {
    const S = sc.bub || (sc.bub = new Sk(3101).penOn().rrect(150, y0 + 210, 500, 150, 18, { w: 3.6 }));
    S.at(t, mAns - 0.45, 0.5);
    writeText('含税价 = 138', 200, y0 + 288, hand(46, 700), C.ink, t, seq(mAns + 0.2, '含税价 = 138', 0.07), 0.1);
    label('一句看似正确的回答', 150, y0 + 400, t, mAns + 0.5, 40);
    const X = sc.cross || (sc.cross = new Sk(3102).penOn());
    if (!sc.cross_b) { X.line(120, y0 + 180, 690, y0 + 390, { w: 7, col: COL_A, a: 0.45 }); X.line(690, y0 + 180, 120, y0 + 390, { w: 7, col: COL_A, a: 0.45 }); sc.cross_b = 1; }
    X.at(t, mAns + 1.0, 0.35);
  }
  // 右：任务四步 —— 计算 → 保存 → 读回 → 可检查
  const steps = [['计算', mAns + 1.1], ['保存', mSave], ['读回', mRead], ['可检查', mCheck]];
  for (let k = 0; k < 4; k++) {
    const x = 830 + k * 240, tk = steps[k][1];
    if (t < tk - 0.35) continue;
    const S = sc['st' + k] || (sc['st' + k] = new Sk(3111 + k).penOn().rrect(x, y0 + 220, 200, 120, 14, { w: 3.4, col: k === 3 ? COL_A : C.ink }));
    S.at(t, tk, 0.45);
    writeText(steps[k][0], x + 100, y0 + 280, hand(40, 700), k === 3 ? COL_A : C.ink, t, seq(tk + 0.25, steps[k][0], 0.08), 0.1, 'center');
    if (k < 3) { const A = sc['sa' + k] || (sc['sa' + k] = new Sk(3121 + k).penOn()); if (!sc['sa' + k + 'b']) { arrowTo(A, x + 208, y0 + 280, x + 230, y0 + 280, { w: 3 }); sc['sa' + k + 'b'] = 1; } A.at(t, tk + 0.4, 0.22); }
  }
  label('工具执行接入对话 → 可检查的连续过程', 830, y0 + 400, t, mRead + 0.4, 40);
  // 底部：观察 → 思考 → 行动 循环 + 明确条件结束
  const loop = [['观察', mLoop], ['思考', mLoop + 0.5], ['行动', mLoop + 1.0]];
  for (let k = 0; k < 3; k++) {
    const x = 260 + k * 400, tk = loop[k][1];
    if (t < tk - 0.35) continue;
    const S = sc['lp' + k] || (sc['lp' + k] = new Sk(3131 + k).penOn().rrect(x, y0 + 540, 300, 120, 60, { w: 3.4 }));
    S.at(t, tk, 0.45);
    writeText(loop[k][0], x + 150, y0 + 600, hand(44, 700), C.ink, t, seq(tk + 0.25, loop[k][0], 0.09), 0.1, 'center');
    if (k < 2) { const A = sc['la' + k] || (sc['la' + k] = new Sk(3141 + k).penOn()); if (!sc['la' + k + 'b']) { arrowTo(A, x + 308, y0 + 600, x + 388, y0 + 600, { w: 3 }); sc['la' + k + 'b'] = 1; } A.at(t, tk + 0.4, 0.22); }
  }
  if (t >= mLoop + 1.2) {
    const A = sc.ret || (sc.ret = new Sk(3151).penOn());
    if (!sc.ret_b) { A.curve([[1560, y0 + 600], [1660, y0 + 700], [960, y0 + 720], [260, y0 + 700], [410, y0 + 668]], { w: 3.4, col: COL_A }); sc.ret_b = 1; }
    A.at(t, mLoop + 1.2, 0.5);
  }
  if (t >= mEnd) {
    writeText('明确条件结束整个任务', 900, y0 + 800, hand(46, 700), COL_A, t, seq(mEnd + 0.05, '明确条件结束整个任务', 0.06), 0.1, 'center');
  }
});

// ---------------- s02 观察 → 思考 → 行动 ----------------
scene(1, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mObs = MS('s02_观察', sc.st + 0.5), mDec = MS('s02_决策器', sc.st + 2.5), mRun = MS('s02_运行时', sc.st + 5),
        mEg = MS('s02_例子', sc.st + 7), m18 = MS('s02_十八', sc.st + 9),
        mBack = MS('s02_回流', sc.st + 11), mChk = MS('s02_核对', sc.st + 13);
  const boxes = [['观察', '用户请求 + 工具结果', 190, mObs, C.ink], ['思考', '决策器结合历史', 760, mDec, C.ink], ['行动', '运行时执行工具', 1330, mRun, C.ink]];
  for (let k = 0; k < 3; k++) {
    const [nm, sub, x, tk, col] = boxes[k];
    if (t < tk - 0.4) continue;
    const S = sc['bx' + k] || (sc['bx' + k] = new Sk(3201 + k).penOn().rrect(x, y0 + 230, 400, 160, 18, { w: 3.6, col }));
    S.at(t, tk, 0.5);
    writeText(nm, x + 200, y0 + 292, hand(50, 700), col, t, seq(tk + 0.25, nm, 0.09), 0.1, 'center');
    writeText(sub, x + 200, y0 + 352, hand(30, 700), C.ink, t, seq(tk + 0.6, sub, 0.05), 0.1, 'center');
    if (k < 2) { const A = sc['ar' + k] || (sc['ar' + k] = new Sk(3221 + k).penOn()); if (!sc['ar' + k + 'b']) { arrowTo(A, x + 408, y0 + 310, x + 562, y0 + 310, { w: 3.4 }); sc['ar' + k + 'b'] = 1; } A.at(t, tk + 0.55, 0.3); }
  }
  // 例子
  if (t >= mEg) {
    writeText('120 × 15% = 18', 500, y0 + 500, hand(48, 700), COL_A, t, seq(mEg + 0.1, '120 × 15% = 18', 0.06), 0.1);
    writeText('新观察写入历史 → 进入下一轮决策', 500, y0 + 570, hand(38, 700), C.ink, t, seq(m18 + 0.1, '新观察写入历史 → 进入下一轮决策', 0.05), 0.1);
  }
  // 回流箭头
  if (t >= mBack - 0.4) {
    const A = sc.bk || (sc.bk = new Sk(3231).penOn());
    if (!sc.bk_b) { A.curve([[1530, y0 + 400], [1600, y0 + 640], [960, y0 + 700], [300, y0 + 640], [390, y0 + 404]], { w: 4, col: COL_A }); sc.bk_b = 1; }
    A.at(t, mBack - 0.35, 0.65);
    if (t >= mChk) writeText('结果不能只打印给人看，要进入后续上下文', 700, y0 + 790, hand(40, 700), COL_A, t, seq(mChk, '结果不能只打印给人看，要进入后续上下文', 0.05), 0.1, 'center');
  }
});

// ---------------- s03 ReAct：标准格式 ----------------
scene(2, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mRe = MS('s03_react', sc.st + 0.5), mPlan = MS('s03_打算', sc.st + 2), mAct = MS('s03_调用', sc.st + 4),
        mObs = MS('s03_观察', sc.st + 6), mPrice = MS('s03_原价', sc.st + 8), m138 = MS('s03_138', sc.st + 10),
        mTeach = MS('s03_教学', sc.st + 13);
  // 两轮轨迹：Thought / Action / Observation
  const rows = [[['Thought', mPlan], ['Action', mAct], ['Observation', mObs]],
                [['Thought', mObs + 1.6], ['Action', mObs + 2.4], ['Observation', mObs + 3.2]]];
  for (let r = 0; r < 2; r++) for (let k = 0; k < 3; k++) {
    const [nm, tk] = rows[r][k];
    const x = 190 + k * 540, y = y0 + 200 + r * 180;
    if (t < tk - 0.4) continue;
    const S = sc['tr' + r + k] || (sc['tr' + r + k] = new Sk(3301 + r * 10 + k).penOn().rrect(x, y, 480, 130, 14, { w: 3.2, col: k === 0 ? C.ink : k === 1 ? COL_A : COL_B }));
    S.at(t, tk, 0.45);
    writeText(nm, x + 40, y + 46, hand(42, 700), k === 0 ? C.ink : k === 1 ? COL_A : COL_B, t, seq(tk + 0.25, nm, 0.07), 0.1);
    if (k < 2) { const A = sc['ta' + r + k] || (sc['ta' + r + k] = new Sk(3331 + r * 10 + k).penOn()); if (!sc['ta' + r + k + 'b']) { arrowTo(A, x + 488, y + 65, x + 528, y + 65, { w: 3 }); sc['ta' + r + k + 'b'] = 1; } A.at(t, tk + 0.45, 0.25); }
  }
  // 数字链
  if (t >= mPrice - 0.4) {
    const S = sc.nums || (sc.nums = new Sk(3361).penOn());
    if (!sc.nums_b) { S.line(300, y0 + 620, 1620, y0 + 620, { w: 2.6, col: C.gray2 }); sc.nums_b = 1; }
    S.at(t, mPrice - 0.35, 0.5);
    writeText('原价 120', 320, y0 + 690, hand(44, 700), C.ink, t, seq(mPrice, '原价 120', 0.06), 0.1);
    if (t >= mPrice + 1.2) writeText('税额 18', 820, y0 + 690, hand(44, 700), COL_A, t, seq(mPrice + 1.2, '税额 18', 0.06), 0.1);
    if (t >= m138) writeText('总价 138', 1320, y0 + 690, hand(44, 700), COL_A, t, seq(m138, '总价 138', 0.06), 0.1);
  }
  if (t >= mTeach) writeText('思考文本是预先编写的教学脚本，不代表真实模型的内部推理', 960, y0 + 800, hand(34, 700), C.gray, t, seq(mTeach, '思考文本是预先编写的教学脚本', 0.05), 0.1, 'center');
});

// ---------------- s04 原生推理：控制流仍然相同 ----------------
scene(3, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mNat = MS('s04_原生', sc.st + 0.5), mTag = MS('s04_标签', sc.st + 3),
        mProto = MS('s04_协议', sc.st + 6), mPriv = MS('s04_私有', sc.st + 8),
        mSend = MS('s04_回传', sc.st + 10), mOff = MS('s04_离线', sc.st + 12);
  // 两个入口
  if (t >= mNat - 0.5) {
    const A = sc.in1 || (sc.in1 = new Sk(3401).penOn().rrect(160, y0 + 220, 420, 140, 16, { w: 3.4 }));
    const B = sc.in2 || (sc.in2 = new Sk(3402).penOn().rrect(160, y0 + 420, 420, 140, 16, { w: 3.4, col: COL_A }));
    A.at(t, mNat - 0.45, 0.5); B.at(t, mNat + 0.2, 0.5);
    writeText('普通回答', 200, y0 + 268, hand(42, 700), C.ink, t, seq(mNat + 0.2, '普通回答', 0.07), 0.1);
    if (t >= mTag) writeText('打印一行思考标签', 200, y0 + 322, hand(30, 700), C.gray, t, seq(mTag, '打印一行思考标签', 0.05), 0.1);
    writeText('原生推理', 200, y0 + 468, hand(42, 700), COL_A, t, seq(mNat + 0.6, '原生推理', 0.07), 0.1);
    writeText('推理状态由接口自己保存', 200, y0 + 522, hand(30, 700), C.gray, t, seq(mNat + 1.0, '推理状态由接口自己保存', 0.05), 0.1);
    const AR = sc.ar || (sc.ar = new Sk(3411).penOn());
    if (!sc.ar_b) { arrowTo(AR, 588, y0 + 290, 800, y0 + 340, { w: 3 }); arrowTo(AR, 588, y0 + 490, 800, y0 + 430, { w: 3, col: COL_A }); sc.ar_b = 1; }
    AR.at(t, mNat + 1.4, 0.5);
  }
  // 控制流方框
  if (t >= mProto - 0.5) {
    const S = sc.flow || (sc.flow = new Sk(3421).penOn().rrect(820, y0 + 250, 520, 260, 18, { w: 3.8 }));
    S.at(t, mProto - 0.45, 0.5);
    writeText('控制流不变', 1080, y0 + 305, hand(44, 700), C.ink, t, seq(mProto + 0.2, '控制流不变', 0.08), 0.1, 'center');
    if (t >= mPriv) writeText('推理状态按各自协议，不能互相搬运', 1080, y0 + 375, hand(30, 700), C.gray, t, seq(mPriv, '推理状态按各自协议', 0.05), 0.1, 'center');
    if (t >= mSend) {
      writeText('工具请求 → 执行 → 结果回传', 1080, y0 + 455, hand(34, 700), COL_A, t, seq(mSend, '工具请求 → 执行 → 结果回传', 0.05), 0.1, 'center');
    }
  }
  if (t >= mOff - 0.4) {
    writeText('本集只验证离线控制流，没有接入真实供应商', 960, y0 + 700, hand(38, 700), C.gray, t, seq(mOff, '本集只验证离线控制流', 0.05), 0.1, 'center');
  }
});

// ---------------- s05 五大要素 ----------------
scene(4, (sc, t) => {
  const y0 = sc.y0; sceneHead(sc, t);
  const mBuf = MS('s05_缓冲区', sc.st + 0.6), mReg = MS('s05_注册表', sc.st + 2.5),
        mFmt = MS('s05_格式化', sc.st + 5), mStop = MS('s05_停止', sc.st + 7), mBud = MS('s05_预算', sc.st + 9),
        mList = MS('s05_清单', sc.st + 11);
  const items = [['消息缓冲区', '保留过程', 150, mBuf], ['工具注册表', '名称 → 函数', 490, mReg],
                 ['观察格式化器', '结果变成可读信息', 830, mFmt], ['停止条件', '何时退出', 1170, mStop],
                 ['轮数预算', '硬上限', 1510, mBud]];
  for (let k = 0; k < 5; k++) {
    const [nm, sub, x, tk] = items[k];
    if (t < tk - 0.4) continue;
    const S = sc['bx' + k] || (sc['bx' + k] = new Sk(3501 + k).penOn().rrect(x, y0 + 260, 290, 180, 16, { w: 3.4, col: k >= 3 ? COL_A : C.ink }));
    S.at(t, tk, 0.5);
    writeText(nm, x + 145, y0 + 330, hand(38, 700), k >= 3 ? COL_A : C.ink, t, seq(tk + 0.25, nm, 0.07), 0.1, 'center');
    writeText(sub, x + 145, y0 + 392, hand(28, 700), C.ink, t, seq(tk + 0.6, sub, 0.05), 0.1, 'center');
    writeText('0' + (k + 1), x + 30, y0 + 296, hand(28, 700), C.gray, t, seq(tk + 0.1, '0' + (k + 1), 0.08), 0.1);
  }
  if (t >= mFmt - 0.6) {
    const L = sc.line1 || (sc.line1 = new Sk(3521).penOn());
    if (!sc.line1_b) { L.line(150, y0 + 500, 1780, y0 + 500, { w: 3, col: C.orange }); sc.line1_b = 1; }
    L.at(t, mFmt - 0.55, 0.6);
    writeText('连接决策与执行', 960, y0 + 560, hand(38, 700), C.ink, t, seq(mFmt + 0.2, '连接决策与执行', 0.07), 0.1, 'center');
  }
  if (t >= mList) writeText('这五项是本课实现的检查清单：能做事、能记住、知道何时停下', 960, y0 + 720, hand(38, 700), COL_A, t, seq(mList, '这五项是本课实现的检查清单', 0.05), 0.1, 'center');
});
