# -*- coding: utf-8 -*-
"""統計学Ⅱ 第11回（交絡と疑似相関）の図。"""
import os
import numpy as np
from svgkit import Svg, RED, INDIGO, TEAL, AMBER

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg.render())
    print(f"  -> out/{name}")


def resid(a, b):
    return a - np.polyval(np.polyfit(b, a, 1), b)


# ===== 図A：アイスと水難事故 ===========================================
def fig_ice():
    rg = np.random.default_rng(3016)
    n = 180
    z = rg.uniform(5, 32, n)                 # 気温
    x = 20 + 3.0 * z + rg.normal(0, 12, n)   # アイス売上
    y = 0.3 * z + rg.normal(0, 1.6, n)       # 水難事故
    r = np.corrcoef(x, y)[0, 1]
    ex, ey = resid(x, z), resid(y, z)
    pr = np.corrcoef(ex, ey)[0, 1]
    print(f"  そのまま r={r:.3f} ／ 気温を統制した偏相関 r={pr:.3f}")

    s = Svg(720, 396, "ic",
            "アイスと水難事故 ―― 気温を差し引くと関係が消える",
            f"左はアイス売上と水難事故をそのまま描いたもので、相関は{r:.2f}と強い。"
            f"点の色は気温で、暖色ほど暑い日である。"
            f"色の並びを見ると、右上に集まっているのは暑い日ばかりだと分かる。"
            f"右は両方から気温で説明できる分を引いた残り同士を描いたもので、"
            f"相関は{pr:.2f}とほぼ消える。"
            f"見えていたのは気温が作った疑似相関だった。")
    s.text(0, 28, "同じ気温の日どうしで比べれば、関係は残らない", 13.5, bold=True)

    def temp_color(v):
        t = (v - z.min()) / (z.max() - z.min())
        return f"#{int(60+195*t):02x}{int(130-70*t):02x}{int(200-160*t):02x}"

    def panel(x0, w, xa, ya, title, sub, col=None):
        T, B = 96, 272
        xlo, xhi = xa.min(), xa.max()
        ylo, yhi = ya.min(), ya.max()
        mx, my = (xhi - xlo) * .08, (yhi - ylo) * .12
        px = lambda v: x0 + (v - xlo + mx) / (xhi - xlo + 2*mx) * w
        py = lambda v: B - (v - ylo + my) / (yhi - ylo + 2*my) * (B - T)
        s.text(x0, 70, title, 12.5, bold=True)
        s.text(x0, 88, sub, 11, op=0.8)
        s.line(x0, B, x0 + w, B, op=0.4)
        s.line(x0, T, x0, B, op=0.4)
        for j in range(n):
            s.circle(px(xa[j]), py(ya[j]), 3.0,
                     temp_color(z[j]) if col is None else col, 0.72)
        b = np.polyfit(xa, ya, 1)
        s.path([(px(xlo), py(np.polyval(b, xlo))),
                (px(xhi), py(np.polyval(b, xhi)))], RED, 2.2, 0.85)

    panel(14, 320, x, y, "① そのまま描く", f"相関 r = {r:.2f}（強い正）")
    panel(392, 320, ex, ey, "② 気温で説明できる分を引いたあと",
          f"偏相関 r = {pr:.2f}（ほぼ 0）".replace("-", "−"))
    s.text(14, 294, "アイス売上 →", 11, op=0.75)
    s.text(392, 294, "アイス売上の残り →", 11, op=0.75)
    # 気温の色の凡例
    for i in range(24):
        v = z.min() + (z.max() - z.min()) * i / 23
        s.rect(250 + i * 5, 36, 5, 10, fill=temp_color(v), fop=0.9, sop=0)
    s.text(244, 45, "気温", 11, anchor="end", op=0.8)
    s.text(374, 45, "暑い", 11, op=0.8)
    s.text(0, 330, "同じ色（＝同じくらいの気温）の点だけを見ると、"
           "左の図でももう傾きはほとんどない。", 11.5, op=0.95)
    s.text(0, 354, "共通の原因である気温を統制すると、見せかけの相関は消える。"
           "これが「交絡を断つ」ということ。", 11.5, op=0.95)
    s.text(0, 384, f"（本文と同じ仕組みで作り直した模式図・n={n}。"
           f"縦軸は左が水難事故、右はその残り。）", 11, op=0.7)
    save("11_ice.svg", s)


