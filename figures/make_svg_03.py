# -*- coding: utf-8 -*-
"""統計学Ⅱ 第03回（ベイズの定理）の図。数値はすべてここで計算する。"""
import math, os
import numpy as np
from scipy import stats
from svgkit import Svg, RED, INDIGO, TEAL, AMBER

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
SENS, SPEC = 0.99, 0.99


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg.render())
    print(f"  -> out/{name}")


def ppv(pi, sens=SENS, spec=SPEC):
    return sens * pi / (sens * pi + (1 - spec) * (1 - pi))


# ===== 図A：100万人の自然頻度 ==========================================
def fig_freq():
    N, pi = 1_000_000, 0.01
    sick = int(N * pi); well = N - sick
    tp = int(sick * SENS); fp = int(well * (1 - SPEC))
    print(f"  病気 {sick:,} → 陽性 {tp:,} ／ 健康 {well:,} → 陽性 {fp:,}")
    print(f"  陽性 {tp+fp:,} 人のうち本当に病気は {tp:,} 人 = {tp/(tp+fp)*100:.1f}%")

    s = Svg(720, 400, "fq",
            "100万人を検査すると、陽性の半分は健康な人",
            f"有病率1%なので100万人のうち病気は{sick:,}人、健康は{well:,}人。"
            f"感度99%なので病気の人からは{tp:,}人が陽性になる。"
            f"特異度99%でも健康な人は{well:,}人と多いので、"
            f"その1%にあたる{fp:,}人が誤って陽性になる。"
            f"陽性{tp+fp:,}人のうち本当に病気なのは{tp:,}人で、"
            f"{tp/(tp+fp)*100:.0f}%にしかならない。")
    s.text(0, 28, "検査の精度99%と、陽性的中率50%は別の数字", 13.5, bold=True)
    # 帯で100万人を表す
    X, W0, Y, H = 20, 680, 60, 40
    ws = W0 * sick / N
    s.rect(X, Y, ws, H, fill=RED, fop=0.3, stroke=RED, sop=0.7, r=3)
    s.rect(X + ws, Y, W0 - ws, H, fill=TEAL, fop=0.22, stroke=TEAL, sop=0.6, r=3)
    s.text(X + 6, Y - 10, f"病気 {sick:,}人（1%）", 11.5, bold=True, color=RED)
    s.text(X + W0, Y - 10, f"健康 {well:,}人（99%）", 11.5, anchor="end",
           bold=True, color=TEAL)
    s.text(X + W0 / 2, Y + 25, "100万人", 13, anchor="middle", bold=True)
    # 陽性になる人
    Y2 = 160
    s.arrow(X + ws / 2, Y + H + 4, X + ws / 2, Y2 - 6, RED, 1.6, 0.7)
    s.arrow(X + ws + (W0 - ws) / 2, Y + H + 4, X + ws + (W0 - ws) / 2, Y2 - 6,
            TEAL, 1.6, 0.7)
    s.text(X + ws / 2 + 8, Y + H + 22, "感度99%", 11, color=RED)
    s.text(X + ws + (W0 - ws) / 2 + 8, Y + H + 22, "健康な人の1%が誤って陽性", 11,
           color=TEAL)
    # 陽性者の内訳（拡大して描く）
    BW = 600
    wtp = BW * tp / (tp + fp)
    s.rect(X, Y2, wtp, 52, fill=RED, fop=0.3, stroke=RED, sop=0.7, r=4)
    s.rect(X + wtp, Y2, BW - wtp, 52, fill=TEAL, fop=0.22, stroke=TEAL,
           sop=0.6, r=4)
    s.text(X + wtp / 2, Y2 + 32, f"真陽性 {tp:,}人", 12.5, anchor="middle",
           bold=True, color=RED)
    s.text(X + wtp + (BW - wtp) / 2, Y2 + 32, f"偽陽性 {fp:,}人", 12.5,
           anchor="middle", bold=True, color=TEAL)
    s.text(X, Y2 - 12, f"陽性になった {tp+fp:,}人（ここに拡大して内訳を見る）", 12,
           bold=True)
    s.text(0, 268, f"P(病気 | 陽性) ＝ {tp:,} ÷ {tp+fp:,} ＝ "
           f"{tp/(tp+fp)*100:.0f}%", 14, bold=True, color=AMBER)
    s.text(0, 300, "病気の人はもともと少ないので、健康な人のたった1%でも、"
           "人数にすると真陽性と同じだけ出てしまう。", 11.5, op=0.95)
    s.text(0, 324, "直感が外すのは P(陽性 | 病気) ＝ 99% と "
           "P(病気 | 陽性) ＝ 50% を取り違えるから。縦棒のどちらが条件かで別の量になる。",
           11.5, op=0.95)
    s.text(0, 348, "検査の性能が低いのではない。50%は「有病率1%のもとでの答え」である。",
           11.5, op=0.95)
    s.text(0, 382, "（感度99%・特異度99%・有病率1%としたときの計算。"
           "人数は小数を切り捨てている。）", 11, op=0.7)
    save("03_freq.svg", s)


