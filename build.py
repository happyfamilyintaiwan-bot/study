#!/usr/bin/env python3
"""產生 study.knittinghiyori.com 的全部頁面，產生完順便做上線前檢查。
用法：
  1. 在 notes/<主題>/ 裡新增或修改 .md 筆記（格式看 notes/_範例筆記.md）
  2. 新主題先加到 topics.json
  3. python3 build.py   → 出現「0 頁有問題」才可以 push
不需要安裝任何套件（Markdown 轉換是本檔自己寫的簡易版）。
"""
import datetime, html, json, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).parent
SITE = 'https://study.knittinghiyori.com'
BLOG = 'https://knittinghiyori.com/'
PRIVACY = 'https://knittinghiyori.com/privacy-policy/'
GA_ID = 'G-ZQZHTYTRMQ'                  # GA4 評估 ID（全站共用，core §1）
ADS_CLIENT = 'ca-pub-2022028565680247'  # AdSense 發布商 ID（全站共用）
ADS_SLOT = ''   # TODO：study 專屬 AdSense 單元，到 AdSense 後台建立後填入；空白＝不放廣告
DRIVE = ''      # TODO：study 專屬 Travelpayouts Drive 網址；空白＝不載入
SPEC = 'core-v1.3/study-v0.2'
SITE_NAME = '編織日和 · 學習筆記'
VER = datetime.date.today().strftime('%Y%m%d')
YEAR = datetime.date.today().year
KINDS = ['公開課', '自學', '上過的課']
KIND_EN = {'公開課': 'Open Course', '自學': 'Self-Study', '上過的課': 'Coursework', '想學清單': 'Wishlist'}
KIND_NOTE = {'公開課': '名校免費公開的課，<br>跟著課程進度學。', '自學': '自己找資源，<br>自己排進度。',
             '上過的課': '真的報名上過的課，<br>整理重點與心得。', '想學清單': '之後想學，<br>先記下來。'}
STATUSES = ['進行中', '已完成', '想學']
COLORS = ['sora', 'peach', 'lavender', 'sakura', 'matcha', 'lemon']
ARROW = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h9m-3.5-4L12 8l-3.5 4" '
         'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
SLUG = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
E = lambda s: html.escape(str(s), quote=True)
OUT_DIRS = []   # build 產生的資料夾，重建前先清掉


# ── 簡易 Markdown → HTML ─────────────────────────────────────────
def inline(t):
    t = E(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)', r'<img src="\2" alt="\1" loading="lazy">', t)
    def link(m):
        url = m.group(2)
        ext = url.startswith('http') and not url.startswith(SITE)
        attr = ' target="_blank" rel="noopener"' if ext else ''
        return f'<a href="{url}"{attr}>{m.group(1)}</a>'
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![*\w])\*([^*\s][^*]*)\*(?!\w)', r'<em>\1</em>', t)
    return t


