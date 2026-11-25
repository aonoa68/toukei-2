# -*- coding: utf-8 -*-
"""統計学Ⅱ 第10回（因果推論：RCTと観察研究）の図。"""
import os
import numpy as np
from svgkit import Svg, RED, INDIGO, TEAL, AMBER

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg.render())
    print(f"  -> out/{name}")


def node(s, x, y, w, h, text, col, sub=None):
    s.rect(x - w/2, y - h/2, w, h, fill=col, fop=0.12, stroke=col, sop=0.7, r=6)
    s.text(x, y + (0 if sub is None else -4), text, 12.5, anchor="middle",
           bold=True, color=col)
    if sub:
        s.text(x, y + 14, sub, 10.5, anchor="middle", op=0.7)


# ===== 図A：観察研究とRCTのちがい（DAG） ==============================
def fig_dag():
    s = Svg(720, 384, "dg",
            "観察研究とRCT ―― ランダム化は矢印を1本切る",
            "左は観察研究。健康志向が「サプリを飲むかどうか」と「健康」の両方に"
            "矢印を出しているので、飲んだ人と飲まない人の差には"
            "サプリの効果と健康志向の差が混ざってしまう。"
            "右はRCT。くじ引きが飲むかどうかを決めるので、"
            "健康志向からサプリへの矢印が切れる。"
            "残った差はサプリの効果だけになる。")
    s.text(0, 28, "ランダム化が切るのは、この1本だけ", 13.5, bold=True)

    def diagram(x0, w, title, cut):
        cx = x0 + w / 2
        s.text(x0, 60, title, 12.5, bold=True)
        node(s, cx, 108, 150, 46, "健康志向", AMBER, "（交絡）")
        node(s, cx - 98, 216, 124, 46, "サプリを飲む", INDIGO)
        node(s, cx + 98, 216, 124, 46, "健康", TEAL)
        # 健康志向 → サプリ
        if cut:
            s.line(cx - 46, 126, cx - 86, 190, AMBER, 2, 0.25, dash="5 4")
            s.line(cx - 80, 144, cx - 52, 174, RED, 3, 0.95)
            s.line(cx - 52, 144, cx - 80, 174, RED, 3, 0.95)
            s.text(cx - 110, 166, "切れる", 11.5, anchor="end", bold=True, color=RED)
        else:
            s.arrow(cx - 46, 126, cx - 86, 190, AMBER, 2, 0.9)
        s.arrow(cx + 46, 126, cx + 86, 190, AMBER, 2, 0.9)   # 健康志向 → 健康
        s.arrow(cx - 34, 216, cx + 34, 216, INDIGO, 2, 0.9)  # サプリ → 健康
        s.text(cx, 206, "効果 0", 11, anchor="middle", op=0.75)
        if cut:
            node(s, cx - 98, 300, 124, 40, "くじ引き", RED)
            s.arrow(cx - 98, 280, cx - 98, 242, RED, 2, 0.9)

    diagram(10, 330, "① 観察研究（本人が飲むかどうかを決める）", False)
    s.line(360, 50, 360, 330, op=0.18)
    diagram(390, 330, "② RCT（くじ引きで決める）", True)
    s.text(16, 272, "飲んだ人の健康 − 飲まない人の健康", 11, op=0.9)
    s.text(16, 290, "＝ サプリの効果 ＋ 健康志向の差", 11.5, bold=True, color=RED)
    s.text(16, 310, "2つを分けられない（交絡）", 11, color=RED, op=0.9)
    s.text(0, 352, "くじ引きは健康志向を見ないので、2つの群の健康志向は平均的にそろう。"
           "残った差はサプリの効果だけになる。", 11.5, op=0.95)
    s.text(0, 378, "（第6〜7回は「独立が崩れると推測が壊れる」だった。"
           "因果推論は逆に、独立を自分で作り出して使う。）", 11, op=0.7)
    save("10_dag.svg", s)


