# -*- coding: utf-8 -*-
"""IG/FB carousel: 10 slides at 1080x1350 (4:5)."""
import sys, pathlib
OUT = pathlib.Path(sys.argv[1])
N = 10

def slide(i, body, theme="light", title_tag=""):
    return f'''<section class="s {theme}">
  <div class="top"><span class="brand">保險傳承證據代理人</span><span class="tag">{title_tag}</span></div>
  <div class="body">{body}</div>
  <div class="bot"><span>示範試算・非個案核定・申報前請洽會計師／律師</span><span class="pg">{i:02d}<i>/{N:02d}</i></span></div>
</section>'''

S = []

# 1 cover
S.append(f'''<section class="s cover">
  <div class="top"><span class="brand">保險傳承證據代理人</span><span class="tag">繼承稅務 ・ 案例拆解</span></div>
  <div class="cv">
    <div class="q">爸爸借了 4,200 萬<br>一毛都沒花</div>
    <div class="big">子女賣房<br>可能少繳 <b>360</b> 萬？</div>
    <div class="chips"><span>遺產稅</span><span>房地合一稅</span><span>1,800 萬額外負擔</span></div>
  </div>
  <div class="cvfoot">
    <div class="nums"><div><b>8,000</b><em>萬 存款</em></div><div><b>4,200</b><em>萬 房貸</em></div><div><b>6,000</b><em>萬 賣房</em></div></div>
    <div class="swipe">往左滑，10 張看懂 →</div>
  </div>
</section>''')

# 2 facts
steps = [("2022", "爸爸借款", "原有存款 3,800 萬，用房子抵押向銀行借 <b>4,200 萬</b>，全部存著沒動用"),
         ("2024", "爸爸過世", "存款 <b>8,000 萬</b>、房地現值 <b>2,400 萬</b>、銀行房貸還欠 <b>4,200 萬</b>"),
         ("2025", "子女還款", "子女用繼承來的存款，把 4,200 萬房貸一次還清"),
         ("2026", "出售房子", "以 <b>6,000 萬</b>賣出，接著要申報房地合一稅")]
st = "".join(f'<div class="step"><div class="yr">{a}</div><div><h3>{b}</h3><p>{c}</p></div></div>' for a, b, c in steps)
S.append(slide(2, f'''<h1>先看懂案情<br><span>四年、四件事</span></h1><div class="steps">{st}</div>
<div class="callout">一句話：借來的 4,200 萬<b>不是新增財產</b>——存款多 4,200 萬，負債也多 4,200 萬。</div>''', "light", "案情"))

# 3 estate tax
rows = [("銀行存款（含借款）", "8,000", ""), ("房地現值（不是市價）", "2,400", ""), ("扣：未償銀行貸款", "−4,200", "neg"),
        ("扣：免稅額", "−1,333", "neg"), ("扣：成年子女 1 名", "−56", "neg"), ("扣：喪葬費", "−138", "neg"),
        ("課稅遺產淨額", "4,673", "sum")]
rw = "".join(f'<div class="row {c}"><span>{a}</span><b>{b}</b></div>' for a, b, c in rows)
S.append(slide(3, f'''<h1>第一個稅<br><span>遺產稅怎麼算？</span></h1>
<div class="ledger">{rw}</div>
<div class="result"><div><em>應納遺產稅</em><small>4,673 × 10%（113 年級距 5,621 萬以下）</small></div><b>467.3<i>萬</i></b></div>
<p class="fine">假設：無配偶、一名成年子女、無其他財產。家庭結構不同，稅額就不同。</p>''', "light", "遺產稅"))

# 4 neutral
S.append(slide(4, f'''<h1>關鍵洞見<br><span>借款對遺產稅「沒有影響」</span></h1>
<div class="vs">
  <div class="col"><div class="lab">如果爸爸沒借款</div><div class="eq">3,800 存款<br>＋ 2,400 房地</div><div class="tot">6,200</div></div>
  <div class="mid">＝</div>
  <div class="col hl"><div class="lab">爸爸借了 4,200</div><div class="eq">10,400 資產<br>− 4,200 貸款</div><div class="tot">6,200</div></div>
</div>
<div class="callout dark">遺產稅一樣是 <b>467.3 萬</b>。<br>真正的差別，藏在<b>兩年後賣房子</b>的時候 →</div>''', "navy", "遺產稅"))

