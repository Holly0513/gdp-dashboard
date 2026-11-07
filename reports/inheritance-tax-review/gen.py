# -*- coding: utf-8 -*-
"""Generate the premium A4 tax-review report (HTML), then print to PDF with Playwright."""
import sys, pathlib

OUT = pathlib.Path(sys.argv[1])

SRC = {
    1: ("財政部 109 年 7 月 15 日令釋（繼承房地額外負擔）", "https://gazette.nat.gov.tw/egFront/eguploadpubWrapper?file=%2FEG_FileManager%2Feguploadpub%2Feg026132%2Fch04%2Ftype2%2Fgov30%2Fnum11%2FEg.htm&metaid=117054"),
    2: ("財政部臺北國稅局｜繼承房貸額外負擔說明", "https://www.mof.gov.tw/singlehtml/384fb3077bb349ea973e7fc6f13b6974?cntId=ae1948f2ee40413cb8a43bdaf65038f3"),
    3: ("財政部 112 年 11 月 23 日公告（113 年遺產稅免稅額、扣除額及級距）", "https://gazette.nat.gov.tw/EG_FileManager/eguploadpub/eg029222/ch04/type3/gov30/num19/Eg.htm"),
    4: ("遺產及贈與稅法 第 10、13、14、17 條等", "https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0340072"),
    5: ("所得稅法 第 4 條之 4、第 14 條之 4 至 14 條之 5 等", "https://law-out.mof.gov.tw/LawContent.aspx?id=FL005935"),
    6: ("財政部 110 年 6 月 11 日令釋（房地合一非自願出售）", "https://gazette.nat.gov.tw/EG_FileManager/eguploadpub/eg027108/ch04/type1/gov30/num5/Eg.htm"),
    7: ("納稅者權利保護法 第 7 條（租稅規避）", "https://law-out.mof.gov.tw/LawContent.aspx?KeyWord=&id=GL010199"),
    8: ("臺北高等行政法院 114 年度訴字第 174 號判決", "https://judgment.judicial.gov.tw/FJUD/printData.aspx?id=TPBA%2C114%2C%E8%A8%B4%2C174%2C20260129%2C2"),
    9: ("財政部稅務入口網｜生前未清償債務扣除及證明文件", "https://www.etax.nat.gov.tw/etwmain/tax-info/understanding/tax-q-and-a/national/estate-tax/exemption/g8njZxx"),
    10: ("財政部 115 年 7 月 15 日令釋", "https://law-out.mof.gov.tw/LawContent.aspx?id=GL011745"),
}

def cite(*ns):
    return "".join(f'<a class="cite" href="{SRC[n][1]}">[{n}]</a>' for n in ns)

TOTAL = 12
def page(n, section, body, cls=""):
    return f'''
<section class="page {cls}">
  <header class="run"><span class="brand">保險傳承證據代理人</span><span class="sec">{section}</span></header>
  <div class="content">{body}</div>
  <footer class="foot"><span>繼承房地稅務審閱報告書　｜　審閱稿・待會計師／律師覆核</span><span class="pn">{n:02d}<i> / {TOTAL:02d}</i></span></footer>
</section>'''

def h(kicker, title, lead=""):
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="h"><div class="kicker">{kicker}</div><h2>{title}</h2>{l}</div>'

# ---------- charts (inline SVG) ----------
def waterfall():
    steps = [("銀行存款", 8000, "add"), ("房地現值", 2400, "add"), ("遺產總額", 10400, "total"),
             ("未償貸款", -4200, "sub"), ("扣債後價值", 6200, "total"),
             ("免稅額", -1333, "sub"), ("成年子女", -56, "sub"), ("喪葬費", -138, "sub"),
             ("課稅淨額", 4673, "total")]
    W, H, top, base = 640, 270, 24, 220
    sc = (base - top) / 10400
    bw, gap, x0 = 50, 18, 20
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="遺產稅瀑布圖">']
    for v in (0, 2500, 5000, 7500, 10000):
        y = base - v * sc
        out.append(f'<line x1="14" x2="{W-10}" y1="{y:.1f}" y2="{y:.1f}" class="grid"/>')
    run = 0
    prev_end = None
    for i, (lab, v, kind) in enumerate(steps):
        x = x0 + i * (bw + gap)
        if kind == "total":
            y0, y1 = 0, v; run = v; c = "c-total"
        elif kind == "add":
            y0, y1 = run, run + v; run += v; c = "c-add"
        else:
            y0, y1 = run + v, run; run += v; c = "c-sub"
        yt, yb = base - max(y0, y1) * sc, base - min(y0, y1) * sc
        hgt = max(yb - yt, 1.5)
        out.append(f'<rect x="{x}" y="{yt:.1f}" width="{bw}" height="{hgt:.1f}" rx="2" class="{c}"/>')
        if prev_end is not None:
            out.append(f'<line x1="{prev_end[0]}" x2="{x}" y1="{prev_end[1]:.1f}" y2="{prev_end[1]:.1f}" class="conn"/>')
        prev_end = (x + bw, base - run * sc)
        txt = f'{v:+,}'.replace("+", "") if kind != "sub" else f'−{abs(v):,}'
        out.append(f'<text x="{x+bw/2}" y="{yt-6:.1f}" class="vl">{txt}</text>')
        out.append(f'<text x="{x+bw/2}" y="{base+16}" class="xl">{lab}</text>')
    out.append(f'<line x1="14" x2="{W-10}" y1="{base}" y2="{base}" class="axis"/>')
    out.append('</svg>')
    return "".join(out)

