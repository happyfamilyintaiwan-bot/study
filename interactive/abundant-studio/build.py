# -*- coding: utf-8 -*-
"""產生 豐盛工作室 中英兩頁。
python3 build.py → dist/（上架用完整 HTML）＋ preview/（artifact 預覽）
"""
import json, html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import WEEKS, DATES, AFFIRM, FAQ, T, UI, AFF, AFF_TXT
from studio_svg import svg as studio_svg

SPEC = os.environ.get("HY_SPEC", "core-v1.5/study-v0.4")   # 由 study 的 build.py 帶入
DRIVE = os.environ.get("HY_DRIVE", "")                     # Travelpayouts Drive（core §1）
ADS_CLIENT = os.environ.get("HY_ADS_CLIENT", "")
ADS_SLOT = os.environ.get("HY_ADS_SLOT", "")               # 空白＝不放廣告版位
OG = os.environ.get("HY_STUDIO_OG", "og.png")              # 換圖一律用新檔名
GA = "G-ZQZHTYTRMQ"
TOPIC = "artists-way"
SLUG = "abundant-studio"
BASE = "https://study.knittinghiyori.com"
URL = {"zh": f"{BASE}/{TOPIC}/{SLUG}/", "en": f"{BASE}/en/{TOPIC}/{SLUG}/"}
FONTS = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500"
         "&amp;family=Instrument+Serif:ital@0;1&amp;family=Noto+Sans+TC:wght@400;500;700"
         "&amp;family=Noto+Serif+TC:wght@700;900&amp;display=swap")
e = html.escape


def lum(hexc):
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def on_color(bg):
    return "#ffffff" if contrast(bg, "#ffffff") >= 4.5 else "#1b1a17"


