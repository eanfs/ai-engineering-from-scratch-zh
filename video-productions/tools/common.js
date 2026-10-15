// ===================== 手绘笔记公共底座（13/9 场通用） =====================
// 版式：整片一张竖长笔记纸，宽 1920，每场 SEC_H 像素；镜头往下「读」，每场一个镜头。
// 所有动作都卡在 TL 的卡点上（MS/markTimes），页面里不写死秒数。
const SEC_H = 1000;
const SCENES = TL.shots.map((s, i) => ({ i, s, y0: i * SEC_H, st: s.start, en: s.end }));
const D = [];
const scene = (i, fn) => { D[i] = fn; };
const RQ = (n) => mulberry32(n);
function gridSk(S, x, y, w, h, nx, ny, o = {}) {
  const ww = o.w ?? 2.2, col = o.col;
  for (let i = 0; i <= nx; i++) S.line(x + i * w / nx, y, x + i * w / nx, y + h, { w: ww, col });
  for (let j = 0; j <= ny; j++) S.line(x, y + j * h / ny, x + w, y + j * h / ny, { w: ww, col });
  return S;
}
function arrowTo(S, x0, y0, x1, y1, o = {}) {
  const w = o.w ?? 3.2, col = o.col ?? C.ink, L = o.head ?? 18;
  S.line(x0, y0, x1, y1, { w, col });
  const a = Math.atan2(y1 - y0, x1 - x0);
  S.line(x1, y1, x1 - Math.cos(a - 0.42) * L, y1 - Math.sin(a - 0.42) * L, { w, col });
  S.line(x1, y1, x1 - Math.cos(a + 0.42) * L, y1 - Math.sin(a + 0.42) * L, { w, col });
  return S;
}
function sceneHead(sc, t) {
  const { s, y0, st, i } = sc;
  tag('@' + (i + 1), 92, y0 + 96, 40, P(t, st, 0.25));
  const tf = hand(58, 700), tt = seq(st + 0.18, s.title, 0.055), twd = tw(s.title, tf);
  const tx = 96 + tagW('@' + (i + 1), 40) + 26;
  writeText(s.title, tx, y0 + 96, tf, C.ink, t, tt, 0.09);
  underline(tx, tx + twd, y0 + 136, RQ(700 + i), P(t, tt[tt.length - 1], 0.3), 6, C.orange, tt[tt.length - 1]);
}
function label(str, x, y, t, t0, size = 40, step = 0.07) {
  writeText(str, x, y, hand(size, 700), C.ink, t, seq(t0, str, step), 0.09);
}
function shapeBox(S, x, y, w, h, o = {}) { S.rrect(x, y, w, h, o.r ?? 14, { w: o.w ?? 3.4 }); return S; }
function miniMat(S, x, y, size, n, seed, o = {}) { gridSk(S, x, y, size, size, n, n, { w: o.w ?? 2, col: o.col }); return { x, y, size, n }; }
// 一个「卡片」：手绘框 + 居中标题（标题逐字写出）
function card(sc, key, x, y, w, h, tk, t, text, o = {}) {
  if (t < tk - 0.35) return;
  const S = sc[key] || (sc[key] = new Sk(o.seed ?? 3001).penOn().rrect(x, y, w, h, o.r ?? 16, { w: o.w ?? 3.4, col: o.col }));
  S.at(t, tk, 0.45);
  writeText(text, x + w / 2, y + h / 2, hand(o.size ?? 44, 700), o.tcol ?? C.ink, t, seq(tk + 0.28, text, 0.07), 0.1, 'center');
}