def tax_bars():
    # 20% / 35% x 不准扣 / 准扣
    data = [("適用 20%", 656, 296), ("適用 35%", 1148, 518)]
    W, H, l, r = 640, 190, 92, 96
    mx = 1200; sc = (W - l - r) / mx
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="房地合一稅比較">']
    for v in (0, 300, 600, 900, 1200):
        x = l + v * sc
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="12" y2="{H-24}" class="grid"/><text x="{x:.1f}" y="{H-8}" class="xl">{v:,}</text>')
    y = 20
    for lab, a, b in data:
        out.append(f'<text x="{l-12}" y="{y+30}" class="yl">{lab}</text>')
        out.append(f'<rect x="{l}" y="{y}" width="{a*sc:.1f}" height="22" rx="2" class="c-sub"/><text x="{l+a*sc+8:.1f}" y="{y+16}" class="vl l">{a:,} 不准扣</text>')
        out.append(f'<rect x="{l}" y="{y+26}" width="{b*sc:.1f}" height="22" rx="2" class="c-total"/><text x="{l+b*sc+8:.1f}" y="{y+42}" class="vl l">{b:,} 全額准扣</text>')
        y += 76
    out.append('</svg>')
    return "".join(out)

def balance():
    # 死亡日資產負債快照
    W, H = 640, 150
    tot = 10400; sc = 560 / tot; x0 = 40
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="死亡日資產負債">']
    out.append(f'<text x="{x0}" y="16" class="cap">資產　10,400 萬</text>')
    out.append(f'<rect x="{x0}" y="24" width="{3800*sc:.1f}" height="34" class="c-total"/>')
    out.append(f'<rect x="{x0+3800*sc:.1f}" y="24" width="{4200*sc:.1f}" height="34" class="c-hatch"/>')
    out.append(f'<rect x="{x0+8000*sc:.1f}" y="24" width="{2400*sc:.1f}" height="34" class="c-add"/>')
    for x, w, t in ((x0, 3800, "原有存款 3,800"), (x0+3800*sc, 4200, "借款存入 4,200"), (x0+8000*sc, 2400, "房地現值 2,400")):
        out.append(f'<text x="{x + w*sc/2:.1f}" y="46" class="in">{t}</text>')
    out.append(f'<text x="{x0}" y="90" class="cap">負債　4,200 萬</text>')
    out.append(f'<rect x="{x0+3800*sc:.1f}" y="98" width="{4200*sc:.1f}" height="34" class="c-sub"/>')
    out.append(f'<text x="{x0+3800*sc+4200*sc/2:.1f}" y="120" class="in">銀行抵押貸款 4,200</text>')
    out.append(f'<line x1="{x0+3800*sc:.1f}" x2="{x0+3800*sc:.1f}" y1="20" y2="138" class="dash"/>')
    out.append(f'<line x1="{x0+8000*sc:.1f}" x2="{x0+8000*sc:.1f}" y1="20" y2="138" class="dash"/>')
    out.append('</svg>')
    return "".join(out)

def scen_bars():
    data = [("基準示範", 467.3, "c-total"), ("情境 A 兩名子女", 461.7, "c-add"), ("情境 B 配偶在世", 412.0, "c-add")]
    W, H, l = 420, 150, 118
    sc = (W - l - 60) / 500
    out = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="各情境遺產稅">']
    y = 14
    for lab, v, c in data:
        out.append(f'<text x="{l-10}" y="{y+17}" class="yl">{lab}</text><rect x="{l}" y="{y}" width="{v*sc:.1f}" height="26" rx="2" class="{c}"/><text x="{l+v*sc+6:.1f}" y="{y+18}" class="vl l">{v}</text>')
        y += 42
    out.append('</svg>')
    return "".join(out)

# ---------- pages ----------
P = []

# 01 cover
P.append(f'''
<section class="page cover">
  <div class="cv-top">
    <div class="cv-brand">保險傳承證據代理人<span>INHERITANCE &amp; TAX REVIEW</span></div>
    <div class="cv-tag">審閱稿 ・ 2026 年 11 月</div>
  </div>
  <div class="cv-main">
    <div class="cv-kicker">臺灣不動產暨稅務審閱報告書</div>
    <h1>繼承房地<br>稅務審閱報告</h1>
    <div class="cv-rule"></div>
    <p class="cv-sub">8,000 萬存款 ・ 4,200 萬房貸 ・ 1,800 萬額外負擔<br>遺產稅與房地合一稅之分段判斷、證據要求與風險界線</p>
  </div>
  <div class="cv-figs">
    <div><b>467.3</b><span>萬元</span><em>遺產稅示範稅額</em></div>
    <div><b>1,800</b><span>萬元</span><em>額外負擔差額上限</em></div>
    <div><b>360–630</b><span>萬元</span><em>售屋所得稅差額區間</em></div>
  </div>
  <div class="cv-meta">
    <dl>
      <dt>案件</dt><dd>父親抵押借款後身故；子女以繼承存款清償房貸並出售房地</dd>
      <dt>審閱範圍</dt><dd>遺產稅（2024 繼承）｜房地合一稅（2026 出售）｜租稅規避界線</dd>
      <dt>文件狀態</dt><dd>示範試算；尚未經證據、會計師、律師及發布審核</dd>
    </dl>
  </div>
</section>''')

