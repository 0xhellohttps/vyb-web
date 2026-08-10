#!/usr/bin/env python3
"""Assemble /Users/b/Projects/vyb-web/pulse.html from site.css + pulse_extra.css + pulse_body.html."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/Users/b/Projects/vyb-web/pulse.html'

css   = open(os.path.join(HERE, 'site.css')).read()
extra = open(os.path.join(HERE, 'pulse_extra.css')).read()
body  = open(os.path.join(HERE, 'pulse_body.html'), encoding='utf-8').read()

js = """(function () {
  'use strict';
  var html = document.documentElement;
  var KEY = 'vyb-theme';
  var toggle = document.getElementById('themeToggle');
  var meta = document.getElementById('themeColorMeta');
  var mq = window.matchMedia('(prefers-color-scheme: dark)');

  function apply(dark) {
    html.setAttribute('data-theme', dark ? 'dark' : 'light');
    if (meta) meta.setAttribute('content', dark ? '#000000' : '#ffffff');
  }
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}
  var dark = stored ? stored === 'dark' : mq.matches;
  apply(dark);

  if (toggle) {
    toggle.addEventListener('click', function () {
      dark = !dark;
      apply(dark);
      try { localStorage.setItem(KEY, dark ? 'dark' : 'light'); } catch (e) {}
    });
  }
  mq.addEventListener('change', function (e) {
    if (!stored) { dark = e.matches; apply(dark); }
  });

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var io = document.querySelectorAll('[data-io]');
  if (reduce || !('IntersectionObserver' in window)) {
    io.forEach(function (el) { el.classList.add('in'); });
  } else {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); obs.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    io.forEach(function (el) { obs.observe(el); });
  }

  /* transparent nav while over the dark hero */
  var hero = document.querySelector('.pl-hero');
  if (hero) {
    var syncNav = function () {
      var over = window.scrollY < hero.offsetHeight - 56;
      document.body.classList.toggle('nav-over', over);
    };
    syncNav();
    window.addEventListener('scroll', syncNav, { passive: true });
    window.addEventListener('resize', syncNav);
  }

  /* rail scrollspy */
  var rail = document.getElementById('plRail');
  if (rail) {
    var links = [].slice.call(rail.querySelectorAll('a'));
    var secs = links.map(function (a) { return document.querySelector(a.getAttribute('href')); });
    if (links.length) { links[0].classList.add('on'); }
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var i = secs.indexOf(e.target);
        if (i < 0) return;
        links.forEach(function (l) { l.classList.remove('on'); });
        links[i].classList.add('on');
      });
    }, { rootMargin: '-12% 0px -72% 0px' });
    secs.forEach(function (s) { if (s) spy.observe(s); });
  }
})();"""

TITLE = "VYB Pulse — Artist development &amp; financial infrastructure"
DESC = ("VYB Pulse is VYB's artist development initiative: non-recoupable development capital, "
        "mentorship and the VYB financial stack for a small cohort of independent artists. "
        "No equity, nothing recouped.")

page = f"""<!DOCTYPE html>
<html lang="en" data-theme="light"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#ffffff" id="themeColorMeta">
<meta name="color-scheme" content="light dark">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="VYB Pulse — Artist development &amp; financial infrastructure">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://vybapp.io/pulse">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://vybapp.io/pulse">
<style>{css}{extra}</style>
</head>
<body>
{body}
<script>
{js}
</script>
</body></html>
"""

open(OUT, 'w', encoding='utf-8').write(page)
print(f"wrote {OUT} ({len(page)} bytes)")