CSS = r"""
:root{
  /* 版面：大標＋柔光插畫框（hero）→ 方正筆記卡片＋左上索引標籤；底部浮動膠囊導覽。單一淺色主題：白底黑字 */
  --paper:#ffffff; --ink:#1b1a17; --muted:#5d584f; --line:#e7e0d4; --dot:#e9e4da;
  --blue:#1f4e86; --terra:#b8492a; --mustard:#e2a83c; --teal:#2f7a72; --cream:#f7eedd; --blush:#f6dcd8;
  --wk:#1f4e86; --wk-on:#ffffff;
  --serif-lat:"Instrument Serif","Noto Serif TC",Georgia,serif;
  --display:"Noto Serif TC","Songti TC","Noto Serif",Georgia,serif;
  --body:"Noto Sans TC","PingFang TC","Helvetica Neue",Arial,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
  color-scheme:light;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{scroll-behavior:smooth;scroll-padding-top:16px}
html,body{background:var(--paper);color:var(--ink)}
body{font-family:var(--body);font-size:16px;line-height:1.75;
  background-image:radial-gradient(var(--dot) 1px,transparent 1.3px);background-size:24px 24px;
  padding-inline:16px;padding-block:0 120px}
.wrap{max-width:1120px;margin:0 auto}
a{color:var(--blue)}
:focus-visible{outline:2px solid var(--blue);outline-offset:3px}
button{font:inherit;cursor:pointer;color:inherit}

/* 廣告版位（study.md §2：每頁最多 1 個，內容最下面） */
.kh-ad{width:100%;max-width:728px;margin:150px auto 40px}
.kh-ad-label{font-size:12px;color:var(--muted);margin:0 0 4px}
.kh-ad ins[data-ad-status="unfilled"]{display:none}

/* 品牌列 */
.kh-brand-row{display:flex;justify-content:space-between;align-items:center;gap:12px;padding-block:14px}
.kh-brand{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-family:var(--display);font-weight:700;font-size:17px}
.kh-brand img{width:40px;height:40px}
.kh-brand .site{font-weight:700;color:var(--muted)}
.pill{display:inline-flex;align-items:center;gap:6px;min-height:36px;padding:6px 14px;border-radius:999px;border:1px solid var(--line);background:var(--paper);font-family:var(--mono);font-size:12px;letter-spacing:.06em;color:var(--ink);text-decoration:none}
.pill.dark{background:var(--ink);color:var(--paper);border-color:var(--ink)}

/* Hero */
.hero{text-align:center;padding-block:28px 0}
.eyebrow{margin:0 auto 22px}
h1{margin:0;font-weight:900;line-height:1;letter-spacing:.01em;text-wrap:balance}
:lang(zh-Hant-TW) h1{font-family:var(--display);font-size:clamp(56px,11vw,128px);letter-spacing:.06em}
:lang(en) h1{font-family:var(--serif-lat);font-weight:400;font-size:clamp(60px,11.5vw,148px);letter-spacing:-.01em}
.lede{font-size:clamp(16px,1.6vw,18px);max-width:34em;margin:18px auto 0}
.frame{position:relative;margin-top:30px;border-radius:28px;padding:10px;background:var(--paper);border:1px solid var(--line);box-shadow:0 30px 60px -40px rgba(60,40,20,.35)}
.frame-in{position:relative;border-radius:20px;overflow:hidden;
  background:radial-gradient(60% 70% at 78% 18%,#f7d3d6 0%,rgba(247,211,214,0) 70%),radial-gradient(55% 60% at 12% 92%,#f8e2c6 0%,rgba(248,226,198,0) 70%),#fbf5f0;
  padding:22px 16px 8px}
.studio{display:block;width:100%;height:auto;max-width:860px;margin:0 auto}
.hud{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:8px;padding:14px 8px 10px}
.hud .stat{display:inline-flex;align-items:baseline;gap:8px;min-height:40px;padding:6px 14px;border-radius:999px;background:rgba(255,255,255,.85);border:1px solid var(--line)}
.hud b{font-family:var(--serif-lat);font-weight:400;font-size:24px;line-height:1;font-variant-numeric:tabular-nums}
.hud span{font-size:12px;color:var(--muted)}
.cta{min-height:48px;padding:10px 22px;border-radius:999px;border:0;background:var(--ink);color:var(--paper);font-weight:700;font-size:15px;display:inline-flex;align-items:center;gap:8px;text-decoration:none}
.cta:hover{background:var(--blue)}
.cta .arr{font-family:var(--mono)}
.week7{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;margin-top:20px;padding-top:16px;border-top:1px solid var(--line)}
.week7 .d{display:flex;flex-direction:column;align-items:center;gap:6px;font-family:var(--mono);font-size:11px;color:var(--muted)}
.week7 .d i{width:28px;height:28px;border-radius:50%;border:1.5px dashed #cfc6b6;display:block}
.week7 .d.on i{border:0;background:var(--c,#1f4e86)}
.week7 .d.today span{color:var(--ink);font-weight:500}
.week7 .d.today i{box-shadow:0 0 0 3px #f6dcd8}
.finale{margin:6px auto 14px;max-width:34em;font-family:var(--display);font-weight:700;font-size:18px}
.credit{font-size:12.5px;color:var(--muted);max-width:56em;margin:16px auto 0}

/* 插畫狀態 */
.it{opacity:.1;filter:grayscale(1);transition:opacity .9s ease,filter .9s ease}
.it.now{opacity:.32;animation:hint 2.8s ease-in-out infinite}
.it.on{opacity:1;filter:none;animation:none}
.it.pop{animation:pop .9s cubic-bezier(.2,1.4,.4,1) both;transform-box:fill-box;transform-origin:50% 100%}
@keyframes hint{50%{opacity:.5}}
@keyframes pop{0%{transform:translateY(-18px) scale(.9);opacity:0}100%{transform:none;opacity:1}}
.strip{opacity:0;transition:opacity .8s}
.strip.on{opacity:1}
.lampglow{animation:breathe 5s ease-in-out infinite}
@keyframes breathe{50%{opacity:.7}}

/* 區塊與卡片 */
.sec{margin-top:72px;scroll-margin-top:16px}
.sec-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 16px;margin-bottom:20px}
.sec-no{font-family:var(--mono);font-size:12px;letter-spacing:.08em;color:var(--muted)}
h2{font-family:var(--display);font-weight:900;font-size:clamp(28px,4vw,40px);line-height:1.2;margin:0;text-wrap:balance}
  :lang(en) h2{font-family:var(--serif-lat);font-weight:400;font-size:clamp(36px,5vw,52px);letter-spacing:-.01em}
h3{font-family:var(--display);font-weight:700;font-size:19px;line-height:1.35;margin:0 0 6px}
.note{font-size:14.5px;color:var(--muted);margin:0 0 14px}
.grid{display:grid;gap:20px}
@media (min-width:860px){.g2{grid-template-columns:1.35fr 1fr}.g2b{grid-template-columns:1fr 1fr}}
.card{position:relative;background:var(--paper);border:1px solid var(--ink);padding:30px 22px 22px;min-width:0}
.tab{position:absolute;top:-1px;left:-1px;background:var(--ink);color:var(--paper);font-family:var(--mono);font-size:11px;letter-spacing:.08em;padding:3px 10px}

/* 晨間隨筆 */
.pad{position:relative;border:1px solid var(--line);background:#fff;
  background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 31px,#e8ecf2 31px,#e8ecf2 32px);background-position:0 8px}
.pad::before{content:"";position:absolute;top:0;bottom:0;left:40px;width:1px;background:#e07a6a}
.pad textarea{display:block;width:100%;min-height:256px;border:0;background:transparent;resize:vertical;font-family:var(--body);font-size:17px;line-height:32px;padding:8px 14px 8px 54px;color:var(--ink)}
.pad textarea:focus{outline:none}
.pad:focus-within{border-color:var(--blue)}
.gauge{display:flex;align-items:center;gap:12px;margin:14px 0 4px}
.gauge-bar{position:relative;flex:1;height:10px;border-radius:99px;background:#eef1f6;overflow:hidden}
.gauge-fill{position:absolute;inset:0 auto 0 0;width:0;border-radius:99px;background:linear-gradient(90deg,var(--blue),var(--teal),var(--mustard));transition:width .3s}
.gauge-bar i{position:absolute;top:0;bottom:0;width:2px;background:#fff}
.gauge-num{font-family:var(--mono);font-size:13px;font-variant-numeric:tabular-nums;white-space:nowrap}
.btns{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.btn{min-height:44px;padding:8px 18px;border-radius:999px;border:1px solid var(--ink);background:var(--paper);font-size:15px}
.btn.primary{background:var(--ink);color:var(--paper)}
.btn.big{min-height:52px;padding:10px 24px;font-weight:700}
.btn:disabled{opacity:.35;cursor:not-allowed}
.btn:not(:disabled):hover{background:var(--blue);border-color:var(--blue);color:#fff}
.small{font-size:13px;color:var(--muted);margin:12px 0 0}
.or{display:flex;align-items:center;gap:10px;font-family:var(--mono);font-size:11px;color:var(--muted);margin:18px 0 10px}
.or::before,.or::after{content:"";flex:1;height:1px;background:var(--line)}
.done-box{border-radius:14px;background:#eef4ec;border:1px solid #cfe0c8;padding:14px 16px;margin-top:4px;font-weight:500}

/* 靈感芽 */
.sprout-card{display:flex;flex-direction:column;align-items:center;text-align:center;background:linear-gradient(180deg,#fff 0%,#fbf3ea 100%)}
.sprout{width:170px;height:190px}
.leaf{transform-box:fill-box;transform-origin:0% 100%;transform:scale(0);transition:transform .7s cubic-bezier(.2,1.4,.4,1)}
.leaf.r{transform-origin:100% 100%}
.leaf.on{transform:scale(1)}
.bloom{transform-box:fill-box;transform-origin:50% 50%;transform:scale(0);transition:transform .8s cubic-bezier(.2,1.4,.4,1)}
.bloom.on{transform:scale(1)}
.affirm{font-family:var(--display);font-weight:700;font-size:22px;line-height:1.45;margin:8px 0 4px;text-wrap:balance}
:lang(en) .affirm{font-family:var(--serif-lat);font-weight:400;font-size:28px;font-style:italic}
.leafcount{font-family:var(--mono);font-size:12px;color:var(--muted)}

/* 本週 */
.week-band{position:relative;border:1px solid var(--ink);background:var(--wk);color:var(--wk-on);padding:28px 24px 24px;display:grid;gap:8px 28px;overflow:hidden}
@media (min-width:860px){.week-band{grid-template-columns:auto 1fr;align-items:end}}
.week-band .big{font-family:var(--serif-lat);font-size:clamp(72px,12vw,140px);line-height:.85;letter-spacing:-.02em}
.week-band .big small{font-size:.32em;letter-spacing:0;margin-right:.15em}
.week-band h3{font-size:clamp(22px,3vw,30px);font-weight:900;margin:0;color:inherit}
.week-band .theme{font-family:var(--mono);font-size:12px;letter-spacing:.08em;opacity:.85}
.week-band p{margin:6px 0 0;max-width:40em;color:inherit}
.practices{display:grid;gap:20px;margin-top:20px}
@media (min-width:700px){.practices{grid-template-columns:1fr 1fr}}
.pc-top{display:flex;align-items:center;gap:10px;margin-bottom:6px}
.pc-ic{width:34px;height:34px;flex:none}
.check-ok{display:inline-flex;align-items:center;gap:6px;font-size:14px;font-weight:700;color:#2f6a2a}
.datecard{position:relative;border-radius:16px;padding:18px 18px 16px;min-height:96px;margin:8px 0 2px;display:flex;align-items:flex-end;
  background:linear-gradient(135deg,#fde7c9 0%,#f8d2d0 55%,#dfe6f6 100%);font-family:var(--display);font-weight:700;font-size:19px;line-height:1.45}
:lang(en) .datecard{font-family:var(--serif-lat);font-weight:400;font-size:24px}
.datecard .lbl{position:absolute;top:12px;left:16px;font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:.08em;color:var(--muted)}
.datecard.blank{background:repeating-linear-gradient(135deg,#faf7f2 0 10px,#f4efe6 10px 20px);color:var(--muted);font-weight:500}
.tasks{list-style:none;padding:0;margin:0;display:grid;gap:8px}
.tasks label{display:flex;gap:10px;align-items:flex-start;cursor:pointer;padding:10px 12px;border-radius:12px;border:1px solid var(--line);font-size:15px;line-height:1.6}
.tasks input{width:20px;height:20px;margin-top:3px;flex:none;accent-color:var(--blue)}
.tasks label:has(input:checked){background:#f2f6fb;border-color:#b9cbe3}
.tasks label:has(input:checked) span{color:var(--muted);text-decoration:line-through;text-decoration-color:#9fb4d3}
.bring{display:flex;flex-wrap:wrap;align-items:center;gap:12px 18px;margin-top:22px;padding:18px 20px;border:1px dashed var(--ink);border-radius:18px;background:#fffdf8}
.bring p{margin:0;font-size:14.5px;color:var(--muted);flex:1;min-width:14em}

/* 12 件 */
.items{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.items li{position:relative;border:1px solid var(--line);border-radius:16px;padding:16px 16px 14px;background:var(--paper);min-width:0;display:grid;grid-template-columns:auto 1fr;gap:4px 14px;align-items:start}
.items .sw{grid-row:span 3;width:46px;height:46px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-family:var(--serif-lat);font-size:22px}
.items strong{font-family:var(--display);font-size:17px;line-height:1.35}
.items .meta{display:flex;justify-content:space-between;gap:8px;font-family:var(--mono);font-size:11px;color:var(--muted);letter-spacing:.04em}
.items .chip{border-radius:99px;padding:0 8px;border:1px solid var(--line);white-space:nowrap}
.items p{margin:0;font-size:13.5px;color:var(--muted);grid-column:2}
.items li.on{border-color:var(--ink)}
.items li.on .chip{background:var(--ink);color:#fff;border-color:var(--ink)}
.items li.now{border-color:var(--ink);box-shadow:0 0 0 3px #f6dcd8}
.items li.now .chip{background:#f6dcd8;border-color:#e9b9b2;color:var(--ink)}
.items li.later .sw{filter:grayscale(.85);opacity:.55}

/* 書架（聯盟） */
.aff-inline{font-weight:500}
.shelf{display:grid;gap:16px}
@media (min-width:760px){.shelf{grid-template-columns:1fr 1fr}}
.book{display:grid;grid-template-columns:96px 1fr;gap:18px;padding:18px;border:1px solid var(--ink);background:var(--paper);color:var(--ink);text-decoration:none;min-width:0;transition:transform .25s ease,box-shadow .25s ease}
.book:hover{transform:translateY(-3px);box-shadow:0 18px 30px -22px rgba(40,30,20,.45)}
.spine{display:flex;align-items:center;flex-direction:column;justify-content:center;height:136px;overflow:hidden;border-radius:4px 10px 10px 4px;box-shadow:inset 6px 0 0 rgba(0,0,0,.18);padding:10px 8px}
.spine span{color:#fff;font-family:var(--display);font-weight:700;font-size:15px;line-height:1.35;text-align:center;letter-spacing:.08em;padding-top:4px;border-top:2px solid rgba(255,255,255,.6)}
.book-txt{display:flex;flex-direction:column;gap:4px;min-width:0}
.book strong{font-family:var(--display);font-size:18px;line-height:1.4}
.book .by{font-size:12.5px;color:var(--muted)}
.book .bn{font-size:14.5px;margin-top:4px}
.book .go{margin-top:auto;padding-top:8px;font-family:var(--mono);font-size:12px;color:var(--blue)}
.disclosure{margin-top:14px}
/* 說明、FAQ */
.howto{padding-left:1.3em;margin:0}
.howto li{margin-bottom:8px}
.care{font-size:14px;border-radius:12px;background:#f6f1e8;padding:12px 14px;margin:16px 0 0}
details{border-top:1px solid var(--line);padding:12px 0}
details:last-of-type{border-bottom:1px solid var(--line)}
summary{cursor:pointer;font-weight:700;list-style:none;display:flex;justify-content:space-between;gap:12px;min-height:28px}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";font-family:var(--mono);font-weight:400;font-size:18px;line-height:1.5}
details[open] summary::after{content:"−"}
details p{margin:8px 0 0;font-size:15px}
.confirm{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:12px;padding:12px 14px;border-radius:14px;border:1px solid var(--terra)}

/* 浮動膠囊導覽 */
.dock{position:fixed;left:50%;bottom:calc(14px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);z-index:6;display:flex;gap:4px;padding:5px;border-radius:999px;background:rgba(255,255,255,.88);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border:1px solid var(--line);box-shadow:0 10px 30px -12px rgba(0,0,0,.25);max-width:calc(100vw - 24px)}
.dock a{display:inline-flex;align-items:center;min-height:38px;padding:4px 14px;border-radius:999px;text-decoration:none;color:var(--ink);font-size:13.5px;white-space:nowrap}
.dock a:hover{background:#f3eee6}
.dock .wk{background:var(--ink);color:#fff;font-family:var(--mono);font-size:12px}
.toast{position:fixed;left:50%;bottom:calc(76px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);background:var(--ink);color:#fff;padding:10px 16px;border-radius:999px;font-size:14px;z-index:7;max-width:calc(100vw - 32px)}
.kh-legal{font-size:12px;color:var(--muted);margin-top:56px;padding-top:14px;border-top:1px solid var(--line)}

@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}html{scroll-behavior:auto}}
@media (max-width:560px){.hud{display:grid;grid-template-columns:1fr 1fr}.hud .stat{justify-content:center}.hud .cta{grid-column:1/-1;justify-content:center}.kh-brand .site{display:none}.frame{padding:6px;border-radius:22px}.frame-in{padding:14px 6px 4px;border-radius:16px}.hud b{font-size:20px}.dock a{padding:4px 10px;font-size:12.5px}.card{padding:28px 16px 18px}}
"""