# 02 contents + how to read
toc = [("01", "執行摘要", "三個結論、稅負總覽與關鍵洞見", "03"),
       ("02", "案件事實", "2022–2026 時間軸與死亡日資產負債", "04"),
       ("03", "第一階段｜遺產稅", "列報原則、瀑布試算與家庭情境敏感度", "05"),
       ("04", "第二階段｜房地合一稅", "新舊制、持有期間與稅率判定", "07"),
       ("05", "1,800 萬額外負擔", "准扣與不准扣之稅額差、四道要件", "08"),
       ("06", "租稅規避界線", "對照分析、支持事實與待查疑點", "10"),
       ("07", "法院判決參考", "114 年度訴字第 174 號之可用與不可用處", "11"),
       ("08", "行動計畫與證據清單", "風險矩陣、申報前文件、官方來源", "12")]
toc_html = "".join(f'<li><span class="tn">{a}</span><span class="tt"><b>{b}</b><em>{c}</em></span><span class="tp">{d}</span></li>' for a, b, c, d in toc)
P.append(page(2, "目錄", f'''
{h("CONTENTS", "目錄")}
<ol class="toc">{toc_html}</ol>
<div class="howto">
  <h3>閱讀指引</h3>
  <div class="legend">
    <span><i class="dot g"></i><b>已可確認</b>數字或法律規定明確，與事實無涉</span>
    <span><i class="dot y"></i><b>待查證</b>結論方向成立，但須以原始文件證明</span>
    <span><i class="dot r"></i><b>風險點</b>可能被國稅局調整或爭訟之處</span>
  </div>
  <p>金額單位除另註明外均為<strong>新臺幣萬元</strong>。所有稅額均為依限定假設之<strong>示範試算</strong>，不等於稽徵機關核定稅額；實際家庭成員、其他財產、扣除額或取得日不同時，應重新計算。</p>
</div>
'''))

# 03 executive summary
P.append(page(3, "01　執行摘要", f'''
{h("EXECUTIVE SUMMARY", "兩種稅、兩個課稅事件，不能混為一談",
   "本案涉及 2024 年「繼承」與 2026 年「出售」兩個獨立課稅事件，應分別適用遺產及贈與稅法與所得稅法房地合一規定，並另行檢視是否構成租稅規避。")}
<div class="kpis">
  <div class="kpi"><em>遺產稅（示範）</em><b>467.3</b><span>無配偶、一名成年子女</span><i class="dot g"></i></div>
  <div class="kpi"><em>額外負擔差額</em><b>1,800</b><span>4,200 − 2,400；扣除資格待查</span><i class="dot y"></i></div>
  <div class="kpi"><em>售屋稅差（20%）</em><b>360</b><span>適用 35% 時為 630</span><i class="dot y"></i></div>
  <div class="kpi"><em>兩稅合計（20%）</em><b>763–1,123</b><span>准扣 ↔ 不准扣</span><i class="dot r"></i></div>
</div>
<div class="three">
  <div class="card"><div class="no">01</div><h4>遺產稅</h4><p>銀行存款 8,000 萬應全數列入遺產；有確實證明的死亡前未償銀行債務 4,200 萬，依法另行審查扣除。{cite(4,9)}</p></div>
  <div class="card"><div class="no">02</div><h4>房地合一稅</h4><p>繼承時房地現值 2,400 萬，抵押債務 4,200 萬；超出之 1,800 萬僅在符合 109 年令釋及實際負擔要件時可減除。{cite(1,5)}</p></div>
  <div class="card"><div class="no">03</div><h4>本案核心風險</h4><p>借款未動用、現金留在遺產，子女再以繼承存款還款。須查核借貸真實性、資金歸屬及是否濫用法律形式。{cite(7)}</p></div>
</div>
<div class="insight">
  <div class="ins-k">關鍵洞見</div>
  <p><b>借款對遺產稅是「中性」的；真正的稅負差異只出現在售屋所得稅。</b>存款增加 4,200 萬、負債同步增加 4,200 萬，扣債後遺產價值與未借款時同為 6,200 萬。若 1,800 萬額外負擔獲准扣除，效果完全體現在房地合一稅（20% 時少 360 萬），這也正是稽徵機關檢視「是否濫用法律形式」的焦點。</p>
</div>
<div class="qs3"><div class="qh">三個分開判斷的法律問題</div>
  <div><b>①</b>遺產現金與債務是否如實列報？</div><div><b>②</b>1,800 萬額外負擔是否確由子女承受？</div><div><b>③</b>借款是否存在濫用法律形式的安排？</div></div>
<div class="next3">
  <div><em>NEXT 1</em><b>調閱原始取得日</b><span>登記謄本、異動索引，決定新舊制與稅率</span></div>
  <div><em>NEXT 2</em><b>備齊扣除證據</b><span>抵押、死亡日餘額、清償紀錄、分割協議</span></div>
  <div><em>NEXT 3</em><b>交專業覆核</b><span>會計師試算申報，律師檢視租稅規避風險</span></div>
</div>
<div class="verdict">不是「有 8,000 萬現金就必不准扣」，也不是「有 4,200 萬房貸就必准扣」。</div>
'''))