# ===== 図B：シンプソンのパラドックス ==================================
def fig_simpson():
    data = {"A": {"文系": (0.70, 200), "理系": (0.30, 80)},
            "B": {"文系": (0.75, 80), "理系": (0.35, 200)}}
    tot = {}
    for app, d in data.items():
        num = sum(p * m for p, m in d.values())
        den = sum(m for _, m in d.values())
        tot[app] = num / den
        print(f"  アプリ{app}: 文系{d['文系'][1]}人 {d['文系'][0]*100:.0f}% ／ "
              f"理系{d['理系'][1]}人 {d['理系'][0]*100:.0f}% → 全体 {tot[app]*100:.1f}%")

    s = Svg(720, 396, "sp",
            "シンプソンのパラドックス ―― 棒の幅が人数",
            "棒の高さが合格率、幅が人数である。文系でも理系でもアプリBのほうが"
            "合格率は高い。ところがアプリAは合格しやすい文系の受験者が200人と多く、"
            "アプリBは合格しにくい理系が200人と多い。"
            "そのため合算するとAが58.6%、Bが46.4%となり、順位が逆転する。"
            "正しいのは学部で分けて見た結論、すなわちBのほうが上である。")
    s.text(0, 28, "どちらの学部でもBが上。なのに合算するとAが上になる", 13.5,
           bold=True)
    T, B = 72, 250
    hy = lambda p: B - p * (B - T)
    for v in (0, 0.25, 0.5, 0.75):
        s.line(30, hy(v), 690, hy(v), op=0.5 if v == 0 else 0.12)
        s.text(24, hy(v) + 4, f"{int(v*100)}%", 11, anchor="end", op=0.75)
    SC = 0.42          # 人数→棒の幅
    X = 54
    for app, col in (("A", INDIGO), ("B", AMBER)):
        gw = sum(m for _, m in data[app].values()) * SC + 10
        s.text(X + gw / 2, 54, f"アプリ{app}", 13, anchor="middle",
               bold=True, color=col)
        for fac in ("文系", "理系"):
            p, m = data[app][fac]
            w = m * SC
            s.rect(X, hy(p), w, B - hy(p), fill=col, fop=0.3, stroke=col,
                   sop=0.7, r=3)
            s.text(X + w/2, hy(p) - 8, f"{p*100:.0f}%", 12, anchor="middle",
                   bold=True, color=col)
            s.text(X + w/2, B + 18, fac, 11, anchor="middle", op=0.85)
            s.text(X + w/2, B + 33, f"{m}人", 10.5, anchor="middle", op=0.6)
            X += w + 10
        X += 44
    # 合算
    X += 10
    for app, col in (("A", INDIGO), ("B", AMBER)):
        w = 280 * SC
        s.rect(X, hy(tot[app]), w, B - hy(tot[app]), fill=col, fop=0.18,
               stroke=col, sop=0.7, r=3)
        s.text(X + w/2, hy(tot[app]) - 8, f"{tot[app]*100:.1f}%", 12,
               anchor="middle", bold=True, color=col)
        s.text(X + w/2, B + 18, f"合算{app}", 11, anchor="middle", op=0.85)
        s.text(X + w/2, B + 33, "280人", 10.5, anchor="middle", op=0.6)
        X += w + 10
    s.text(0, 300, "幅が人数。アプリAには合格しやすい文系が200人、"
           "アプリBには合格しにくい理系が200人いる。", 11.5, op=0.95)
    s.text(0, 324, "この構成比の偏り（＝学部という交絡）が、合算したときに"
           "本当の優劣を覆い隠してしまう。", 11.5, op=0.95)
    s.text(0, 348, "正しいのは学部で分けて見た結論 ―― Bのほうが上である。",
           12, bold=True, color=AMBER)
    s.text(0, 382, "（本文の表と同じ数値。合算は 文系と理系の合格者を足して"
           "280人で割ったもの。）", 11, op=0.7)
    save("11_simpson.svg", s)


