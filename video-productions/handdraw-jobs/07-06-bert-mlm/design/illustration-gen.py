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
    s = Sheet(806)
    s.text(110, 60, "预测下一个词 vs 预测缺失的词", size=46)

    # GPT card
    s.box(110, 170, 760, 470, r=16, width=9, fill=PAPER)
    s.text(140, 195, "GPT", size=40)
    s.text(140, 250, "只看左边", size=28)
    words = ["今天", "天气", "很"]
    for i, w in enumerate(words):
        s.box(150 + i * 150, 330, 280 + i * 150, 420, r=10, width=7, fill=PAPER)
        s.text(215 + i * 150, 375, w, size=34, anchor="mm")
    s.box(600, 330, 730, 420, r=10, width=8, fill=YELLOW)
    s.streaks((608, 338, 722, 412), step=28, width=2)
    s.text(665, 375, "好", size=38, anchor="mm", stroke=2)
    s.arrow(575, 375, 596, 375, width=7)

    # BERT card
    s.box(840, 170, 1490, 470, r=16, width=9, fill=PAPER)
    s.text(870, 195, "BERT", size=40)
    s.text(870, 250, "两边都看", size=28)
    words = ["今天", "天气"]
    for i, w in enumerate(words):
        s.box(880 + i * 140, 330, 1000 + i * 140, 420, r=10, width=7, fill=PAPER)
        s.text(940 + i * 140, 375, w, size=34, anchor="mm")
    s.box(1160, 330, 1330, 420, r=10, width=9, fill=INK)
    s.text(1245, 375, "[MASK]", size=34, anchor="mm", fill=PAPER)
    s.box(1350, 330, 1460, 420, r=10, width=7, fill=PAPER)
    s.text(1405, 375, "好", size=34, anchor="mm")
    s.arrow(1245, 470, 1245, 445, width=7)
    s.text(1245, 490, "补回「很」", size=30, anchor="mt")

    s.line([(110, 600), (1490, 600)], width=6)
    s.text(110, 640, "2018 年之前：每个 NLP 任务都在自己的标注数据上从零训练", size=36)
    s.text(110, 700, "没有一份「懂英语」的预训练 checkpoint 可以微调", size=36)
    s.text(110, 775, "填空，就是那个预训练任务", size=40)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(807)
    s.text(110, 60, "一句话，遮住 15%", size=48)
    words = ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
    mask_at = {1, 5}
    x0, y = 90, 165
    step = 158
    for i, w in enumerate(words):
        x = x0 + i * step
        masked = i in mask_at
        s.box(x, y, x + 130, y + 90, r=10, width=8,
              fill=INK if masked else PAPER)
        if masked:
            s.text(x + 65, y + 45, "[M]", size=34, anchor="mm", fill=PAPER)
        else:
            s.text(x + 65, y + 45, w, size=30, anchor="mm")
    # arrows down to the originals
    for i in mask_at:
        x = x0 + i * step + 65
        s.arrow(x, y + 96, x, y + 170, width=7)
        s.text(x, y + 190, words[i], size=32, anchor="mt", stroke=2)
    s.text(110, 400, "被选中的 15% 位置，标签就是原词", size=36)
    s.text(110, 470, "其余位置不参与损失", size=36)
    # bidirectional band
    s.box(110, 540, 1490, 700, r=16, width=9, fill=YELLOW)
    s.streaks((120, 550, 1480, 690), step=42, width=2)
    s.text(800, 585, "编码器是双向的", size=44, anchor="mt", stroke=2)
    s.text(800, 650, "补位置 1 的词，可以用上位置 2 之后的全部上下文", size=34, anchor="mt", stroke=2)
    s.text(110, 745, "这是 GPT 做不到的事：它只能看左边", size=34)
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(808)
    s.text(110, 60, "被选中的 15% 里，再分三份", size=46)
    base = 640
    bars = [("80%", "换成 [MASK]", 360, YELLOW), ("10%", "换成随机词", 170, METAL), ("10%", "保持原样", 170, PAPER)]
    s.line([(140, base), (1460, base)], width=8)
    for i, (pct, name, h, fill) in enumerate(bars):
        x = 250 + i * 420
        s.box(x - 110, base - h, x + 110, base, r=10, width=9, fill=fill)
        s.text(x, base - h - 46, pct, size=46, anchor="mm")
        s.text(x, base + 34, name, size=28, anchor="mt")
    s.text(800, 778, "为什么不全用 [MASK]？", size=42, anchor="mm")
    s.text(800, 840, "推理时根本不会出现 [MASK]，训练全用它就制造分布偏移", size=30, anchor="mm")
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(809)
    s.text(110, 60, "实跑：一万次抽样", size=48)
    stats = [
        ("15.03%", "被选中", "目标 15%", True),
        ("79.80%", "换成 [MASK]", "目标 80%", False),
        ("10.15%", "换成随机词", "目标 10%", False),
        ("10.04%", "保持原样", "目标 10%", False),
    ]
    for i, (big, label, target, hot) in enumerate(stats):
        x = 110 + i * 380
        s.box(x, 200, x + 330, 470, r=16, width=9, fill=YELLOW if hot else PAPER)
        if hot:
            s.streaks((x + 10, 210, x + 320, 460), step=34, width=2)
        s.text(x + 165, 270, big, size=54, anchor="mm", stroke=2 if hot else 0)
        s.text(x + 165, 355, label, size=30, anchor="mm", stroke=2 if hot else 0)
        s.text(x + 165, 425, target, size=28, anchor="mm", stroke=2 if hot else 0)
    s.line([(110, 540), (1490, 540)], width=6)
    s.text(110, 580, "三分规则确实在按比例执行", size=40)
    s.text(110, 650, "代码路径：create_mlm_batch → 逐个位置掷两枚骰子", size=34)
    s.text(110, 705, "第一枚决定要不要遮，第二枚决定遮成什么", size=34)
    s.text(110, 790, "其余位置的标签记 -100，损失直接跳过", size=36)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(810)
    s.text(110, 60, "下一句预测，被消融掉了", size=46)
    # A and B
    s.box(120, 175, 700, 265, r=12, width=9, fill=PAPER)
    s.text(410, 220, "句子 A：猫坐在垫子上。", size=32, anchor="mm")
    s.box(120, 320, 700, 410, r=12, width=9, fill=PAPER)
    s.text(410, 365, "句子 B：它今天很困。", size=32, anchor="mm")
    s.arrow(410, 272, 410, 313, width=7)
    s.text(760, 300, "B 是否紧跟 A？", size=32, anchor="lm")
    # verdict
    s.circle(1050, 300, 74, width=11, fill=PAPER)
    s.text(1050, 300, "?", size=56, anchor="mm")
    s.cross(1330, 300, r=62, width=16)
    s.text(1330, 405, "RoBERTa 2019 消融", size=30, anchor="mt")
    s.line([(110, 500), (1490, 500)], width=6)
    s.text(110, 540, "结论：这个辅助任务帮倒忙，不是帮忙", size=38)
    s.text(110, 615, "现代编码器只保留掩码语言建模", size=38)
    s.box(110, 680, 1490, 800, r=14, width=8, fill=YELLOW)
    s.streaks((120, 690, 1480, 790), step=44, width=2)
    s.text(800, 740, "一个预训练目标，撑起整个编码器时代", size=38, anchor="mm", stroke=2)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(811)
    s.text(110, 60, "整词掩码与特殊符号", size=46)
    tokens = ["[CLS]", "play", "##ing", "foot", "##ball", "[SEP]"]
    masked = {1, 2, 3, 4}
    x0, y = 110, 180
    step = 230
    for i, t in enumerate(tokens):
        x = x0 + i * step
        hot = i in masked
        s.box(x, y, x + 200, y + 90, r=10, width=8, fill=INK if hot else PAPER)
        s.text(x + 100, y + 45, t, size=30, anchor="mm", fill=PAPER if hot else INK)
    # span brackets under masked words
    s.line([(x0 + step, y + 110), (x0 + step, y + 140), (x0 + 5 * step - 30, y + 140),
            (x0 + 5 * step - 30, y + 110)], width=6)
    s.text(x0 + 2.5 * step, y + 160, "整词一起遮，或一起不遮", size=30, anchor="mt")

    s.text(110, 420, "序列开头 [CLS]，句子之间 [SEP]", size=36)
    s.text(110, 485, "被遮位置之外的标签全部记 -100", size=36)
    s.box(110, 545, 1490, 720, r=16, width=9, fill=YELLOW)
    s.streaks((120, 555, 1480, 710), step=44, width=2)
    s.text(800, 572, "忽略索引 = -100", size=42, anchor="mt", stroke=2)
    s.text(800, 645, "损失只算被遮的那几个位置，其余不贡献梯度", size=30, anchor="mt", stroke=2)
    s.text(110, 750, "标点、填充、特殊符号都靠这条规则排除在外", size=34)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(812)
    s.text(110, 60, "十八个月，横扫所有榜单", size=46)
    # timeline
    s.line([(110, 300), (1490, 300)], width=8)
    points = [(230, "2018", "BERT"), (640, "+18 个月", "横扫榜单"), (1050, "2020", "每个搜索"), (1400, "2026", "每 token 快 5–10×")]
    for i, (x, year, note) in enumerate(points):
        s.circle(x, 300, 26, width=8, fill=YELLOW if i == 3 else INK)
        s.text(x, 235, year, size=32, anchor="mb")
        s.text(x, 345, note, size=30, anchor="mt")
    s.text(110, 450, "搜索引擎、内容审核、语义检索，都装着一个 BERT", size=36)
    s.text(110, 515, "2026 年，纯编码器仍是分类、检索、抽取的正确工具", size=36)

    s.box(110, 590, 720, 780, r=16, width=9, fill=PAPER)
    s.text(415, 620, "每 token 更快", size=34, anchor="mt")
    s.text(415, 700, "5–10×", size=66, anchor="mm")
    s.box(790, 590, 1490, 780, r=16, width=9, fill=YELLOW)
    s.streaks((800, 600, 1480, 770), step=40, width=2)
    s.text(1140, 620, "检索栈的脊梁", size=34, anchor="mt", stroke=2)
    s.text(1140, 700, "embedding 就是微调过的 BERT", size=30, anchor="mm", stroke=2)
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(813)
    s.text(110, 60, "ModernBERT：同一个编码器，现代原语", size=42)
    s.text(530, 146, "2018", size=32, anchor="mm")
    s.text(1060, 146, "2024", size=32, anchor="mm")
    s.line([(110, 175), (1490, 175)], width=7)
    rows = [
        ("位置", "学习式绝对", "RoPE"),
        ("激活", "GELU", "GeGLU"),
        ("归一化", "LayerNorm", "前置 RMSNorm"),
        ("注意力", "完整稠密", "局部 128 + 全局"),
        ("上下文", "512", "8192"),
        ("分词", "WordPiece", "BPE"),
    ]
    for i, (k, old, new) in enumerate(rows):
        y = 235 + i * 88
        s.text(110, y, k, size=32, anchor="lm")
        s.text(530, y, old, size=32, anchor="mm")
        s.arrow(730, y, 800, y, width=7)
        hot = i in (2, 4)
        s.box(840, y - 34, 1240, y + 34, r=10, width=7, fill=YELLOW if hot else PAPER)
        s.text(1040, y, new, size=30, anchor="mm", stroke=2 if hot else 0)
    s.box(1265, 205, 1490, 355, r=12, width=8, fill=PAPER)
    s.text(1378, 232, "8K 时比", size=26, anchor="mt")
    s.text(1378, 275, "DeBERTa-v3", size=26, anchor="mm")
    s.text(1378, 325, "快 2–3×", size=30, anchor="mm")
    s.text(110, 800, "Flash Attention 原生，GLUE 分数还更高", size=34)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(814)
    s.text(110, 60, "什么时候别选 BERT", size=46)
    # left: don't
    s.box(110, 160, 720, 560, r=18, width=10, fill=PAPER)
    s.text(415, 195, "别选", size=40, anchor="mt")
    items = ["任何生成式任务", "编码器没法自回归输出", "1B 以下的小解码器更灵活"]
    for i, item in enumerate(items):
        s.cross(160, 300 + i * 80, r=18, width=7)
        s.text(200, 300 + i * 80, item, size=30, anchor="lm")
    s.text(415, 530, "Phi-3-Mini · Qwen2-1.5B", size=26, anchor="mb")
    # right: do
    s.box(790, 160, 1490, 560, r=18, width=10, fill=YELLOW)
    s.streaks((800, 170, 1480, 550), step=44, width=2)
    s.text(1140, 195, "该选", size=40, anchor="mt", stroke=2)
    items = ["检索与语义搜索嵌入", "分类：情感 / 意图 / 毒性", "NER 等逐位置标注", "交叉编码器重排"]
    for i, item in enumerate(items):
        s.check(840, 300 + i * 66, r=17, width=7)
        s.text(880, 300 + i * 66, item, size=28, anchor="lm", stroke=2)
    s.line([(110, 620), (1490, 620)], width=6)
    s.text(110, 660, "交叉编码器把 query 和 doc 一起喂进 BERT", size=34)
    s.text(110, 720, "双向注意力带来比双编码器更高的相关性质量", size=34)
    s.text(110, 790, "重排器还会比 LLM 重排快约十倍", size=36)
    s.save("p09")


# ---------------------------------------------------------------- cover
def cover():
    base = Image.new("RGB", (1920, 1080), PAPER)
    d = ImageDraw.Draw(base)
    title_font = ImageFont.truetype(FONT, 112)
    sub_font = ImageFont.truetype(FONT, 62)
    meta_font = ImageFont.truetype(FONT, 32)
    d.text((120, 160), "BERT", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((120, 300), "掩码语言建模", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((120, 460), "预测被挖掉的词", font=sub_font, fill=INK)
    d.rectangle([120, 570, 700, 580], fill=INK)
    d.text((120, 610), "07-06 · Transformers Deep Dive", font=meta_font, fill=INK)
    art = Image.open(OUT / "p01.png").convert("RGB")
    art = art.resize((1040, 585), Image.LANCZOS)
    base.paste(art, (800, 400))
    base.save(OUT / "cover.png")
    print("wrote", OUT / "cover.png")


if __name__ == "__main__":
    for fn in (p01, p02, p03, p04, p05, p06, p07, p08, p09):
        fn()
    cover()