# 04 facts
tl = [("2022 / 6 / 1", "父親借款", "原有存款 3,800 萬；以本案房地抵押向銀行借款 4,200 萬，全數存入銀行、未動用。"),
      ("2024 / 6 / 1", "父親死亡（繼承開始）", "存款 8,000 萬（含借款 4,200 萬）；房地課稅現值 2,400 萬；未償銀行抵押貸款 4,200 萬。"),
      ("2025", "子女清償房貸", "子女以繼承存款 4,200 萬清償；僅就現金而言，未計稅費前餘 3,800 萬。"),
      ("2026", "出售房地", "以 6,000 萬出售。所得與稅率須另確認父親原始取得日、費用、土地漲價總數額及新舊制。")]
tl_html = "".join(f'<li><div class="td">{a}</div><div class="tb"><b>{b}</b><p>{c}</p></div></li>' for a, b, c in tl)
P.append(page(4, "02　案件事實", f'''
{h("CASE FACTS", "2022 至 2026：借款、繼承、清償、出售")}
<ol class="timeline">{tl_html}</ol>
<div class="panel">
  <div class="ph"><b>死亡日（2024/6/1）資產負債快照</b><span>單位：萬元</span></div>
  {balance()}
  <p class="note">金色區塊即借款存入之 4,200 萬：它同時出現在資產與負債兩側，<strong>並非新增淨資產</strong>。{cite(1,9)}</p>
</div>
<div class="panel">
  <div class="ph"><b>家族現金流全貌（示範 A，稅率 20%）</b><span>單位：萬元</span></div>
  <div class="flow">
    <div class="fs"><em>繼承存款</em><b>8,000</b></div><i>→</i>
    <div class="fs neg"><em>繳遺產稅</em><b>−467.3</b></div><i>→</i>
    <div class="fs neg"><em>清償房貸</em><b>−4,200</b></div><i>→</i>
    <div class="fs pos"><em>出售房地</em><b>+6,000</b></div><i>→</i>
    <div class="fs neg"><em>有憑證費用</em><b>−100</b></div><i>→</i>
    <div class="fs neg"><em>房地合一稅</em><b>−296 / −656</b></div>
  </div>
  <div class="flowres"><div><em>額外負擔全額准扣</em><b>8,936.7</b></div><div><em>額外負擔不准扣</em><b>8,576.7</b></div><div class="d"><em>差額</em><b>360</b></div></div>
  <p class="note">未計土地增值稅、契稅、代書與其他交易成本；僅用於理解資金走向，不代表實際可支配金額。</p>
</div>
'''))

# 05 estate tax waterfall
P.append(page(5, "03　第一階段｜遺產稅", f'''
{h("STAGE 1 ・ ESTATE TAX", "現金與負債必須同時揭露",
   "遺產稅以死亡時財產價值計算；房地以公告土地現值及房屋評定標準價格核認，不以 6,000 萬市價計。")}
<div class="panel">
  <div class="ph"><b>由遺產總額到課稅遺產淨額</b><span>單位：萬元</span></div>
  {waterfall()}
  <div class="lg"><span><i class="sw c-add"></i>資產</span><span><i class="sw c-sub"></i>減項</span><span><i class="sw c-total"></i>小計</span></div>
</div>
<div class="two">
  <table class="tbl">
    <thead><tr><th>項目（113 年適用金額）</th><th class="n">萬元</th></tr></thead>
    <tbody>
      <tr><td>銀行存款（含借款存入）</td><td class="n">8,000</td></tr>
      <tr><td>房地課稅現值（非市價）</td><td class="n">2,400</td></tr>
      <tr class="sub"><td>遺產總額</td><td class="n">10,400</td></tr>
      <tr><td>確有證明之未償貸款</td><td class="n neg">−4,200</td></tr>
      <tr><td>免稅額</td><td class="n neg">−1,333</td></tr>
      <tr><td>成年子女扣除額（1 名）</td><td class="n neg">−56</td></tr>
      <tr><td>喪葬費扣除額</td><td class="n neg">−138</td></tr>
      <tr class="sub"><td>課稅遺產淨額</td><td class="n">4,673</td></tr>
      <tr class="tot"><td>應納遺產稅（10%）</td><td class="n">467.3</td></tr>
    </tbody>
  </table>
  <div class="side">
    <h4>計算與法律前提</h4>
    <p>4,673 落在 113 年第一級距（課稅遺產淨額 5,621 萬以下）稅率 10%：4,673 × 10% ＝ <b>467.3 萬</b>。{cite(3)}</p>
    <p>遺產及贈與稅法第 17 條第 1 項第 9 款：被繼承人死亡前未償債務須<b>具確實證明</b>，銀行貸款應備借款契約、撥款紀錄及死亡日餘額證明。{cite(4,9)}</p>
    <p class="muted">原報告寫「5,000 萬以下 10%」係法定基準金額；113 年經物價指數調整後級距上限為 5,621 萬，本版已更正，結果不變。</p>
  </div>
</div>
'''))

