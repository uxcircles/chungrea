/* Chung & Rea concept: menu, appeal-deadline worksheet, booking form (mailto), lazy map. */
(() => {
  const lang = document.documentElement.lang.startsWith('zh-Hans') ? 'sc' : document.documentElement.lang.startsWith('zh') ? 'zh' : 'en';
  const T = {
    en: {
      enter: 'Enter the date above', left: (n) => `${n} day${n === 1 ? '' : 's'} left`, today: 'Due today, call now',
      past: (n) => `${n} day${n === 1 ? '' : 's'} ago. A late appeal needs reasons; call today`,
      moved: 'Moved to the next working day (the deadline fell on a weekend).',
      rule: (d) => `${d} days from the date on the letter.`, bad: 'Check the date: it is in the future.',
      subject: 'Meeting request', name: 'Name', phone: 'Phone', topic: 'Matter', mlang: 'Language', deadline: 'Deadline on letter', msg: 'Notes', menu: 'Menu', close: 'Close',
    },
    zh: {
      enter: '請先輸入上方日期', left: (n) => `尚餘 ${n} 日`, today: '今天到期，請立即致電',
      past: (n) => `已過期 ${n} 日。逾期上訴須說明理由，請今天致電`,
      moved: '期限落在週末，已順延至下一個工作日。',
      rule: (d) => `由信上日期起計 ${d} 日。`, bad: '請檢查日期：這是未來的日期。',
      subject: '預約會面', name: '姓名', phone: '電話', topic: '事項', mlang: '語言', deadline: '信上期限', msg: '補充', menu: '選單', close: '關閉',
    },
  };
  T.sc = {
    ...T.zh, enter: '请先输入上方日期', left: (n) => `尚余 ${n} 日`, today: '今天到期，请立即致电',
    past: (n) => `已过期 ${n} 日。逾期上诉须说明理由，请今天致电`, moved: '期限落在周末，已顺延至下一个工作日。',
    rule: (d) => `由信上日期起计 ${d} 日。`, bad: '请检查日期：这是未来的日期。',
    subject: '预约会面', name: '姓名', phone: '电话', topic: '事项', mlang: '语言', deadline: '信上期限', msg: '补充', menu: '菜单', close: '关闭',
  };
  const t = T[lang];
  const locale = { en: 'en-GB', zh: 'zh-HK', sc: 'zh-CN' }[lang];

  // menu
  const btn = document.querySelector('.menu-btn');
  const menu = document.getElementById('menu');
  if (btn && menu) {
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', open);
      menu.hidden = !open;
      btn.textContent = open ? t.close : t.menu;
      document.documentElement.classList.toggle('menu-open', open);
    });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !menu.hidden) { btn.click(); btn.focus(); } });
  }

  // dates (local, no time zone surprises)
  const parse = (v) => { const [y, m, d] = v.split('-').map(Number); return new Date(y, m - 1, d); };
  const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  const today = () => { const n = new Date(); return new Date(n.getFullYear(), n.getMonth(), n.getDate()); };
  const fmt = (d) => d.toLocaleDateString(locale, { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });

  // appeal-deadline worksheet
  const date = document.getElementById('d-date');
  if (date) {
    const out = document.getElementById('d-out');
    const note = document.getElementById('d-note');
    const book = document.getElementById('letter-book');
    date.max = iso(today());
    const run = () => {
      const days = Number(document.querySelector('input[name=where]:checked').value);
      if (!date.value) { out.innerHTML = `<span class="out-empty">${t.enter}</span>`; note.textContent = ''; return; }
      const sent = parse(date.value);
      if (sent > today()) { out.innerHTML = `<span class="out-empty">${t.bad}</span>`; note.textContent = ''; return; }
      const due = new Date(sent); due.setDate(due.getDate() + days);
      let moved = false;
      while (due.getDay() === 0 || due.getDay() === 6) { due.setDate(due.getDate() + 1); moved = true; }
      const diff = Math.round((due - today()) / 864e5);
      out.textContent = fmt(due);
      note.textContent = `${t.rule(days)} ${moved ? t.moved + ' ' : ''}${diff > 0 ? t.left(diff) : diff === 0 ? t.today : t.past(-diff)}`;
      if (book) book.href = `contact.html?deadline=${iso(due)}#book`;
    };
    date.addEventListener('input', run);
    date.addEventListener('change', run);
    document.querySelectorAll('input[name=where]').forEach((r) => r.addEventListener('change', run));
    run();
  }

  // booking form -> mailto
  const form = document.getElementById('book-form');
  if (form) {
    const dl = new URLSearchParams(location.search).get('deadline');
    if (dl && /^\d{4}-\d{2}-\d{2}$/.test(dl)) form.deadline.value = dl;
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const err = document.getElementById('f-err');
      let ok = true;
      ['name', 'phone'].forEach((k) => {
        const bad = !form[k].value.trim();
        form[k].setAttribute('aria-invalid', bad);
        if (bad && ok) { form[k].focus(); ok = false; }
      });
      err.hidden = ok;
      if (!ok) return;
      const lines = [
        `${t.name}: ${form.name.value.trim()}`,
        `${t.phone}: ${form.phone.value.trim()}`,
        `${t.topic}: ${form.topic.value}`,
        `${t.mlang}: ${form.lang.value}`,
        form.deadline.value ? `${t.deadline}: ${fmt(parse(form.deadline.value))}` : '',
        form.msg.value.trim() ? `\n${t.msg}:\n${form.msg.value.trim()}` : '',
      ].filter(Boolean);
      location.href = `mailto:info@chungrea.com?subject=${encodeURIComponent(`${t.subject}: ${form.topic.value}`)}&body=${encodeURIComponent(lines.join('\n'))}`;
    });
  }

  // map: load MapLibre only when the map scrolls near
  const box = document.querySelector('[data-map]');
  if (box && 'IntersectionObserver' in window) {
    const root = document.querySelector('link[rel=stylesheet][href*="assets/site.css"]').getAttribute('href').split('assets/')[0];
    const load = () => {
      const css = document.createElement('link'); css.rel = 'stylesheet'; css.href = root + 'assets/vendor/maplibre/maplibre-gl.css'; document.head.appendChild(css);
      const s1 = document.createElement('script'); s1.src = root + 'assets/vendor/maplibre/maplibre-gl.js';
      s1.onload = () => {
        const s2 = document.createElement('script'); s2.src = root + 'assets/map.js?v=1';
        s2.onload = () => { try { const map = window.crMap(box); map.on('load', () => box.querySelector('.map-fallback').style.visibility = 'hidden'); } catch (e) { /* keep the sketch */ } };
        document.head.appendChild(s2);
      };
      document.head.appendChild(s1);
    };
    const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) { io.disconnect(); load(); } }, { rootMargin: '400px' });
    io.observe(box);
  }
})();
