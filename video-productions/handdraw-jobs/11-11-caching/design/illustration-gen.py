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
    s.text(110, 60, "一万日活，月账单 22500 美元", size=44)

    s.box(110, 170, 720, 470, r=20, width=11, fill=PAPER)
    s.text(415, 225, "每月成本", size=36, anchor="mm")
    s.text(415, 340, "$22,500", size=64, anchor="mm")
    s.text(415, 425, "还只是语言模型", size=30, anchor="mm")

    s.box(780, 170, 1490, 470, r=20, width=11, fill=YELLOW)
    s.streaks((790, 180, 1480, 460), step=56, width=3)
    s.text(1135, 225, "其中重复查询", size=36, anchor="mm", stroke=2)
    s.text(1135, 340, "40% - 60%", size=60, anchor="mm", stroke=2)
    s.text(1135, 425, "同一份计算付好几次", size=30, anchor="mm", stroke=2)

    s.text(110, 550, "不是死于糟糕的模型", size=44)
    s.text(110, 630, "是死于糟糕的单位经济", size=50)
    s.text(110, 740, "这一课把账单砍掉七成", size=42)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(2112)
    s.text(110, 70, "缓存、限流与成本优化", size=58)
    s.text(110, 165, "阶段 11 · 第 11 课", size=36)
    s.line([(110, 250), (1490, 250)], width=10)

    s.text(110, 300, "七层优化，按顺序叠加", size=44)
    layers = ["prompt 缓存", "精确缓存", "语义缓存", "模型路由", "限流配额"]
    for i, name in enumerate(layers):
        y = 400 + i * 95
        s.box(110, y, 1490, y + 78, r=14, width=9,
              fill=YELLOW if i < 3 else PAPER)
        if i < 3:
            s.streaks((120, y + 6, 1480, y + 72), step=44, width=3)
        s.text(180, y + 39, name, size=38, anchor="lm", stroke=2 if i < 3 else 0)

    s.text(800, 900, "前三层通常就能砍掉一半", size=36, anchor="mm")
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(2113)
    s.text(110, 55, "一次调用的成本构成", size=50)

    parts = [("system prompt", "每个请求都一样", YELLOW),
             ("检索上下文", "同话题反复出现", YELLOW),
             ("用户消息", "真正独有的", PAPER)]
    for i, (name, note, fill) in enumerate(parts):
        y = 160 + i * 190
        s.box(110, y, 1490, y + 155, r=20, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 147), step=54, width=3)
        s.text(180, y + 55, name, size=42, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(180, y + 118, note, size=32, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.text(110, 800, "前两部分占大头，而且每次都重复发", size=36)
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(2114)
    s.text(110, 55, "system prompt 是无声杀手", size=46)
    s.text(110, 135, "假设它是 1500 token", size=40)

    rows = [("100 万次请求", "$3.75"),
            ("一天 10 万请求", "$375"),
            ("一个月", "$11,250")]
    for i, (a, b) in enumerate(rows):
        y = 220 + i * 160
        hot = i == 2
        s.box(110, y, 1490, y + 135, r=20, width=10,
              fill=YELLOW if hot else PAPER)
        if hot:
            s.streaks((120, y + 8, 1480, y + 127), step=52, width=3)
        s.text(180, y + 67, a, size=38, anchor="lm", stroke=2 if hot else 0)
        s.text(1000, y + 67, b, size=48, anchor="lm", stroke=2 if hot else 0)

    s.line([(110, 730), (1490, 730), ], width=9)
    s.text(110, 775, "这段文字你从没改过", size=42)
    s.text(110, 855, "但每次都付全价", size=44)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(2115)
    s.text(110, 55, "三家厂商的缓存折扣", size=48)

    rows = [("Anthropic", "显式标记", "省 90%", YELLOW),
            ("OpenAI", "自动前缀", "省 50%", PAPER),
            ("Gemini", "显式缓存", "省 75%", PAPER)]
    for i, (name, mech, save, fill) in enumerate(rows):
        y = 160 + i * 175
        s.box(110, y, 1490, y + 145, r=20, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 137), step=52, width=3)
        s.text(180, y + 48, name, size=42, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(180, y + 108, mech, size=30, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(1400, y + 72, save, size=46, anchor="rm", stroke=2 if fill == YELLOW else 0)

    s.line([(110, 720), (1490, 720), ], width=9)
    s.text(110, 765, "都要求前缀完全相同", size=42)
    s.text(110, 845, "不同问法要靠语义缓存", size=38)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(2116)
    s.text(110, 55, "语义缓存：不同问法，同一意图", size=42)

    s.box(110, 150, 660, 250, r=18, width=10, fill=PAPER)
    s.text(385, 200, "退货政策是什么", size=32, anchor="mm")
    s.box(110, 290, 660, 390, r=18, width=10, fill=PAPER)
    s.text(385, 340, "我怎么退货", size=32, anchor="mm")
    s.arrow(690, 270, 780, 270, width=10)
    s.text(735, 240, "嵌入", size=30, anchor="mb")

    s.box(800, 150, 1490, 390, r=20, width=11, fill=YELLOW)
    s.streaks((810, 160, 1480, 380), step=54, width=3)
    s.text(1145, 210, "余弦相似度", size=36, anchor="mm", stroke=2)
    s.text(1145, 300, "0.96 > 0.95", size=50, anchor="mm", stroke=2)
    s.text(1145, 360, "直接返回缓存", size=30, anchor="mm", stroke=2)

    s.line([(110, 470), (1490, 470)], width=9)
    s.text(110, 515, "嵌入成本每百万 token 两美分", size=40)
    s.text(110, 600, "查缓存几乎不花钱", size=42)
    s.text(110, 690, "实测命中 52%，账单砍一半", size=42)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(2117)
    s.text(110, 55, "精确缓存：哈希匹配", size=50)

    s.box(110, 160, 1490, 290, r=18, width=10, fill=YELLOW)
    s.streaks((120, 170, 1480, 280), step=52, width=3)
    s.text(800, 225, "hash(prompt) → 查表 → 命中", size=42, anchor="mm", stroke=2)

    s.text(110, 350, "三种场景完美适用", size=42)
    cases = ["固定 prompt + 固定上下文", "相同工具定义的调用", "同一文档反复处理"]
    for i, c in enumerate(cases):
        y = 450 + i * 105
        s.check(150, y + 30, r=20, width=10)
        s.text(215, y + 30, c, size=36, anchor="lm")

    s.line([(110, 790), (1490, 790), ], width=9)
    s.text(110, 835, "比语义缓存简单一个数量级", size=40)
    s.text(110, 915, "代价是只能命中「一字不差」", size=36)
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(2118)
    s.text(110, 55, "模型路由：不是每个都要大模型", size=42)

    s.box(400, 140, 1200, 250, r=18, width=10, fill=PAPER)
    s.text(800, 195, "复杂度分类器", size=42, anchor="mm")

    branches = [("简单", "mini", "65%", YELLOW),
                ("中等", "sonnet", "27%", PAPER),
                ("复杂", "gpt-4o", "8%", PAPER)]
    for i, (label, model, pct, fill) in enumerate(branches):
        x = 140 + i * 480
        s.arrow(800, 260, x + 150, 320, width=9)
        s.box(x, 330, x + 380, 500, r=18, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((x + 10, 340, x + 370, 490), step=46, width=3)
        s.text(x + 190, 375, label, size=36, anchor="mm", stroke=2 if fill == YELLOW else 0)
        s.text(x + 190, 435, model, size=32, anchor="mm", stroke=2 if fill == YELLOW else 0)
        s.text(x + 190, 480, pct, size=38, anchor="mm", stroke=2 if fill == YELLOW else 0)

    s.line([(110, 560), (1490, 560)], width=9)
    s.text(110, 605, "65% 的查询可以走 mini", size=46)
    s.text(110, 690, "光这一项省 40-70%", size=42)
    s.text(110, 780, "分类器要准，误判更贵", size=38)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(2119)
    s.text(110, 55, "限流：不只是公平，是生存", size=46)

    s.text(110, 135, "令牌桶：每人一个桶，按速率回填", size=38)
    s.box(110, 220, 1490, 330, r=18, width=10, fill=PAPER)
    s.text(800, 275, "容量 N · 每秒回填 R", size=40, anchor="mm")

    rows = [("等级", "每日 token", "每分钟"),
            ("免费", "50,000", "10"),
            ("专业", "500,000", "60"),
            ("企业", "5,000,000", "300")]
    for i, (a, b, c) in enumerate(rows):
        y = 390 + i * 105
        s.box(90, y, 1470, y + 88, r=14, width=9,
              fill=METAL if i == 0 else PAPER)
        for j, v in enumerate([a, b, c]):
            s.text(180 + j * 440, y + 44, v, size=36 if i else 32, anchor="lm")

    s.text(110, 820, "没有限流，一个爬虫跑光预算", size=40)
    s.save("p09")


# ---------------------------------------------------------------- p10
def p10():
    s = Sheet(2120)
    s.text(110, 55, "预算三档告警", size=50)

    levels = [("70%", "发告警", PAPER),
              ("85%", "切便宜模型", YELLOW),
              ("95%", "拒绝新请求", INK)]
    for i, (pct, action, fill) in enumerate(levels):
        y = 170 + i * 190
        s.box(110, y, 1490, y + 160, r=20, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 152), step=54, width=3)
        txt = PAPER if fill == INK else INK
        s.text(220, y + 80, pct, size=64, anchor="lm", fill=txt)
        s.text(500, y + 80, action, size=44, anchor="lm", fill=txt)

    s.line([(110, 750), (1490, 750), ], width=9)
    s.text(110, 795, "没有熔断器，一个 bug 烧穿预算", size=38)
    s.text(110, 875, "三档是最小可用配置", size=40)
    s.save("p10")


# ---------------------------------------------------------------- p11
def p11():
    s = Sheet(2121)
    s.text(110, 55, "实测：优化前后", size=50)

    rows = [("指标", "优化前", "优化后"),
            ("总成本", "$0.029", "$0.0095"),
            ("每次调用", "$0.0029", "$0.0010"),
            ("月账单", "$22,500", "$5,380"),
            ("P95 延迟", "2800ms", "900ms")]
    for i, (a, b, c) in enumerate(rows):
        y = 150 + i * 115
        hot = i == 3
        s.box(90, y, 1470, y + 98, r=14, width=9,
              fill=YELLOW if hot else (METAL if i == 0 else PAPER))
        if hot:
            s.streaks((100, y + 8, 1460, y + 90), step=48, width=3)
        for j, v in enumerate([a, b, c]):
            s.text(180 + j * 440, y + 49, v, size=38 if j else 32, anchor="lm",
                   stroke=2 if hot else 0)

    s.line([(110, 740), (1490, 740), ], width=9)
    s.text(110, 785, "省 67.3%，月账单降到 5380", size=42)
    s.text(110, 865, "嵌入成本一小时赚回来", size=38)
    s.save("p11")


# ---------------------------------------------------------------- p12
def p12():
    s = Sheet(2122)
    s.text(110, 55, "你的产品用了几层缓存？", size=48)

    opts = [("语义缓存", "命中最高，要调阈值", YELLOW),
            ("模型路由", "省 40-70%，要准", PAPER),
            ("熔断器", "保命，平时看不出", PAPER)]
    for i, (name, note, fill) in enumerate(opts):
        y = 170 + i * 155
        s.box(110, y, 1490, y + 130, r=18, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 122), step=50, width=3)
        s.text(200, y + 65, name, size=40, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(700, y + 65, note, size=32, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.text(110, 700, "先加 provider 缓存和精确缓存", size=40)
    s.text(110, 790, "语义和路由要等真实流量再调", size=38)

    s.box(110, 850, 1490, 930, r=14, width=9, fill=PAPER)
    s.text(800, 890, "下一集：护栏与内容过滤", size=34, anchor="mm")
    s.save("p12")


# ---------------------------------------------------------------- cover (大画布 1920x1080)
def cover():
    base = Image.new("RGB", (1920, 1080), PAPER)
    d = ImageDraw.Draw(base)
    title_font = ImageFont.truetype(FONT, 112)
    sub_font = ImageFont.truetype(FONT, 62)
    meta_font = ImageFont.truetype(FONT, 32)
    d.text((120, 160), "同一句话", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((120, 300), "收两次钱", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((120, 460), "一万日活的月账单 22500 美元", font=sub_font, fill=INK)
    d.rectangle([120, 570, 700, 580], fill=INK)
    d.text((120, 610), "11-11 · LLM Engineering", font=meta_font, fill=INK)
    art = Image.open(OUT / "p01.png").convert("RGB")
    art = art.resize((1040, 585), Image.LANCZOS)
    base.paste(art, (800, 400))
    base.save(OUT / "cover.png")
    print("wrote", OUT / "cover.png")


if __name__ == "__main__":
    for fn in (cover, p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12):
        fn()