# ===== 図C：コライダー =================================================
def fig_collider():
    rg = np.random.default_rng(259)
    N = 200000
    x, y = rg.normal(0, 1, N), rg.normal(0, 1, N)
    c = (x + y > 1.5)
    r_all = np.corrcoef(x, y)[0, 1]
    r_sel = np.corrcoef(x[c], y[c])[0, 1]
    print(f"  全体 r={r_all:.3f} ／ デビュー率 {c.mean()*100:.1f}% ／ "
          f"デビュー組 r={r_sel:.3f}")

    s = Svg(720, 400, "cl",
            "コライダーを統制すると、無かった相関が生まれる",
            f"才能と容姿は互いに独立で、母集団全体では相関{r_all:.3f}とほぼ0である。"
            f"どちらかが十分高ければデビューできる（才能＋容姿が1.5より大きい）"
            f"という条件をつけると、デビューした{c.mean()*100:.1f}%の人の中では"
            f"相関が{r_sel:.3f}まで下がる。"
            f"才能がさほどでもないのにデビューできた人は容姿が高いはずで、"
            f"条件をつけたこと自体が負の関係を作り出している。")
    s.text(0, 28, "条件をつけたこと自体が、関係を作り出す", 13.5, bold=True)
    sub = rg.choice(N, 1200, replace=False)
    T, Bm = 92, 268

    def panel(x0, w, mask, title, col, rr):
        px = lambda v: x0 + (v + 3.4) / 6.8 * w
        py = lambda v: Bm - (v + 3.4) / 6.8 * (Bm - T)
        s.text(x0, 68, title, 12.5, bold=True, color=col)
        s.text(x0, 86, f"相関 r = {rr:.3f}".replace("-", "−"), 11.5, op=0.85)
        s.rect(x0, T, w, Bm - T, stroke="currentColor", sop=0.25, r=3)
        for j in sub:
            if mask[j]:
                s.circle(px(x[j]), py(y[j]), 2.2, col, 0.45)
        # デビューの境界線 x+y=1.5
        # 枠の中に収まる範囲だけ引く（x+y=1.5 と枠の交点）
        s.path([(px(1.5 - 3.4), py(3.4)), (px(3.4), py(1.5 - 3.4))],
               RED, 1.8, 0.8, dash="5 3")
        s.text(x0 + w - 6, T + 16, "才能＋容姿 = 1.5", 10.5, anchor="end",
               color=RED, op=0.9)
        s.text(x0 + w/2, Bm + 18, "才能 →", 11, anchor="middle", op=0.75)
        s.text(x0 - 4, T - 4, "↑ 容姿", 11, anchor="end", op=0.75)

    panel(14, 320, np.ones(N, bool), "① 母集団ぜんたい", INDIGO, r_all)
    panel(392, 320, c, f"② デビューした人だけ（全体の {c.mean()*100:.1f}%）",
          AMBER, r_sel)
    s.text(0, 316, "同じ「統制」という操作が、交絡（共通の原因）には"
           "見せかけの相関を消し、コライダー（共通の結果）には"
           "無い相関を作り出す。", 11.5, op=0.95)
    s.text(0, 340, "しかも計算式は、統制する変数が原因なのか結果なのかを"
           "知らないまま実行できてしまう。", 11.5, op=0.95)
    s.text(0, 364, "何を統制すべきかはデータからは決まらない。"
           "因果の向きの仮定が先にあって、はじめて決まる。", 12, bold=True,
           color=RED)
    s.text(0, 394, f"（才能と容姿を独立な標準正規分布として20万人ぶん作り、"
           f"図には1,200人を抜き出して描いている。）", 11, op=0.7)
    save("11_collider.svg", s)


if __name__ == "__main__":
    print("図A アイスと水難事故"); fig_ice()
    print("図B シンプソン"); fig_simpson()
    print("図C コライダー"); fig_collider()
