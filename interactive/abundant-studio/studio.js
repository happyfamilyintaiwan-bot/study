/* 豐盛工作室 · study/artists-way · 追蹤碼不使用和號字元 */
(function () {
  var D = window.HY_STUDIO;
  var KEY = 'hy_studio_v1';
  var DEBUG = /hy_debug=1/.test(location.search);
  var LVL = function (n) { return 'l' + (n < 10 ? '0' : '') + n; };
  var PAD = function (n) { return (n < 10 ? '0' : '') + n; };
  var $ = function (id) { return document.getElementById(id); };
  var fmt = function (s, o) { return s.replace(/\{(\w+)\}/g, function (m, k) { return o[k]; }); };

  function track(name, p) {
    try {
      p = p || {};
      if (DEBUG) { p.debug_mode = true; console.log('[hy-study]', name, p); }
      if (typeof window.gtag === 'function') { window.gtag('event', name, p); }
      else { window.dataLayer = window.dataLayer || []; window.dataLayer.push(['event', name, p]); }
    } catch (err) { /* 追蹤失敗不影響功能 */ }
  }

  /* ---------- 日期 ---------- */
  function ymd(d) {
    d = d || new Date();
    return d.getFullYear() + '-' + PAD(d.getMonth() + 1) + '-' + PAD(d.getDate());
  }
  function parse(s) { var a = s.split('-'); return new Date(+a[0], +a[1] - 1, +a[2]); }
  function daysBetween(a, b) { return Math.round((parse(b) - parse(a)) / 86400000); }
  function shift(s, n) { var d = parse(s); d.setDate(d.getDate() + n); return ymd(d); }

  /* ---------- 狀態（只存在這個瀏覽器；不含任何隨筆文字） ---------- */
  var S = null;
  function load() { try { var r = localStorage.getItem(KEY); S = r ? JSON.parse(r) : null; } catch (err) { S = null; } }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (err) { /* 無痕模式等 */ } }
  function fresh() { return { v: 2, start: ymd(), week: 1, weekStart: ymd(), arrived: 0, pages: {}, dates: {}, walks: {}, reads: {}, card: {}, tasks: {} }; }
  function migrate() {
    if (!S) { return; }
    if (S.arrived === undefined) { S.arrived = S.restored || 0; }
    S.walks = S.walks || {}; S.reads = S.reads || {};
  }

  function streak() {
    if (!S) { return 0; }
    var d = ymd(), n = 0;
    if (!S.pages[d]) { d = shift(d, -1); }
    while (S.pages[d]) { n++; d = shift(d, -1); }
    return n;
  }
  function pageDays() { return S ? Object.keys(S.pages).length : 0; }
  function recentPages() {
    if (!S) { return 0; }
    var n = 0, d = ymd();
    for (var i = 0; i < 7; i++) { if (S.pages[d]) { n++; } d = shift(d, -1); }
    return n;
  }
  function weekPageDays() {
    var n = 0, d = S.weekStart, end = ymd();
    while (daysBetween(d, end) >= 0) { if (S.pages[d]) { n++; } d = shift(d, 1); }
    return n;
  }
  function complete() { return S ? S.arrived >= 12 : false; }
  function wk() { return S ? Math.min(S.week, 12) : 1; }

  function count(txt) {
    if (D.lang === 'zh') { return txt.replace(/\s/g, '').length; }
    var w = txt.trim().split(/\s+/);
    return w[0] === '' ? 0 : w.length;
  }

  /* ---------- 畫面 ---------- */
  var affIdx = 0, popW = 0;

  function renderStudio() {
    var objs = document.querySelectorAll('.studio .it');
    var r = S ? S.arrived : 0, cur = S ? S.week : 1;
    for (var i = 0; i < objs.length; i++) {
      var w = +objs[i].getAttribute('data-w');
      objs[i].classList.toggle('on', w <= r);
      objs[i].classList.toggle('now', w === cur ? !complete() : false);
      objs[i].classList.toggle('pop', w === popW);
    }
    for (var k = 0; k < objs.length; k++) {
      if (!objs[k].querySelector('title')) {
        var tt = document.createElementNS('http://www.w3.org/2000/svg', 'title');
        tt.textContent = D.weeks[+objs[k].getAttribute('data-w') - 1].item;
        objs[k].insertBefore(tt, objs[k].firstChild);
      }
    }
    var st = document.querySelectorAll('.strip');
    for (var j = 0; j < st.length; j++) { st[j].classList.toggle('on', +st[j].getAttribute('data-s') <= r); }
  }

  function renderStats() {
    $('st-week').textContent = S ? fmt(D.ui.week_of, { n: wk() }) : '0/12';
    $('st-items').textContent = S ? S.arrived : 0;
    $('st-streak').textContent = streak();
    $('st-pages').textContent = pageDays();
    $('finale').hidden = !complete();
    if (complete()) { $('finale').textContent = D.ui.finale; }
    var cta = $('hero-cta');
    cta.firstChild.nodeValue = (S ? D.t.cta_continue : D.t.cta_start) + ' ';
    $('dock-wk').textContent = 'W' + PAD(wk());
  }

  function renderSprout() {
    var r = complete() ? 7 : recentPages();
    var leaves = document.querySelectorAll('.leaf');
    for (var i = 0; i < leaves.length; i++) { leaves[i].classList.toggle('on', +leaves[i].getAttribute('data-i') <= r); }
    document.querySelector('.bloom').classList.toggle('on', r >= 7);
    $('leafcount').textContent = fmt(D.ui.leaves, { n: r });
    $('affirm').textContent = D.affirm[affIdx % D.affirm.length];
  }

  function renderWeek7() {
    var box = $('week7'), names = D.lang === 'zh' ? '日一二三四五六' : 'SMTWTFS';
    var cols = ['#1f4e86', '#c4542a', '#e2a83c', '#2f7a72', '#4f7d3a', '#2e6f9e', '#b0422f'];
    box.innerHTML = '';
    var d = shift(ymd(), -6);
    for (var i = 0; i < 7; i++) {
      var el = document.createElement('div'), lab = document.createElement('span'), dot = document.createElement('i');
      el.className = 'd';
      if (S ? !!S.pages[d] : false) { el.classList.add('on'); }
      if (i === 6) { el.classList.add('today'); }
      el.style.setProperty('--c', cols[parse(d).getDay()]);
      lab.textContent = names.charAt(parse(d).getDay());
      el.appendChild(lab); el.appendChild(dot); box.appendChild(el);
      d = shift(d, 1);
    }
    box.setAttribute('aria-label', fmt(D.ui.leaves, { n: recentPages() }));
  }

  function renderToday() {
    var started = !!S;
    $('start-box').hidden = started;
    var today = started ? S.pages[ymd()] : null;
    $('write-box').hidden = !started || !!today;
    $('done-box').hidden = !today;
    if (today) { $('done-box').textContent = D.ui['done_' + today] || D.ui.done_typed; }
  }

  function renderWeek() {
    var n = wk(), w = D.weeks[n - 1], started = !!S, locked = !started || complete();
    var band = $('week-band');
    band.style.setProperty('--wk', w.color);
    band.style.setProperty('--wk-on', w.on);
    $('wk-num').textContent = PAD(n);
    $('wk-h2').textContent = w.theme;
    $('wk-theme').textContent = D.lang === 'en' ? w.theme.toUpperCase() : w.theme;
    $('wk-item').textContent = w.item;
    $('wk-intro').textContent = w.intro;
    $('read-d').textContent = fmt(D.t.p_read_d, { n: n });

    var t = started ? (S.tasks[n] || []) : [];
    var boxes = document.querySelectorAll('#tasks input'), texts = document.querySelectorAll('#tasks .task-text');
    for (var i = 0; i < boxes.length; i++) { boxes[i].checked = !!t[i]; boxes[i].disabled = locked; texts[i].textContent = w.tasks[i]; }

    var card = started ? S.card[n] : undefined, hasCard = card === undefined ? false : card !== null;
    var dated = started ? !!S.dates[n] : false;
    $('datecard').classList.toggle('blank', !hasCard);
    $('datetext').textContent = hasCard ? D.dates[card] : D.dates[(n * 5) % D.dates.length];
    $('btn-draw').textContent = hasCard ? D.t.btn_redraw : D.t.btn_draw;
    $('btn-draw').disabled = locked || dated;
    $('btn-date').disabled = locked || dated || !hasCard;
    $('date-ok').hidden = !dated;

    var walked = started ? !!S.walks[n] : false, read = started ? !!S.reads[n] : false;
    $('btn-walk').disabled = locked || walked; $('walk-ok').hidden = !walked;
    $('btn-read').disabled = locked || read; $('read-ok').hidden = !read;

    var bb = $('btn-bring'), wait = $('wait');
    bb.textContent = fmt(D.ui.bring, { item: w.item });
    if (!started) { bb.disabled = true; wait.textContent = D.ui.not_started; return; }
    if (complete()) { bb.disabled = true; wait.textContent = D.ui.finale; return; }
    var left = 7 - daysBetween(S.weekStart, ymd());
    if (left > 0) {
      if (DEBUG) { bb.disabled = false; wait.textContent = ''; }
      else { bb.disabled = true; wait.textContent = fmt(D.ui.bring_wait, { item: w.item, d: left }); }
    } else { bb.disabled = false; wait.textContent = ''; }
  }

  function renderItems() {
    var lis = document.querySelectorAll('#items li'), r = S ? S.arrived : 0, cur = S ? S.week : 1;
    for (var i = 0; i < lis.length; i++) {
      var w = i + 1, on = w <= r, now = on ? false : (w === cur ? !complete() : false);
      lis[i].classList.toggle('on', on);
      lis[i].classList.toggle('now', now);
      lis[i].classList.toggle('later', !on ? !now : false);
      lis[i].querySelector('.chip').textContent = on ? D.ui.arrived : (now ? D.ui.next : D.ui.later);
    }
  }

  function render() {
    var parts = [renderStudio, renderStats, renderSprout, renderToday, renderWeek7, renderWeek, renderItems];
    for (var i = 0; i < parts.length; i++) { try { parts[i](); } catch (err) { if (DEBUG) { console.error(err); } } }
  }

  function toast(msg) {
    var t = $('toast'); t.textContent = msg; t.hidden = false;
    clearTimeout(toast.h); toast.h = setTimeout(function () { t.hidden = true; }, 2400);
  }

  /* ---------- 互動 ---------- */
  function bind() {
    $('btn-start').addEventListener('click', function () {
      try {
        S = fresh(); save();
        track('studio_start', { level: LVL(1), entry_point: /from=invite/.test(location.search) ? 'shared' : 'direct' });
        render();
      } catch (err) {}
    });

    var ta = $('pages');
    ta.addEventListener('input', function () {
      try {
        var c = count(ta.value);
        $('count').textContent = c;
        $('gauge').style.width = Math.min(100, c / D.target * 100) + '%';
        $('btn-done').disabled = c < D.target;
        $('btn-short').disabled = c < 1;
      } catch (err) {}
    });

    function finishPages(option) {
      try {
        if (!S) { return; }
        S.pages[ymd()] = option; save();
        ta.value = ''; $('count').textContent = '0'; $('gauge').style.width = '0';
        track('studio_pages_done', { level: LVL(wk()), option: option });
        var sk = streak();
        if (sk === 7 || sk === 30) { track('studio_streak', { milestone: 's' + sk }); }
        affIdx++; render();
      } catch (err) {}
    }
    $('btn-paper').addEventListener('click', function () { finishPages('paper'); });
    $('btn-done').addEventListener('click', function () { finishPages('typed'); });
    $('btn-short').addEventListener('click', function () { finishPages('short'); });

    $('btn-draw').addEventListener('click', function () {
      try {
        var n = wk(), prev = S.card[n], k;
        do { k = Math.floor(Math.random() * D.dates.length); } while (k === prev);
        S.card[n] = k; save(); render();
      } catch (err) {}
    });
    $('btn-date').addEventListener('click', function () {
      try { var n = wk(); S.dates[n] = ymd(); save(); track('studio_date_done', { level: LVL(n) }); render(); } catch (err) {}
    });
    $('btn-walk').addEventListener('click', function () {
      try { var n = wk(); S.walks[n] = ymd(); save(); track('studio_walk_done', { level: LVL(n) }); render(); } catch (err) {}
    });
    $('btn-read').addEventListener('click', function () {
      try { var n = wk(); S.reads[n] = ymd(); save(); render(); } catch (err) {}
    });

    $('tasks').addEventListener('change', function (ev) {
      try {
        var i = +ev.target.getAttribute('data-t'), n = wk();
        var t = S.tasks[n] || [false, false, false, false];
        t[i] = ev.target.checked; S.tasks[n] = t; save();
      } catch (err) {}
    });

    $('btn-bring').addEventListener('click', function () {
      try {
        var n = S.week, t = S.tasks[n] || [];
        var done = t.filter(function (x) { return x; }).length;
        track('studio_week_complete', { level: LVL(n), item_count: weekPageDays(), score: done });
        S.arrived = n; popW = n;
        if (n < 12) { S.week = n + 1; S.weekStart = ymd(); }
        save(); render();
        var top = document.querySelector('.frame');
        if (top.scrollIntoView) { top.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
      } catch (err) {}
    });

    $('btn-share').addEventListener('click', function () {
      var link = D.url + '?from=invite';
      try {
        if (navigator.share) {
          navigator.share({ title: document.title, text: D.ui.share_text, url: link }).then(function () {
            track('share', { method: 'native', content_type: 'study' });
          }).catch(function (err) {
            if (err ? err.name === 'AbortError' : false) { track('share_cancel', { method: 'native', content_type: 'study' }); }
            else { copyLink(link); }
          });
        } else { copyLink(link); }
      } catch (err) { copyLink(link); }
    });
    function copyLink(link) {
      var ok = function () { toast(D.ui.copied); track('share', { method: 'copy_link', content_type: 'study' }); };
      try { navigator.clipboard.writeText(D.ui.share_text + ' ' + link).then(ok).catch(function () { toast(link); }); }
      catch (err) { toast(link); }
    }

    $('btn-reset').addEventListener('click', function () { $('confirm').hidden = false; });
    $('reset-no').addEventListener('click', function () { $('confirm').hidden = true; });
    $('reset-yes').addEventListener('click', function () {
      try { track('studio_progress_reset', { level: LVL(wk()) }); localStorage.removeItem(KEY); } catch (err) {}
      S = null; popW = 0; $('confirm').hidden = true; render();
    });

    var faqs = document.querySelectorAll('details[data-q]');
    for (var i = 0; i < faqs.length; i++) {
      faqs[i].addEventListener('toggle', function () { if (this.open) { track('faq_open', { option: this.getAttribute('data-q') }); } });
    }
    $('langlink').addEventListener('click', function () { track('lang_switch', { source: 'header', from_lang: D.pageLang }); });

    document.addEventListener('click', function (ev) {
      try {
        var a = ev.target.closest('[data-cta]');
        if (!a) { return; }
        var p = { cta_id: a.getAttribute('data-cta'), cta_type: a.getAttribute('data-cta-type') || 'other', link_url: a.href || '' };
        if (a.getAttribute('data-option')) { p.option = a.getAttribute('data-option'); }
        track('cta_click', p);
      } catch (err) {}
    });

    affIdx = new Date().getDate();
  }

  load(); migrate();
  try { bind(); } catch (err) {}
  render();
})();