PRACTICE_ICONS = {
    "date": '<svg class="pc-ic" viewBox="0 0 34 34" aria-hidden="true"><circle cx="17" cy="17" r="16" fill="#f6dcd8"/><path d="M10 22 l7-12 l7 12z" fill="#c4542a"/><circle cx="23" cy="11" r="3" fill="#e2a83c"/></svg>',
    "walk": '<svg class="pc-ic" viewBox="0 0 34 34" aria-hidden="true"><circle cx="17" cy="17" r="16" fill="#e2efe0"/><path d="M8 25 q9 -10 18 -2" stroke="#4f7d3a" stroke-width="3" fill="none" stroke-linecap="round"/><circle cx="12" cy="13" r="3" fill="#2f7a72"/><circle cx="21" cy="10" r="2" fill="#2f7a72"/></svg>',
    "read": '<svg class="pc-ic" viewBox="0 0 34 34" aria-hidden="true"><circle cx="17" cy="17" r="16" fill="#e2eaf5"/><path d="M8 11 q5 -2 9 1 v12 q-4 -3 -9 -1z" fill="#1f4e86"/><path d="M26 11 q-5 -2 -9 1 v12 q4 -3 9 -1z" fill="#2e6f9e"/></svg>',
    "tasks": '<svg class="pc-ic" viewBox="0 0 34 34" aria-hidden="true"><circle cx="17" cy="17" r="16" fill="#fbeccc"/><path d="M10 17 l5 5 l9 -10" stroke="#b07a12" stroke-width="3.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}

SPROUT = """<svg class="sprout" viewBox="0 0 170 190" aria-hidden="true">
<ellipse cx="85" cy="182" rx="50" ry="6" fill="#1b1a17" opacity=".08"/>
<path d="M52 128 h66 l-8 52 h-50z" fill="#c4542a"/><rect x="46" y="120" width="78" height="14" rx="4" fill="#d76a40"/>
<path d="M85 122 C84 96 86 70 85 40" stroke="#4f7d3a" stroke-width="4" fill="none" stroke-linecap="round"/>
<path class="leaf r" data-i="1" d="M84 112 C66 112 52 104 48 92 C62 90 78 96 84 112Z" fill="#6aa04e"/>
<path class="leaf" data-i="2" d="M86 102 C102 100 116 90 120 78 C106 78 90 86 86 102Z" fill="#5b8f43"/>
<path class="leaf r" data-i="3" d="M84 90 C68 88 56 78 54 66 C68 66 82 74 84 90Z" fill="#4f7d3a"/>
<path class="leaf" data-i="4" d="M86 78 C100 76 112 66 114 54 C102 54 88 62 86 78Z" fill="#6aa04e"/>
<path class="leaf r" data-i="5" d="M84 66 C72 64 62 56 60 46 C72 46 82 52 84 66Z" fill="#5b8f43"/>
<path class="leaf" data-i="6" d="M86 56 C96 54 106 46 108 38 C98 38 88 44 86 56Z" fill="#4f7d3a"/>
<path class="leaf r" data-i="7" d="M85 44 C78 40 74 32 76 24 C84 28 88 36 85 44Z" fill="#6aa04e"/>
<g class="bloom"><circle cx="85" cy="30" r="9" fill="#e2a83c"/><circle cx="85" cy="18" r="8" fill="#f2b8b0"/><circle cx="97" cy="30" r="8" fill="#f2b8b0"/><circle cx="73" cy="30" r="8" fill="#f2b8b0"/><circle cx="85" cy="42" r="8" fill="#f2b8b0"/><circle cx="85" cy="30" r="6" fill="#e2a83c"/></g>
</svg>"""


def page(lang, preview=False):
    t, ui = T[lang], UI[lang]
    label = {"zh": "豐盛工作室剖面插畫：12 件會陸續搬進來的東西", "en": "Cross-section of the studio with 12 pieces that will arrive over the weeks"}[lang]
    target = 750
    w0 = WEEKS[0]

    items = []
    for i, w in enumerate(WEEKS, 1):
        items.append(
            f'<li data-w="{i}"><span class="sw" style="background:{w["color"]};color:{on_color(w["color"])}">{i}</span>'
            f'<div class="meta"><span>WEEK {i:02d}・{e(w["theme"][lang])}</span><span class="chip">{e(ui["later"])}</span></div>'
            f'<strong>{e(w["item"][lang])}</strong><p>{e(w["intro"][lang])}</p></li>')

    tasks0 = "".join(
        f'<li><label><input type="checkbox" id="task{j}" data-t="{j}" disabled><span class="task-text">{e(x)}</span></label></li>'
        for j, x in enumerate(w0["tasks"][lang]))
    faq_html = "".join(f'<details data-q="q{k}"><summary>{e(q)}</summary><p>{e(a)}</p></details>'
                       for k, (q, a) in enumerate(FAQ[lang], 1))
    howto = "".join(f"<li>{e(x)}</li>" for x in t["about"])
    nav = t["nav"]

    data = {"lang": lang, "pageLang": t["page_lang"], "target": target, "url": URL[lang],
            "weeks": [{"item": w["item"][lang], "theme": w["theme"][lang], "intro": w["intro"][lang],
                       "tasks": w["tasks"][lang], "color": w["color"], "on": on_color(w["color"])} for w in WEEKS],
            "dates": DATES[lang], "affirm": AFFIRM[lang], "ui": ui,
            "t": {k: t[k] for k in ("btn_draw", "btn_redraw", "cta_start", "cta_continue", "p_read_d")}}

    jsonld = [
        {"@context": "https://schema.org", "@type": "LearningResource", "name": t["h1"], "description": t["desc"],
         "url": URL[lang], "inLanguage": t["lang"], "isAccessibleForFree": True,
         "learningResourceType": "interactive practice", "timeRequired": "P12W",
         "about": {"@type": "Book", "name": "The Artist's Way", "author": {"@type": "Person", "name": "Julia Cameron"}},
         "publisher": {"@type": "Organization", "name": "編織日和 Knitting Hiyori", "url": "https://knittinghiyori.com/"}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[lang]]},
    ]

    brand_href = "https://study.knittinghiyori.com/" if preview else ("/" if lang == "zh" else "/en/")
    lang_href = t["lang_href_rel"]
    if preview:
        lang_href = "en/index.html" if lang == "zh" else "../"
    rel = 'rel="sponsored nofollow noopener" target="_blank" data-google-vignette="false"'
    read_aff = ""
    shelf = ""
    if lang == "zh":
        a = AFF["artists_way"]
        read_aff = (f'<p class="small"><a class="aff-inline" href="{a["url"]}" {rel} data-cta="read_card" '
                    f'data-cta-type="shopee" data-option="artists_way">{e(AFF_TXT["read_link"])} ↗</a></p>')
        cards = ""
        for key, b in AFF.items():
            cards += (f'<a class="book" href="{b["url"]}" {rel} data-cta="book_shelf" data-cta-type="shopee" data-option="{key}">'
                      f'<span class="spine" style="background:{b["color"]}"><span>{e(b["title"].split("：")[0])}</span></span>'
                      f'<span class="book-txt"><strong>{e(b["title"])}</strong><span class="by">{e(b["author"])}・{e(b["en"])}</span>'
                      f'<span class="bn">{e(b["note"])}</span><span class="go">{e(AFF_TXT["go"])} ↗</span></span></a>')
        shelf = (f'<section class="sec" id="books"><div class="sec-head"><span class="sec-no">05 / 書架</span><h2>{e(AFF_TXT["shelf_h"])}</h2></div>'
                 f'<p class="note">{e(AFF_TXT["shelf_p"])}</p><div class="shelf">{cards}</div>'
                 f'<p class="small disclosure">{e(AFF_TXT["disclosure"])}</p></section>')
    logo = '<img src="/icons/logo-knitting-120.webp" srcset="/icons/logo-knitting-240.webp 2x" width="40" height="40" alt="" onerror="this.hidden=true">'
    ok_icon = '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="8" fill="#2f6a2a"/><path d="M4.5 8.2l2.2 2.2 4.6-4.8" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>'

    drive = ('<script data-cfasync="false" data-cmp-ab="2">(function(){var s=document.createElement("script");s.async=1;'
             's.setAttribute("data-cmp-ab","2");s.src="' + DRIVE + '";document.head.appendChild(s)})();</script>\n') if DRIVE else ""
    head_prod = drive + f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(t["title_tag"])}</title>