def md(text):
    lines, out, i = text.split('\n'), [], 0
    para = []
    def flush():
        if para:
            out.append('<p>' + '<br>'.join(inline(x) for x in para) + '</p>')
            para.clear()
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith('```'):
            flush(); lang = s[3:].strip(); buf = []; i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                buf.append(lines[i]); i += 1
            cls = f' class="lang-{E(lang)}"' if lang else ''
            out.append(f'<pre><code{cls}>' + E('\n'.join(buf)) + '</code></pre>')
        elif not s:
            flush()
        elif m := re.match(r'(#{2,4})\s+(.*)', s):
            flush(); n = len(m.group(1))
            out.append(f'<h{n}>{inline(m.group(2))}</h{n}>')
        elif s.startswith('>'):
            flush(); buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip()[1:].strip()); i += 1
            out.append('<blockquote>' + md('\n'.join(buf)) + '</blockquote>'); continue
        elif re.match(r'([-*]|\d+\.)\s+', s):
            flush(); ordered = bool(re.match(r'\d+\.', s)); items = []
            while i < len(lines) and re.match(r'\s*([-*]|\d+\.)\s+', lines[i]):
                item = re.sub(r'^\s*([-*]|\d+\.)\s+', '', lines[i])
                box = re.match(r'\[( |x)\]\s+(.*)', item)
                if box:
                    item = ('☑ ' if box.group(1) == 'x' else '☐ ') + box.group(2)
                items.append('<li>' + inline(item) + '</li>'); i += 1
            tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag}>' + ''.join(items) + f'</{tag}>'); continue
        elif s.startswith('|') and i + 1 < len(lines) and re.match(r'\s*\|[\s:|-]+\|\s*$', lines[i + 1]):
            flush(); cells = lambda r: [c.strip() for c in r.strip().strip('|').split('|')]
            head = cells(s); i += 2; rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append(cells(lines[i])); i += 1
            th = ''.join(f'<th>{inline(c)}</th>' for c in head)
            tb = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in rows)
            out.append(f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'); continue
        elif re.match(r'-{3,}$', s):
            flush(); out.append('<hr>')
        else:
            para.append(s)
        i += 1
    flush()
    return '\n'.join(out)


def read_note(path):
    raw = path.read_text(encoding='utf-8')
    meta, body = {}, raw
    m = re.match(r'---\n(.*?)\n---\n?(.*)', raw, re.S)
    if m:
        for ln in m.group(1).splitlines():
            if ':' in ln:
                k, v = ln.split(':', 1); meta[k.strip()] = v.strip()
        body = m.group(2)
    return meta, body


def plain(text, n=110):
    t = re.sub(r'```.*?```', '', text, flags=re.S)
    t = re.sub(r'[#>*`|\[\]]|\(http[^)]*\)', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n] + ('…' if len(t) > n else '')


def js(v):
    """放進 <script> 的字串：不讓「和號」與 < 出現在追蹤碼裡（core §3-1 #7）"""
    return json.dumps(v, ensure_ascii=False).replace('&', '\\x26').replace('<', '\\x3c')


# ── 版型 ───────────────────────────────────────────────────────
def head(title, desc, path, page_title, topic, extra_ld=None):
    url = SITE + path
    drive = ''
    if DRIVE:
        drive = ('<script data-cfasync="false">(function(){var s=document.createElement("script");'
                 f's.async=1;s.src="{DRIVE}";document.head.appendChild(s);}})();</script>\n')
    ads = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" '
           'crossorigin="anonymous"></script>\n') if ADS_SLOT else ''
    ld = [{'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE_NAME, 'url': SITE + '/'}]
    if extra_ld:
        ld.append(extra_ld)
    ld_html = ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>\n' for x in ld)
    return f'''<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
{drive}<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="編織日和 Alison">
<link rel="icon" href="/icons/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#f6f5f1">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:locale" content="zh_TW">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/icons/og-cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/study.css?v={VER}">
{ads}<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
window.dataLayer=window.dataLayer||[];
function gtag(){{dataLayer.push(arguments);}}
gtag("js",new Date());
gtag("set",{{content_group:"study",topic:{js(topic)},page_lang:"zh-Hant",page_title:{js(page_title)}}});
gtag("config","{GA_ID}",/[?]hy_debug=1/.test(location.search)?{{cookie_domain:".knittinghiyori.com",debug_mode:true}}:{{cookie_domain:".knittinghiyori.com"}});
</script>
{ld_html}<meta name="spec-version" content="{SPEC}">
</head>
<body>
<header class="top"><div class="wrap">
  <a class="kh-brand" href="{SITE}/" data-cta="brand_hub" data-cta-type="study"><img src="/icons/logo-knitting-120.webp" width="40" height="40" alt=""><span>編織日和<span class="kh-site">・學習筆記</span></span></a>
  <a class="home" href="{BLOG}">回編織日和</a>
</div></header>
<main class="wrap">
'''


def ad_block():
    if not ADS_SLOT:
        return ''
    return (f'<div class="kh-ad"><p class="kh-ad-label">廣告</p><ins class="adsbygoogle" style="display:block" '
            f'data-ad-client="{ADS_CLIENT}" data-ad-slot="{ADS_SLOT}" data-ad-format="auto" '
            'data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>\n')


FOOT = f'''</main>
<footer class="foot"><div class="wrap">
  <p class="mark-f">{SITE_NAME}</p>
  <p>上過的課、公開課與自學主題，一邊學一邊整理成筆記。</p>
  <nav><a href="{BLOG}">母站 編織日和</a><a href="https://story.knittinghiyori.com/">故事</a><a href="https://tools.knittinghiyori.com/">小工具</a></nav>
  <p class="kh-legal">本站使用 Cookie 進行流量分析（Google Analytics）與顯示廣告（Google AdSense），部分連結為聯盟連結。<a href="{PRIVACY}">隱私權政策</a></p>
  <small>© {YEAR} KNITTING HIYORI</small>
</div></footer>
<script>
/* 點擊追蹤：有 data-cta 的連結送 cta_click；追蹤壞掉不影響閱讀 */
(function(){{
  var dbg=/[?]hy_debug=1/.test(location.search);
  document.addEventListener("click",function(e){{
    try{{
      var a=e.target.closest?e.target.closest("[data-cta]"):null;
      if(!a)return;
      var p={{cta_id:a.getAttribute("data-cta"),cta_type:a.getAttribute("data-cta-type")||"other",link_url:a.href||""}};
      if(dbg)console.log("[hy-study] cta_click",p);
      if(typeof gtag==="function")gtag("event","cta_click",p);
    }}catch(err){{}}
  }});
}})();
</script>
</body>
</html>
'''


def vignette(s):
    """不開自動廣告：所有連結加 data-google-vignette=false（core §4）"""
    return re.sub(r'<a (?![^>]*data-google-vignette)', '<a data-google-vignette="false" ', s)


def write(path, s):
    p = ROOT / path.strip('/') / 'index.html' if path != '/' else ROOT / 'index.html'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(vignette(s), encoding='utf-8')
    return p


def card_href(t, notes):
    return f'/{t["id"]}/' if notes or not t.get('blog') else t['blog']


def card_type(t, notes):
    return 'study' if notes or not t.get('blog') else 'article'


def card(t, notes, i=0, cta='topic_card'):
    """主題卡：有筆記連主題頁；還沒有筆記時直接連部落格主力文章（study.md §1）"""
    latest = notes[0] if notes else None
    href, ctype = card_href(t, notes), card_type(t, notes)
    go = '看全部筆記' if ctype == 'study' else '讀部落格文章'
    cnt = f'{len(notes)} 篇筆記・最近 {E(latest["date"])}' if latest else '筆記整理中'
    return (f'<a class="card t-{t["color"]}" style="--i:{i}" href="{E(href)}" data-cta="{cta}" data-cta-type="{ctype}">'
            f'<span class="idx" aria-hidden="true">{i + 1:02d}</span><span class="mark" aria-hidden="true">{E(t["mark"])}</span>'
            f'<span class="tags"><span class="tag">{E(t["kind"])}</span><span class="tag st">{E(t["status"])}</span></span>'
            f'<span class="ct">{E(t["name"])}</span><span class="cd">{E(t["desc"])}</span>'
            f'<span class="meta"><span>{cnt}</span><span class="go">{go}{ARROW}</span></span></a>')


def note_li(n, show_topic=None):
    tp = f'<span class="tag">{E(show_topic)}</span>' if show_topic else ''
    return (f'<li><a href="/{n["topic"]}/{n["slug"]}/">{tp}<span class="nt">{E(n["title"])}</span>'
            f'<span class="nd">{E(n["date"])}</span><span class="ns">{E(n["summary"])}</span></a></li>')


# ── 主程式 ─────────────────────────────────────────────────────
def build():
    errs = []
    topics = json.loads((ROOT / 'topics.json').read_text(encoding='utf-8'))['topics']
    ids = set()
    for t in topics:
        if not SLUG.match(t['id']): errs.append(f'topics.json：id「{t["id"]}」只能用英文小寫、數字、連字號')
        if t['id'] in ids: errs.append(f'topics.json：id「{t["id"]}」重複')
        if t['kind'] not in KINDS: errs.append(f'topics.json：{t["id"]} 的 kind 只能是 {"／".join(KINDS)}')
        if t['status'] not in STATUSES: errs.append(f'topics.json：{t["id"]} 的 status 只能是 {"／".join(STATUSES)}')
        if t.get('color') not in COLORS: errs.append(f'topics.json：{t["id"]} 的 color 只能是 {"／".join(COLORS)}')
        if not t.get('mark'): errs.append(f'topics.json：{t["id"]} 缺 mark（卡片貼紙字）')
        if t.get('blog') and not t['blog'].startswith('https://knittinghiyori.com/'): errs.append(f'topics.json：{t["id"]} 的 blog 要是 knittinghiyori.com 的文章網址')
        ids.add(t['id'])
    for d in (ROOT / 'notes').iterdir():
        if d.is_dir() and d.name not in ids:
            errs.append(f'notes/{d.name}/ 沒有登記在 topics.json')

    # 清掉上一次產生的頁面（只清 topics 的資料夾，不碰其他檔案）
    for t in topics:
        shutil.rmtree(ROOT / t['id'], ignore_errors=True)

    notes = {t['id']: [] for t in topics}
    for t in topics:
        for f in sorted((ROOT / 'notes' / t['id']).glob('*.md')) if (ROOT / 'notes' / t['id']).exists() else []:
            if f.name.startswith('_'):
                continue
            meta, body = read_note(f)
            slug = f.stem
            if not SLUG.match(slug):
                errs.append(f'notes/{t["id"]}/{f.name}：檔名要用英文小寫＋連字號（例：week-0-scratch.md）'); continue
            if not meta.get('title'):
                errs.append(f'notes/{t["id"]}/{f.name}：缺 title'); continue
            if meta.get('draft') == 'true':
                continue
            date = meta.get('date', '')
            if not re.match(r'\d{4}-\d{2}-\d{2}$', date):
                errs.append(f'notes/{t["id"]}/{f.name}：date 要寫成 2026-10-04 這種格式'); continue
            notes[t['id']].append(dict(topic=t['id'], slug=slug, title=meta['title'], date=date,
                                       summary=meta.get('summary') or plain(body), source=meta.get('source', ''),
                                       body=body))
        notes[t['id']].sort(key=lambda n: n['date'], reverse=True)

    urls = ['/']
    # 筆記頁
    for t in topics:
        for n in notes[t['id']]:
            path = f'/{t["id"]}/{n["slug"]}/'
            src = ''
            if n['source']:
                src = (f'<p class="src">來源：<a href="{E(n["source"])}" target="_blank" rel="noopener" '
                       f'data-cta="source_link" data-cta-type="other">{E(n["source"])}</a></p>')
            ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': n['title'],
                  'datePublished': n['date'], 'author': {'@type': 'Person', 'name': 'Alison'},
                  'inLanguage': 'zh-Hant', 'url': SITE + path}
            page = head(f'{n["title"]}｜{t["name"]} 筆記｜{SITE_NAME}', n['summary'], path,
                        f'筆記|{t["name"]}|{n["title"]}', t['id'], ld)
            page += (f'<nav class="crumb"><a href="/">學習筆記</a> › <a href="/{t["id"]}/">{E(t["name"])}</a></nav>\n'
                     f'<article class="note"><h1>{E(n["title"])}</h1><p class="date">{E(n["date"])}・{E(t["kind"])}</p>'
                     f'{src}\n{md(n["body"])}\n</article>\n')
            page += ad_block()
            page += f'<p class="back"><a href="/{t["id"]}/">← 回 {E(t["name"])} 全部筆記</a></p>\n' + FOOT
            write(path, page); urls.append(path)

    # 主題頁
    for t in topics:
        path = f'/{t["id"]}/'
        btns = ''
        if t.get('blog'):
            btns += (f'<a class="btn" href="{E(t["blog"])}" data-cta="blog_link" data-cta-type="article">'
                     f'先讀部落格文章{ARROW}</a>')
        if t['link']:
            btns += (f'<a class="btn ghost" href="{E(t["link"])}" target="_blank" rel="noopener" data-cta="course_link" '
                     f'data-cta-type="other">課程官網</a>')
        btns = f'<p class="btns">{btns}</p>' if btns else ''
        if notes[t['id']]:
            lst = '<ul class="notes">' + ''.join(note_li(n) for n in notes[t['id']]) + '</ul>'
        else:
            more = (f'<a class="btn ghost" href="{E(t["blog"])}" data-cta="blog_link" data-cta-type="article">'
                    f'先讀部落格文章{ARROW}</a>') if t.get('blog') else ''
            lst = f'<div class="empty-box"><p>這個主題的筆記還在整理中。</p>{more}</div>'
        page = head(f'{t["full"]} 學習筆記｜{SITE_NAME}', t['desc'], path, f'筆記|{t["name"]}|主題總覽', t['id'])
        page += (f'<nav class="crumb"><a href="/">學習筆記</a> › {E(t["name"])}</nav>\n'
                 f'<section class="topic-hero t-{t["color"]}"><span class="mark" aria-hidden="true">{E(t["mark"])}</span>'
                 f'<p class="tags"><span class="tag">{E(t["kind"])}</span><span class="tag st">{E(t["status"])}</span></p>'
                 f'<h1><span class="hl">{E(t["full"])}</span></h1><p class="lead">{E(t["desc"])}</p>{btns}</section>\n'
                 f'<section class="sec"><div class="sec-h"><h2>全部筆記</h2><span class="sub">{len(notes[t["id"]])} 篇</span></div>{lst}</section>\n')
        page += ad_block() + FOOT
        write(path, page); urls.append(path)

    # 首頁
    groups, n, i = '', 0, 0
    sections = [(k, [t for t in topics if t['kind'] == k and t['status'] != '想學']) for k in KINDS]
    sections.append(('想學清單', [t for t in topics if t['status'] == '想學']))
    for k, ts in sections:
        if not ts:
            continue
        n += 1
        cards = ''
        for t in ts:
            cards += card(t, notes[t['id']], i); i += 1
        groups += (f'<section class="sec split"><div class="sec-h"><span class="no">{KIND_EN[k]}</span><h2>{k}</h2>'
                   f'<p class="what">{KIND_NOTE[k]}</p><span class="sub">{len(ts)} 個主題</span></div>'
                   f'<div class="grid">{cards}</div></section>\n')
    allnotes = sorted((x for v in notes.values() for x in v), key=lambda x: x['date'], reverse=True)[:6]
    name = {t['id']: t['name'] for t in topics}
    recent = ('<section class="sec"><div class="sec-h"><span class="no">NEW</span><h2>最近更新</h2></div><ul class="notes">'
              + ''.join(note_li(x, name[x['topic']]) for x in allnotes) + '</ul></section>\n') if allnotes else ''
    total = sum(len(v) for v in notes.values())
    stats = (f'<ul class="facts"><li><b>{len(topics)}</b>個主題</li><li><b>{len({t["kind"] for t in topics})}</b>種學法</li>'
             + (f'<li><b>{total}</b>篇筆記</li>' if total else '<li>筆記陸續整理中</li>') + '</ul>')
    desc = '上過的課、公開課與自學的學習筆記：' + '、'.join(t['name'] for t in topics) + '，以及之後想學的新主題。'
    page = head(f'{SITE_NAME}｜課程與自學筆記', desc, '/', '筆記|學習筆記|總覽', 'hub')
    order = [t for k, ts in sections for t in ts]
    toc = ''.join(f'<li><a href="{E(card_href(t, notes[t["id"]]))}" data-cta="toc_link" data-cta-type="{card_type(t, notes[t["id"]])}">'
                  f'<span class="n">{j + 1:02d}</span><span class="t">{E(t["name"])}</span><span class="k">{E(t["kind"])}</span></a></li>'
                  for j, t in enumerate(order))
    page += ('<section class="hero"><div><p class="eyebrow label">Study Notes</p>'
             '<h1>學習筆記<span class="rule" aria-hidden="true"></span></h1>'
             '<p class="lead"><span class="nb">把上過的課、看過的公開課和自學的東西，</span><span class="nb">整理成之後自己也找得回來的筆記。</span></p>'
             f'{stats}</div><nav class="toc" aria-label="目次"><p class="label"><span>目次</span><span>Contents</span></p><ol>{toc}</ol></nav></section>\n'
             f'{recent}{groups}')
    page += ad_block() + FOOT
    write('/', page)

    # 404、sitemap、robots、manifest
    p404 = head(f'找不到這一頁｜{SITE_NAME}', '找不到這一頁', '/404.html', '筆記|404|找不到頁面', 'hub')
    p404 = p404.replace('content="index, follow, max-image-preview:large"', 'content="noindex"')
    cards = ''.join(card(t, notes[t['id']], i, 'notfound_topic') for i, t in enumerate(order))
    p404 += ('<section class="nf"><p class="nf-code" aria-hidden="true">4<span>0</span>4</p>'
             '<span class="label">Page not found</span><h1>找不到這一頁</h1>'
             '<p class="lead">可能網址打錯，或筆記換了位置。回首頁看看，或從下面挑一個主題繼續讀。</p>'
             '<p class="btns"><a class="btn" href="/" data-cta="notfound_hub" data-cta-type="study">回學習筆記首頁</a></p></section>\n'
             f'{recent}<section class="sec"><div class="sec-h"><h2>看看其他主題</h2><span class="sub">{len(topics)} 個主題</span></div>'
             f'<div class="grid">{cards}</div></section>\n' + FOOT)
    (ROOT / '404.html').write_text(vignette(p404), encoding='utf-8')
    today = datetime.date.today().isoformat()
    sm = ''.join(f'<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls)
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + sm + '</urlset>\n', encoding='utf-8')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /notes/\n\nSitemap: {SITE}/sitemap.xml\n', encoding='utf-8')
    (ROOT / 'site.webmanifest').write_text(json.dumps({
        'name': SITE_NAME, 'short_name': '學習筆記', 'lang': 'zh-Hant-TW', 'start_url': '/', 'display': 'standalone',
        'background_color': '#f6f5f1', 'theme_color': '#f6f5f1',
        'icons': [{'src': '/icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                  {'src': '/icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]},
        ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return errs, urls


def check(urls):
    """上線前檢查（core §9 能自動查的部分）"""
    bad = 0
    pages = [ROOT / 'index.html', ROOT / '404.html'] + [ROOT / u.strip('/') / 'index.html' for u in urls if u != '/']
    for p in pages:
        s = p.read_text(encoding='utf-8')
        miss = []
        if GA_ID not in s: miss.append('GA4')
        if 'name="spec-version"' not in s: miss.append('spec-version meta')
        if 'adsbygoogle.js?client=' in s: miss.append('不開自動廣告：載入碼不能帶 ?client=')
        if re.search(r'<a (?![^>]*data-google-vignette)', s): miss.append('有連結少了 vignette 標記')
        if 'href="#"' in s: miss.append('有 href="#" 空連結')
        if '/icons/favicon.ico' not in s: miss.append('品牌 icon')
        if 'data-cta="brand_hub"' not in s or 'logo-knitting-120.webp' not in s: miss.append('頁首品牌列（core §7）')
        for js in re.findall(r'<script>(.*?)</script>', s, re.S):
            if '&' in js: miss.append('追蹤碼出現「和號」字元'); break
        for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try: json.loads(ld)
            except ValueError: miss.append('JSON-LD 解析失敗')
        if DRIVE and not re.search(r'<head>\s*<script', s): miss.append('Drive 不是 head 第一個 script')
        rel = p.relative_to(ROOT)
        print(('✅ ' if not miss else '❌ ') + str(rel) + ('' if not miss else '　缺：' + '、'.join(miss)))
        bad += bool(miss)
    return len(pages), bad


if __name__ == '__main__':
    errs, urls = build()
    for e in errs:
        print('❌ ' + e)
    n, bad = check(urls)
    bad += len(errs)
    print(f'\n共 {n} 頁，{bad} 個問題')
    if not ADS_SLOT: print('（提醒：ADS_SLOT 還沒填，目前不放廣告）')
    if not DRIVE: print('（提醒：DRIVE 還沒填，目前不載 Travelpayouts）')
    sys.exit(1 if bad else 0)
