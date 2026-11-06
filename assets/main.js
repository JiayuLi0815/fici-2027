/* =========================================================
   2027 第二十四届中国文化产业新年论坛 — 交互脚本
   ========================================================= */
(function () {
  'use strict';

  var header   = document.getElementById('siteHeader');
  var nav      = document.getElementById('nav');
  var navToggle= document.getElementById('navToggle');
  var navScrim = document.getElementById('navScrim');
  var toTop    = document.getElementById('toTop');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 导航：滚动状态 ---------- */
  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop;
    header.classList.toggle('is-stuck', y > 8);
    if (toTop) toTop.classList.toggle('is-visible', y > 900);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- 移动端菜单 ---------- */
  function setMenu(open) {
    nav.classList.toggle('is-open', open);
    navToggle.classList.toggle('is-open', open);
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? '关闭菜单' : '打开菜单');
    navScrim.hidden = !open;
    document.body.style.overflow = open ? 'hidden' : '';
  }

  if (navToggle) {
    navToggle.addEventListener('click', function () {
      setMenu(!nav.classList.contains('is-open'));
    });
  }
  if (navScrim) navScrim.addEventListener('click', function () { setMenu(false); });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) {
      setMenu(false);
      navToggle.focus();
    }
  });

  /* 移动端：一级菜单点击展开二级 */
  document.querySelectorAll('.has-drop > a').forEach(function (link) {
    link.addEventListener('click', function (e) {
      if (window.matchMedia('(max-width: 900px)').matches) {
        e.preventDefault();
        link.parentElement.classList.toggle('is-open');
      }
    });
  });

  /* 点击任意锚点后收起菜单 */
  nav.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function () {
      if (!a.parentElement.classList.contains('has-drop')) setMenu(false);
    });
  });

  /* ---------- 导航高亮 ---------- */
  var sections = Array.prototype.slice.call(document.querySelectorAll('main section[id]'));
  var navLinks = Array.prototype.slice.call(nav.querySelectorAll('.nav-list > li > a'));
  var linkMap = {};
  navLinks.forEach(function (a) {
    var id = (a.getAttribute('href') || '').replace('#', '');
    if (id) linkMap[id] = a;
  });

  if (sections.length) {
    var currentId = '';
    var setActive = function (id) {
      if (id === currentId) return;
      currentId = id;
      navLinks.forEach(function (a) { a.parentElement.classList.remove('is-active'); });
      if (linkMap[id]) linkMap[id].parentElement.classList.add('is-active');
    };

    var spyQueued = false;
    var runSpy = function () {
      spyQueued = false;
      var line = window.scrollY + (parseInt(getComputedStyle(document.documentElement)
        .getPropertyValue('--nav-h'), 10) || 68) + 120;
      var current = '';
      for (var i = 0; i < sections.length; i++) {
        if (sections[i].offsetTop <= line) current = sections[i].id;
      }
      setActive(current);
    };

    window.addEventListener('scroll', function () {
      if (!spyQueued) { spyQueued = true; requestAnimationFrame(runSpy); }
    }, { passive: true });

    window.addEventListener('resize', runSpy);
    runSpy();
  }

  /* ---------- 入场动画 ---------- */
  if (!reduceMotion && 'IntersectionObserver' in window) {
    var revealTargets = document.querySelectorAll(
      '.section-head, .about-body, .about-aside, .news-feature, .news-list, ' +
      '.agenda-day, .prog-card, .speaker, .pub-card, .ph-photo, .year-grid, ' +
      '.service-card, .contact-band'
    );

    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          ro.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });

    revealTargets.forEach(function (el, i) {
      el.classList.add('reveal');
      el.style.transitionDelay = Math.min(i % 6, 5) * 55 + 'ms';
      ro.observe(el);
    });
  }

  /* ---------- 倒计时 ---------- */
  var cd = document.getElementById('countdown');
  if (cd) {
    var target = new Date('2027-01-09T09:00:00+08:00').getTime();
    var update = function () {
      var diff = target - Date.now();
      if (diff <= 0) { cd.textContent = '今天'; return; }
      cd.textContent = Math.ceil(diff / 86400000);
    };
    update();
    setInterval(update, 60000);
  }

  /* ---------- 占位链接：不跳转 ---------- */
  document.querySelectorAll('a[aria-disabled="true"]').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); });
  });

  /* ---------- 平滑锚点（含固定导航偏移） ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (!id || id === '#' || a.getAttribute('aria-disabled') === 'true') return;
      // 移动端的一级下拉菜单只负责展开，不跳转
      if (a.parentElement.classList.contains('has-drop') && window.matchMedia('(max-width: 900px)').matches) return;
      var el = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      var top = el.getBoundingClientRect().top + window.scrollY - (parseInt(getComputedStyle(document.documentElement).getPropertyValue('--nav-h'), 10) || 68) + 1;
      window.scrollTo({ top: top, behavior: reduceMotion ? 'auto' : 'smooth' });
      history.replaceState(null, '', id);
    });
  });
})();