<meta name="description" content="{e(t["desc"])}">
<link rel="canonical" href="{URL[lang]}">
<link rel="alternate" hreflang="zh-Hant-TW" href="{URL["zh"]}">
<link rel="alternate" hreflang="en" href="{URL["en"]}">
<link rel="alternate" hreflang="x-default" href="{URL["zh"]}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(t["h1"])}">
<meta property="og:description" content="{e(t["desc"])}">
<meta property="og:url" content="{URL[lang]}">
<meta property="og:image" content="{BASE}/{TOPIC}/{SLUG}/{OG}">
<meta property="og:image:alt" content="{"編織日和・學習筆記：豐盛工作室，The Artist's Way 12 週練習" if lang == "zh" else "Knitting Hiyori Study Notes: The Abundant Studio, a 12-week The Artist's Way practice"}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/{TOPIC}/{SLUG}/{OG}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{"zh_TW" if lang == "zh" else "en_US"}">
<link rel="icon" href="/icons/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('set', {{content_group: 'study', topic: '{TOPIC}', page_lang: '{t["page_lang"]}', page_title: '{t["page_title"]}'}});
gtag('config', '{GA}', /hy_debug=1/.test(location.search) ? {{cookie_domain: '.knittinghiyori.com', debug_mode: true}} : {{cookie_domain: '.knittinghiyori.com'}});
</script>
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
<meta name="spec-version" content="{SPEC}">"""

    ad = (f'<div class="kh-ad"><p class="kh-ad-label">{"廣告" if lang == "zh" else "Advertisement"}</p>'
          f'<ins class="adsbygoogle" style="display:block" data-ad-client="{ADS_CLIENT}" data-ad-slot="{ADS_SLOT}" '
          'data-ad-format="auto" data-full-width-responsive="true"></ins>'
          '<script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>') if ADS_SLOT and not preview else ""

    head_preview = f"""<title>{"豐盛工作室" if lang == "zh" else "The Abundant Studio"}</title>
