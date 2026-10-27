# 第04回　離散確率分布：二項分布・ポアソン分布

**10/20（火）Ⅲ講 13:00〜14:40・B402教室**

> 「独立な試行」を数式にする

---


<!-- LINKS:START -->
!!! info "今日のリンク"
    - [📊 スライドを開く](slides/04.html)
    - [📓 Colabノートを開く（04_discrete.ipynb）](https://colab.research.google.com/github/aonoa68/toukei-2/blob/main/colab/04_discrete.ipynb)
    - [📝 課題を提出する（Moodle・第4回）](https://moodle.hokusei.ac.jp/mod/assign/view.php?id=990639)
    - 課題の本文は**このページの末尾**にあります
    - [🤖 NotebookLMで復習する](https://notebook.google.com/notebook/9c04a206-efa4-468f-93e7-a45258e4c56d)（この回の内容をAIに質問できます）
<!-- LINKS:END -->

## この回のゴール

- 確率変数・期待値・分散を理解する
- 確率変数に **離散型と連続型** があることを理解する（値を1つずつ数え上げられるか、測定の目盛りをいくらでも細かくできるか）
- **二項分布**：独立な試行 $n$ 回中の成功回数の分布
- **ポアソン分布**：一定の範囲で起こる件数の分布、二項→ポアソン近似
- 両者が置いている前提（**成功確率が一定・各試行が独立** ／ **発生率が一定・区間ごとに独立**）を言えるようになり、独立が崩れると分布が壊れることを知る
- **発展**：二項分布の式 $\binom{n}{k}p^k(1-p)^{n-k}$ と、$E[X]=np$・$V[X]=np(1-p)$ を、自分で導ける

到達目標との対応：**G1（確率の理解）** と **G4（独立性）**。

---

## 1. 直感クイズ ―― 10回投げて7回表。イカサマ？

公正なコイン（表の確率0.5）を10回投げたら表が **7回** 出た。

**問い：これは「イカサマだ」と言えるほど珍しいか？**

二項分布で計算すると、**7回以上が出る確率は約17%**（$P(X\ge 7)=0.1719$）。5〜6回に1回は起きる、ありふれた偶然だ。これだけではイカサマとは言えない。

!!! note "ここで見ているのは「表が多い側」だけ"
    ちょうど7回の確率（$P(X=7)=0.1172$）と、7回**以上**の確率（$0.1719$）は別物である。ここで見ているのは後者、しかも「表が多い側」だけだ。「どちら向きでも同じくらい偏る確率」を見るなら、裏が多い側も足して $P(X\le 3)+P(X\ge 7)=34.4\%$ になる。片側だけを見るのか両側を見るのかは、第8〜9回の検定で正面から扱う。

!!! note "後の伏線"
    「珍しさ」を確率で測るこの発想は、第8〜9回の **仮説検定・p値** につながる。「珍しい＝偶然では説明しにくい」をどこで線引きするかが、後の大問題になる。

---

## 2. 二項分布 ―― 独立な試行を n 回

**確率変数**：偶然で値が決まる量（ここでは「10回中の表の回数」）。

!!! note "確率変数には2種類ある ―― 離散型と連続型"
    確率変数は、**とりうる値をどう刻めるか**で2つに分かれる。

    - **離散型**：とりうる値を1つずつ数え上げられる。サイコロの目は $1,2,\dots,6$ で、$1.1$ や $5.4$ という目はない。「知っていますか？ Yes / No」も、10回中の表の回数 $0,1,\dots,10$ も離散型である。
    - **連続型**：**測定の目盛りを、いくらでも細かくできる**。身長を「120〜121 cm が2人、121〜122 cm が3人」と数えていたのを、「120〜120.5 cm が1人、120.5〜121 cm が1人……」と刻み直せる。さらに 120.25 cm でも刻める。体重・気温・時間も同じである。

    見分け方は「**隣り合う2つの値のあいだに、もう1つ値を入れられるか**」。入れられないのが離散型、いくらでも入れられるのが連続型だ。

    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 276" role="img" aria-labelledby="t t2" style="width:100%;height:auto;max-width:720px;display:block;margin:0.6em auto" font-family="system-ui,-apple-system,'Hiragino Sans','Yu Gothic',Meiryo,sans-serif" font-size="13"><title id="t">離散型と連続型のちがい</title><desc id="t2">左：サイコロの目は1から6の点だけで、あいだに値が入らない。右：身長は目盛りをいくらでも細かく刻める。</desc><text x="10.0" y="20.0" font-size="14" text-anchor="start" font-weight="bold" fill="#5c6bc0" fill-opacity="1.0">離散型 ―― 値は点。あいだに入れられない</text><line x1="20.0" y1="70.0" x2="296.0" y2="70.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/><circle cx="20" cy="70" r="6" fill="#5c6bc0"/><text x="20.0" y="92.0" font-size="13" text-anchor="middle" font-weight="normal" fill="currentColor" fill-opacity="1.0">1</text><circle cx="75" cy="70" r="6" fill="#5c6bc0"/><text x="75.0" y="92.0" font-size="13" text-anchor="middle" font-weight="normal" fill="currentColor" fill-opacity="1.0">2</text><circle cx="130" cy="70" r="6" fill="#5c6bc0"/><text x="130.0" y="92.0" font-size="13" text-anchor="middle" font-weight="normal" fill="currentColor" fill-opacity="1.0">3</text><circle cx="185" cy="70" r="6" fill="#5c6bc0"/><text x="185.0" y="92.0" font-size="13" text-anchor="middle" font-weight="normal" fill="currentColor" fill-opacity="1.0">4</text><circle cx="240" cy="70" r="6" fill="#5c6bc0"/><text x="240.0" y="92.0" font-size="13" text-anchor="middle" font-weight="normal" fill="currentColor" fill-opacity="1.0">5</text><circle cx="295" cy="70" r="6" fill="#5c6bc0"/><text x="295.0" y="92.0" font-size="13" text-anchor="middle" font-weight="normal" fill="currentColor" fill-opacity="1.0">6</text><text x="47.5" y="56.0" font-size="12" text-anchor="middle" font-weight="normal" fill="#c62828" fill-opacity="0.8">×</text><text x="102.5" y="56.0" font-size="12" text-anchor="middle" font-weight="normal" fill="#c62828" fill-opacity="0.8">×</text><text x="157.5" y="56.0" font-size="12" text-anchor="middle" font-weight="normal" fill="#c62828" fill-opacity="0.8">×</text><text x="212.5" y="56.0" font-size="12" text-anchor="middle" font-weight="normal" fill="#c62828" fill-opacity="0.8">×</text><text x="267.5" y="56.0" font-size="12" text-anchor="middle" font-weight="normal" fill="#c62828" fill-opacity="0.8">×</text><text x="20.0" y="120.0" font-size="12" text-anchor="start" font-weight="normal" fill="currentColor" fill-opacity="0.75">サイコロに 1.1 や 5.4 の目はない</text><text x="20.0" y="140.0" font-size="12" text-anchor="start" font-weight="normal" fill="currentColor" fill-opacity="0.75">「知っていますか？ Yes / No」も同じ</text><line x1="348.0" y1="10.0" x2="348.0" y2="212.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.25"/><text x="366.0" y="20.0" font-size="14" text-anchor="start" font-weight="bold" fill="#ef6c00" fill-opacity="1.0">連続型 ―― 目盛りをいくらでも細かくできる</text><line x1="396.0" y1="50.0" x2="690.0" y2="50.0" stroke="#ef6c00" stroke-width="2" stroke-opacity="0.85"/><line x1="396.0" y1="44.0" x2="396.0" y2="56.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="543.0" y1="44.0" x2="543.0" y2="56.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="690.0" y1="44.0" x2="690.0" y2="56.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><text x="390.0" y="54.0" font-size="11" text-anchor="end" font-weight="normal" fill="currentColor" fill-opacity="0.8">幅 1 cm</text><line x1="396.0" y1="95.0" x2="690.0" y2="95.0" stroke="#ef6c00" stroke-width="2" stroke-opacity="0.85"/><line x1="396.0" y1="89.0" x2="396.0" y2="101.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="469.5" y1="89.0" x2="469.5" y2="101.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="543.0" y1="89.0" x2="543.0" y2="101.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="616.5" y1="89.0" x2="616.5" y2="101.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="690.0" y1="89.0" x2="690.0" y2="101.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><text x="390.0" y="99.0" font-size="11" text-anchor="end" font-weight="normal" fill="currentColor" fill-opacity="0.8">幅 0.5 cm</text><line x1="396.0" y1="140.0" x2="690.0" y2="140.0" stroke="#ef6c00" stroke-width="2" stroke-opacity="0.85"/><line x1="396.0" y1="134.0" x2="396.0" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="410.7" y1="134.0" x2="410.7" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="425.4" y1="134.0" x2="425.4" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="440.1" y1="134.0" x2="440.1" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="454.8" y1="134.0" x2="454.8" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="469.5" y1="134.0" x2="469.5" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="484.2" y1="134.0" x2="484.2" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="498.9" y1="134.0" x2="498.9" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="513.6" y1="134.0" x2="513.6" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="528.3" y1="134.0" x2="528.3" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="543.0" y1="134.0" x2="543.0" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="557.7" y1="134.0" x2="557.7" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="572.4" y1="134.0" x2="572.4" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="587.1" y1="134.0" x2="587.1" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="601.8" y1="134.0" x2="601.8" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="616.5" y1="134.0" x2="616.5" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="631.2" y1="134.0" x2="631.2" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="645.9" y1="134.0" x2="645.9" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="660.6" y1="134.0" x2="660.6" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="675.3" y1="134.0" x2="675.3" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><line x1="690.0" y1="134.0" x2="690.0" y2="146.0" stroke="#ef6c00" stroke-width="1.2" stroke-opacity="0.85"/><text x="390.0" y="144.0" font-size="11" text-anchor="end" font-weight="normal" fill="currentColor" fill-opacity="0.8">幅 0.1 cm</text><text x="396.0" y="40.0" font-size="11" text-anchor="middle" font-weight="normal" fill="currentColor" fill-opacity="0.7">120</text><text x="543.0" y="40.0" font-size="11" text-anchor="middle" font-weight="normal" fill="currentColor" fill-opacity="0.7">121</text><text x="690.0" y="40.0" font-size="11" text-anchor="middle" font-weight="normal" fill="currentColor" fill-opacity="0.7">122 cm</text><text x="396.0" y="175.0" font-size="12" text-anchor="start" font-weight="normal" fill="currentColor" fill-opacity="0.75">刻み直しても、まだあいだに値が入る</text><text x="396.0" y="195.0" font-size="12" text-anchor="start" font-weight="normal" fill="currentColor" fill-opacity="0.75">120.25 cm でも、120.001 cm でも刻める</text><line x1="16.0" y1="236.0" x2="704.0" y2="236.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.3"/><text x="360.0" y="262.0" font-size="13.5" text-anchor="middle" font-weight="bold" fill="currentColor" fill-opacity="1.0">見分け方：隣り合う2つの値のあいだに、もう1つ値を入れられるか</text></svg>

    **今日の二項分布・ポアソン分布は離散型。次回の正規分布は連続型**である。この違いは見た目だけの話ではなく、「確率がどこにあるか」が変わる（→第5回）。

!!! warning "数えられる量でも、連続型の道具を使うことがある"
    金額（1円刻み）、年齢（1歳刻み）、人口（1人刻み）は、厳密には離散型である。それでも刻みがデータの散らばりに比べて細かいときは、連続型の道具（正規分布、面積としての確率）で近似するのがふつうだ。**どちらに分類されるかと、どちらの道具を使うかは、別の話である。**

    逆向きもある。離散型の二項分布は、$n$ を大きくすると連続型の正規分布で近似できる（$p=0.5$ で $n$ を増やしていくと釣鐘型に重なる。→第5〜6回）。**離散と連続は、互いに近づく関係にある。**

成功確率 $p$ の試行を **独立に** $n$ 回くりかえし、成功回数を数えると **二項分布** $\mathrm{Binom}(n,p)$ になる。

$$P(X=k) = \binom{n}{k}\,p^{k}(1-p)^{n-k}, \qquad E[X]=np,\quad V[X]=np(1-p)$$

この形になるために、実は4つの条件を置いている。

1. 試行回数 $n$ が決まっている
2. 各試行の結果を**成功・失敗の2値**で表せる
3. 成功確率 $p$ が**毎回同じ**
4. 各試行が**独立**

**今日とくに注目するのは4の独立だが、3もいっしょに使っている。** 独立でも各回の $p$ が違えば、ふつうの二項分布にはならない。たとえば独立な2回で成功確率が $0.1$ と $0.9$ なら、2回とも成功する確率は $0.1\times0.9=0.09$。平均をとって「$p=0.5$ の二項分布」と置き換えると $0.25$ になり、合わない。

Colabで1万セットのコイン投げをシミュレーションすると、ヒストグラムが理論の二項分布にぴったり重なり、平均 $\approx 5$・分散 $\approx 2.5$ が再現される。

???+ note "導出①：二項分布の式は「1つの並びの確率」×「並び方の数」"

    まず、**特定の並び1つ**の確率を考える。たとえば $n=5$ で「表・表・裏・表・裏」（成功 $k=3$ 回）という並び。

    各回が**独立**なら、同時に起きる確率は単純なかけ算でよい。

    $$p \times p \times (1-p) \times p \times (1-p) \;=\; p^{3}(1-p)^{2}$$

    **かけ算にできるのは独立だからである。** そして、かける中身がどの回も $p$ と $1-p$ で書けるのは、成功確率が毎回同じだからだ。1回目の結果が2回目の確率を変えるなら、この式は最初の一歩で崩れる（→第4節）。独立性は、今日とくに注目する前提である。

    並びが変わっても、成功が $k$ 回・失敗が $n-k$ 回であれば、かける中身の順番が入れ替わるだけで積は同じ $p^{k}(1-p)^{n-k}$ になる。

    あとは**そのような並びが何通りあるか**を数えればよい。$n$ 回のうちどの $k$ 回が成功かを選ぶ選び方なので $\binom{n}{k}$ 通り。同じ確率の排反な並びが $\binom{n}{k}$ 個あるので、足し合わせて

    $$P(X=k)=\binom{n}{k}\,p^{k}(1-p)^{n-k}$$

    **数値で確かめる**：$n=10,\ p=0.5$ のとき、この式で $k=7,8,9,10$ を足すと $P(X\ge 7)=0.1719$。第1節の「約17%」はこの計算である。

    **使った数学**：独立な事象の確率のかけ算、組合せ $\binom{n}{k}$（数A）。

???+ note "導出②：$E[X]=np$ と $V[X]=np(1-p)$ ―― 期待値と分散で、独立の要り方が違う"

    $i$ 回目が成功なら $1$、失敗なら $0$ をとる確率変数 $X_i$ を考えると、成功回数はただの和になる。

    $$X = X_1+X_2+\dots+X_n$$

    まず**1回分**を計算する。$X_i$ は $1$ を確率 $p$、$0$ を確率 $1-p$ でとるので、

    $$E[X_i] = 1\cdot p + 0\cdot(1-p) = p$$

    $X_i^2$ は $X_i$ と同じ値をとる（$1^2=1$、$0^2=0$）ので $E[X_i^2]=p$。よって

    $$V[X_i] = E[X_i^2]-\left(E[X_i]\right)^2 = p - p^2 = p(1-p)$$

    ここから $n$ 倍にする。期待値は**和について常に線形**なので、独立でなくても足してよい。

    $$E[X] = \sum_{i=1}^{n} E[X_i] = np$$

    分散はそうはいかない。一般には、$X_i$ どうしの**共分散**の項が付いてくる。

    $$V[X] = \sum_{i=1}^{n} V[X_i] \;+\; 2\sum_{i<j}\mathrm{Cov}(X_i,X_j) \;=\; np(1-p) + 2\sum_{i<j}\mathrm{Cov}(X_i,X_j)$$

    各試行が独立なら共分散はすべて $0$ になるので、第2項が消えて

    $$V[X] = \sum_{i=1}^{n} V[X_i] = np(1-p)$$

    （独立は、共分散を $0$ にするための**十分条件**である。独立でなくても共分散の合計が $0$ なら、分散はそのまま足せる。）

    !!! warning "期待値は独立でなくても足せる。分散では共分散の影響を考える"
        この違いが今日の要点である。第4節で「平均は同じなのに分散だけが約5.4倍に膨らむ」のを見るが、それは偶然ではない。期待値の式に共分散は現れず、**分散の式にだけ現れる**からだ。

    **数値で確かめる**：$n=10,\ p=0.5$ なら $E[X]=5$、$V[X]=2.5$。二項分布の確率を定義どおりに足して計算しても $5$ と $2.5$ で一致する。

    **使った数学**：期待値の線形性、$V[X]=E[X^2]-(E[X])^2$、独立なときの分散の加法性。

!!! warning "大前提は『成功確率が一定・各試行が独立』"
    二項分布は、**成功確率 $p$ が毎回同じ**で、**各試行が独立**であることを前提にしている。1回目の結果が2回目に影響しないからこそ、確率を単純にかけ算できる。この前提が崩れると、**成功回数が二項分布になる保証はなくなる**（→第4節）。

---

## 3. ポアソン分布 ―― 一定の範囲で起こる件数

「1日の迷惑電話の件数」「1ページの誤植の数」「1時間の来客数」――
**一定の時間や空間の範囲で起こる件数**を表すモデルが **ポアソン分布** $\mathrm{Poisson}(\lambda)$ である。

$$P(X=k)=\frac{\lambda^{k}e^{-\lambda}}{k!},\qquad E[X]=V[X]=\lambda$$

ここで考えているのは、次の3つが置ける場合である。

1. 単位時間（単位面積）あたりの**発生率が一定**
2. **重ならない区間の件数が互いに独立**
3. ごく短い区間に**複数件がまとまって起こることが、ほとんどない**

この3つから、一定時間内の件数がポアソン分布になるモデルが得られる。なお「稀な事象」というのは、観測期間全体の件数が少ないという意味ではなく、**一つ一つの小さな機会での発生確率が小さい**という意味である。

!!! warning "例の名前だけで分布は決まらない"
    同じ「来客数」でも、団体客がまとめて来店するなら3が崩れ、昼と深夜で来店ペースが違うなら1が崩れる。そういう場面では、このモデルは合わない。**具体例の名前ではなく、上の条件が置けそうかどうかで判断する。**

$\lambda$ は「平均して何件起きるか」。二項分布で $n$ が大きく $p$ が小さいとき（$\lambda=np$ 一定）、二項分布はポアソン分布に近づく。Colabで $n=10,50,500$ と大きくすると、二項分布がポアソン分布に重なっていくのが見える。

???+ note "導出③：なぜ二項分布はポアソン分布に近づくのか"

    仮定をはっきりさせる。**$\lambda=np$ を一定に保ったまま、$n$ を大きく・$p$ を小さくしていく**。機会の数は増えるが、1回あたりの確率がそれに反比例して小さくなる、という状況である。

    二項分布の式に $p=\lambda/n$ を代入して、部分に分ける。

    $$\binom{n}{k}\left(\frac{\lambda}{n}\right)^{k}\left(1-\frac{\lambda}{n}\right)^{n-k} \;=\; \underbrace{\frac{n(n-1)\cdots(n-k+1)}{n^{k}}}_{(\mathrm{i})}\cdot\frac{\lambda^{k}}{k!}\cdot\underbrace{\left(1-\frac{\lambda}{n}\right)^{n}}_{(\mathrm{ii})}\cdot\underbrace{\left(1-\frac{\lambda}{n}\right)^{-k}}_{(\mathrm{iii})}$$

    $k$ を固定して $n$ を大きくすると、(i) は $\frac{n}{n}\cdot\frac{n-1}{n}\cdots$ という $k$ 個の分数の積なので $1$ に近づく。(ii) は $e^{-\lambda}$ に近づく。(iii) も $1$ に近づく。残るのは

    $$P(X=k) \;\longrightarrow\; \frac{\lambda^{k}e^{-\lambda}}{k!}$$

    これがポアソン分布である。**結論はあくまで近似**であり、$n$ が小さいうちは一致しない。

    **数値で確かめる**：$\lambda=5$ に固定して $n$ を変え、二項分布とポアソン分布の確率の差の最大値を見る。

    | $n$ | $p=\lambda/n$ | 確率の差の最大 |
    |---:|---:|---:|
    | 10 | 0.5 | 0.0706 |
    | 50 | 0.1 | 0.0095 |
    | 500 | 0.01 | 0.0009 |
    | 5000 | 0.001 | 0.0001 |

    $n=10$ ではまるで別物だが、$\lambda=5$ のこの例では、$n=500$ まで来ると確率の差は最大でも約 $0.0009$ になる。「$n$ が大きく $p$ が小さい」がどの程度を指すのかが、数字で見える。

    なお「差が $0.001$ 未満」は「小数第3位まで同じ数字が並ぶ」ことではない。$n=500$・$k=5$ の確率は、二項が $0.17635$、ポアソンが $0.17547$ で、小数第3位に丸めると $0.176$ と $0.175$ に分かれる。

    !!! note "極限の厳密な扱いは範囲外"
        $\left(1-\lambda/n\right)^{n} \to e^{-\lambda}$ の証明や、極限と和の交換の正当化は、この授業で扱う統計数理の範囲外である。ここでは「何を仮定すると何が出るか」の筋道を押さえておけばよい。

    **使った数学**：指数関数の極限 $\left(1+x/n\right)^{n}\to e^{x}$（数Ⅲ）、式の分解。

| | 二項分布 | ポアソン分布 |
|---|---|---|
| 使う場面 | 試行回数 $n$ が決まっている（10回投げる） | 機会が膨大で件数だけ分かる（1日の件数） |
| パラメータ | $n,\ p$ | $\lambda$（平均件数） |
| 前提 | $n$ が固定・**成功確率 $p$ が一定**・**各試行が独立** | **発生率が一定**・**重ならない区間の件数が独立**・短い区間に複数件が集中しない |

### 分布どうしの関係

二項分布とポアソン分布だけが孤立しているわけではない。**条件を変えると、分布どうしは互いに近づく。**

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 320" role="img" aria-labelledby="t t2" style="width:100%;height:auto;max-width:720px;display:block;margin:0.6em auto" font-family="system-ui,-apple-system,'Hiragino Sans','Yu Gothic',Meiryo,sans-serif" font-size="13"><title id="t">分布どうしの関係</title><desc id="t2">超幾何分布はNが大きいと二項分布に、二項分布はnが大きくpが小さいとポアソン分布に、ポアソン分布はλが大きいと正規分布に近づく。二項分布も標準化してnを大きくすると正規分布に近づく。</desc><text x="16.0" y="24.0" font-size="14" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">分布どうしは、条件を変えると互いに近づく</text><rect x="25.0" y="67.0" width="150" height="50" rx="8" fill="#00897b" fill-opacity="0.16" stroke="#00897b" stroke-width="1.8"/><text x="100.0" y="90.0" font-size="13" text-anchor="middle" font-weight="bold" fill="currentColor" fill-opacity="1.0">超幾何分布</text><text x="100.0" y="107.0" font-size="9.5" text-anchor="middle" font-weight="normal" fill="currentColor" fill-opacity="0.75">非復元抽出</text><rect x="255.0" y="67.0" width="150" height="50" rx="8" fill="#5c6bc0" fill-opacity="0.16" stroke="#5c6bc0" stroke-width="1.8"/><text x="330.0" y="90.0" font-size="13" text-anchor="middle" font-weight="bold" fill="currentColor" fill-opacity="1.0">二項分布</text><text x="330.0" y="107.0" font-size="9.5" text-anchor="middle" font-weight="normal" fill="currentColor" fill-opacity="0.75">n回中の成功回数</text><rect x="485.0" y="67.0" width="150" height="50" rx="8" fill="#ef6c00" fill-opacity="0.16" stroke="#ef6c00" stroke-width="1.8"/><text x="560.0" y="90.0" font-size="13" text-anchor="middle" font-weight="bold" fill="currentColor" fill-opacity="1.0">ポアソン分布</text><text x="560.0" y="107.0" font-size="9.5" text-anchor="middle" font-weight="normal" fill="currentColor" fill-opacity="0.75">一定範囲の件数</text><rect x="245.0" y="223.0" width="170" height="50" rx="8" fill="#c62828" fill-opacity="0.16" stroke="#c62828" stroke-width="1.8"/><text x="330.0" y="246.0" font-size="13" text-anchor="middle" font-weight="bold" fill="currentColor" fill-opacity="1.0">正規分布</text><text x="330.0" y="263.0" font-size="9.5" text-anchor="middle" font-weight="normal" fill="currentColor" fill-opacity="0.75">連続型（第5回）</text><line x1="176.0" y1="92.0" x2="243.0" y2="92.0" stroke="#00897b" stroke-width="2.2"/><polygon points="254.0,92.0 241.0,86.0 241.0,98.0" fill="#00897b"/><text x="215.0" y="78.0" font-size="10" text-anchor="middle" font-weight="normal" fill="#00897b" fill-opacity="1.0">N を大きく</text><line x1="406.0" y1="92.0" x2="473.0" y2="92.0" stroke="#5c6bc0" stroke-width="2.2"/><polygon points="484.0,92.0 471.0,86.0 471.0,98.0" fill="#5c6bc0"/><text x="445.0" y="72.0" font-size="10" text-anchor="middle" font-weight="normal" fill="#5c6bc0" fill-opacity="1.0">n 大・p 小</text><text x="445.0" y="85.0" font-size="9" text-anchor="middle" font-weight="normal" fill="#5c6bc0" fill-opacity="0.85">（λ=np 一定）</text><line x1="130.0" y1="117.0" x2="249.7" y2="220.8" stroke="#00897b" stroke-width="2.2"/><polygon points="258.0,228.0 252.1,215.0 244.2,224.0" fill="#00897b"/><text x="150.0" y="190.0" font-size="10" text-anchor="start" font-weight="normal" fill="#00897b" fill-opacity="1.0">M/N が小さく</text><text x="150.0" y="203.0" font-size="10" text-anchor="start" font-weight="normal" fill="#00897b" fill-opacity="0.85">n が大きい</text><line x1="330.0" y1="117.0" x2="330.0" y2="212.0" stroke="#5c6bc0" stroke-width="2.2"/><polygon points="330.0,223.0 336.0,210.0 324.0,210.0" fill="#5c6bc0"/><text x="340.0" y="160.0" font-size="10.5" text-anchor="start" font-weight="bold" fill="#5c6bc0" fill-opacity="1.0">標準化して n を大きく</text><text x="340.0" y="174.0" font-size="9.5" text-anchor="start" font-weight="normal" fill="#5c6bc0" fill-opacity="0.85">（ラプラスの定理）</text><line x1="540.0" y1="117.0" x2="418.4" y2="220.9" stroke="#ef6c00" stroke-width="2.2"/><polygon points="410.0,228.0 423.8,224.1 416.0,215.0" fill="#ef6c00"/><text x="470.0" y="190.0" font-size="10" text-anchor="start" font-weight="normal" fill="#ef6c00" fill-opacity="1.0">λ を大きく</text><line x1="16.0" y1="282.0" x2="704.0" y2="282.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.3"/><text x="16.0" y="304.0" font-size="12" text-anchor="start" font-weight="bold" fill="currentColor" fill-opacity="1.0">「近づく」は近似であって、一致ではない。どれくらい近いかは n や λ の大きさで決まる（→ 導出③の表）。</text></svg>

**超幾何分布**は、限られた母集団から**戻さずに**取り出すときの成功回数の分布である（箱から赤玉を戻さずに n 個取る）。母集団 \( N \) が大きくなると、1個取り出しても残りの構成がほとんど変わらないので、**毎回同じ \( p \) で独立に引くのと区別がつかなくなる** ―― つまり二項分布に近づく。

第5回で扱う**正規分布**には、2つの道で合流する。二項分布を標準化して \( n \) を大きくする道（**ラプラスの定理**）と、ポアソン分布の \( \lambda \) を大きくする道である。

!!! note "なぜこの地図が要るのか"
    現実のデータに「この分布を当てはめてよいか」を考えるとき、**どの条件が崩れると、どの分布に移るのか**が分かっていると判断しやすい。
    たとえば「非復元抽出なので厳密には超幾何分布だが、母集団が十分大きいので二項分布でよい」という判断は、この図の左の矢印そのものである。

---

## 4. もし試行が「独立でなかったら」？

二項分布もポアソン分布も、**独立**を前提にしていた。では独立が崩れたら？

10人が順番に答えるクイズを考える。ルールはこうだ。

- 1人目は、公正なコインで答えを決める（正解する確率 $0.5$）
- 2人目以降は、**8割の確率で直前の人と同じ答えにし**、残り2割では自分でコインを投げる

一人ひとりはコインで決めるつもりでも、互いに影響し合っている。
（自分で投げたときにも偶然同じ答えになるので、**直前の人と答えが一致する確率は $0.8+0.2\times0.5=0.9$**。8割のほうは「真似ることを選ぶ確率」である。）

**このルールでは、どの人も正解する確率は $0.5$ のまま**であることに注意しよう。変わるのは、正解・不正解が**そろいやすくなる**ことだけだ。Colabで「10人中の正解者数」の分布を見ると：

| | 平均 | 分散 | 極端な結果（全員一致）の割合 |
|---|---|---|---|
| 独立に判断 | 約5.0 | 約2.5 | 0.2% |
| 8割で真似る | 約5.0 | **約13.5** | **38%** |

**平均は5人のまま。だが分散は約5.4倍（SDなら約2.3倍）に膨らみ、0人や10人といった極端な結果が激増する。**

- 平均が動かないのは、**一人ひとりの正解確率が $0.5$ に保たれている**から（期待値に共分散は効かない）
- 分散が膨らむのは、真似によって答えの間に**正の相関**が生まれ、共分散の項が足されるから

!!! note "「独立でない」＝「分散が増える」ではない"
    増えるのは、**正の相関**が生じたときである。たとえば10人を5組に分け、各組の2人目は必ず1人目と**逆**の答えを出すとしよう。一人ひとりの正解確率は $0.5$ のままだが、どの組でもちょうど1人が正解するので、正解者数は**いつも5人・分散は $0$**。独立ではないのに、独立なとき（$2.5$）より小さい。
    **独立が崩れたときに何が起きるかは、相関の向きで決まる。**

!!! quote "今期の背骨"
    独立が崩れると、二項分布という前提が成り立たない。一人ひとりの正解確率は $0.5$ のままなのに、**正解者数の分布は二項分布では予測できなくなる**。
    ただし今回のモデルでは、全員不正解が増えるのと同じだけ全員正解も増える。だから「集団としての正解率が下がった」ことまでは、今日の実験からは言えない。言えるのは **結果が極端に振れやすくなる** ことである。
    この依存が、情報の集約や多数決の信頼性にどう関わるか ―― そこを第12回 **情報カスケード**・第13回 **コンドルセの陪審定理** で扱う。今日はその種を見た。

---

## 今日のまとめ

確率変数には離散型（数え上げられる）と連続型（目盛りをいくらでも細かくできる）があり、今日の2つはどちらも離散型である。

| 分布 | 何の分布か | 式 | 前提 |
|---|---|---|---|
| 二項分布 | 独立な試行 $n$ 回中の成功回数 | $\binom{n}{k}p^k(1-p)^{n-k}$ | $n$ 固定・$p$ 一定・各試行が独立 |
| ポアソン分布 | 一定の範囲で起こる件数 | $\dfrac{\lambda^k e^{-\lambda}}{k!}$ | 発生率一定・区間ごとに独立・集中発生なし |

---

## 今日の課題（Moodle提出）

**配点：100点（選択40点 ＋ 記述60点）／ 提出先：Moodle ／ 提出期限：次回授業の開始時刻まで**

第4回のColabノート `04_discrete.ipynb` を上から実行し、結果を見たうえで答えること。

---

### パートA：選択問題（各10点 ×4＝40点）

**A1.** 公正なコイン（p=0.5）を10回投げて、表が **7回以上** 出る確率に **最も近い** のは？

- (ア) 約 2%　(イ) 約 17%　(ウ) 約 50%

**A2.** 二項分布 $\mathrm{Binom}(n,p)$ の期待値（平均）と分散の組として正しいのは？

- (ア) 平均 $np$、分散 $np(1-p)$
- (イ) 平均 $p$、分散 $np$
- (ウ) 平均 $np$、分散 $\lambda$

**A3.** 次のうち、**ポアソン分布** でモデル化するのが最も自然なのはどれか？

- (ア) サイコロを20回振って6が出る回数
- (イ) ある書店に1時間あたりに来店する客の人数
- (ウ) 10人の学生のうち、特定の1人が選ばれるかどうか

> 第3節の3条件（発生率が一定・重ならない区間の件数が独立・短い区間に複数件が集中しない）が置けそうなものを選ぶこと。

**A4.** Colabで「10人が8割の確率で前の人の答えを真似る（独立でない）」場合、独立なときと比べて起きたことは？

- (ア) 平均も分散もほとんど変わらない
- (イ) 平均はほぼ同じだが、分散が大きく増え、全員一致のような極端な結果が増えた
- (ウ) 平均が大きく下がった

---

### パートB：記述問題（AIフィードバック対象・60点）

**B1.（30点）** 二項分布とポアソン分布について、**①それぞれどんな場面で使うか ②それぞれどんな前提を置いているか** を、具体例を1つずつ挙げながら**150〜250字程度**で説明しなさい。②では、両者に共通する「独立」に加えて、二項分布の「試行回数が決まっていて成功確率が毎回同じ」・ポアソン分布の「発生率が一定」にも触れること。

**B2.（30点）** Colabの最後で、「各人が前の人を真似る（独立でない）」と、10人中の正解者数の **分散が大きく膨らみ、全員一致のような極端な結果が増える** ことを見た。**このモデルでは、一人ひとりが正解する確率は0.5に保たれている**（真似ても、各人の正解率は変わらない）。これを踏まえて次の2点を書きなさい。

1. それでも極端な結果が増えるのはなぜか。**平均が5人のまま変わらない理由**と、**分散が大きくなる理由**を、分けて説明する
2. もし現実に「みんなが独立に判断していると思い込んで」二項分布で予測したら、実際の集団（真似合う集団）に対してどんな読み違いをするか

> ヒント：B2は第12〜13回（情報カスケード・コンドルセの陪審定理）への助走である。「みんなが同じ方向に流れる」とき、予測は何を外すのか、を意識して書くとよい。

> 文字数の目安：B1・B2あわせて 300〜500字。コピペ・引き写しは評価しない。**自分の言葉**で書くこと。
>
> **字数は目安です。多少の過不足で減点はしません。**見るのは、設問が挙げた要素（上の箇条書き）が書けているかどうかです。ただし要素が抜けていれば、その分は引きます。


!!! abstract "次回予告"
    第5回「連続確率分布：正規分布の数理」。なぜ世界は正規分布だらけなのか ―― 答えはまた **独立** にある（多数の独立な要因の和）。そして「すべてが正規」ではないことも見る。