# 06 estate sensitivity
sens = [("基準示範", "無配偶、一名成年子女", "4,673", "467.3", "base"),
        ("情境 A", "無配偶、兩名成年子女（+56）", "4,617", "461.7", ""),
        ("情境 B", "配偶在世、一名成年子女（+553）", "4,120", "412.0", ""),
        ("情境 C", "情境 B ＋ 配偶主張剩餘財產差額分配請求權", "依請求額再減", "另計", "")]
sens_html = "".join(f'<tr class="{e}"><td><b>{a}</b></td><td>{b}</td><td class="n">{c}</td><td class="n">{d}</td></tr>' for a, b, c, d, e in sens)
P.append(page(6, "03　第一階段｜遺產稅", f'''
{h("STAGE 1 ・ SENSITIVITY", "467.3 萬只在限定假設下成立",
   "家庭成員結構直接影響扣除額。以下以 113 年適用金額示範，其他財產、生前贈與或其他扣除額均未納入。")}
<table class="tbl wide">
  <thead><tr><th>情境</th><th>家庭條件</th><th class="n">課稅遺產淨額</th><th class="n">遺產稅（10%）</th></tr></thead>
  <tbody>{sens_html}</tbody>
</table>
<div class="three">
  <div class="card soft"><h4>借款存在與否，遺產稅不變</h4><p>未借款：存款 3,800 ＋ 房地 2,400 ＝ 6,200。<br>有借款：10,400 − 4,200 ＝ 6,200。<br>兩者扣債後價值完全相同。</p></div>
  <div class="card soft"><h4>扣債的證據門檻</h4><p>需能證明貸款期間、撥款入帳、死亡日餘額，且債務屬被繼承人本人。缺證明時，存款照列、債務不准扣，稅負反而上升。{cite(9)}</p></div>
  <div class="card soft"><h4>重病期間舉債之檢查</h4><p>若借款時被繼承人已重病無法處理事務，繼承人須說明借款用途。本案資金仍在存款中並已列入遺產，宜備妥流水佐證。</p></div>
</div>
<div class="two w64">
  <div class="panel"><div class="ph"><b>各情境遺產稅</b><span>單位：萬元</span></div>{scen_bars()}</div>
  <table class="tbl">
    <thead><tr><th>113 年課稅遺產淨額</th><th class="n">稅率</th></tr></thead>
    <tbody>
      <tr class="hl-g"><td>5,621 萬以下</td><td class="n">10%</td></tr>
      <tr><td>5,621–11,242 萬</td><td class="n">15%</td></tr>
      <tr><td>11,242 萬以上</td><td class="n">20%</td></tr>
    </tbody>
  </table>
</div>
<div class="insight"><div class="ins-k">配偶提醒</div><p>若配偶在世，除 553 萬配偶扣除額外，還可主張<b>剩餘財產差額分配請求權</b>，自遺產總額中扣除，常是影響稅額最大的一項；須於申報時主張並附財產證明。</p></div>
<div class="verdict">資產 10,400 − 貸款 4,200 ＝ 6,200 萬，仍不是最終「課稅遺產淨額」；應以實際家庭與財產狀況重算。{cite(3)}</div>
'''))

# 07 house tax regime
P.append(page(7, "04　第二階段｜房地合一稅", f'''
{h("STAGE 2 ・ REGIME", "賣房先判定新舊制與持有期間",
   "因繼承取得之房地，持有期間得合併被繼承人持有期間計算；但新舊制與稅率仍取決於「父親原始取得日」，而非借款日或繼承日。")}
<div class="three">
  <div class="card"><div class="no">A</div><h4>父親 2018/6 取得</h4><p>子女 2026/6 出售，原則適用新制；合併持有約 8 年，境內居住者稅率 <b>20%</b>。</p><div class="pill g">稅率 20%</div></div>
  <div class="card"><div class="no">B</div><h4>父親 2022/6 取得</h4><p>子女 2026/6 出售，原則適用新制；合併持有約 4 年，境內居住者稅率 <b>35%</b>。</p><div class="pill r">稅率 35%</div></div>
  <div class="card"><div class="no">C</div><h4>父親 2015 年以前取得</h4><p>須檢查舊制與過渡規定；不能僅因子女於 2024 年繼承，就一律套用新制 20%。</p><div class="pill y">另行查核</div></div>
</div>
<table class="tbl wide rates">
  <thead><tr><th>境內居住者持有期間（合併計算）</th><th class="n">稅率</th><th>本案示範</th></tr></thead>
  <tbody>
    <tr><td>2 年以內</td><td class="n">45%</td><td></td></tr>
    <tr class="hl-r"><td>超過 2 年、未逾 5 年</td><td class="n">35%</td><td>示範 B（約 4 年）</td></tr>
    <tr class="hl-g"><td>超過 5 年、未逾 10 年</td><td class="n">20%</td><td>示範 A（約 8 年）</td></tr>
    <tr><td>超過 10 年</td><td class="n">15%</td><td></td></tr>
  </tbody>
</table>
<div class="steps4">
  <div><em>STEP 1</em><b>調閱謄本</b><span>確認父親原始取得日與取得原因</span></div>
  <div><em>STEP 2</em><b>判定新舊制</b><span>以 105/1/1 前後及過渡規定判斷</span></div>
  <div><em>STEP 3</em><b>合併持有期間</b><span>父親持有期間＋子女繼承後持有</span></div>
  <div><em>STEP 4</em><b>確定稅率試算</b><span>再代入成本、費用、額外負擔</span></div>
</div>
<div class="insight"><div class="ins-k">為何先查日期</div><p>同樣 3,280 萬課稅所得，稅率 20% 為 656 萬、35% 為 1,148 萬，<b>相差 492 萬</b>，甚至大於 1,800 萬額外負擔帶來的 360 萬差額。取得日的查證，是本案效益最高的一步。</p></div>
<div class="verdict">關鍵：2022 年是「借款日」，不一定是「原始購屋日」。未核對權狀與原始取得資料前，不能確定售屋稅率。{cite(5,6,10)}</div>
'''))