<link rel="stylesheet" href="{FONTS}">
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}</script>"""

    def practice(key, title, desc, body):
        return f'<div class="card"><div class="pc-top">{PRACTICE_ICONS[key]}<h3>{e(title)}</h3></div><p class="note">{e(desc)}</p>{body}</div>'

    date_body = f"""<div class="datecard blank" id="datecard"><span class="lbl">ARTIST DATE</span><span id="datetext">{e(DATES[lang][6])}</span></div>
      <div class="btns"><button class="btn" id="btn-draw" type="button" disabled>{e(t["btn_draw"])}</button><button class="btn primary" id="btn-date" type="button" disabled>{e(t["btn_date_done"])}</button></div>
      <p class="check-ok" id="date-ok" hidden>{ok_icon}<span>{e(ui["date_ok"])}</span></p>"""
    walk_body = f"""<div class="btns"><button class="btn primary" id="btn-walk" type="button" disabled>{e(t["btn_walk"])}</button></div><p class="check-ok" id="walk-ok" hidden>{ok_icon}<span>{e(ui["walk_ok"])}</span></p>"""
    read_body = f"""<div class="btns"><button class="btn primary" id="btn-read" type="button" disabled>{e(t["btn_read"])}</button></div><p class="check-ok" id="read-ok" hidden>{ok_icon}<span>{e(ui["read_ok"])}</span></p>{read_aff}"""

    body = f"""<div class="wrap">
