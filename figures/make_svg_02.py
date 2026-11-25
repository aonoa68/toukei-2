# -*- coding: utf-8 -*-
"""統計学Ⅱ 第02回（条件付き確率）の図。"""
import os
import numpy as np
from svgkit import Svg, RED, INDIGO, TEAL, AMBER

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg.render())
    print(f"  -> out/{name}")


# ===== 図A：2人の子ども問題 ============================================
def fig_children():
    s = Svg(720, 342, "ch",
            "2人の子ども問題 ―― 消えるのは1通りだけ",
            "男女が半々で独立に決まるとき、2人の組み合わせは"
            "（男,男）（男,女）（女,男）（女,女）の4通りが等確率である。"
            "「少なくとも1人は女」と分かると（男,男）の1通りだけが消え、"
            "残りは3通り。そのうち「2人とも女」は1通りなので、"
            "確率は4分の1から3分の1に更新される。2分の1にはならない。")
    s.text(0, 28, "「少なくとも1人は女」で消えるのは、4通りのうち1通りだけ", 13.5,
           bold=True)
    cells = [("男", "男", False), ("男", "女", True),
             ("女", "男", True), ("女", "女", True)]
    W, H, G = 150, 96, 14
    X0, Y0 = 60, 62
    for i, (a, b, keep) in enumerate(cells):
        x = X0 + i * (W + G)
        col = TEAL if keep else RED
        s.rect(x, Y0, W, H, fill=col, fop=0.10 if keep else 0.18,
               stroke=col, sop=0.6, r=5)
        s.text(x + W/2, Y0 + 36, f"上の子 {a}", 12.5, anchor="middle")
        s.text(x + W/2, Y0 + 60, f"下の子 {b}", 12.5, anchor="middle")
        s.text(x + W/2, Y0 + 84, "各 1/4", 10.5, anchor="middle", op=0.6)
        if not keep:
            s.line(x + 10, Y0 + 10, x + W - 10, Y0 + H - 10, RED, 2.4, 0.8)
            s.line(x + W - 10, Y0 + 10, x + 10, Y0 + H - 10, RED, 2.4, 0.8)
            s.text(x + W/2, Y0 + H + 22, "消える", 12, anchor="middle",
                   bold=True, color=RED)
    x3 = X0 + 3 * (W + G)
    s.rect(x3 - 3, Y0 - 3, W + 6, H + 6, stroke=AMBER, width=2.4, sop=0.9, r=7)
    s.text(x3 + W/2, Y0 + H + 22, "これが「2人とも女」", 12, anchor="middle",
           bold=True, color=AMBER)
    s.line(X0 + W + G - 7, 196, X0 + 4*(W+G) - G, 196, TEAL, 2, 0.6)
    s.text(X0 + W + G + (3*W + 2*G)/2, 216,
           "残るのは 3通り（どれも同じ確からしさ）", 12.5, anchor="middle",
           bold=True, color=TEAL)
    s.text(0, 258, "答えは 1/3。「もう1人が男か女か」と考えると 1/2 に見えるが、"
           "それは（女,男）と（男,女）を1つに数えてしまっている。", 11.5, op=0.95)
    s.text(0, 282, "情報を得る ＝ 舞台を絞り込む ＝ 確率を更新する。"
           "ここでは 1/4 → 1/3 に上がった。", 11.5, op=0.95)
    s.text(0, 316, "（男女が半々・独立という仮定のもとでの値。"
           "10万世帯のシミュレーションでも約 0.333 になる。）", 11, op=0.7)
    save("02_children.svg", s)


# ===== 図B：100人で見る「条件の世界に絞る」 =============================
def fig_grid():
    nA, nB, nAB = 30, 20, 12
    print(f"  P(A)={nA/100:.2f} P(B)={nB/100:.2f} P(A∩B)={nAB/100:.2f}")
    print(f"  P(A|B)={nAB/nB:.2f}  P(B|A)={nAB/nA:.2f}  "
          f"P(A)P(B)={nA*nB/10000:.2f}")
    s = Svg(720, 392, "gd",
            "100人の格子で見る条件付き確率",
            f"学生100人のうちアルバイトをしているのが{nA}人、一人暮らしが{nB}人、"
            f"その両方が{nAB}人。左は100人ぜんたいで、アルバイトの割合は"
            f"{nA}/100 = {nA/100:.2f}。右は「一人暮らし」の{nB}人だけに舞台を絞ったもので、"
            f"その中でアルバイトは{nAB}人、割合は{nAB}/{nB} = {nAB/nB:.2f} に変わる。"
            f"分母も分子も切り替わっている。")
    s.text(0, 28, "条件がつくと、分母も分子も切り替わる", 13.5, bold=True)
    # 1..100 の属性を決める（上から順に：両方12・アルバイトのみ18・一人暮らしのみ8）
    kind = []
    for i in range(100):
        if i < nAB:
            kind.append("both")
        elif i < nA:
            kind.append("A")
        elif i < nA + (nB - nAB):
            kind.append("B")
        else:
            kind.append("none")

    def grid(x0, y0, keep):
        for i, k in enumerate(kind):
            r, c = divmod(i, 10)
            x, y = x0 + c * 22, y0 + r * 22
            if keep and k not in ("both", "B"):
                s.circle(x, y, 6.5, "currentColor", 0.07)
                continue
            col = {"both": AMBER, "A": INDIGO, "B": TEAL, "none": "currentColor"}[k]
            op = 0.85 if k in ("both",) else (0.6 if k != "none" else 0.14)
            s.circle(x, y, 6.5, col, op)

    grid(40, 76, False)
    grid(420, 76, True)
    s.text(40 - 16, 60, "① 100人ぜんたい", 12.5, bold=True)
    s.text(420 - 16, 60, "② 一人暮らしの20人だけに絞る", 12.5, bold=True, color=TEAL)
    s.text(24, 340, f"アルバイト {nA}人 ÷ 100人 ＝ {nA/100:.2f}", 12.5,
           bold=True, color=INDIGO)
    s.text(24, 360, "これが P(A)", 11.5, op=0.8)
    s.text(404, 340, f"アルバイト {nAB}人 ÷ {nB}人 ＝ {nAB/nB:.2f}", 12.5,
           bold=True, color=AMBER)
    s.text(404, 360, "これが P(A | B)", 11.5, op=0.8)
    # 凡例
    s.circle(28, 306, 6.5, AMBER, 0.85); s.text(42, 310, f"両方 {nAB}人", 11)
    s.circle(140, 306, 6.5, INDIGO, 0.6); s.text(154, 310, f"アルバイトのみ {nA-nAB}人", 11)
    s.circle(300, 306, 6.5, TEAL, 0.6); s.text(314, 310, f"一人暮らしのみ {nB-nAB}人", 11)
    s.text(0, 388, f"P(A)={nA/100:.2f} なのに P(A|B)={nAB/nB:.2f}。"
           f"知ると確率が変わるので、この100人の中で A と B は独立ではない"
           f"（{nA/100:.2f}×{nB/100:.2f}＝{nA*nB/10000:.2f} ≠ {nAB/100:.2f}）。",
           11.5, op=0.95)
    save("02_grid.svg", s)