# 5 1800
S.append(slide(5, f'''<h1>第二個稅<br><span>房地合一稅的「額外負擔」</span></h1>
<div class="bars3">
  <div class="b"><div class="bar" style="height:100%"><b>4,200</b></div><em>死亡時房貸餘額</em></div>
  <div class="op">−</div>
  <div class="b"><div class="bar alt" style="height:57%"><b>2,400</b></div><em>繼承時房地現值</em></div>
  <div class="op">＝</div>
  <div class="b"><div class="bar gold" style="height:43%"><b>1,800</b></div><em>超過的額外負擔</em></div>
</div>
<div class="callout">依財政部 109 年令釋，子女<b>真的承擔並還掉</b>的這 1,800 萬，賣房時有機會從所得中減除。</div>''', "light", "房地合一稅"))

# 6 difference
S.append(slide(6, f'''<h1>准不准扣<br><span>稅差有多大？</span></h1>
<div class="cmp2">
  <div class="c no"><em>不准扣</em><div class="calc">6,000 − 2,520 − 200<br>＝ 課稅所得 3,280</div><b>656<i>萬</i></b><small>× 20%</small></div>
  <div class="c ok"><em>全額准扣</em><div class="calc">再減 1,800<br>＝ 課稅所得 1,480</div><b>296<i>萬</i></b><small>× 20%</small></div>
</div>
<div class="diff"><div><em>稅率 20%</em><b>少繳 360 萬</b></div><div><em>稅率 35%</em><b>少繳 630 萬</b></div></div>
<p class="fine">示範假設：爸爸 2018 年購屋、物價調整 105%、費用與土地漲價總數額共 200 萬。</p>''', "light", "房地合一稅"))

# 7 rate
rt = [("2 年以內", "45%", ""), ("2–5 年", "35%", "r"), ("5–10 年", "20%", "g"), ("10 年以上", "15%", "")]
rth = "".join(f'<div class="rt {c}"><span>{a}</span><b>{b}</b></div>' for a, b, c in rt)
S.append(slide(7, f'''<h1>稅率看什麼？<br><span>爸爸「原始買房日」</span></h1>
<div class="rates">{rth}</div>
<div class="cases">
  <div><b>2018 年買</b><span>合併持有約 8 年 → 20%</span></div>
  <div><b>2022 年買</b><span>合併持有約 4 年 → 35%</span></div>
  <div><b>2015 年前買</b><span>要另查舊制規定</span></div>
</div>
<div class="callout dark">注意：2022 是「借款日」，<b>不一定是買房日</b>！一定要調權狀核對。</div>''', "navy", "稅率"))

# 8 four requirements
rq = [("1", "同一間房", "貸款要用這次繼承、出售的那間房地抵押"), ("2", "金融機構", "債權人是銀行；私人借貸不算"),
      ("3", "超過現值", "4,200 − 2,400 ＝ 1,800 是上限"), ("4", "真的有還", "要有子女清償紀錄，且依持分認列")]
rqh = "".join(f'<div class="rq"><div class="n">{a}</div><h3>{b}</h3><p>{c}</p></div>' for a, b, c in rq)
S.append(slide(8, f'''<h1>想扣 1,800 萬<br><span>四個條件缺一不可</span></h1>
<div class="rqs">{rqh}</div>
<div class="callout">用繼承的現金去還款，<b>本身不是</b>不准扣的理由；但錢從哪來、誰付的，都要說得清楚。</div>''', "light", "扣除要件"))

# 9 irs & court
S.append(slide(9, f'''<h1>國稅局會看什麼？<br><span>節稅 ≠ 違法，但要經得起查</span></h1>
<div class="qa">
  <div class="qq"><b>？</b><p>借了錢完全沒用，目的是什麼？</p></div>
  <div class="qq"><b>？</b><p>有沒有親友代償、資金回流？</p></div>
  <div class="qq"><b>？</b><p>遺產分配和實際付款人一致嗎？</p></div>
</div>
<div class="law"><em>納稅者權利保護法 第 7 條</em><p>國稅局要證明「濫用法律形式」才能調整，負舉證責任；納稅人有協力義務。</p></div>
<div class="law"><em>北高行 114 年度訴字第 174 號（2026/1/29）</em><p>繼承大量存款的人，很難主張「非自願出售」適用 20%，法院維持 35%。</p></div>''', "navy", "風險"))