<header class="kh-brand-row">
  <a class="kh-brand" href="{brand_href}" data-cta="brand_hub" data-cta-type="study" data-google-vignette="false">{logo}<span>編織日和<span class="site">・{e(t["brand_site"])}</span></span></a>
  <a class="pill" id="langlink" href="{lang_href}" hreflang="{"en" if lang == "zh" else "zh-Hant-TW"}" data-google-vignette="false">{e(t["lang_link"])}</a>
</header>

<section class="hero">
  <p class="pill dark eyebrow">{e(t["eyebrow"])}</p>
  <h1>{e(t["h1"])}</h1>
  <p class="lede">{e(t["lede"])}</p>
  <div class="frame"><div class="frame-in">
    {studio_svg(label)}
    <p class="finale" id="finale" hidden></p>
    <div class="hud">
      <span class="stat"><b id="st-week">0/12</b><span>{e(t["stat_week"])}</span></span>
      <span class="stat"><b id="st-items">0</b><span>{e(t["stat_items"])}</span></span>
      <span class="stat"><b id="st-streak">0</b><span>{e(t["stat_streak"])}</span></span>
      <span class="stat"><b id="st-pages">0</b><span>{e(t["stat_pages"])}</span></span>
      <a class="cta" id="hero-cta" href="#today">{e(t["cta_start"])} <span class="arr">↓</span></a>
    </div>
  </div></div>
  <p class="credit">{e(t["credit"])}</p>
