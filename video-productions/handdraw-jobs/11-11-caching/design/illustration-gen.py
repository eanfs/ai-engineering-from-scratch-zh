#!/usr/bin/env python3
"""Author the 07-05 illustrations locally as industrial-marker diagrams.

No image API is used. Every page is drawn on warm paper with dark marker
outlines, warm-yellow fills and brown streaks, then downsampled so the
hand-drawn strokes stay crisp.
Run with the handdrawn-explainer-video venv Python.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import random
import numpy as np

W, H, S = 1600, 900, 2
OUT = Path(__file__).resolve().parent.parent / "inputs"
FONT = "/Applications/MiniMax Design.app/Contents/Resources/app-resources/fonts/NotoSansCJKsc-Regular.otf"
INK = (43, 47, 51)
PAPER = (253, 253, 247)
YELLOW = (232, 184, 75)
BROWN = (138, 106, 59)
METAL = (154, 163, 168)
GREY = (120, 116, 106)


def font(size):
    return ImageFont.truetype(FONT, int(size * S))


def sc(v):
    return int(round(v * S))


class Sheet:
    def __init__(self, seed=705):
        self.img = Image.new("RGB", (W * S, H * S), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.rng = random.Random(seed)

    # ---------------------------------------------------------------- primitives
    def line(self, pts, width=8, fill=INK, dash=None):
        pts = [(sc(x), sc(y)) for x, y in pts]
        if not dash:
            for pass_index in range(2):
                jittered = [(x + self.rng.uniform(-2.0, 2.0) * S,
                             y + self.rng.uniform(-2.0, 2.0) * S) for x, y in pts]
                stroke = max(1, sc(width * (1.0 if pass_index == 0 else 0.55)))
                self.d.line(jittered, fill=fill, width=stroke, joint="curve")
            return
        for a, b in zip(pts, pts[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            length = math.hypot(dx, dy)
            if length == 0:
                continue
            ux, uy = dx / length, dy / length
            t = 0.0
            while t < length:
                e = min(t + sc(dash), length)
                self.d.line([(a[0] + ux * t, a[1] + uy * t), (a[0] + ux * e, a[1] + uy * e)],
                            fill=fill, width=sc(width))
                t = e + sc(dash * 0.7)

    def arrow(self, x1, y1, x2, y2, width=8, head=22, fill=INK, dash=None):
        ang = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - head * 0.9 * math.cos(ang), y2 - head * 0.9 * math.sin(ang)
        self.line([(x1, y1), (bx, by)], width=width, fill=fill, dash=dash)
        h = head
        p1 = (sc(x2), sc(y2))
        p2 = (sc(x2 - h * math.cos(ang - 0.45)), sc(y2 - h * math.sin(ang - 0.45)))
        p3 = (sc(x2 - h * math.cos(ang + 0.45)), sc(y2 - h * math.sin(ang + 0.45)))
        self.d.polygon([p1, p2, p3], fill=fill)

    def box(self, x1, y1, x2, y2, r=16, width=9, fill=None, outline=INK):
        self.d.rounded_rectangle([sc(x1), sc(y1), sc(x2), sc(y2)], radius=sc(r),
                                 fill=fill, outline=outline, width=sc(width))
        dx, dy = self.rng.uniform(-2, 2), self.rng.uniform(-2, 2)
        self.d.rounded_rectangle([sc(x1 + dx), sc(y1 + dy), sc(x2 + dx), sc(y2 + dy)],
                                 radius=sc(r), outline=outline, width=max(1, sc(width * 0.45)))

    def circle(self, cx, cy, r, width=9, fill=None, outline=INK):
        self.d.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)],
                       fill=fill, outline=outline, width=sc(width))
        dx, dy = self.rng.uniform(-2, 2), self.rng.uniform(-2, 2)
        self.d.ellipse([sc(cx - r + dx), sc(cy - r + dy), sc(cx + r + dx), sc(cy + r + dy)],
                       outline=outline, width=max(1, sc(width * 0.45)))

    def streaks(self, box, base=YELLOW, color=BROWN, step=38, width=2, angle=35):
        x1, y1, x2, y2 = box
        layer = Image.new("RGB", self.img.size, base)
        ld = ImageDraw.Draw(layer)
        diag = math.hypot(x2 - x1, y2 - y1)
        dx, dy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        n = int(diag * 1.8 / step) + 2
        ox, oy = (x1 + x2) / 2, (y1 + y2) / 2
        for i in range(-n, n):
            px, py = ox - dy * i * step, oy + dx * i * step
            ld.line([(sc(px - dx * diag), sc(py - dy * diag)), (sc(px + dx * diag), sc(py + dy * diag))],
                    fill=color, width=sc(width))
        mask = Image.new("L", self.img.size, 0)
        ImageDraw.Draw(mask).rectangle([sc(x1), sc(y1), sc(x2), sc(y2)], fill=255)
        self.img.paste(layer, (0, 0), mask)
        self.d = ImageDraw.Draw(self.img)

    def hatch(self, box, step=26, width=3, angle=45, fill=INK):
        x1, y1, x2, y2 = box
        mask = Image.new("L", self.img.size, 0)
        ImageDraw.Draw(mask).rectangle([sc(x1), sc(y1), sc(x2), sc(y2)], fill=255)
        hatch = Image.new("RGB", self.img.size, PAPER)
        hd = ImageDraw.Draw(hatch)
        diag = math.hypot(x2 - x1, y2 - y1)
        dx, dy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        n = int(diag * 1.6 / step) + 2
        ox, oy = (x1 + x2) / 2, (y1 + y2) / 2
        for i in range(-n, n):
            px, py = ox - dy * i * step, oy + dx * i * step
            hd.line([(sc(px - dx * diag), sc(py - dy * diag)), (sc(px + dx * diag), sc(py + dy * diag))],
                    fill=fill, width=sc(width))
        self.img.paste(hatch, (0, 0), mask)
        self.d = ImageDraw.Draw(self.img)

    def text(self, x, y, s, size=42, fill=INK, anchor="lt", stroke=0, stroke_fill=PAPER):
        self.d.text((sc(x), sc(y)), s, font=font(size), fill=fill, anchor=anchor,
                    stroke_width=sc(stroke) if stroke else 0, stroke_fill=stroke_fill)

    def width_of(self, s, size):
        return self.d.textlength(s, font=font(size)) / S

    def cross(self, cx, cy, r=30, width=11, fill=INK):
        self.line([(cx - r, cy - r), (cx + r, cy + r)], width=width, fill=fill)
        self.line([(cx - r, cy + r), (cx + r, cy - r)], width=width, fill=fill)

    def check(self, cx, cy, r=30, width=11, fill=INK):
        self.line([(cx - r, cy), (cx - r * 0.15, cy + r * 0.75), (cx + r, cy - r * 0.65)],
                  width=width, fill=fill)

    def chip(self, x, y, label, size=30, fill=None, pad=22):
        w = self.width_of(label, size) + pad * 2
        h = size * 1.9
        self.box(x, y, x + w, y + h, r=h / 2, width=6, fill=fill)
        self.text(x + w / 2, y + h / 2, label, size=size, anchor="mm")
        return w

    def card(self, x1, y1, x2, y2, title, note, title_size=40, note_size=27):
        self.box(x1, y1, x2, y2, r=14, width=8, fill=None)
        self.text((x1 + x2) / 2, y1 + 36, title, size=title_size, anchor="mt")
        if note:
            self.text((x1 + x2) / 2, y2 - 40, note, size=note_size, anchor="mb")

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        image = self.img.resize((W, H), Image.LANCZOS)
        rgb = np.array(image.convert("RGB")).astype(int)
        diff = np.abs(rgb - np.array(PAPER)).max(axis=2)
        alpha = np.clip((diff - 2) / 10 * 255, 0, 255).astype(np.uint8)
        rgba = np.dstack([rgb.astype(np.uint8), alpha])
        Image.fromarray(rgba, "RGBA").save(OUT / f"{name}.png")
        print("wrote", OUT / f"{name}.png")




# ---------------------------------------------------------------- p01
def p01():
    s = Sheet(2111)
    s.text(110, 60, "一万日活，每月账单 22500 美元", size=46)
    s.box(110, 170, 700, 420, r=16, width=10, fill=PAPER)
    s.text(405, 220, "每月 LLM 成本", size=30, anchor="mm")
    s.text(405, 320, "$22,500", size=64, anchor="mm")
    s.text(405, 390, "还只是语言模型", size=24, anchor="mm")

    s.box(760, 170, 1490, 420, r=16, width=10, fill=YELLOW)
    s.streaks((770, 180, 1480, 410), step=50, width=2)
    s.text(1125, 220, "其中重复查询", size=30, anchor="mm", stroke=2)
    s.text(1125, 320, "40% 到 60%", size=56, anchor="mm", stroke=2)
    s.text(1125, 390, "你在为同一份计算付好几次钱", size=24, anchor="mm", stroke=2)

    s.line([(110, 490), (1490, 490)], width=7)
    s.text(110, 535, "大多数 AI 创业公司不是死于糟糕的模型", size=34)
    s.text(110, 610, "是死于糟糕的单位经济", size=38)
    s.text(110, 690, "这一课讲怎么把账单砍掉七成", size=32)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(2112)
    s.text(110, 70, "缓存、限流与成本优化", size=56)
    s.text(110, 165, "阶段 11 · 第 11 课", size=34)
    s.line([(110, 240), (1490, 240)], width=9)
    s.text(110, 285, "七层优化，按顺序叠加：", size=34)
    layers = ["1  provider prompt 缓存", "2  精确缓存（哈希）", "3  语义缓存（向量）",
              "4  模型路由（贵 vs 便宜）", "5  限流与配额", "6  prompt 压缩", "7  批处理"]
    for i, name in enumerate(layers):
        y = 370 + i * 68
        s.box(110, y, 1490, y + 56, r=10, width=6,
              fill=YELLOW if i < 5 else PAPER)
        if i < 5:
            s.streaks((120, y + 6, 1480, y + 50), step=44, width=2)
        s.text(160, y + 28, name, size=24, anchor="lm", stroke=2 if i < 5 else 0)
    s.text(800, 850, "前五层通常能把成本降 70% 以上", size=26, anchor="mm")
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(2113)
    s.text(110, 55, "一次调用有五个成本组成部分", size=42)
    parts = [("system prompt", "500 - 2000 token", "每个请求都一样", YELLOW),
             ("检索上下文", "500 - 4000 token", "同话题用户反复出现", YELLOW),
             ("用户消息", "50 - 500 token", "真正独有的部分", PAPER)]
    for i, (name, size_, note, fill) in enumerate(parts):
        y = 160 + i * 175
        s.box(110, y, 1490, y + 145, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 137), step=48, width=2)
        s.text(160, y + 45, name, size=30, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(160, y + 100, size_, size=26, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(1400, y + 72, note, size=24, anchor="rm", stroke=2 if fill == YELLOW else 0)

    s.text(110, 720, "前两部分占了大头，而且每个请求都在重复发送", size=30)
    s.text(110, 800, "真正的独有信息，只有用户那一句", size=30)
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(2114)
    s.text(110, 55, "system prompt 是无声的杀手", size=42)
    s.text(110, 130, "假设 system prompt 是 1500 token：", size=30)
    rows = [("100 万次请求", "$3.75", "光这个前缀"),
            ("一天 10 万请求", "$375/天", "同一天的重复"),
            ("一个月", "$11,250", "为一段从不改变的文字")]
    for i, (a, b, c) in enumerate(rows):
        y = 200 + i * 130
        hot = i == 2
        s.box(110, y, 1490, y + 110, r=14, width=9,
              fill=YELLOW if hot else PAPER)
        if hot:
            s.streaks((120, y + 8, 1480, y + 102), step=48, width=2)
        s.text(160, y + 55, a, size=30, anchor="lm", stroke=2 if hot else 0)
        s.text(700, y + 55, b, size=36, anchor="lm", stroke=2 if hot else 0)
        s.text(1100, y + 55, c, size=24, anchor="lm", stroke=2 if hot else 0)

    s.line([(110, 640), (1490, 640)], width=7)
    s.text(110, 680, "这段文字你从来没改过，但每次都付全价", size=32)
    s.text(110, 755, "provider 缓存就是为这个场景设计的", size=32)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(2115)
    s.text(110, 55, "三家厂商的 prompt 缓存，机制不同", size=40)
    rows = [("Anthropic", "显式 cache_control 标记", "省 90%", "写入多付 25%", YELLOW),
            ("OpenAI", "自动前缀匹配", "省 50%", "零实现成本", PAPER),
            ("Gemini", "显式 CachedContent", "省 75%", "外加存储费", PAPER)]
    for i, (name, mech, save, cost, fill) in enumerate(rows):
        y = 160 + i * 170
        s.box(110, y, 1490, y + 140, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 132), step=48, width=2)
        s.text(160, y + 42, name, size=32, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(160, y + 96, mech, size=24, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(900, y + 42, save, size=34, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(1200, y + 96, cost, size=22, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.text(110, 700, "折扣从 50% 到 90%，但都要求「前缀完全相同」", size=28)
    s.text(110, 780, "不同问法的相同意图，就要靠下一层的语义缓存", size=30)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(2116)
    s.text(110, 55, "语义缓存：不同问法，同一意图", size=42)

    s.box(110, 150, 700, 250, r=12, width=8, fill=PAPER)
    s.text(405, 200, "退货政策是什么", size=28, anchor="mm")
    s.box(110, 280, 700, 380, r=12, width=8, fill=PAPER)
    s.text(405, 330, "我怎么退货", size=28, anchor="mm")
    s.arrow(730, 265, 800, 265, width=9)
    s.text(765, 235, "嵌入", size=22, anchor="mb")

    s.box(820, 150, 1490, 380, r=14, width=9, fill=PAPER)
    s.text(860, 190, "算余弦相似度：", size=26)
    s.text(860, 260, "0.96  >  0.95", size=40)
    s.text(860, 335, "超过阈值 → 直接返回缓存", size=26)

    s.line([(110, 460), (1490, 460)], width=7)
    s.text(110, 495, "嵌入成本可以忽略：每百万 token 两美分", size=30)
    s.text(110, 565, "和一次完整调用相比，查缓存几乎不花钱", size=30)
    s.text(110, 640, "实测命中率 52%，这一层就把账单砍掉一半", size=32)
    s.text(110, 720, "而它新增的嵌入成本，一小时就赚回来了", size=28)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(2117)
    s.text(110, 55, "精确缓存：哈希匹配，最简单也最快", size=40)

    s.box(110, 160, 1490, 260, r=12, width=8, fill=YELLOW)
    s.streaks((120, 170, 1480, 250), step=44, width=2)
    s.text(800, 210, "hash(prompt) → 查表 → 命中返回", size=34, anchor="mm", stroke=2)

    s.text(110, 320, "三种场景完美适用：", size=30)
    cases = ["固定 system prompt + 固定上下文 + 完全相同的查询",
             "带相同工具定义的 function calling",
             "同一份文档被反复处理的批处理"]
    for i, c in enumerate(cases):
        y = 390 + i * 85
        s.check(140, y + 30, r=16, width=8)
        s.text(185, y + 30, c, size=26, anchor="lm")

    s.line([(110, 680), (1490, 680)], width=7)
    s.text(110, 715, "它比语义缓存简单一个数量级", size=32)
    s.text(110, 790, "没有向量库、没有阈值调参、没有误命中", size=30)
    s.text(110, 860, "代价是只能命中「一个字都不差」的请求", size=28)
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(2118)
    s.text(110, 55, "模型路由：不是每个查询都要大模型", size=40)

    s.box(400, 130, 1200, 220, r=12, width=8, fill=PAPER)
    s.text(800, 175, "复杂度分类器", size=30, anchor="mm")

    branches = [("简单：查询、FAQ", "gpt-4o-mini  $0.15/$0.60", 65, YELLOW),
                ("中等：分析、摘要", "claude-sonnet  $3/$15", 27, PAPER),
                ("复杂：推理、代码", "gpt-4o  $2.50/$10", 8, PAPER)]
    for i, (label, model, pct, fill) in enumerate(branches):
        x = 140 + i * 480
        s.arrow(800, 230, x + 150, 300, width=8)
        s.box(x, 310, x + 380, 440, r=12, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((x + 8, 318, x + 372, 432), step=44, width=2)
        s.text(x + 190, 350, label, size=24, anchor="mm", stroke=2 if fill == YELLOW else 0)
        s.text(x + 190, 395, model, size=22, anchor="mm", stroke=2 if fill == YELLOW else 0)
        s.text(x + 190, 425, f"{pct}%", size=26, anchor="mm", stroke=2 if fill == YELLOW else 0)

    s.line([(110, 490), (1490, 490)], width=7)
    s.text(110, 525, "实测：65% 的查询可以走 mini", size=36)
    s.text(110, 595, "光这一项就省 40% 到 70% 的模型成本", size=30)
    s.text(110, 670, "关键是分类器要准，误判会比不做路由更贵", size=28)
    s.text(110, 745, "对了省一半，错了既贵又慢", size=30)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(2119)
    s.text(110, 55, "限流：不只是公平，是生存", size=42)

    s.text(110, 130, "令牌桶：每人一个桶，按速率回填", size=30)
    s.box(110, 200, 1490, 300, r=12, width=8, fill=PAPER)
    s.text(800, 250, "桶容量 N 个令牌 · 每秒回填 R 个", size=32, anchor="mm")

    rows = [("等级", "每日 token", "每分钟请求", "模型访问"),
            ("免费", "50,000", "10", "仅 mini"),
            ("专业", "500,000", "60", "mini + sonnet"),
            ("企业", "5,000,000", "300", "全部")]
    for i, (a, b, c, d) in enumerate(rows):
        y = 340 + i * 90
        s.box(90, y, 1470, y + 74, r=10, width=7,
              fill=METAL if i == 0 else PAPER)
        for j, v in enumerate([a, b, c, d]):
            s.text(140 + j * 320, y + 37, v, size=26, anchor="lm")

    s.text(110, 730, "没有限流，一个爬虫就能把你的月度预算跑光", size=30)
    s.text(110, 810, "令牌桶允许突发，同时强制平均速率", size=30)
    s.save("p09")


# ---------------------------------------------------------------- p10
def p10():
    s = Sheet(2120)
    s.text(110, 55, "预算三档告警与熔断器", size=44)

    levels = [("70%", "发告警", "还能继续跑", PAPER),
              ("85%", "切便宜模型", "自动降级", YELLOW),
              ("95%", "拒绝新请求", "只返回缓存", INK)]
    for i, (pct, action, note, fill) in enumerate(levels):
        y = 170 + i * 180
        s.box(110, y, 1490, y + 150, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 142), step=48, width=2)
        txt_fill = PAPER if fill == INK else INK
        s.text(200, y + 60, pct, size=48, anchor="lm", fill=txt_fill)
        s.text(420, y + 55, action, size=34, anchor="lm", fill=txt_fill)
        s.text(420, y + 110, note, size=24, anchor="lm", fill=txt_fill)

    s.line([(110, 720), (1490, 720), ], width=7)
    s.text(110, 755, "没有熔断器，一个 bug 能在几小时内烧穿整月预算", size=30)
    s.text(110, 830, "三档阈值是最小可用配置", size=32)
    s.save("p10")


# ---------------------------------------------------------------- p11
def p11():
    s = Sheet(2121)
    s.text(110, 55, "实测：优化前后对比", size=44)

    rows = [("指标", "优化前", "优化后", "变化"),
            ("总成本", "$0.0291", "$0.0095", "-67.3%"),
            ("每次调用", "$0.0029", "$0.0010", "-67.3%"),
            ("月账单（1 万日活）", "$22,500", "$5,380", "-76%"),
            ("P95 延迟", "2800ms", "900ms", "-68%")]
    for i, (a, b, c, d) in enumerate(rows):
        y = 150 + i * 100
        hot = i == 3
        s.box(90, y, 1470, y + 84, r=10, width=7,
              fill=YELLOW if hot else (METAL if i == 0 else PAPER))
        if hot:
            s.streaks((100, y + 8, 1460, y + 76), step=44, width=2)
        for j, v in enumerate([a, b, c, d]):
            s.text(140 + j * 340, y + 42, v, size=26 if j else 24, anchor="lm",
                   stroke=2 if hot else 0)

    s.text(110, 700, "七层优化全叠上，月账单从两万二降到五千三", size=32)
    s.text(110, 775, "语义缓存的嵌入成本每月 180 美元，一小时就赚回来", size=28)
    s.text(110, 850, "这就是活下来和烧光跑道的差别", size=32)
    s.save("p11")


# ---------------------------------------------------------------- p12
def p12():
    s = Sheet(2122)
    s.text(110, 55, "你的产品现在用了几层缓存？", size=44)

    opts = [("语义缓存", "命中率最高，要调阈值", YELLOW),
            ("模型路由", "省 40-70%，要准的分类器", PAPER),
            ("熔断器", "保命，但平时看不出效果", PAPER)]
    for i, (name, note, fill) in enumerate(opts):
        y = 170 + i * 150
        s.box(110, y, 1490, y + 120, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 112), step=46, width=2)
        s.text(180, y + 60, name, size=34, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(660, y + 60, note, size=26, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.line([(110, 640), (1490, 640), ], width=7)
    s.text(110, 675, "顺序建议：先加 provider 缓存，再上精确缓存", size=30)
    s.text(110, 745, "语义缓存和路由要等你有真实流量再调", size=30)

    s.box(110, 810, 1490, 870, r=12, width=8, fill=PAPER)
    s.text(800, 840, "下一集：护栏与内容过滤", size=28, anchor="mm")
    s.save("p12")


# ---------------------------------------------------------------- cover
def cover():
    s = Sheet(2100)
    s.text(110, 80, "同一句话，为什么收两次钱？", size=52)
    s.line([(110, 220), (1490, 220)], width=10)
    s.text(110, 275, "一万日活的 AI 产品，月账单 22500 美元", size=34)

    s.box(110, 380, 1490, 640, r=20, width=11, fill=YELLOW)
    s.streaks((120, 390, 1480, 630), step=56, width=3)
    s.text(800, 470, "其中 40%-60% 是重复查询", size=46, anchor="mm", stroke=2)
    s.text(800, 570, "优化后降到 5380 美元", size=44, anchor="mm", stroke=2)

    s.text(110, 730, "缓存、路由、限流，七层把成本砍七成", size=34)
    s.save("cover")


if __name__ == "__main__":
    for fn in (cover, p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12):
        fn()