# 08 1800 difference
P.append(page(8, "05　1,800 萬額外負擔", f'''
{h("STAGE 2 ・ IMPACT", "1,800 萬准扣與不准扣：所得稅差額",
   "示範 A 假設：父親 2018 年購屋、子女 2026 年出售；物價調整 105%、有憑證費用 100 萬、可減除土地漲價總數額 100 萬。")}
<div class="two w64">
  <table class="tbl">
    <thead><tr><th>房地合一稅計算</th><th class="n">不准扣</th><th class="n">全額准扣</th></tr></thead>
    <tbody>
      <tr><td>出售價額</td><td class="n">6,000</td><td class="n">6,000</td></tr>
      <tr><td>繼承現值 × 105%</td><td class="n neg">−2,520</td><td class="n neg">−2,520</td></tr>
      <tr><td>費用與土地漲價總數額</td><td class="n neg">−200</td><td class="n neg">−200</td></tr>
      <tr><td>額外負擔（109 年令釋）</td><td class="n">0</td><td class="n neg">−1,800</td></tr>
      <tr class="sub"><td>課稅所得</td><td class="n">3,280</td><td class="n">1,480</td></tr>
      <tr class="tot"><td>應納稅額（20%）</td><td class="n">656</td><td class="n">296</td></tr>
      <tr><td>應納稅額（35%）</td><td class="n">1,148</td><td class="n">518</td></tr>
    </tbody>
  </table>
  <div class="side">
    <div class="big"><em>稅額差（20%）</em><b>360</b><span>萬元 ＝ 1,800 × 20%</span></div>
    <div class="big r"><em>稅額差（35%）</em><b>630</b><span>萬元 ＝ 1,800 × 35%</span></div>
  </div>
</div>
<div class="panel">
  <div class="ph"><b>應納房地合一稅比較</b><span>單位：萬元</span></div>
  {tax_bars()}
</div>
<table class="tbl wide">
  <thead><tr><th>額外負擔認列比例（對應要件四：實際負擔與持分）</th><th class="n">認列金額</th><th class="n">課稅所得</th><th class="n">稅額（20%）</th><th class="n">稅額（35%）</th></tr></thead>
  <tbody>
    <tr><td>不准扣（0%）</td><td class="n">0</td><td class="n">3,280</td><td class="n">656</td><td class="n">1,148</td></tr>
    <tr><td>部分認列（50%）</td><td class="n">900</td><td class="n">2,380</td><td class="n">476</td><td class="n">833</td></tr>
    <tr class="tot"><td>全額認列（100%）</td><td class="n">1,800</td><td class="n">1,480</td><td class="n">296</td><td class="n">518</td></tr>
  </tbody>
</table>
<p class="note">稅額差僅在全部符合扣除條件時成立；成本、費用、物價指數或稅率不同時應重算。{cite(1,2,5)}</p>
'''))

# 09 four requirements
req = [("一", "同一標的", "死亡時未償債務，必須以本次繼承並出售的「該房地」提供抵押擔保。", "y", "核對抵押權設定", "他項權利證明書、抵押權設定契約、建物／土地謄本"),
       ("二", "金融機構", "以金融機構為債權人；私人間借貸不因有不動產抵押就自動符合令釋。", "g", "本案為銀行貸款", "銀行借款契約、撥款入帳紀錄"),
       ("三", "超過現值", "死亡日抵押貸款餘額 4,200 − 房地現值 2,400 ＝ 1,800 萬，為差額上限。", "g", "金額可確認", "死亡日貸款餘額證明、公告土地現值與房屋評定現值"),
       ("四", "實際負擔", "須核對繼承人負擔與償還紀錄；僅部分真正負擔者，不能不分持分全額認列。", "y", "核對清償憑證與持分", "清償本息扣款紀錄、遺產分割協議、繼承登記持分")]