# 10 checklist + CTA
dc = ["銀行借款契約、抵押權設定、撥款與存款流水", "死亡日房地現值、存款與貸款餘額證明", "遺產稅核定通知書、遺產分割協議",
      "子女清償本金與利息的銀行紀錄", "原始購屋日期、出售契約、仲介費、土地漲價資料"]
dch = "".join(f'<li><i></i>{d}</li>' for d in dc)
S.append(slide(10, f'''<h1>申報前<br><span>這 5 份文件先備齊</span></h1>
<ul class="ck">{dch}</ul>
<div class="cta">
  <div><b>家裡也有繼承房地、房貸要處理？</b><p>私訊預約 15 分鐘免費電話，先了解你的現況。<br>這通電話不談商品，也不要求購買任何東西。</p></div>
  <div class="save">收藏<br>分享</div>
</div>
<p class="fine">本內容為教育用途之示範試算，不構成稅務或法律意見，實際稅額以稽徵機關核定為準。</p>''', "light", "行動清單"))

CSS = r'''
:root{--navy:#13253c;--navy2:#1d3556;--gold:#c9a46a;--gold2:#e7d3ad;--ivory:#f8f4ec;--ink:#1b2430;--ink2:#4c5664;--red:#b0473e;--green:#3f7d5c;--line:#e2dacb}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#888;font-family:"Noto Sans TC",sans-serif;font-variant-numeric:lining-nums}
.s{width:1080px;height:1350px;position:relative;overflow:hidden;display:flex;flex-direction:column;padding:64px 72px 52px;margin:0 auto 20px}
.light{background:var(--ivory);color:var(--ink)}
.navy,.cover{background:var(--navy);color:#f2ede4}
.light::before{content:"";position:absolute;left:0;top:0;bottom:0;width:14px;background:var(--gold)}
.navy::after,.cover::after{content:"";position:absolute;right:-260px;bottom:-260px;width:760px;height:760px;border-radius:50%;border:2px solid rgba(201,164,106,.18);box-shadow:0 0 0 60px rgba(201,164,106,.04),0 0 0 120px rgba(201,164,106,.03)}
.top{display:flex;justify-content:space-between;align-items:center;font-size:24px;letter-spacing:.12em;position:relative;z-index:1}
.brand{color:var(--gold);font-weight:700}
.tag{border:2px solid var(--gold);color:var(--gold);padding:6px 18px;border-radius:40px;font-size:22px;letter-spacing:.08em}
.body{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:space-between;gap:30px;padding:46px 0 36px;position:relative;z-index:1}
.bot{display:flex;justify-content:space-between;align-items:flex-end;font-size:20px;opacity:.6;position:relative;z-index:1}
.pg{font-family:"Cormorant Garamond",serif;font-size:40px;font-weight:600;opacity:1}
.pg i{font-style:normal;font-size:26px}
h1{font-family:"Noto Serif TC",serif;font-weight:900;font-size:76px;line-height:1.18;letter-spacing:.02em}
.light h1{color:var(--navy)}
h1 span{display:block;font-size:52px;color:var(--gold);font-weight:700;margin-top:10px}
.light h1 span{color:#a8813f}
b{font-weight:700}
.callout{font-size:34px;line-height:1.6;background:#fff;border-left:10px solid var(--gold);padding:30px 36px;color:var(--ink);box-shadow:0 8px 24px rgba(19,37,60,.08)}
.callout b{color:var(--red)}
.callout.dark{background:rgba(255,255,255,.07);color:#f2ede4;box-shadow:none}
.callout.dark b{color:var(--gold2)}
.fine{font-size:22px;color:var(--ink2);line-height:1.5}
.navy .fine{color:rgba(242,237,228,.7)}

/* cover */
.cover{padding:64px 72px 60px}
.cv{flex:1;display:flex;flex-direction:column;justify-content:center;gap:34px;position:relative;z-index:1}
.cv .q{font-family:"Noto Serif TC",serif;font-size:62px;font-weight:700;line-height:1.35;color:var(--gold2)}
.cv .big{font-family:"Noto Serif TC",serif;font-size:104px;font-weight:900;line-height:1.2;color:#fff}
.cv .big b{color:var(--gold);font-size:150px;font-family:"Noto Serif TC",serif}
.chips{display:flex;gap:16px;flex-wrap:wrap}
.chips span{font-size:28px;padding:10px 26px;border-radius:40px;background:rgba(201,164,106,.16);color:var(--gold2);border:1.5px solid rgba(201,164,106,.5)}
.cvfoot{position:relative;z-index:1}
.nums{display:grid;grid-template-columns:repeat(3,1fr);border-top:2px solid rgba(201,164,106,.5);border-bottom:2px solid rgba(201,164,106,.5)}
.nums div{padding:26px 0 22px;text-align:center;border-right:1.5px solid rgba(201,164,106,.3)}
.nums div:last-child{border:0}
.nums b{font-family:"Cormorant Garamond",serif;font-size:72px;color:#fff;font-weight:600;line-height:1}
.nums em{display:block;font-style:normal;font-size:24px;color:var(--gold2);margin-top:6px}
.swipe{margin-top:30px;text-align:right;font-size:30px;color:var(--gold);font-weight:700;letter-spacing:.06em}

/* steps */
.steps{display:flex;flex-direction:column;gap:16px}
.step{display:grid;grid-template-columns:150px 1fr;gap:28px;align-items:start;background:#fff;padding:20px 30px;box-shadow:0 6px 18px rgba(19,37,60,.06)}
.yr{font-family:"Cormorant Garamond",serif;font-size:62px;font-weight:600;color:var(--navy);line-height:1;border-right:3px solid var(--gold)}
.step h3{font-family:"Noto Serif TC",serif;font-size:36px;color:var(--navy);margin-bottom:6px}
.step p{font-size:28px;color:var(--ink2);line-height:1.5}
.step p b{color:var(--navy)}

/* ledger */
.ledger{background:#fff;padding:14px 36px;box-shadow:0 6px 18px rgba(19,37,60,.06)}
.row{display:flex;justify-content:space-between;align-items:center;font-size:31px;padding:11px 0;border-bottom:1.5px solid var(--line)}
.row b{font-family:"Cormorant Garamond",serif;font-size:46px;font-weight:600}
.row.neg b{color:var(--red)}
.row.sum{border:0;border-top:3px solid var(--navy);margin-top:4px;font-weight:700;color:var(--navy)}
.result{display:flex;justify-content:space-between;align-items:center;background:var(--navy);color:#fff;padding:30px 40px}
.result em{font-style:normal;font-size:36px;font-weight:700;display:block}
.result small{font-size:22px;color:var(--gold2)}
.result b{font-family:"Cormorant Garamond",serif;font-size:120px;font-weight:600;color:var(--gold);line-height:1}
.result i{font-style:normal;font-size:34px;margin-left:6px;font-family:"Noto Sans TC"}

/* vs */
.vs{display:grid;grid-template-columns:1fr 80px 1fr;align-items:center}
.vs .col{background:rgba(255,255,255,.06);border:2px solid rgba(201,164,106,.35);padding:40px 28px;text-align:center}
.vs .col.hl{border-color:var(--gold);background:rgba(201,164,106,.1)}
.vs .lab{font-size:32px;color:var(--gold2);font-weight:700}
.vs .eq{font-size:30px;margin:24px 0;line-height:1.6;opacity:.85}
.vs .tot{font-family:"Cormorant Garamond",serif;font-size:120px;font-weight:600;color:#fff;line-height:1;border-top:2px solid rgba(201,164,106,.4);padding-top:20px}
.vs .mid{text-align:center;font-size:80px;color:var(--gold);font-weight:700}

/* bars3 */
.bars3{display:grid;grid-template-columns:1fr 60px 1fr 60px 1fr;align-items:end;height:520px}
.bars3 .b{height:100%;display:flex;flex-direction:column;justify-content:flex-end;text-align:center}
.bar{background:var(--navy);display:flex;align-items:flex-start;justify-content:center;padding-top:20px}
.bar.alt{background:#7d97b3}.bar.gold{background:var(--gold)}
.bar b{font-family:"Cormorant Garamond",serif;font-size:66px;color:#fff;font-weight:600}
.bars3 em{font-style:normal;font-size:26px;color:var(--ink2);margin-top:14px;font-weight:500}
.op{font-size:70px;color:var(--gold);text-align:center;align-self:center;font-weight:700}

/* cmp2 */
.cmp2{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.cmp2 .c{background:#fff;padding:36px 30px;text-align:center;border-top:12px solid var(--red);box-shadow:0 6px 18px rgba(19,37,60,.06)}
.cmp2 .c.ok{border-top-color:var(--green)}
.cmp2 em{font-style:normal;font-size:36px;font-weight:700;color:var(--navy)}
.cmp2 .calc{font-size:26px;color:var(--ink2);margin:20px 0;line-height:1.6}
.cmp2 b{display:block;font-family:"Cormorant Garamond",serif;font-size:130px;font-weight:600;line-height:1;color:var(--red)}
.cmp2 .ok b{color:var(--green)}
.cmp2 i{font-style:normal;font-size:34px;font-family:"Noto Sans TC"}
.cmp2 small{font-size:24px;color:var(--ink2)}
.diff{display:grid;grid-template-columns:1fr 1fr;background:var(--navy);color:#fff}
.diff div{padding:30px;text-align:center}
.diff div+div{border-left:2px solid rgba(201,164,106,.4)}
.diff em{font-style:normal;font-size:26px;color:var(--gold2);display:block}
.diff b{font-family:"Noto Serif TC",serif;font-size:56px;color:var(--gold)}

/* rates */
.rates{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.rt{border:2px solid rgba(201,164,106,.4);padding:30px 10px;text-align:center}
.rt span{font-size:28px;color:var(--gold2);display:block}
.rt b{font-family:"Cormorant Garamond",serif;font-size:96px;font-weight:600;line-height:1.1}
.rt.g{background:rgba(63,125,92,.35);border-color:#6fb08a}
.rt.r{background:rgba(176,71,62,.35);border-color:#d8786e}
.cases{display:flex;flex-direction:column;gap:14px}
.cases div{display:flex;justify-content:space-between;font-size:32px;padding:20px 28px;background:rgba(255,255,255,.06)}
.cases b{color:#fff}.cases span{color:var(--gold2)}

/* reqs */
.rqs{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.rq{background:#fff;padding:34px 30px;box-shadow:0 6px 18px rgba(19,37,60,.06);position:relative;min-height:290px}
.rq .n{width:72px;height:72px;border-radius:50%;background:var(--navy);color:var(--gold);font-family:"Cormorant Garamond",serif;font-size:46px;font-weight:600;display:flex;align-items:center;justify-content:center;margin-bottom:18px}
.rq h3{font-family:"Noto Serif TC",serif;font-size:40px;color:var(--navy);margin-bottom:10px}
.rq p{font-size:28px;color:var(--ink2);line-height:1.5}

/* qa */
.qa{display:flex;flex-direction:column;gap:16px}
.qq{display:flex;gap:24px;align-items:center;background:rgba(255,255,255,.07);padding:22px 28px}
.qq b{width:60px;height:60px;border-radius:50%;background:var(--gold);color:var(--navy);font-size:38px;display:flex;align-items:center;justify-content:center;flex:none}
.qq p{font-size:34px;font-weight:500}
.law{border-left:8px solid var(--gold);padding:8px 0 8px 28px}
.law em{font-style:normal;font-size:28px;color:var(--gold);font-weight:700}
.law p{font-size:29px;line-height:1.55;margin-top:6px;opacity:.92}

/* checklist + cta */
.ck{list-style:none;display:flex;flex-direction:column;gap:16px}
.ck li{display:flex;gap:22px;align-items:center;font-size:31px;background:#fff;padding:22px 28px;box-shadow:0 6px 18px rgba(19,37,60,.06)}
.ck i{flex:none;width:40px;height:40px;border:4px solid var(--navy);border-radius:6px;position:relative}
.ck i::after{content:"";position:absolute;left:9px;top:1px;width:12px;height:22px;border:solid var(--gold);border-width:0 6px 6px 0;transform:rotate(45deg)}
.cta{display:grid;grid-template-columns:1fr 170px;gap:24px;background:var(--navy);color:#fff;padding:34px 36px;align-items:center}
.cta b{font-family:"Noto Serif TC",serif;font-size:38px;color:var(--gold2)}
.cta p{font-size:26px;line-height:1.55;margin-top:10px;opacity:.9}
.save{width:150px;height:150px;border-radius:50%;background:var(--gold);color:var(--navy);display:flex;align-items:center;justify-content:center;text-align:center;font-size:32px;font-weight:900;line-height:1.3}
'''
html = f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>繼承稅務輪播圖</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=Noto+Serif+TC:wght@700;900&family=Cormorant+Garamond:wght@600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{"".join(S)}</body></html>'''
OUT.write_text(html, encoding="utf-8")
print(len(S))