</section>

<section class="sec" id="today">
  <div class="sec-head"><span class="sec-no">01 / {e(t["today_no"])}</span><h2>{e(t["today_h"])}</h2></div>
  <div class="grid g2">
    <div class="card">
      <span class="tab">MORNING PAGES</span>
      <p class="note">{e(t["today_p"])}</p>
      <div id="start-box">
        <button class="btn primary big" id="btn-start" type="button">{e(t["cta_start"])}</button>
        <p class="small">{e(t["start_note"])}</p>
      </div>
      <div id="write-box" hidden>
        <button class="btn primary big" id="btn-paper" type="button">{e(t["btn_paper"])}</button>
        <div class="or" aria-hidden="true">OR</div>
        <div class="pad"><textarea id="pages" aria-label="{e(t["today_h"])}" placeholder="{e(t["ph"])}" spellcheck="false" autocomplete="off"></textarea></div>
        <div class="gauge"><div class="gauge-bar"><span class="gauge-fill" id="gauge"></span><i style="left:33.3%"></i><i style="left:66.6%"></i></div><span class="gauge-num"><span id="count">0</span> / {target} {e(t["count_unit"])}</span></div>
        <div class="btns">
          <button class="btn primary" id="btn-done" type="button" disabled>{e(t["btn_done"])}</button>
          <button class="btn" id="btn-short" type="button" disabled>{e(t["btn_short"])}</button>
        </div>
        <p class="small">{e(t["privacy"])}</p>
      </div>
      <p class="done-box" id="done-box" hidden></p>
      <div class="week7" id="week7" aria-label="7"></div>
    </div>
    <div class="card sprout-card" aria-live="polite">
      <span class="tab">{e(t["sprout"]).upper() if lang == "en" else e(t["sprout"])}</span>
      {SPROUT}
      <p class="affirm" id="affirm">{e(AFFIRM[lang][0])}</p>
      <p class="leafcount" id="leafcount">{e(ui["leaves"].replace("{n}", "0"))}</p>
      <p class="small">{e(t["sprout_p"])}</p>
    </div>
  </div>
</section>

