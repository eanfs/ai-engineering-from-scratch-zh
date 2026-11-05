#!/usr/bin/env python3
"""Author the 07-08 illustrations locally as industrial-marker diagrams.

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
    s = Sheet(808)
    s.text(110, 60, "编码器 → 解码器：把两个拼回去", size=44)
    # encoder
    s.box(140, 190, 700, 570, r=18, width=9, fill=PAPER)
    s.text(170, 215, "编码器", size=34)
    s.text(170, 265, "双向读完整段输入，只跑一次", size=26)
    for i, label in enumerate(["自注意力", "前馈"]):
        s.box(180, 320 + i * 70, 660, 378 + i * 70, r=10, width=6, fill=PAPER)
        s.text(420, 349 + i * 70, label, size=26, anchor="mm")
    s.text(420, 500, "重复 N 层", size=28, anchor="mm")
    # arrow
    s.arrow(712, 380, 790, 380, width=9, head=26)
    s.text(751, 350, "K, V", size=24, anchor="mb")
    # decoder
    s.box(800, 190, 1460, 570, r=18, width=9, fill=PAPER)
    s.text(830, 215, "解码器", size=34)
    s.text(830, 265, "自回归生成，每步看一次编码器", size=26)
    for i, label in enumerate(["masked 自注意力", "交叉注意力", "前馈"]):
        s.box(840, 320 + i * 70, 1420, 378 + i * 70, r=10, width=6, fill=YELLOW if i == 1 else PAPER)
        s.text(1130, 349 + i * 70, label, size=26, anchor="mm", stroke=2 if i == 1 else 0)
    s.chip(170, 640, "T5：文本进，文本出", size=28)
    s.chip(560, 640, "BART：去噪，重建整句", size=28)
    s.text(170, 750, "编码器输出可以缓存，长输入几乎是免费的", size=32)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(809)
    s.text(110, 60, "交叉注意力：源和目标在这里对话", size=42)
    # encoder stack
    s.box(120, 180, 560, 620, r=16, width=8, fill=PAPER)
    s.text(150, 205, "编码器", size=32)
    for i in range(3):
        s.box(150, 260 + i * 105, 530, 330 + i * 105, r=10, width=6, fill=PAPER)
        s.text(340, 295 + i * 105, "双向自注意力", size=24, anchor="mm")
    s.text(120, 660, "输入序列", size=28)
    # decoder stack
    s.box(760, 180, 1180, 620, r=16, width=8, fill=PAPER)
    s.text(790, 205, "解码器", size=32)
    s.box(790, 260, 1150, 330, r=10, width=6, fill=PAPER)
    s.text(970, 295, "masked 自注意力", size=24, anchor="mm")
    s.box(790, 380, 1150, 450, r=10, width=8, fill=YELLOW)
    s.streaks((798, 388, 1142, 442), step=28, width=2)
    s.text(970, 415, "交叉注意力", size=26, anchor="mm", stroke=2)
    s.box(790, 500, 1150, 570, r=10, width=6, fill=PAPER)
    s.text(970, 535, "前馈", size=24, anchor="mm")
    # arrows
    s.arrow(568, 415, 780, 415, width=8, head=22)
    s.text(640, 385, "K, V", size=24, anchor="mb")
    s.text(1200, 200, "Q 来自目标", size=26)
    # right notes
    s.text(1340, 260, "编码器信息", size=28)
    s.text(1340, 310, "进入解码器的", size=28)
    s.text(1340, 360, "唯一通道", size=34, stroke=2)
    s.text(1340, 480, "每个解码步", size=26)
    s.text(1340, 525, "都对同一个", size=26)
    s.text(1340, 570, "编码器输出做", size=26)
    s.text(120, 740, "Q 来自解码器，K 和 V 来自编码器——这就是「对话」的位置", size=30)
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(810)
    s.text(110, 60, "训练：错位一格 + teacher forcing", size=42)
    s.text(150, 160, "解码器输入", size=26)
    for i, t in enumerate(["<bos>", "我", "爱", "你"]):
        x = 150 + i * 160
        s.box(x, 200, x + 130, 280, r=10, width=7, fill=PAPER)
        s.text(x + 65, 240, t, size=28, anchor="mm")
    s.text(150, 320, "目标", size=26)
    for i, t in enumerate(["我", "爱", "你", "<eos>"]):
        x = 240 + i * 160
        s.box(x, 360, x + 130, 440, r=10, width=8, fill=YELLOW)
        s.streaks((x + 8, 368, x + 122, 432), step=26, width=2)
        s.text(x + 65, 400, t, size=28, anchor="mm", stroke=2)
        s.arrow(x - 10, 286, x + 60, 354, width=6)
    s.box(960, 180, 1480, 440, r=14, width=8, fill=PAPER)
    s.text(990, 210, "和 GPT 完全一样", size=30)
    s.text(990, 275, "只算错位一格", size=26)
    s.text(990, 320, "的交叉熵", size=26)
    s.text(990, 390, "只是多了编码器条件", size=24)
    s.text(110, 530, "teacher forcing：训练时喂真实的上一词，不是模型自己的预测", size=30)
    s.box(110, 610, 1490, 710, r=16, width=9, fill=YELLOW)
    s.streaks((120, 620, 1480, 700), step=36, width=2)
    s.text(800, 660, "同一个损失：下一个 token 的交叉熵", size=34, anchor="mm", stroke=2)
    s.text(110, 770, "训练并行，推理串行——和纯解码器没有区别", size=30)
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(811)
    s.text(110, 60, "T5：把 span 换成哨兵", size=46)
    s.text(130, 160, "源序列", size=28)
    src = ["The", "quick", "[extra_id_0]", "fox", "jumps", "[extra_id_1]", "dog"]
    x = 130
    for w in src:
        hot = w.startswith("[")
        wd = s.width_of(w, 26) + 34
        s.box(x, 200, x + wd, 280, r=10, width=6, fill=YELLOW if hot else PAPER)
        s.text(x + wd / 2, 240, w, size=24, anchor="mm", stroke=2 if hot else 0)
        x += wd + 14
    s.text(130, 340, "解码目标", size=28)
    tgt = ["[extra_id_0]", "brown", "[extra_id_1]", "over the lazy"]
    x = 130
    for w in tgt:
        hot = w.startswith("[")
        wd = max(140, s.width_of(w, 26) + 34)
        s.box(x, 380, x + wd, 460, r=10, width=7, fill=METAL if hot else PAPER)
        s.text(x + wd / 2, 420, w, size=24, anchor="mm")
        x += wd + 14
    s.text(130, 520, "平均每段 3 个词，总共遮 15%", size=30)
    s.text(130, 580, "解码器只输出被破坏的 span", size=30)
    s.text(130, 640, "比重建整句便宜", size=30)
    s.text(130, 740, "哨兵就是占位符：源里标记挖空处，目标里重新标记输出段", size=28)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(812)
    s.text(110, 60, "T5 实跑：能还原，就说明记账没错", size=42)
    s.box(110, 160, 1490, 330, r=14, width=8, fill=PAPER)
    s.text(140, 180, "被破坏的源", size=26)
    s.text(140, 230, "the quick <extra_id_0> fox jumps over the lazy dog", size=24)
    s.text(140, 270, "a <extra_id_1> time saves nine", size=24)
    s.box(110, 370, 1490, 540, r=14, width=8, fill=PAPER)
    s.text(140, 390, "解码器目标", size=26)
    s.text(140, 440, "<extra_id_0> brown   <extra_id_1> stitch in   <extra_id_2>", size=24)
    s.box(110, 600, 1490, 710, r=16, width=9, fill=YELLOW)
    s.streaks((120, 610, 1480, 700), step=36, width=2)
    s.check(200, 655, r=24, width=8)
    s.text(250, 655, "拼回去 = 原句：YES", size=36, anchor="lm", stroke=2)
    s.text(110, 770, "非哨兵源词 + 解出的 span，正好覆盖整句", size=30)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(813)
    s.text(110, 60, "BART：五种加噪，重建整句", size=44)
    cards = [
        ("token 掩码", "词 → <mask>"),
        ("token 删除", "直接删掉"),
        ("文本填充", "span → <mask>"),
        ("句子打乱", "调换顺序"),
        ("文档旋转", "整体移位"),
    ]
    for i, (title, note) in enumerate(cards):
        x = 110 + i * 278
        s.box(x, 180, x + 250, 380, r=14, width=8, fill=YELLOW if i in (2, 3) else PAPER)
        s.text(x + 125, 210, title, size=27, anchor="mt", stroke=2 if i in (2, 3) else 0)
        s.text(x + 125, 320, note, size=24, anchor="mt")
    s.text(110, 450, "文本填充 + 句子打乱：下游分数最好", size=34)
    s.text(110, 520, "解码器始终重建原文，一整句都要还原", size=30)
    s.text(110, 580, "所以预训练算力比 T5 更高", size=30)
    s.text(110, 690, "T5 只解被挖掉的 span；BART 要解整句", size=32)
    s.text(110, 750, "差别在这里，不在编码器", size=30)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(814)
    s.text(110, 60, "推理：beam 宽度 4–5", size=46)
    # beam tree
    s.box(130, 250, 260, 330, r=10, width=8, fill=YELLOW)
    s.text(195, 290, "<bos>", size=26, anchor="mm", stroke=2)
    for i in range(4):
        x = 380 + i * 112
        y = 130 + i * 110
        s.arrow(268, 290, x - 8, y + 28, width=6)
        s.box(x, y, x + 96, y + 56, r=8, width=6, fill=PAPER)
        s.text(x + 48, y + 28, f"候选{i + 1}", size=20, anchor="mm")
    s.line([(110, 640), (760, 640)], width=6)
    s.text(130, 670, "每一步保留 4–5 条部分序列", size=30)
    s.text(130, 730, "最后按总分选一条", size=30)
    # notes
    s.check(850, 230, r=20, width=7)
    s.text(895, 230, "翻译：源句清晰，束搜索有效", size=30, anchor="lm")
    s.check(850, 320, r=20, width=7)
    s.text(895, 320, "摘要：输出分布窄，beam 稳", size=30, anchor="lm")
    s.cross(850, 430, r=18, width=7)
    s.text(895, 430, "聊天：没有固定输入", size=30, anchor="lm")
    s.text(910, 490, "beam 反而让回答变得死板", size=26)
    s.text(870, 590, "贪心适合确定性任务", size=28)
    s.text(870, 640, "top-p 适合开放生成", size=28)
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(815)
    s.text(110, 60, "2026：该怎么选", size=46)
    s.box(110, 160, 760, 560, r=18, width=10, fill=YELLOW)
    s.streaks((120, 170, 750, 550), step=44, width=2)
    s.text(435, 195, "编码器-解码器仍合适", size=34, anchor="mt", stroke=2)
    for i, item in enumerate(["翻译", "语音转写（Whisper）", "摘要", "结构化抽取"]):
        s.check(165, 290 + i * 62, r=16, width=6)
        s.text(205, 290 + i * 62, item, size=28, anchor="lm", stroke=2)
    s.box(820, 160, 1490, 560, r=18, width=10, fill=PAPER)
    s.text(1155, 195, "纯解码器已接管", size=34, anchor="mt")
    for i, item in enumerate(["聊天与推理", "代码补全", "长上下文任务", "需要 RLHF 的助手"]):
        s.check(875, 290 + i * 62, r=16, width=6)
        s.text(915, 290 + i * 62, item, size=28, anchor="lm")
    s.line([(110, 620), (1490, 620)], width=6)
    s.text(110, 660, "指令微调和 RLHF，都假设模型有一个解码器", size=32)
    s.text(110, 730, "输入输出模态不同、或 beam 质量重要时，双栈仍然赢", size=30)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(816)
    s.text(110, 60, "T5 vs BART：同一个双栈，两种预训练", size=40)
    s.box(110, 160, 780, 560, r=18, width=9, fill=PAPER)
    s.text(140, 185, "T5", size=40)
    s.text(140, 255, "一切任务 → 文本进，文本出", size=28)
    s.text(140, 320, "预训练只解被挖掉的 span", size=28)
    s.text(140, 385, "输出更短，算力更省", size=28)
    s.text(140, 470, "encoder-decoder，统一格式", size=24)
    s.box(820, 160, 1490, 560, r=18, width=9, fill=PAPER)
    s.text(850, 185, "BART", size=40)
    s.text(850, 255, "五种噪声，任意组合", size=28)
    s.text(850, 320, "解码器重建整句原文", size=28)
    s.text(850, 385, "信号更强，算力更高", size=28)
    s.text(850, 470, "适合摘要、翻译、生成", size=24)
    s.line([(110, 620), (1490, 620)], width=6)
    s.text(110, 660, "架构没有输，输的是规模和后训练的主战场", size=36)
    s.text(110, 730, "纯解码器拿走了聚光灯，双栈守住了输入模态不同的地方", size=28)
    s.save("p09")


# ---------------------------------------------------------------- cover
def cover():
    base = Image.new("RGB", (1920, 1080), PAPER)
    d = ImageDraw.Draw(base)
    title_font = ImageFont.truetype(FONT, 112)
    sub_font = ImageFont.truetype(FONT, 62)
    meta_font = ImageFont.truetype(FONT, 32)
    d.text((120, 160), "T5 & BART", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((120, 300), "编码器-解码器", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((120, 460), "理解与生成，拼回去", font=sub_font, fill=INK)
    d.rectangle([120, 570, 700, 580], fill=INK)
    d.text((120, 610), "07-08 · Transformers Deep Dive", font=meta_font, fill=INK)
    art = Image.open(OUT / "p01.png").convert("RGB")
    art = art.resize((1040, 585), Image.LANCZOS)
    base.paste(art, (800, 400))
    base.save(OUT / "cover.png")
    print("wrote", OUT / "cover.png")


if __name__ == "__main__":
    for fn in (p01, p02, p03, p04, p05, p06, p07, p08, p09):
        fn()
    cover()