# ===== 図B：基準率を動かすと、答えは激変する ===========================
def fig_baserate():
    marks = [0.0001, 0.001, 0.01, 0.1, 0.5]
    for m in marks:
        print(f"  有病率 {m*100:g}% → 陽性的中率 {ppv(m)*100:.1f}%")
    xs = np.logspace(-4.3, -0.02, 400)
    ys = ppv(xs)

    s = Svg(720, 392, "br",
            "検査の性能は同じでも、珍しい病気ほど陽性的中率は下がる",
            "横軸は有病率（対数目盛り）、縦軸は陽性的中率。"
            "感度99%・特異度99%で固定しているのに、"
            "有病率0.01%なら1.0%、0.1%なら9.0%、1%なら50.0%、"
            "10%なら91.7%、50%なら99.0%と大きく変わる。"
            "検査の性能だけを見て判断すると、この基準率を無視することになる。")
    L, R, T, B = 58, 580, 68, 258
    px = lambda v: L + (math.log10(v) + 4.3) / 4.28 * (R - L)
    py = lambda v: B - v * (B - T)
    s.text(0, 30, "検査の性能は何も変えていない。変えたのは病気の珍しさだけ", 13.5,
           bold=True)
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        s.line(L, py(v), R, py(v), op=0.5 if v == 0 else 0.13)
        s.text(L - 8, py(v) + 4, f"{int(v*100)}%", 11, anchor="end", op=0.75)
    for v, lab in [(0.0001, "0.01%"), (0.001, "0.1%"), (0.01, "1%"),
                   (0.1, "10%"), (0.5, "50%")]:
        s.line(px(v), T, px(v), B, op=0.1)
        s.text(px(v), B + 19, lab, 11, anchor="middle", op=0.75)
    s.line(L, T, L, B, op=0.5)
    s.text((L + R) / 2, B + 42, "有病率（対数目盛り）", 11.5, anchor="middle", op=0.8)
    s.path([(px(x), py(y)) for x, y in zip(xs, ys)], INDIGO, 2.6)
    for m in marks:
        v = ppv(m)
        s.circle(px(m), py(v), 4.6, RED)
        dx, dy, anc = ((10, -10, "start") if m < 0.005 else
                       (10, -10, "start") if m < 0.02 else
                       (10, 18, "start") if m < 0.05 else
                       (-10, -12, "end"))
        s.text(px(m) + dx, py(v) + dy, f"{v*100:.1f}%", 12, anchor=anc,
               bold=True, color=RED)
    s.text(596, 120, "感度 99%", 12, bold=True, color=TEAL)
    s.text(596, 138, "特異度 99%", 12, bold=True, color=TEAL)
    s.text(596, 160, "どの点でも", 11.5, op=0.85)
    s.text(596, 176, "同じ検査", 11.5, op=0.85)
    s.text(0, 322, "もともと稀なものを探すほど、警告の多くは誤りになる。"
           "これを基準率の誤謬という。", 11.5, op=0.95)
    s.text(0, 346, "迷惑メール判定、顔認証、まれな不正の検知 ―― 同じ罠がある。"
           "「精度99%のAIが警告した」だけでは何も言えない。", 11.5, op=0.95)
    s.text(0, 380, "（感度・特異度を99%に固定して、有病率だけを動かしたときの計算値。）",
           11, op=0.7)
    save("03_baserate.svg", s)


