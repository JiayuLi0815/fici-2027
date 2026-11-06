/* =========================================================
   2027 第二十四届中国文化产业新年论坛 — 交互脚本
   ========================================================= */
(function () {
  'use strict';

  var nav      = document.getElementById('nav');
  var navToggle = document.getElementById('navToggle');
  var navScrim = document.getElementById('navScrim');
  var toTop    = document.getElementById('toTop');

  /* ---------- 移动端菜单 ---------- */
  function setMenu(open) {
    if (!nav || !navToggle) return;
    nav.classList.toggle('is-open', open);
    navToggle.classList.toggle('is-open', open);
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? '关闭菜单' : '打开菜单');
    if (navScrim) navScrim.hidden = !open;
    document.body.style.overflow = open ? 'hidden' : '';
  }

  if (navToggle) {
    navToggle.addEventListener('click', function () {
      setMenu(!nav.classList.contains('is-open'));
    });
  }
  if (navScrim) navScrim.addEventListener('click', function () { setMenu(false); });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav && nav.classList.contains('is-open')) {
      setMenu(false);
      navToggle.focus();
    }
  });

  /* ---------- 回到顶部 ---------- */
  function onScroll() {
    if (toTop) toTop.classList.toggle('is-visible', window.scrollY > 800);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

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
})();