# ===== 図C：独立と排反は別物 ===========================================
def fig_indep():
    s = Svg(720, 352, "id",
            "独立と排反は、まったく別の概念",
            "左はサイコロで A＝偶数の目、B＝3の目。重なりがないので排反だが、"
            "3が出たと分かると偶数の確率は1/2から0に変わるので独立ではない。"
            "右はコインを2回投げて A＝2投目が表、B＝1投目が表。"
            "重なりはあり、1投目を知っても2投目の確率は1/2のまま変わらないので独立である。"
            "排反は「重ならない」、独立は「知っても確率が変わらない」。")
    s.text(0, 28, "重ならないこと（排反）と、知っても変わらないこと（独立）", 13.5,
           bold=True)
    # 左：排反だが独立でない
    s.text(10, 64, "サイコロ　A＝偶数の目、B＝3の目", 12.5, bold=True)
    X, Y, CW, CH = 20, 80, 44, 44
    for i in range(6):
        x = X + i * (CW + 8)
        inA, inB = (i + 1) % 2 == 0, (i + 1) == 3
        col = INDIGO if inA else (RED if inB else "currentColor")
        s.rect(x, Y, CW, CH, fill=col, fop=0.22 if (inA or inB) else 0.05,
               stroke=col, sop=0.6 if (inA or inB) else 0.25, r=5)
        s.text(x + CW/2, Y + 28, f"{i+1}", 15, anchor="middle", bold=True)
    s.rect(18, 78, 48, 48, stroke=INDIGO, width=0, sop=0)
    s.text(10, 150, "A＝偶数（2・4・6）", 11.5, color=INDIGO)
    s.text(150, 150, "B＝3", 11.5, color=RED)
    s.text(10, 174, "重なりは無い → 排反", 12, bold=True)
    s.text(10, 196, "だが B（3が出た）と分かると", 11.5, op=0.9)
    s.text(10, 216, "P(A) は 1/2 → 0 に変わる → 独立ではない", 12, bold=True,
           color=RED)
    # 右：独立だが排反でない
    s.text(390, 64, "コイン2回　A＝2投目が表、B＝1投目が表", 12.5, bold=True)
    labs = [("表", "表", True, True), ("表", "裏", True, False),
            ("裏", "表", False, True), ("裏", "裏", False, False)]
    for i, (b, a, inB, inA) in enumerate(labs):
        x = 396 + (i % 2) * 150
        y = 80 + (i // 2) * 52
        col = AMBER if (inA and inB) else (INDIGO if inA else
                                           (TEAL if inB else "currentColor"))
        op = 0.22 if (inA or inB) else 0.05
        s.rect(x, y, 140, 44, fill=col, fop=op, stroke=col,
               sop=0.6 if (inA or inB) else 0.25, r=5)
        s.text(x + 70, y + 27, f"1投目 {b}　2投目 {a}", 11.5, anchor="middle")
    s.text(390, 174, "橙＝A と B の両方／青＝A のみ／緑＝B のみ", 11, op=0.75)
    s.text(390, 196, "重なりがある（表・表）→ 排反ではない", 12, bold=True)
    s.text(390, 218, "1投目を知っても 2投目は 1/2 のまま → 独立", 12, bold=True,
           color=TEAL)
    s.line(360, 56, 360, 232, op=0.2)
    s.text(0, 268, "排反な2つは、片方が起きたらもう片方は起きないと分かる。"
           "つまり「知ると確率が変わる」ので、確率が0でないかぎり独立にはならない。",
           11.5, op=0.95)
    s.text(0, 292, "この2つを同じ言葉で呼ばないこと。"
           "第2回の課題でも、ここは分けて書いてほしい。", 11.5, op=0.95)
    s.text(0, 326, "（サイコロは6面が等確率、コインは表裏が半々で独立、"
           "という仮定のもとでの値。）", 11, op=0.7)
    save("02_indep.svg", s)


if __name__ == "__main__":
    print("図A 2人の子ども問題"); fig_children()
    print("図B 100人の格子"); fig_grid()
    print("図C 独立と排反"); fig_indep()