<section class="sec" id="week">
  <div class="sec-head"><span class="sec-no">02 / {e(t["week_no"])}</span><h2 id="wk-h2">{e(w0["theme"][lang])}</h2></div>
  <div class="week-band" id="week-band">
    <div class="big"><small>WEEK</small><span id="wk-num">01</span></div>
    <div><p class="theme" id="wk-theme" hidden></p><h3 id="wk-item">{e(w0["item"][lang])}</h3><p id="wk-intro">{e(w0["intro"][lang])}</p></div>
  </div>
  <div class="practices">
    {practice("date", t["p_date"], t["p_date_d"], date_body)}
    {practice("walk", t["p_walk"], t["p_walk_d"], walk_body)}
    {practice("read", t["p_read"], t["p_read_d"].replace("{n}", "1"), read_body).replace('<p class="note">', '<p class="note" id="read-d">', 1)}
    {practice("tasks", t["p_tasks"], t["p_tasks_d"], f'<ul class="tasks" id="tasks">{tasks0}</ul>')}
  </div>
  <div class="bring">
    <button class="btn primary big" id="btn-bring" type="button" disabled></button>
    <p id="wait"></p>
  </div>
</section>

<section class="sec" id="pieces">
  <div class="sec-head"><span class="sec-no">03 / {e(t["map_no"])}</span><h2>{e(t["map_h"])}</h2></div>
  <p class="note">{e(t["map_p"])}</p>
  <ol class="items" id="items">{"".join(items)}</ol>
</section>

<section class="sec" id="guide">
  <div class="sec-head"><span class="sec-no">04 / {e(t["about_no"])}</span><h2>{e(t["about_h"])}</h2></div>
  <div class="grid g2b">
    <div class="card">
      <span class="tab">HOW TO PLAY</span>
      <ol class="howto">{howto}</ol>
      <p class="care">{e(t["care"])}</p>
      <h3 style="margin-top:22px">{e(t["invite_h"])}</h3>
      <p class="note">{e(t["invite_p"])}</p>
      <div class="btns"><button class="btn primary" id="btn-share" type="button">{e(t["btn_share"])}</button><button class="btn" id="btn-reset" type="button">{e(t["btn_reset"])}</button></div>
      <div class="confirm" id="confirm" hidden><span>{e(t["reset_q"])}</span><button class="btn primary" id="reset-yes" type="button">{e(t["reset_yes"])}</button><button class="btn" id="reset-no" type="button">{e(t["reset_no"])}</button></div>
    </div>
    <div class="card">
      <span class="tab">FAQ</span>
      <h3>{e(t["faq_h"])}</h3>
      {faq_html}
    </div>
  </div>
</section>

{shelf}

{ad}
<footer class="kh-legal">{e(t["legal"])}<a href="https://knittinghiyori.com/privacy-policy/" data-google-vignette="false">{e(t["privacy_link"])}</a></footer>
</div>
<nav class="dock" aria-label="{e(t["h1"])}"><a class="wk" href="#week" id="dock-wk">W01</a><a href="#today">{e(nav[0])}</a><a href="#week">{e(nav[1])}</a><a href="#pieces">{e(nav[2])}</a><a href="#guide">{e(nav[3])}</a></nav>
<div class="toast" id="toast" role="status" hidden></div>
<script>window.HY_STUDIO = {json.dumps(data, ensure_ascii=False)};</script>
<script>{JS}</script>"""

    css = f"<style>{CSS}</style>"
    if preview:
        if lang == "zh":
            return head_preview + "\n" + css + '\n<div lang="zh-Hant-TW">' + body + "</div>"
        return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">{head_preview}{css}</head><body>{body}</body></html>'
    return f'<!doctype html>\n<html lang="{t["lang"]}">\n<head>\n{head_prod}\n{css}\n</head>\n<body>\n{body}\n</body>\n</html>\n'


JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "studio.js"), encoding="utf-8").read()

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    out = {
        f"dist/{TOPIC}/{SLUG}/index.html": page("zh"),
        f"dist/en/{TOPIC}/{SLUG}/index.html": page("en"),
        "preview/index.html": page("zh", True),
        "preview/en/index.html": page("en", True),
    }
    for p, s in out.items():
        fp = os.path.join(root, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(s)
    assert "&" not in JS, "JS 含和號"
    for p in list(out)[:2]:
        s = out[p]
        for m in re.findall(r"<script(?![^>]*ld\+json)[^>]*>(.*?)</script>", s, re.S):
            assert "&" not in m, p + " script 含和號"
        assert SPEC in s
    # 對比檢查（文字色 vs 底色）
    pairs = [("#5d584f", "#ffffff"), ("#1b1a17", "#fbf5f0"), ("#5d584f", "#fbf5f0"), ("#1f4e86", "#ffffff"), ("#2f6a2a", "#ffffff"), ("#5d584f", "#f6f1e8")]
    for w in WEEKS:
        pairs.append((on_color(w["color"]), w["color"]))
    bad = [(a, b, round(contrast(a, b), 2)) for a, b in pairs if contrast(a, b) < 4.5]
    print("contrast fails:", bad)
    print("ok")