req_html = "".join(f'<div class="req"><div class="rn">要件{a}</div><h4>{b}</h4><p>{c}</p><div class="ev"><em>應備證據</em>{f}</div><div class="st"><i class="dot {d}"></i>{e}</div></div>' for a, b, c, d, e, f in req)
P.append(page(9, "05　1,800 萬額外負擔", f'''
{h("ELIGIBILITY", "109 年令釋：四道要件都要成立",
   "四項要件為「且」的關係，任何一項無法證明，1,800 萬即不得自售屋所得中減除。")}
<div class="reqs">{req_html}</div>
<div class="insight">
  <div class="ins-k">實務提醒</div>
  <p>以繼承現金清償貸款，本身<b>並非</b>令釋列出的排除原因；但還款資金的來源、付款人與遺產分配是否一致，仍須查明。若遺產分割協議由特定繼承人取得房地與對應存款，應由該繼承人名義清償並保留扣款紀錄。{cite(1,2)}</p>
</div>
'''))

# 10 avoidance boundary
P.append(page(10, "06　租稅規避界線", f'''
{h("ANTI-AVOIDANCE", "真實借貸、現金保留與租稅規避的界線",
   "把「父親未借款」作為對照組，可以看清此安排的稅務效果落在哪裡，也就知道稽徵機關會檢視什麼。")}
<table class="tbl wide">
  <thead><tr><th>對照分析（示範 A，20%）</th><th class="n">父親未借款</th><th class="n">借款且准扣</th><th class="n">差異</th></tr></thead>
  <tbody>
    <tr><td>扣債後遺產價值</td><td class="n">6,200</td><td class="n">6,200</td><td class="n">0</td></tr>
    <tr><td>遺產稅</td><td class="n">467.3</td><td class="n">467.3</td><td class="n">0</td></tr>
    <tr><td>房地合一稅</td><td class="n">656</td><td class="n">296</td><td class="n neg">−360</td></tr>
    <tr class="tot"><td>兩稅合計</td><td class="n">1,123.3</td><td class="n">763.3</td><td class="n">−360</td></tr>
  </tbody>
</table>
<div class="three">
  <div class="card g"><h4>支持扣除的事實</h4><p>金融機構真實放款、抵押有效、死亡時仍未償；8,000 萬存款與 4,200 萬負債均如實列報；子女確實承受並清償。</p></div>
  <div class="card y"><h4>需加強調查的疑點</h4><p>借款完全未動用，資金目的為何？是否有親友代償、補償或資金回流？繼承分配與付款人是否一致？</p></div>
  <div class="card r"><h4>依法調整不能靠臆測</h4><p>納保法第 7 條：須證明濫用法律形式、非常規交易、違背立法目的等要件；稽徵機關負舉證責任，納稅人負協力義務。{cite(7)}</p></div>
</div>
<div class="spec">
  <div class="sbar"><span class="z1">合法節稅</span><span class="z2">灰色地帶・須說明</span><span class="z3">租稅規避／虛偽</span></div>
  <div class="slab"><div>真實借貸、如實列報、子女實際清償</div><div>借款未動用、目的未說明、付款人與分配不一致</div><div>虛偽借貸、資金回流、親友代償未揭露</div></div>
</div>
<div class="steps4">
  <div><em>說明 1</em><b>交易真實</b><span>契約、撥款、抵押登記完整</span></div>
  <div><em>說明 2</em><b>資金未挪用</b><span>存款流水連續，並已列入遺產</span></div>
  <div><em>說明 3</em><b>負擔歸屬</b><span>分割協議、清償人與持分一致</span></div>
  <div><em>說明 4</em><b>借款目的</b><span>依實際情況說明，不得事後虛構</span></div>
</div>
<div class="verdict">不是「有節稅目的就違法」，也不是「銀行放款真實就一律排除租稅規避」。</div>
'''))