# ===== 図B：交絡が「効果」を捏造する ==================================
def fig_confound():
    rg = np.random.default_rng(3078)
    n = 400
    c = rg.normal(0, 1, n)                        # 健康志向
    t = (c + rg.normal(0, 0.6, n) > 0).astype(int)  # 自分で飲むか決める
    h = 50 + 8 * c + rg.normal(0, 3, n)           # 健康（サプリの効果は 0）
    d = h[t == 1].mean() - h[t == 0].mean()
    m1, m0 = c[t == 1].mean(), c[t == 0].mean()
    # 同じ健康志向の帯の中だけで比べる
    band = (c > -0.3) & (c < 0.3)
    db = h[band & (t == 1)].mean() - h[band & (t == 0)].mean()
    print(f"  観察差 {d:+.1f}／健康志向 飲んだ群 {m1:+.2f}・飲まない群 {m0:+.2f}")
    print(f"  健康志向 −0.3〜+0.3 の帯の中だけで比べると {db:+.1f}"
          f"（飲んだ{(band&(t==1)).sum()}人・飲まない{(band&(t==0)).sum()}人）")

    s = Svg(720, 392, "cf",
            "サプリの効果はゼロなのに、飲んだ人のほうが健康に見える",
            f"横軸は健康志向、縦軸は健康。サプリの効果はゼロに設定してある。"
            f"それでも飲んだ人（青）は健康志向が高いほうに偏っているので"
            f"（平均{m1:+.2f} 対 {m0:+.2f}）、単純に平均を比べると{d:+.1f}の差が出る。"
            f"同じ健康志向の帯の中だけで比べれば差は{db:+.1f}しかない。"
            f"見えていた差は、健康志向の差がそのまま映ったものである。")
    L, R, T, B = 62, 560, 72, 262
    xlo, xhi = c.min() - 0.2, c.max() + 0.2
    ylo, yhi = h.min() - 2, h.max() + 2
    px = lambda v: L + (v - xlo) / (xhi - xlo) * (R - L)
    py = lambda v: B - (v - ylo) / (yhi - ylo) * (B - T)
    s.text(0, 30, "効果ゼロの世界で、差が +9 も出てしまう", 13.5, bold=True)
    # 帯
    s.rect(px(-0.3), T, px(0.3) - px(-0.3), B - T, fill=AMBER, fop=0.12,
           stroke=AMBER, sop=0.5, r=3)
    s.text((px(-0.3) + px(0.3)) / 2, T - 10, "同じ健康志向の帯", 11,
           anchor="middle", bold=True, color=AMBER)
    for j in range(n):
        s.circle(px(c[j]), py(h[j]), 2.6, INDIGO if t[j] else TEAL, 0.5)
    for g, col, lab in [(1, INDIGO, "飲んだ人"), (0, TEAL, "飲まない人")]:
        mc, mh = c[t == g].mean(), h[t == g].mean()
        s.line(px(mc), py(mh) - 10, px(mc), py(mh) + 10, col, 2.6)
        s.line(px(mc) - 10, py(mh), px(mc) + 10, py(mh), col, 2.6)
    s.line(L, B, R, B, op=0.4); s.line(L, T, L, B, op=0.4)
    for v in (-2, -1, 0, 1, 2):
        s.text(px(v), B + 19, f"{v}".replace("-", "−"), 11, anchor="middle", op=0.7)
    s.text((L + R) / 2, B + 40, "健康志向", 11.5, anchor="middle", op=0.8)
    s.text(L - 8, T - 12, "健康", 11.5, op=0.8)
    s.circle(578, 104, 5, INDIGO, 0.6); s.text(592, 108, "飲んだ人", 11.5)
    s.text(592, 124, f"健康志向 平均 {m1:+.2f}".replace("+", "＋"), 11, op=0.8)
    s.circle(578, 152, 5, TEAL, 0.6); s.text(592, 156, "飲まない人", 11.5)
    s.text(592, 172, f"健康志向 平均 {m0:+.2f}".replace("-", "−"), 11, op=0.8)
    s.text(578, 206, f"単純に比べると", 11.5)
    s.text(578, 226, f"{d:+.1f}".replace("+", "＋"), 15, bold=True, color=RED)
    s.text(578, 248, "帯の中だけなら", 11.5)
    s.text(578, 268, f"{db:+.1f}".replace("+", "＋").replace("-", "−"), 15,
           bold=True, color=AMBER)
    s.text(0, 320, "差の正体は、飲む人と飲まない人で健康志向が偏っていること。"
           "本人が飲むかどうかを決めるかぎり、この偏りは消えない。", 11.5, op=0.95)
    s.text(0, 344, "くじ引きで決めれば、2つの群の健康志向はそろう。"
           "だから残った差を効果と呼べるようになる。", 11.5, op=0.95)
    s.text(0, 378, f"（本文と同じ仕組みで作り直した模式図・n={n}。"
           f"乱数が違うので、本文の数値とわずかにずれる。）", 11, op=0.7)
    save("10_confound.svg", s)


if __name__ == "__main__":
    print("図A DAG"); fig_dag()
    print("図B 交絡"); fig_confound()