# ===== 図C：逐次更新 ===================================================
def fig_update():
    # 本文の事後平均 0.714 / 0.773 / 0.696 から、表の回数を復元する
    steps = [(0, 0), (5, 4), (20, 16), (100, 70)]
    for n, k in steps:
        print(f"  {n}回中 表{k}回 → 事後 Beta({1+k}, {1+n-k}) "
              f"平均 {(k+1)/(n+2):.3f}")
    s = Svg(720, 404, "up",
            "観測が増えると、事後分布は締まっていく",
            "横軸は未知の表確率 p の候補、縦軸はその候補の確からしさ（密度）。"
            "最初は真っ平らで、p について何も分かっていない状態を表す。"
            "5回で事後平均0.714、20回で0.773、100回で0.696となり、"
            "山は細く高くなっていく。ただし20回の時点のほうが5回の時点より"
            "真の値0.7から離れており、毎回かならず近づくわけではない。")
    L, R, T, B = 58, 690, 66, 268
    px = lambda v: L + v * (R - L)
    ymax = 10.0
    py = lambda v: B - min(v, ymax) / ymax * (B - T)
    s.text(0, 30, "毎回かならず近づくのではない。それでも山は細くなる", 13.5, bold=True)
    xs = np.linspace(0.001, 0.999, 400)
    cols = ["currentColor", TEAL, AMBER, INDIGO]
    for (n, k), col in zip(steps, cols):
        a, b = 1 + k, 1 + n - k
        ys = stats.beta.pdf(xs, a, b)
        s.path([(px(x), py(y)) for x, y in zip(xs, ys)], col, 2.4,
               0.55 if n == 0 else 1.0)
    s.line(L, B, R, B, op=0.5)
    for v in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        s.line(px(v), T, px(v), B, op=0.08)
        s.text(px(v), B + 19, f"{v:g}", 11, anchor="middle", op=0.75)
    s.text((L + R) / 2, B + 42, "未知の表確率 p の候補", 11.5, anchor="middle", op=0.8)
    s.line(px(0.7), T - 14, px(0.7), B, RED, 1.6, 0.8, dash="4 3")
    s.text(px(0.7), T - 20, "真の値 0.7", 11.5, anchor="middle", bold=True, color=RED)
    ylab = [("0回（真っ平ら）", "currentColor", 0.7),
            ("5回　事後平均 0.714", TEAL, 1.0),
            ("20回　事後平均 0.773", AMBER, 1.0),
            ("100回　事後平均 0.696", INDIGO, 1.0)]
    for i, (lab, col, op) in enumerate(ylab):   # 凡例は図の中の空いた左上に置く
        y = 102 + i * 26
        s.line(80, y - 4, 112, y - 4, col, 2.4, op)
        s.text(120, y, lab, 11.5, op=0.95)
    s.text(0, 330, "20回の時点のほうが、5回の時点より真の値から離れている。"
           "計算の誤りではなく、標本のばらつきである。", 11.5, op=0.95)
    s.text(0, 354, "言えるのは「モデルが正しく、データが十分にあれば絞り込める」まで。"
           "「増やすたびに必ず近づく」ではない。", 11.5, op=0.95)
    s.text(0, 388, "（一様な事前 Beta(1,1) から出発し、表 k 回・裏 n−k 回で "
           "Beta(1+k, 1+n−k) に更新したもの。本文の事後平均と同じ観測。）",
           11, op=0.7)
    save("03_update.svg", s)


if __name__ == "__main__":
    print("図A 100万人の自然頻度"); fig_freq()
    print("図B 基準率"); fig_baserate()
    print("図C 逐次更新"); fig_update()