# 11 court case
P.append(page(11, "07　法院判決參考", f'''
{h("CASE LAW", "114 年度訴字第 174 號：扣除與 20% 稅率分開審",
   "臺北高等行政法院高等行政訴訟庭，2026/1/29 判決，原告之訴駁回；判決確定狀態另待查。")}
<div class="two">
  <div class="card"><div class="no">A</div><h4>A 房地</h4><p>超額房貸負擔 1,367 萬餘元<br>核定交易所得 2,122 萬餘元</p></div>
  <div class="card"><div class="no">B</div><h4>B 房地</h4><p>超額房貸負擔 2,796 萬餘元<br>核定交易所得 1,356 萬餘元</p></div>
</div>
<div class="cmp">
  <div><h4><i class="dot g"></i>可以參考的部分</h4><ul>
    <li>超額房貸負擔已在所得計算中認列，顯示「額外負擔扣除」與「稅率適用」是兩個獨立爭點。</li>
    <li>主張非自願出售 20%，須客觀證明無足夠資力清償貸款。</li>
    <li>法院會綜合衡量遺產市值、存款、股票與家庭資力。</li></ul></div>
  <div><h4><i class="dot r"></i>不能直接套用的部分</h4><ul>
    <li>該案並非「4,200 萬借款原封不動留在 8,000 萬存款」的情形，不是本案直接判例。</li>
    <li>不得把另一件判決當作本案已獲核定的證據。</li>
    <li>本案繼承 8,000 萬存款，僅稱房貸很高，難以主張非自願出售。</li></ul></div>
</div>
<table class="tbl wide">
  <thead><tr><th>比較項目</th><th>114 年度訴字第 174 號</th><th>本案</th></tr></thead>
  <tbody>
    <tr><td><b>主要爭點</b></td><td>非自願出售能否適用 20%</td><td>額外負擔扣除資格、原始取得日與稅率</td></tr>
    <tr><td><b>額外負擔</b></td><td>已在所得計算中認列</td><td>1,800 萬，待查證四要件</td></tr>
    <tr><td><b>繼承人資力</b></td><td>法院衡量遺產市值、存款、股票</td><td>繼承 8,000 萬存款</td></tr>
    <tr><td><b>結果</b></td><td>原告之訴駁回，維持 35%</td><td>尚未申報／核定</td></tr>
  </tbody>
</table>
<div class="verdict">結論：本案若主張非自願出售 20%，勝算有限；應以實際持有期間決定稅率，並將資源集中於額外負擔要件的舉證。{cite(6,8)}</div>
'''))

# 12 action plan + checklist + sources
risk = [("額外負擔 1,800 萬遭否准", "高", "高", "備齊抵押、清償與分配文件；依持分認列"),
        ("父親原始取得日不明致稅率錯用", "中", "高", "調閱權狀、登記謄本與原始買賣契約"),
        ("被認定濫用法律形式（納保法 §7）", "中", "中", "說明借款目的與資金流向；不作臆測性主張"),
        ("遺產稅扣債證明不足", "低", "中", "取得銀行死亡日餘額證明與撥款紀錄")]
risk_html = "".join(f'<tr><td>{a}</td><td class="c"><span class="lv {"r" if b=="高" else "y" if b=="中" else "g"}">{b}</span></td><td class="c"><span class="lv {"r" if c=="高" else "y" if c=="中" else "g"}">{c}</span></td><td>{d}</td></tr>' for a, b, c, d in risk)
docs = ["銀行借款契約、抵押權設定、2022 年撥款與存款完整流水",
        "2024/6/1 死亡日房地現值、銀行存款與貸款餘額證明",
        "遺產稅申報書／核定通知書、繼承人名冊、遺產分割協議",
        "2025 年子女清償本金及利息之銀行扣款／清償證明",
        "原始購屋日期、2026 出售契約、仲介費、土地漲價總數額資料"]
docs_html = "".join(f'<li><i class="box"></i>{d}</li>' for d in docs)
src_html = "".join(f'<li><a href="{u}">[{n}] {t}</a></li>' for n, (t, u) in SRC.items())
P.append(page(12, "08　行動計畫與證據清單", f'''
{h("ACTION PLAN", "申報前：風險矩陣、證據清單與官方來源")}
<table class="tbl wide risk">
  <thead><tr><th>風險事項</th><th class="c">可能性</th><th class="c">影響</th><th>因應措施</th></tr></thead>
  <tbody>{risk_html}</tbody>
</table>
<div class="two">
  <div><h4 class="sh">申報／覆核前必備原件</h4><ul class="check">{docs_html}</ul>
    <p class="note">期限提醒：房地合一稅應於完成所有權移轉登記日之次日起 30 日內申報；遺產稅原應於死亡後 6 個月內申報，請確認已申報並取得核定通知書。</p></div>
  <div><h4 class="sh">三個結論的適用界線</h4><ul class="bound">
    <li><b>遺產稅 467.3 萬</b>：僅適用一名成年子女、無配偶等限定假設。</li>
    <li><b>額外負擔 1,800 萬</b>：金額差額成立；個案扣除資格尚待查證。</li>
    <li><b>售屋稅差 360 萬</b>：僅適用 20% 及示範成本費用之條件試算。</li></ul></div>
</div>
<h4 class="sh">官方原始來源（可點擊）</h4>
<ol class="srcs">{src_html}</ol>
<table class="tbl wide sign">
  <thead><tr><th>審閱紀錄</th><th>姓名</th><th>日期</th><th>意見／簽章</th></tr></thead>
  <tbody><tr><td>編製</td><td></td><td></td><td></td></tr><tr><td>會計師覆核</td><td></td><td></td><td></td></tr><tr><td>律師覆核</td><td></td><td></td><td></td></tr></tbody>
</table>
<p class="disc">本報告為稅務審閱之示範試算與教育用途，不構成稅務、法律意見或特定商品推薦，亦不保證稽徵機關核定結果；尚未通過證據、專家及發布審核，申報前請交由會計師／律師核對。</p>
'''))

CSS = open(pathlib.Path(__file__).with_name("style.css"), encoding="utf-8").read()
html = f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>繼承房地稅務審閱報告</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@500;700;900&family=Cormorant+Garamond:wght@500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{"".join(P)}</body></html>'''
OUT.write_text(html, encoding="utf-8")
print("pages", len(P))
