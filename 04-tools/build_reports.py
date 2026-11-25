#!/usr/bin/env python3
"""Build readable Daily Learning reports and the workspace dashboard."""
from pathlib import Path
from html import escape
import csv
import os
import re

ROOT = Path(__file__).resolve().parents[1]

CSS = '''<style>
:root{
  --bg-1:#e9f3f0;
  --bg-2:#d9eae4;
  --bg-3:#cbe1da;
  --shell:rgba(255,255,255,.46);
  --shell-border:rgba(255,255,255,.78);
  --sidebar:rgba(255,255,255,.62);
  --glass:rgba(255,255,255,.66);
  --glass-border:rgba(255,255,255,.84);
  --ink:#10241e;
  --ink-soft:#3d574f;
  --muted:#678077;
  --accent:#1f7a63;
  --accent-2:#34b592;
  --accent-soft:rgba(31,122,99,.12);
  --sky:#4b89a8;
  --amber:#b86e22;
  --amber-bg:rgba(184,110,34,.14);
  --good-bg:rgba(31,122,99,.13);
  --good-ink:#16614e;
  --dark-1:#112922;
  --dark-2:#091713;
  --radius-xl:28px;
  --radius-lg:22px;
  --radius-md:16px;
  --shadow-shell:0 28px 70px rgba(16,48,39,.12),0 2px 8px rgba(16,48,39,.05);
  --shadow-card:0 10px 28px rgba(18,54,44,.065);
  --shadow-pill:0 8px 22px rgba(20,68,55,.12),0 1px 3px rgba(20,68,55,.07);
  --font:-apple-system,BlinkMacSystemFont,"SF Pro Display","Inter","Segoe UI",Roboto,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;min-height:100%}
body{
  font:14px/1.6 var(--font);
  color:var(--ink);
  background:
    radial-gradient(920px 620px at 8% 5%, rgba(255,255,255,.92), transparent 60%),
    radial-gradient(760px 560px at 92% 16%, rgba(114,205,179,.32), transparent 60%),
    radial-gradient(720px 540px at 72% 94%, rgba(121,179,204,.26), transparent 62%),
    linear-gradient(135deg, var(--bg-1) 0%, var(--bg-2) 52%, var(--bg-3) 100%);
  padding:22px;
  -webkit-font-smoothing:antialiased;
}
a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:3px;font-weight:600}
code{font-family:var(--mono);font-size:12px;background:rgba(31,122,99,.09);color:#145645;border-radius:6px;padding:2px 6px}
.shell{
  max-width:1320px;
  margin:0 auto;
  display:grid;
  grid-template-columns:228px minmax(0,1fr);
  gap:20px;
  padding:18px;
  border-radius:var(--radius-xl);
  background:var(--shell);
  backdrop-filter:blur(26px);
  -webkit-backdrop-filter:blur(26px);
  border:1px solid var(--shell-border);
  box-shadow:var(--shadow-shell);
  min-height:calc(100vh - 44px);
}
/* 01 Sidebar & Liquid Pill */
.sidebar{
  display:flex;
  flex-direction:column;
  justify-content:space-between;
  padding:18px 12px 14px;
  border-radius:var(--radius-lg);
  background:var(--sidebar);
  border:1px solid rgba(255,255,255,.8);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.88);
}
.brand{display:flex;align-items:center;gap:11px;padding:4px 10px 20px}
.brand-mark{
  width:34px;height:34px;border-radius:11px;
  background:linear-gradient(135deg,#2fa987 0%,#15614e 100%);
  box-shadow:0 6px 14px rgba(21,97,78,.28),inset 0 1px 1px rgba(255,255,255,.5);
  display:grid;place-items:center;color:#fff;font-weight:800;font-size:13px;flex:0 0 auto;
}
.brand-name{font-size:15px;font-weight:750;letter-spacing:-.02em;line-height:1.2}
.brand-sub{font-size:11px;color:var(--muted)}
.nav-wrap{position:relative;display:flex;flex-direction:column;gap:4px}
.nav-pill{
  position:absolute;left:0;right:0;height:42px;border-radius:999px;
  background:rgba(255,255,255,.96);border:1px solid #fff;box-shadow:var(--shadow-pill);
  pointer-events:none;
  transition:transform .46s cubic-bezier(.34,1.38,.64,1),height .3s ease;
  z-index:0;
}
.nav-item{
  position:relative;z-index:1;display:flex;align-items:center;gap:10px;height:42px;padding:0 14px;
  border:0;background:transparent;color:var(--ink-soft);font:550 13.5px var(--font);
  border-radius:999px;cursor:pointer;text-align:left;transition:color .2s ease;
}
.nav-item:hover{color:var(--ink)}
.nav-item.active{color:var(--ink);font-weight:700}
.nav-item svg{width:16px;height:16px;stroke:currentColor;fill:none;stroke-width:1.85;flex:0 0 auto;opacity:.8}
.nav-item.active svg{opacity:1;stroke:var(--accent)}
.nav-count{
  margin-left:auto;font-size:11px;font-weight:700;color:var(--muted);
  background:rgba(16,36,30,.07);padding:2px 7px;border-radius:999px;
}
.nav-item.active .nav-count{background:var(--accent-soft);color:var(--accent)}
.sidebar-foot{
  margin-top:20px;padding:12px;border-radius:16px;
  background:rgba(255,255,255,.72);border:1px solid rgba(255,255,255,.9);
  display:flex;align-items:center;gap:10px;
}
.avatar{
  width:34px;height:34px;border-radius:999px;
  background:linear-gradient(135deg,#2ea685,#3e7f9c);
  color:#fff;font-weight:750;font-size:12px;display:grid;place-items:center;flex:0 0 auto;
}
.foot-title{font-size:12.5px;font-weight:700;line-height:1.25;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.foot-sub{font-size:11px;color:var(--muted)}
/* Main & Topbar */
.main{display:flex;flex-direction:column;gap:16px;min-width:0;padding:4px 4px 8px}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;padding:4px 4px 2px}
.title-block h1{margin:0;font-size:clamp(22px,2.5vw,28px);font-weight:780;letter-spacing:-.03em;line-height:1.15}
.title-sub{margin:3px 0 0;font-size:12.5px;color:var(--muted)}
.toolbar{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
/* 04 Liquid Split Filter & Crisp SVG Search */
.split-wrap{
  display:inline-flex;align-items:center;gap:6px;padding:4px;border-radius:999px;
  background:rgba(255,255,255,.64);border:1px solid rgba(255,255,255,.88);
  box-shadow:0 4px 14px rgba(16,48,39,.06);
}
.split-trigger,.split-chip,.icon-btn{border:0;font:600 12.5px var(--font);cursor:pointer;transition:all .26s cubic-bezier(.34,1.35,.64,1)}
.split-trigger{
  display:inline-flex;align-items:center;gap:6px;padding:7px 14px;border-radius:999px;
  background:#fff;color:var(--ink);box-shadow:0 3px 10px rgba(16,48,39,.08);
}
.split-trigger:hover{transform:translateY(-1px)}
.split-chips{
  display:flex;align-items:center;gap:4px;max-width:0;opacity:0;overflow:hidden;
  transition:max-width .45s cubic-bezier(.22,1,.36,1),opacity .28s ease;
}
.split-wrap.open .split-chips{max-width:520px;opacity:1;padding-right:4px}
.split-chip{padding:6px 11px;border-radius:999px;background:rgba(255,255,255,.78);color:var(--ink-soft);white-space:nowrap;transform:scale(.86)}
.split-wrap.open .split-chip{transform:scale(1)}
.split-chip:hover{background:#fff;color:var(--ink)}
.split-chip.active{background:var(--accent);color:#fff;box-shadow:0 4px 12px rgba(31,122,99,.28)}
.icon-btn{
  width:38px;height:38px;border-radius:999px;display:grid;place-items:center;
  background:rgba(255,255,255,.8);border:1px solid rgba(255,255,255,.92);color:var(--ink-soft);
  box-shadow:0 4px 12px rgba(16,48,39,.06);
}
.icon-btn svg{width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.icon-btn:hover{background:#fff;color:var(--ink);transform:translateY(-1px)}
.search-box{
  display:none;align-items:center;background:rgba(255,255,255,.92);border:1px solid #fff;
  border-radius:999px;padding:0 14px;height:38px;
}
.search-box.open{display:inline-flex}
.search-box input{border:0;outline:0;background:transparent;font:13px var(--font);color:var(--ink);width:170px}
/* Bento & 02 Light Follow + 3D Tilt */
.bento{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:16px;align-items:stretch}
.card{
  position:relative;border-radius:var(--radius-lg);background:var(--glass);
  backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px);
  border:1px solid var(--glass-border);box-shadow:var(--shadow-card);padding:20px;
  overflow:hidden;transform-style:preserve-3d;
  transition:transform .28s cubic-bezier(.22,1,.36,1),box-shadow .28s ease,opacity .25s ease;
  --mx:50%;--my:50%;
}
.card::before{
  content:"";position:absolute;inset:0;border-radius:inherit;
  background:radial-gradient(300px circle at var(--mx) var(--my), rgba(255,255,255,.65), transparent 64%);
  opacity:0;pointer-events:none;transition:opacity .28s ease;z-index:0;
}
.card::after{
  content:"";position:absolute;inset:0;border-radius:inherit;padding:1.25px;
  background:radial-gradient(220px circle at var(--mx) var(--my), rgba(255,255,255,.98), rgba(52,181,146,.34) 45%, transparent 72%);
  -webkit-mask:linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;
  opacity:0;pointer-events:none;transition:opacity .28s ease;z-index:2;
}
.card:hover::before,.card:hover::after{opacity:1}
.card:hover{box-shadow:0 18px 40px rgba(16,48,39,.11)}
.card > *{position:relative;z-index:1}
/* Deep Pine Hero Card */
.card-dark{
  background:
    radial-gradient(260px circle at 92% 10%, rgba(52,211,153,.24), transparent 62%),
    linear-gradient(155deg, var(--dark-1) 0%, var(--dark-2) 78%);
  border:1px solid rgba(167,243,208,.16);color:#eefaf5;
  box-shadow:0 18px 42px rgba(9,23,19,.24);
}
.card-dark::before{background:radial-gradient(280px circle at var(--mx) var(--my), rgba(110,231,183,.16), transparent 64%)}
.card-dark::after{background:radial-gradient(220px circle at var(--mx) var(--my), rgba(110,231,183,.58), transparent 70%)}
.card-dark .card-title{color:#eefaf5}
.card-dark .card-sub,.card-dark .muted{color:rgba(238,250,245,.66)}
.card-dark a{color:#6ee7b7}
.card-dark .expand-btn{background:rgba(255,255,255,.1);color:#fff;border-color:rgba(255,255,255,.18)}
.card-dark .expand-btn:hover{background:rgba(255,255,255,.2)}
.span-3{grid-column:span 3}.span-4{grid-column:span 4}.span-5{grid-column:span 5}
.span-6{grid-column:span 6}.span-7{grid-column:span 7}.span-8{grid-column:span 8}.span-12{grid-column:span 12}
/* KPI */
.kpi-label{font-size:12.5px;color:var(--muted);font-weight:600}
.kpi-row{display:flex;align-items:flex-end;justify-content:space-between;gap:10px;margin-top:8px}
.kpi-val{font-size:30px;font-weight:780;letter-spacing:-.04em;line-height:1.05;font-variant-numeric:tabular-nums}
.kpi-foot{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:12px}
.kpi-pill{
  display:inline-flex;align-items:center;padding:3px 9px;border-radius:999px;font-size:11px;font-weight:650;
  background:linear-gradient(135deg,#259276,#196d57);color:#fff;white-space:nowrap;
}
.kpi-pill.soft{background:rgba(16,36,30,.08);color:var(--ink-soft)}
.kpi-pill.warn{background:var(--amber-bg);color:var(--amber)}
.spark{width:68px;height:22px;overflow:visible}
.spark path{fill:none;stroke:var(--accent-2);stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
/* Card Header & 03 Expand in Place */
.card-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:14px}
.card-title{margin:0;font-size:16px;font-weight:730;letter-spacing:-.02em}
.card-sub{margin:2px 0 0;font-size:12px;color:var(--muted)}
.card-head-right{display:flex;align-items:center;gap:8px;flex-shrink:0}
.big-stat{font-size:24px;font-weight:760;letter-spacing:-.03em;font-variant-numeric:tabular-nums;color:var(--accent)}
.expand-btn{
  width:30px;height:30px;border-radius:999px;border:1px solid rgba(16,36,30,.14);
  background:rgba(255,255,255,.82);color:var(--ink-soft);display:grid;place-items:center;
  cursor:pointer;font-size:14px;font-weight:600;line-height:1;flex:0 0 auto;transition:all .2s ease;
}
.expand-btn:hover{background:#fff;color:var(--ink);transform:scale(1.06)}
.mini-stat-badge{
  display:none;align-items:center;padding:3px 9px;border-radius:999px;font-size:11.5px;font-weight:700;
  background:var(--accent-soft);color:var(--accent);width:fit-content;margin-top:8px;
}
.bento.has-expanded .card:not(.is-expanded){
  grid-column:span 3;padding:16px;cursor:pointer;opacity:.88;
  display:flex;flex-direction:column;justify-content:space-between;min-height:124px;
}
.bento.has-expanded .card:not(.is-expanded) .hide-mini,
.bento.has-expanded .card:not(.is-expanded) .big-stat{display:none}
.bento.has-expanded .card:not(.is-expanded) .mini-stat-badge{display:inline-flex}
.bento.has-expanded .card:not(.is-expanded) .card-head{margin-bottom:8px;gap:8px}
.bento.has-expanded .card:not(.is-expanded) .card-head > div:first-child{min-width:0;flex:1}
.bento.has-expanded .card:not(.is-expanded) .card-title{font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bento.has-expanded .card:not(.is-expanded) .card-sub{
  font-size:11.5px;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-top:4px;
}
.bento.has-expanded .card:not(.is-expanded) .dark-hero-num{font-size:24px;margin:4px 0 0}
.bento.has-expanded .card:not(.is-expanded):hover{opacity:1;transform:translateY(-2px)}
.bento.has-expanded .card.is-expanded{grid-column:1 / -1;order:-1;padding:26px;box-shadow:0 24px 60px rgba(16,48,39,.15)}
.bento.has-expanded .card.is-expanded .capsule-chart{height:250px}
/* Mastery Capsule Chart */
.capsule-chart{display:flex;align-items:flex-end;justify-content:space-between;gap:14px;height:184px;padding:10px 8px 2px;transition:height .35s ease}
.capsule-col{flex:1;height:100%;display:flex;flex-direction:column;align-items:center;gap:8px;min-width:44px}
.capsule-val{font-size:12px;font-weight:750;color:var(--ink-soft);font-variant-numeric:tabular-nums}
.capsule-track{
  width:100%;max-width:28px;flex:1;border-radius:999px;background:rgba(255,255,255,.72);
  border:1px solid rgba(255,255,255,.92);display:flex;align-items:flex-end;overflow:hidden;padding:2px;
}
.capsule-fill{width:100%;border-radius:999px;background:linear-gradient(180deg,#34b592 0%,#4b89a8 100%);transition:height .55s cubic-bezier(.22,1,.36,1)}
.capsule-fill.warn{background:linear-gradient(180deg,#e0984f 0%,#c76d3b 100%)}
.capsule-lbl{font-size:11px;color:var(--muted);font-weight:600;text-align:center}
/* Dark Hero Bars & Progress */
.dark-hero-num{font-size:34px;font-weight:780;letter-spacing:-.04em;line-height:1.05;margin:4px 0 2px}
.dark-bars{display:flex;flex-direction:column;gap:12px;margin-top:16px}
.dark-bar-head{display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:5px}
.dark-bar-head span{color:rgba(238,250,245,.86)}
.dark-bar-head b{color:#fff;font-weight:650}
.dark-bar-track{height:8px;border-radius:999px;background:rgba(255,255,255,.12);overflow:hidden}
.dark-bar-track i{display:block;height:100%;border-radius:999px;background:linear-gradient(90deg,#34d399 0%,#6ee7b7 100%);transition:width .55s ease}
/* Prompts, Knowledge, Lessons & Tables */
.prompt-card{
  display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:12px 14px;border-radius:14px;background:rgba(255,255,255,.78);
  border:1px solid rgba(255,255,255,.94);margin:10px 0;
}
.prompt-card p{margin:0;font-size:13px;color:var(--ink)}
.copy-btn{
  border:1px solid rgba(31,122,99,.25);background:#fff;color:var(--accent);border-radius:999px;
  padding:6px 12px;font:650 11.5px var(--font);cursor:pointer;white-space:nowrap;flex:0 0 auto;transition:all .2s ease;
}
.copy-btn:hover{background:var(--accent);color:#fff}
.answer-box{
  background:rgba(233,243,240,.85);border:1px solid rgba(31,122,99,.18);border-radius:14px;
  padding:14px 16px;margin:10px 0;font-size:13px;
}
.answer-box p{margin:4px 0}
.k-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:12px}
.k-box{background:rgba(255,255,255,.72);border:1px solid rgba(255,255,255,.92);border-radius:16px;padding:15px}
.k-box h3{margin:0 0 8px;font-size:14px;font-weight:730;color:var(--ink)}
.k-box ul{margin:0;padding-left:18px}
.k-box li{margin:5px 0;font-size:13px}
details.lesson{
  border:1px solid rgba(16,36,30,.12);border-radius:14px;margin:10px 0;background:rgba(255,255,255,.76);overflow:hidden;
}
details.lesson summary{
  display:flex;align-items:center;justify-content:space-between;gap:14px;padding:14px 16px;
  font-size:15px;font-weight:700;color:var(--ink);cursor:pointer;list-style:none;
}
details.lesson[open] summary{border-bottom:1px solid rgba(16,36,30,.1);background:rgba(233,243,240,.55)}
.lesson-body{padding:16px}
.lesson-body p{margin:0 0 10px}
.pill{
  display:inline-flex;align-items:center;border-radius:999px;padding:3px 10px;
  font-size:11.5px;font-weight:700;background:var(--accent-soft);color:var(--accent);white-space:nowrap;
}
.pill.warn{background:var(--amber-bg);color:var(--amber)}
.record-id,.path-note{display:block;color:var(--muted);font-size:11.5px;font-weight:500;margin-top:2px;font-family:var(--mono);word-break:break-word}
.table-wrap{overflow:auto;border-radius:14px;border:1px solid rgba(16,36,30,.12);background:rgba(255,255,255,.74)}
table{width:100%;border-collapse:collapse;min-width:640px}
th,td{padding:11px 13px;text-align:left;vertical-align:top;border-bottom:1px solid rgba(16,36,30,.09);font-size:13px}
th{background:rgba(230,242,238,.85);color:var(--ink-soft);font-size:11px;font-weight:750;text-transform:uppercase;letter-spacing:.05em;cursor:pointer;user-select:none}
th:hover{color:var(--accent)}
tr:last-child td{border-bottom:0}
tbody tr{transition:background .16s ease,opacity .16s ease}
tbody tr[draggable="true"]{cursor:grab}
tbody tr.dragging{opacity:.45}
tbody tr.drag-over-row td{border-top:2px solid var(--accent)}
tbody tr:hover td{background:rgba(255,255,255,.7)}
.drag-grip{display:inline-block;margin-right:6px;color:var(--muted);opacity:.45;font-size:12px;letter-spacing:-1px;user-select:none}
tbody tr:hover .drag-grip{opacity:.95;color:var(--accent)}
.muted{color:var(--muted);font-size:12.5px}
.nav-links{display:flex;flex-wrap:wrap;gap:12px;margin-top:10px}
.foot-note{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;padding:6px 6px 0;font-size:12px;color:var(--muted)}
.toast{
  position:fixed;right:26px;bottom:26px;background:#10241e;color:#eefaf5;padding:10px 16px;
  border-radius:999px;font-size:12.5px;font-weight:600;box-shadow:0 12px 30px rgba(9,23,19,.28);
  opacity:0;transform:translateY(10px);pointer-events:none;transition:all .25s ease;z-index:99;
}
.toast.show{opacity:1;transform:translateY(0)}
.hidden-sec{display:none !important}
@media(max-width:980px){
  .shell{grid-template-columns:1fr;padding:14px}
  .sidebar{flex-direction:row;align-items:center;flex-wrap:wrap;padding:12px}
  .brand{padding:0 8px 0 0}
  .nav-wrap{flex-direction:row;flex-wrap:wrap}
  .nav-pill{display:none}
  .nav-item.active{background:#fff;box-shadow:var(--shadow-pill)}
  .sidebar-foot{display:none}
  .span-3{grid-column:span 6}.span-5,.span-6,.span-7,.span-4,.span-8{grid-column:span 12}
}
@media(max-width:620px){
  body{padding:10px}.span-3{grid-column:span 12}.prompt-card{flex-direction:column;align-items:flex-start}
}
</style>'''

JS = '''<script>
(() => {
  const navPill = document.getElementById('nav-pill');
  const navItems = Array.from(document.querySelectorAll('.nav-item'));
  const bento = document.getElementById('bento');
  const cards = Array.from(document.querySelectorAll('.card[data-tilt]'));
  const splitWrap = document.getElementById('split-wrap');
  const splitTrigger = document.getElementById('split-trigger');
  const splitLabel = document.getElementById('split-label');
  const searchToggle = document.getElementById('search-toggle');
  const searchBox = document.getElementById('search-box');
  const searchInput = document.getElementById('search-input');
  const toast = document.getElementById('toast');

  let activeFilter = 'ALL';
  let searchQuery = '';

  function showToast(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(showToast._t);
    showToast._t = setTimeout(() => toast.classList.remove('show'), 2200);
  }

  /* 01 Liquid Pill Navigation */
  function positionPill(btn) {
    if (!navPill || !btn) return;
    navPill.style.transform = `translateY(${btn.offsetTop}px)`;
    navPill.style.height = `${btn.offsetHeight}px`;
  }

  function setSection(section) {
    clearExpand();
    navItems.forEach((btn) => {
      const on = btn.dataset.section === section;
      btn.classList.toggle('active', on);
      if (on) positionPill(btn);
    });
    document.querySelectorAll('[data-groups]').forEach((el) => {
      const groups = (el.dataset.groups || '').split(' ');
      el.classList.toggle('hidden-sec', !groups.includes(section));
    });
  }

  navItems.forEach((btn) => btn.addEventListener('click', () => setSection(btn.dataset.section)));
  window.addEventListener('resize', () => {
    const active = navItems.find((b) => b.classList.contains('active'));
    if (active) positionPill(active);
  });
  requestAnimationFrame(() => positionPill(navItems[0]));

  /* 02 Light Follow + Subtle 3D Tilt (<= 3.2deg) */
  cards.forEach((card) => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      card.style.setProperty('--mx', `${x}px`);
      card.style.setProperty('--my', `${y}px`);
      if (card.classList.contains('is-expanded')) {
        card.style.transform = '';
        return;
      }
      const nx = (x / rect.width - 0.5) * 2;
      const ny = (y / rect.height - 0.5) * 2;
      card.style.transform = `perspective(920px) rotateX(${(-ny * 3.0).toFixed(2)}deg) rotateY(${(nx * 3.0).toFixed(2)}deg) translateY(-2px)`;
    });
    card.addEventListener('mouseleave', () => { card.style.transform = ''; });
  });

  /* 03 Expand in Place */
  function clearExpand() {
    if (!bento) return;
    bento.classList.remove('has-expanded');
    document.querySelectorAll('.card.is-expanded').forEach((c) => {
      c.classList.remove('is-expanded');
      const btn = c.querySelector('.expand-btn');
      if (btn) btn.textContent = '⤢';
    });
  }

  function toggleExpand(card) {
    const already = card.classList.contains('is-expanded');
    clearExpand();
    if (!already && bento) {
      bento.classList.add('has-expanded');
      card.classList.add('is-expanded');
      card.style.transform = '';
      const btn = card.querySelector('.expand-btn');
      if (btn) btn.textContent = '×';
    }
  }

  document.querySelectorAll('.expand-btn').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const card = btn.closest('.card');
      if (card) toggleExpand(card);
    });
  });

  document.querySelectorAll('.card[data-expandable]').forEach((card) => {
    card.addEventListener('click', () => {
      if (bento && bento.classList.contains('has-expanded') && !card.classList.contains('is-expanded')) {
        toggleExpand(card);
      }
    });
  });

  /* 04 Liquid Split Filter & Search */
  if (splitTrigger && splitWrap) {
    splitTrigger.addEventListener('click', () => splitWrap.classList.toggle('open'));
    document.querySelectorAll('.split-chip').forEach((chip) => {
      chip.addEventListener('click', () => {
        activeFilter = chip.dataset.filter || 'ALL';
        document.querySelectorAll('.split-chip').forEach((c) => c.classList.toggle('active', c === chip));
        if (splitLabel) splitLabel.textContent = activeFilter === 'ALL' ? 'All Records' : chip.textContent;
        applyFilters();
      });
    });
  }

  if (searchToggle && searchBox && searchInput) {
    searchToggle.addEventListener('click', () => {
      searchBox.classList.toggle('open');
      if (searchBox.classList.contains('open')) searchInput.focus();
    });
    searchInput.addEventListener('input', (e) => {
      searchQuery = (e.target.value || '').trim().toLowerCase();
      applyFilters();
    });
  }

  function applyFilters() {
    document.querySelectorAll('[data-filterable]').forEach((node) => {
      const f = node.dataset.filterable || '';
      const text = (node.textContent || '').toLowerCase();
      const matchFilter = activeFilter === 'ALL' || f === activeFilter;
      const matchSearch = !searchQuery || text.includes(searchQuery);
      node.style.display = matchFilter && matchSearch ? '' : 'none';
    });
  }

  /* Copy Prompt & Answer Template Buttons */
  document.querySelectorAll('.copy-btn').forEach((btn) => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const text = btn.dataset.copy || '';
      try {
        await navigator.clipboard.writeText(text);
        showToast('Copied — paste into Agent chat');
      } catch {
        showToast(text);
      }
    });
  });

  /* Sortable & Draggable Review History Table */
  const reviewTable = document.querySelector('#review-table');
  if (reviewTable) {
    const tbody = reviewTable.querySelector('tbody');
    let draggedRow = null;
    if (tbody) {
      tbody.querySelectorAll('tr[draggable="true"]').forEach((row) => {
        row.addEventListener('dragstart', (e) => {
          draggedRow = row;
          row.classList.add('dragging');
          e.dataTransfer.effectAllowed = 'move';
        });
        row.addEventListener('dragend', () => {
          row.classList.remove('dragging');
          tbody.querySelectorAll('.drag-over-row').forEach((r) => r.classList.remove('drag-over-row'));
          draggedRow = null;
        });
        row.addEventListener('dragover', (e) => {
          if (!draggedRow || draggedRow === row) return;
          e.preventDefault();
          row.classList.add('drag-over-row');
        });
        row.addEventListener('dragleave', () => row.classList.remove('drag-over-row'));
        row.addEventListener('drop', (e) => {
          e.preventDefault();
          row.classList.remove('drag-over-row');
          if (!draggedRow || draggedRow === row) return;
          const rect = row.getBoundingClientRect();
          const after = e.clientY > rect.top + rect.height / 2;
          tbody.insertBefore(draggedRow, after ? row.nextSibling : row);
          showToast('Review priority order updated');
        });
      });

      reviewTable.querySelectorAll('thead th').forEach((th, idx) => {
        th.addEventListener('click', () => {
          const asc = th.dataset.sortDir !== 'asc';
          th.dataset.sortDir = asc ? 'asc' : 'desc';
          const rows = Array.from(tbody.querySelectorAll('tr[draggable="true"]'));
          rows.sort((a, b) => {
            const va = (a.children[idx]?.textContent || '').trim().toLowerCase();
            const vb = (b.children[idx]?.textContent || '').trim().toLowerCase();
            return asc ? va.localeCompare(vb) : vb.localeCompare(va);
          });
          rows.forEach((r) => tbody.appendChild(r));
        });
      });
    }
  }
})();
</script>'''


def read_rows(path):
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def meta(path):
    text = path.read_text(encoding='utf-8')
    out = {'title': text.splitlines()[0].lstrip('# ').strip()}
    for line in text.splitlines():
        match = re.match(r'- ([^:]+):\s*(.*)', line)
        if match:
            out[match.group(1).strip().lower()] = match.group(2).strip()
    return out


def section(text, name):
    match = re.search(rf'^## {re.escape(name)}\s*$\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    return match.group(1).strip() if match else ''


def count_knowledge_items(text, name):
    value = section(text, name)
    normalized = re.sub(r'^[-*]\s*', '', value.strip()).strip().lower()
    if not value or normalized in ('none', 'none yet', 'none yet.'):
        return 0
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    return len(lines)


def blocks(value):
    parts = []
    bullets = []

    def inline(text):
        return re.sub(r'`([^`]+)`', r'<code>\1</code>', escape(text))

    def flush():
        nonlocal bullets
        if bullets:
            parts.append('<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in bullets) + '</ul>')
            bullets = []

    for raw in value.splitlines():
        line = raw.strip()
        if line.startswith('- '):
            bullets.append(line[2:])
        elif not line:
            flush()
        else:
            flush()
            parts.append(f'<p>{inline(line)}</p>')
    flush()
    return ''.join(parts) or '<p class="muted">Nothing recorded.</p>'


def knowledge_block(text, name, empty_message):
    value = section(text, name)
    normalized = re.sub(r'^[-*]\s*', '', value.strip()).strip().lower()
    if not value or normalized in ('none', 'none yet', 'none yet.'):
        return f'<p class="muted">{escape(empty_message)}</p>'
    return blocks(value)


def mastery_chart(rows):
    if not rows:
        return '<p class="muted">No lessons recorded yet. Create your first Sprint through Agent chat.</p>'
    buckets = [
        ("Demonstrated", sum(r.get('mastery_status') == 'demonstrated' for r in rows), False),
        ("Emerging", sum(r.get('mastery_status') == 'emerging' for r in rows), False),
        ("Needs Review", sum(r.get('mastery_status') == 'needs_review' for r in rows), True),
        ("Unassessed", sum(r.get('mastery_status') in ('', 'unassessed') for r in rows), False),
    ]
    maximum = max(count for _, count, _ in buckets) or 1
    cols = []
    for label, count, is_warn in buckets:
        h = max(14, round(100 * count / maximum)) if count else 8
        cls = 'capsule-fill warn' if is_warn else 'capsule-fill'
        cols.append(
            f'<div class="capsule-col">'
            f'<span class="capsule-val">{count}</span>'
            f'<div class="capsule-track"><div class="{cls}" style="height:{h}%"></div></div>'
            f'<span class="capsule-lbl">{escape(label)}</span>'
            f'</div>'
        )
    return f'<div class="capsule-chart">{"".join(cols)}</div>'


def submission_guidance(practice, lesson_title):
    numbers = re.findall(r'^\s*(\d+)\.\s+', practice, re.M)
    if numbers:
        prompts_html = ''.join(f'<p>{escape(number)}. Your answer:</p>' for number in numbers)
        plain_template = f'Submitting practice for "{lesson_title}":\n' + '\n'.join(f'{n}. ' for n in numbers)
    else:
        prompts_html = '<p>My response:</p><p>My reasoning or notes:</p><p>What I am unsure about:</p>'
        plain_template = f'Submitting practice for "{lesson_title}":\nMy response:\nMy reasoning:\nWhat I am unsure about:'
    return (
        f'<div class="answer-box">'
        f'<div style="display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:8px">'
        f'<strong>Submit in Agent chat</strong>'
        f'<button type="button" class="copy-btn" data-copy="{escape(plain_template, quote=True)}">Copy Answer Template</button>'
        f'</div>'
        f'<p>Reply in the same Agent conversation with your answers. The Agent will record the submission, review it, and update your knowledge, weak points, and next Session.</p>'
        f'<p><strong>Copy this answer format if useful:</strong></p>'
        f'{prompts_html}'
        f'<p class="muted" style="margin-top:8px">The HTML report is for reading and progress review. You do not need to edit files or open a separate answer page.</p>'
        f'</div>'
    )


def report(sprint, sample):
    info = meta(sprint / 'learning-plan.md')
    rows = read_rows(sprint / 'progress.csv')
    mistakes = read_rows(sprint / 'mistakes.csv')
    knowledge = (sprint / 'knowledge.md').read_text(encoding='utf-8')
    lesson_titles = {row['lesson_id']: row['title'] for row in rows}
    done = [row for row in rows if row['status'] == 'completed']
    upcoming = next((row for row in rows if row['status'] != 'completed'), None)
    pct = round(100 * len(done) / len(rows)) if rows else 0
    dem_count = count_knowledge_items(knowledge, 'Demonstrated')
    rev_count = count_knowledge_items(knowledge, 'Needs review')

    lessons = []
    for row in done:
        text = (sprint / row['evidence_path']).read_text(encoding='utf-8')
        m_status = row['mastery_status'].replace('_', ' ')
        pill_cls = 'pill warn' if row['mastery_status'] == 'needs_review' else 'pill'
        lessons.append(
            f'<details class="lesson" data-filterable="{escape(row["mastery_status"])}">'
            f'<summary><span>{escape(row["title"])}<small class="record-id">Internal lesson ID: {escape(row["lesson_id"])}</small></span>'
            f'<span class="{pill_cls}">{escape(m_status)}</span></summary>'
            f'<div class="lesson-body">'
            f'<p><strong>What was learned.</strong></p>{blocks(section(text, "Learning content"))}'
            f'<p><strong>Practice.</strong></p>{blocks(section(text, "Practice"))}'
            f'<p><strong>Learner submission.</strong></p>{blocks(section(text, "Learner submission"))}'
            f'<p><strong>Feedback.</strong></p>{blocks(section(text, "Feedback"))}'
            f'<p><a href="{escape(row["evidence_path"])}">Open {escape(row["title"])}</a></p>'
            f'<p class="path-note">File: {escape(row["evidence_path"])}</p>'
            f'</div></details>'
        )

    if mistakes:
        mistake_rows = ''.join(
            f'<tr draggable="true" data-filterable="{escape(x["status"])}">'
            f'<td><span class="drag-grip" aria-hidden="true">⋮⋮</span><strong>{escape(x["concept"])}</strong><span class="record-id">Internal mistake ID: {escape(x["mistake_id"])}</span></td>'
            f'<td>{escape(lesson_titles.get(x["lesson_id"], "Related lesson"))}<span class="record-id">Internal lesson ID: {escape(x["lesson_id"])}</span></td>'
            f'<td>{escape(x["learner_response"])}</td>'
            f'<td>{escape(x["feedback"])}</td>'
            f'<td><span class="pill {"warn" if x["status"] != "resolved" else ""}">{escape(x["status"].replace("_", " "))}</span><br><span class="muted">{escape(x["next_review"])}</span></td>'
            f'</tr>'
            for x in mistakes
        )
    else:
        mistake_rows = '<tr><td colspan="5" class="muted">No mistake or review record yet.</td></tr>'

    if upcoming:
        text = (sprint / upcoming['evidence_path']).read_text(encoding='utf-8')
        practice = section(text, 'Practice')
        continue_prompt = f'Let’s continue Daily Learning on "{upcoming["title"]}".'
        next_html = (
            f'<div class="prompt-card">'
            f'<div><strong>{escape(upcoming["title"])}</strong><span class="record-id">Internal lesson ID: {escape(upcoming["lesson_id"])}</span></div>'
            f'<button type="button" class="copy-btn" data-copy="{escape(continue_prompt, quote=True)}">Copy Continue Prompt</button>'
            f'</div>'
            f'{blocks(section(text, "Learning content"))}'
            f'<p><strong>Practice task.</strong></p>{blocks(practice)}'
            f'<p><strong>Next action.</strong> {escape(upcoming["next_action"])}</p>'
            f'{submission_guidance(practice, upcoming["title"])}'
        )
    else:
        next_html = '<h3>Sprint complete</h3><p>Review the remaining weak points, then choose a follow-on goal that uses the demonstrated skills.</p>'

    dashboard_rel = os.path.relpath(ROOT / 'dashboard.html', sprint).replace(os.sep, '/')
    footer = 'Sample report · Illustrative learning record' if sample else 'Daily Learning · Personal learning record'

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(info["title"])} | Learning Report</title>
{CSS}
</head>
<body>
<div class="shell">
  <aside class="sidebar" aria-label="Report Navigation">
    <div>
      <div class="brand">
        <div class="brand-mark">DL</div>
        <div>
          <div class="brand-name">Daily Learning</div>
          <div class="brand-sub">Sprint Report</div>
        </div>
      </div>
      <nav class="nav-wrap">
        <div class="nav-pill" id="nav-pill"></div>
        <button type="button" class="nav-item active" data-section="overview">
          <svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>
          Overview
        </button>
        <button type="button" class="nav-item" data-section="next">
          <svg viewBox="0 0 24 24"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          Next Step
        </button>
        <button type="button" class="nav-item" data-section="knowledge">
          <svg viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          Knowledge
          <span class="nav-count">{dem_count}</span>
        </button>
        <button type="button" class="nav-item" data-section="sessions">
          <svg viewBox="0 0 24 24"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
          Sessions
          <span class="nav-count">{len(done)}</span>
        </button>
        <button type="button" class="nav-item" data-section="review">
          <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/></svg>
          Review
          <span class="nav-count">{len(mistakes)}</span>
        </button>
      </nav>
    </div>
    <div class="sidebar-foot">
      <div class="avatar">{pct}%</div>
      <div style="min-width:0">
        <div class="foot-title">{escape(info["title"])}</div>
        <div class="foot-sub">{len(done)}/{len(rows)} Sessions</div>
      </div>
    </div>
  </aside>

  <main class="main">
    <header class="topbar">
      <div class="title-block">
        <h1>{escape(info["title"])}</h1>
        <p class="title-sub">{escape(info.get("goal", ""))}</p>
      </div>
      <div class="toolbar">
        <div class="split-wrap" id="split-wrap">
          <button type="button" class="split-trigger" id="split-trigger">
            <span id="split-label">All Records</span>
            <span style="opacity:.55">⌄</span>
          </button>
          <div class="split-chips">
            <button type="button" class="split-chip active" data-filter="ALL">All</button>
            <button type="button" class="split-chip" data-filter="demonstrated">Demonstrated</button>
            <button type="button" class="split-chip" data-filter="emerging">Emerging</button>
            <button type="button" class="split-chip" data-filter="needs_review">Needs Review</button>
          </div>
        </div>
        <div class="search-box" id="search-box">
          <input type="search" id="search-input" placeholder="Search lessons or mistakes..." aria-label="Search records">
        </div>
        <button type="button" class="icon-btn" id="search-toggle" title="Search records" aria-label="Search records">
          <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
        </button>
      </div>
    </header>

    <div class="bento" id="bento">
      <section class="card span-3" data-tilt data-groups="overview">
        <div class="kpi-label">Completed sessions</div>
        <div class="kpi-row"><div class="kpi-val">{len(done)} / {len(rows)}</div><svg class="spark" viewBox="0 0 68 22"><path d="M2 18 L18 15 L32 13 L48 8 L66 4"/></svg></div>
        <div class="kpi-foot"><span class="kpi-pill">{pct}%</span><span class="muted">Reviewed</span></div>
      </section>
      <section class="card span-3" data-tilt data-groups="overview">
        <div class="kpi-label">Starting level</div>
        <div class="kpi-row"><div class="kpi-val" style="font-size:22px">{escape(info.get("starting level", "N/A"))}</div></div>
        <div class="kpi-foot"><span class="kpi-pill soft">{escape(info.get("session length", "Flexible"))}</span><span class="muted">Per session</span></div>
      </section>
      <section class="card span-3" data-tilt data-groups="overview">
        <div class="kpi-label">Knowledge demonstrated</div>
        <div class="kpi-row"><div class="kpi-val">{dem_count}</div><svg class="spark" viewBox="0 0 68 22"><path d="M2 17 L20 14 L36 11 L52 7 L66 3"/></svg></div>
        <div class="kpi-foot"><span class="kpi-pill">Evidence</span><span class="muted">Verified</span></div>
      </section>
      <section class="card span-3" data-tilt data-groups="overview">
        <div class="kpi-label">Needs review</div>
        <div class="kpi-row"><div class="kpi-val">{rev_count}</div></div>
        <div class="kpi-foot"><span class="kpi-pill {"warn" if rev_count else "soft"}">{len(mistakes)} Mistakes</span><span class="muted">Tracked</span></div>
      </section>

      <section class="card span-7" data-tilt data-expandable data-groups="overview">
        <div class="card-head">
          <div>
            <h2 class="card-title">Progress</h2>
            <p class="card-sub">Mastery distribution across planned sessions</p>
            <span class="mini-stat-badge">{pct}% Complete</span>
          </div>
          <div class="card-head-right">
            <span class="big-stat">{pct}%</span>
            <button type="button" class="expand-btn" title="Expand module">⤢</button>
          </div>
        </div>
        <div class="hide-mini">
          {mastery_chart(rows)}
          <p class="muted" style="margin-top:12px"><strong>Day and Session.</strong> A Day is the suggested position in the plan. A Session is one lesson, practice, and review cycle. Completed means practice was submitted and reviewed.</p>
        </div>
      </section>

      <section class="card card-dark span-5" data-tilt data-expandable data-groups="overview">
        <div class="card-head">
          <div>
            <h2 class="card-title">Sprint Overview</h2>
            <p class="card-sub">Source mode: {escape(info.get("source mode", "").replace("_", " "))}</p>
          </div>
          <div class="card-head-right"><button type="button" class="expand-btn" title="Expand module">⤢</button></div>
        </div>
        <div class="dark-hero-num">{pct}%</div>
        <div class="muted">{len(done)} of {len(rows)} sessions completed</div>
        <div class="hide-mini">
          <div class="dark-bars">
            <div class="dark-bar-row"><div class="dark-bar-head"><span>Completion</span><b>{pct}%</b></div><div class="dark-bar-track"><i style="width:{max(4, pct)}%"></i></div></div>
          </div>
          <div class="nav-links" style="margin-top:16px">
            <a href="{escape(dashboard_rel)}">Dashboard</a>
            <a href="learning-plan.md">Learning plan</a>
            <a href="sources.md">Sources</a>
          </div>
          <p class="path-note" style="color:rgba(238,250,245,.55);margin-top:8px">Files: {escape(dashboard_rel)} · learning-plan.md · sources.md</p>
        </div>
      </section>

      <section class="card span-12" data-tilt data-expandable data-groups="overview next">
        <div class="card-head">
          <div><h2 class="card-title">Next Step</h2><p class="card-sub">Current lesson, practice task, and Agent submission format</p></div>
          <div class="card-head-right"><button type="button" class="expand-btn" title="Expand module">⤢</button></div>
        </div>
        <div class="hide-mini">{next_html}</div>
      </section>

      <section class="card span-7" data-tilt data-expandable data-groups="overview knowledge">
        <div class="card-head">
          <div><h2 class="card-title">Knowledge I Can Use</h2><p class="card-sub">My Knowledge reflects reviewed learner evidence—not everything that appeared in a lesson.</p></div>
          <div class="card-head-right"><button type="button" class="expand-btn" title="Expand module">⤢</button></div>
        </div>
        <div class="hide-mini">
          <div class="k-grid">
            <div class="k-box"><h3>Demonstrated</h3>{knowledge_block(knowledge, "Demonstrated", "No demonstrated knowledge yet. Complete and review a practice first.")}</div>
            <div class="k-box"><h3>Still Developing</h3>{knowledge_block(knowledge, "Developing", "No developing knowledge has been recorded yet.")}</div>
          </div>
        </div>
      </section>

      <section class="card span-5" data-tilt data-expandable data-groups="overview knowledge">
        <div class="card-head">
          <div><h2 class="card-title">Focus Next</h2><p class="card-sub">Concepts scheduled for retrieval or review</p></div>
          <div class="card-head-right"><button type="button" class="expand-btn" title="Expand module">⤢</button></div>
        </div>
        <div class="hide-mini">{knowledge_block(knowledge, "Needs review", "No weak point or scheduled review has been recorded yet.")}</div>
      </section>

      <section class="card span-12" data-tilt data-expandable data-groups="overview sessions">
        <div class="card-head">
          <div><h2 class="card-title">Session Records</h2><p class="card-sub">Open a completed Session to read its learning content, practice, submission, and feedback</p></div>
          <div class="card-head-right"><button type="button" class="expand-btn" title="Expand module">⤢</button></div>
        </div>
        <div class="hide-mini">{"".join(lessons) if lessons else '<p class="muted">No reviewed practice yet.</p>'}</div>
      </section>

      <section class="card span-12" data-tilt data-expandable data-groups="overview review">
        <div class="card-head">
          <div><h2 class="card-title">Review History</h2><p class="card-sub">Click headers to sort or drag rows to pin priority mistakes</p></div>
          <div class="card-head-right"><button type="button" class="expand-btn" title="Expand module">⤢</button></div>
        </div>
        <div class="hide-mini">
          <div class="table-wrap">
            <table id="review-table">
              <thead><tr><th>Concept or question</th><th>Related lesson</th><th>Submission</th><th>Feedback</th><th>Status / next review</th></tr></thead>
              <tbody>{mistake_rows}</tbody>
            </table>
          </div>
        </div>
      </section>
    </div>

    <footer class="foot-note">
      <span>{footer}</span>
      <span>Plan → Learn → Practise → Review → Adapt</span>
    </footer>
  </main>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
{JS}
</body>
</html>
'''


def dashboard():
    pointer = ROOT / '01-workspace' / 'active-sprint.txt'
    active_dir = (ROOT / '01-workspace' / 'sprints' / pointer.read_text(encoding='utf-8').strip()) if pointer.is_file() else None
    if active_dir and active_dir.is_dir():
        sprint = active_dir
        info = meta(sprint / 'learning-plan.md')
        rows = read_rows(sprint / 'progress.csv')
        mistakes = read_rows(sprint / 'mistakes.csv')
        knowledge_text = (sprint / 'knowledge.md').read_text(encoding='utf-8')
        done = sum(r['status'] == 'completed' for r in rows)
        total = len(rows)
        pct = round(100 * done / total) if total else 0
        nxt = next((r for r in rows if r['status'] != 'completed'), None)
        dem_count = count_knowledge_items(knowledge_text, 'Demonstrated')
        rev_count = count_knowledge_items(knowledge_text, 'Needs review')
        sprint_name = info['title']
        report_rel = f"01-workspace/sprints/{sprint.name}/learning-report.html"

        dark_hero = (
            f'<div class="dark-hero-num">{pct}%</div>'
            f'<div class="muted">{done}/{total} Sessions complete</div>'
            f'<div class="hide-mini">'
            f'<div class="dark-bars"><div class="dark-bar-row"><div class="dark-bar-head"><span>{escape(info["title"])}</span><b>{done}/{total}</b></div>'
            f'<div class="dark-bar-track"><i style="width:{max(4, pct)}%"></i></div></div></div>'
            f'<p style="margin:14px 0 6px;font-size:13px">{escape(info.get("goal", ""))}</p>'
            f'<p style="margin:8px 0 4px"><a href="{escape(report_rel)}">Open report</a></p>'
            f'<p class="path-note" style="color:rgba(238,250,245,.58)">File: {escape(report_rel)}</p>'
            f'</div>'
        )
        chart_html = mastery_chart(rows)
        continue_prompt = f'Let’s continue Daily Learning on "{nxt["title"]}".' if nxt else 'Let’s review my completed Sprint and plan the next learning goal.'
        next_step_text = escape(nxt['next_action']) if nxt else 'Review the Sprint and choose a follow-on goal.'
        submit_note = '<p class="muted" style="margin-top:8px"><strong>Submit in Agent chat.</strong> Reply in the same Agent conversation; the Agent will review your answer and update the files and report.</p>' if nxt else ''
        next_card_html = (
            f'<div class="prompt-card"><p>{next_step_text}</p>'
            f'<button type="button" class="copy-btn" data-copy="{escape(continue_prompt, quote=True)}">Copy Continue Prompt</button></div>'
            f'{submit_note}'
        )
        knowledge_html = (
            f'<p class="muted">This section grows only after practice has been submitted and reviewed. Lesson content alone is not counted as learned knowledge.</p>'
            f'<div class="k-grid">'
            f'<div class="k-box"><h3>Knowledge I Can Use</h3>{knowledge_block(knowledge_text, "Demonstrated", "Nothing demonstrated yet.")}</div>'
            f'<div class="k-box"><h3>Still Developing</h3>{knowledge_block(knowledge_text, "Developing", "Nothing recorded yet.")}</div>'
            f'<div class="k-box"><h3>Needs Review</h3>{knowledge_block(knowledge_text, "Needs review", "Nothing scheduled for review yet.")}</div>'
            f'</div>'
        )
    else:
        done = total = pct = dem_count = rev_count = 0
        mistakes = []
        sprint_name = 'No Active Sprint'
        p1 = 'Create a 7-day Business English writing Sprint for clearer work emails and meeting summaries. I have 25 minutes per Session.'
        p2 = 'Create a 10-day LLM fundamentals Sprint covering tokens, embeddings, RAG, and agent workflows for a beginner. I have 30 minutes per Session.'
        p3 = 'Create a 7-day Finance fundamentals Sprint covering financial statements, cash flow, and risk basics. I have 25 minutes per Session.'
        p4 = 'Use the local notes and PDFs I attached to identify key themes and create a flexible 14-day learning Sprint with daily recall practice.'
        dark_hero = (
            '<div class="dark-hero-num">0%</div>'
            '<div class="muted">Ready for your first Sprint</div>'
            '<div class="hide-mini">'
            '<div class="dark-bars"><div class="dark-bar-row"><div class="dark-bar-head"><span>Sprint Progress</span><b>0 / 0</b></div>'
            '<div class="dark-bar-track"><i style="width:4%"></i></div></div></div>'
            '<p class="muted" style="margin-top:14px">Start from a natural-language goal or attach readable local files in Agent chat.</p>'
            '</div>'
        )
        chart_html = (
            '<h3 style="margin:0 0 8px;font-size:15px">Start your first learning plan</h3>'
            '<p class="muted" style="margin:0 0 10px">Pick a starter prompt below (or attach your own local study files) and paste it into Agent chat:</p>'
            f'<div class="prompt-card"><p><strong>Language Learning:</strong> “{escape(p1)}”</p>'
            f'<button type="button" class="copy-btn" data-copy="{escape(p1, quote=True)}">Copy Prompt</button></div>'
            f'<div class="prompt-card"><p><strong>LLM Fundamentals:</strong> “{escape(p2)}”</p>'
            f'<button type="button" class="copy-btn" data-copy="{escape(p2, quote=True)}">Copy Prompt</button></div>'
            f'<div class="prompt-card"><p><strong>Finance Basics:</strong> “{escape(p3)}”</p>'
            f'<button type="button" class="copy-btn" data-copy="{escape(p3, quote=True)}">Copy Prompt</button></div>'
            f'<div class="prompt-card"><p><strong>From Local Files:</strong> “{escape(p4)}”</p>'
            f'<button type="button" class="copy-btn" data-copy="{escape(p4, quote=True)}">Copy Prompt</button></div>'
            '<p class="muted" style="margin-top:8px">The agent will create the plan and prepare the first lesson; you do not need to create folders or edit tables.</p>'
        )
        next_card_html = (
            '<div class="prompt-card"><p>Choose one starter prompt above. The agent will ask only for missing details, create the Sprint, and prepare the first lesson.</p>'
            '<button type="button" class="copy-btn" data-copy="Let’s continue Daily Learning.">Copy Continue Prompt</button></div>'
        )
        knowledge_html = '<p class="muted">No personal knowledge record yet. It will appear after reviewed practice.</p>'

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Daily Learning</title>
{CSS}
</head>
<body>
<div class="shell">
  <aside class="sidebar" aria-label="Workspace Navigation">
    <div>
      <div class="brand">
        <div class="brand-mark">DL</div>
        <div>
          <div class="brand-name">Daily Learning</div>
          <div class="brand-sub">Study Studio</div>
        </div>
      </div>
      <nav class="nav-wrap">
        <div class="nav-pill" id="nav-pill"></div>
        <button type="button" class="nav-item active" data-section="overview">
          <svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>
          Overview
        </button>
        <button type="button" class="nav-item" data-section="next">
          <svg viewBox="0 0 24 24"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          Next Step
        </button>
        <button type="button" class="nav-item" data-section="knowledge">
          <svg viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          My Knowledge
          <span class="nav-count">{dem_count}</span>
        </button>
        <button type="button" class="nav-item" data-section="guide">
          <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/></svg>
          How It Works
        </button>
      </nav>
    </div>
    <div class="sidebar-foot">
      <div class="avatar">{pct}%</div>
      <div style="min-width:0">
        <div class="foot-title">{escape(sprint_name)}</div>
        <div class="foot-sub">Local-first · Evidence</div>
      </div>
    </div>
  </aside>

  <main class="main">
    <header class="topbar">
      <div class="title-block">
        <h1>Daily Learning</h1>
        <p class="title-sub">Turn a learning goal or local study material into a guided learning journey.</p>
      </div>
      <div class="toolbar">
        <div class="search-box" id="search-box">
          <input type="search" id="search-input" placeholder="Search knowledge..." aria-label="Search knowledge">
        </div>
        <button type="button" class="icon-btn" id="search-toggle" title="Search" aria-label="Search">
          <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
        </button>
      </div>
    </header>

    <div class="bento" id="bento">
      <section class="card span-3" data-tilt data-groups="overview">
        <div class="kpi-label">Completed sessions</div>
        <div class="kpi-row"><div class="kpi-val">{done} / {total}</div><svg class="spark" viewBox="0 0 68 22"><path d="M2 18 L18 15 L32 13 L48 9 L66 4"/></svg></div>
        <div class="kpi-foot"><span class="kpi-pill">Reviewed</span><span class="muted">Active sprint</span></div>
      </section>
      <section class="card span-3" data-tilt data-groups="overview">
        <div class="kpi-label">Completion rate</div>
        <div class="kpi-row"><div class="kpi-val">{pct}%</div><svg class="spark" viewBox="0 0 68 22"><path d="M2 17 L18 16 L34 12 L50 8 L66 5"/></svg></div>
        <div class="kpi-foot"><span class="kpi-pill soft">Progress</span><span class="muted">Verified work</span></div>
      </section>
      <section class="card span-3" data-tilt data-groups="overview">
        <div class="kpi-label">Usable knowledge</div>
        <div class="kpi-row"><div class="kpi-val">{dem_count}</div><svg class="spark" viewBox="0 0 68 22"><path d="M2 16 L18 13 L34 14 L50 7 L66 4"/></svg></div>
        <div class="kpi-foot"><span class="kpi-pill">Evidence</span><span class="muted">Demonstrated</span></div>
      </section>
      <section class="card span-3" data-tilt data-groups="overview">
        <div class="kpi-label">Needs review</div>
        <div class="kpi-row"><div class="kpi-val">{rev_count}</div></div>
        <div class="kpi-foot"><span class="kpi-pill {"warn" if rev_count else "soft"}">{len(mistakes)} Tracked</span><span class="muted">Weak points</span></div>
      </section>

      <section class="card span-7" data-tilt data-expandable data-groups="overview">
        <div class="card-head">
          <div>
            <h2 class="card-title">Current Sprint</h2>
            <p class="card-sub">Evidence-based mastery and active study plan</p>
            <span class="mini-stat-badge">{done}/{total} Done</span>
          </div>
          <div class="card-head-right">
            <span class="big-stat">{pct}%</span>
            <button type="button" class="expand-btn" title="Expand module">⤢</button>
          </div>
        </div>
        <div class="hide-mini">
          {chart_html}
          <p class="muted" style="margin-top:12px"><strong>Day and Session.</strong> Day describes the suggested sequence. A Session is one lesson, practice, and review cycle. You can pause, reschedule, or complete more than one Session in a day.</p>
        </div>
      </section>

      <section class="card card-dark span-5" data-tilt data-expandable data-groups="overview">
        <div class="card-head">
          <div>
            <h2 class="card-title">Sprint Progress</h2>
            <p class="card-sub">Active workspace snapshot</p>
          </div>
          <div class="card-head-right"><button type="button" class="expand-btn" title="Expand module">⤢</button></div>
        </div>
        {dark_hero}
      </section>

      <section class="card span-12" data-tilt data-expandable data-groups="overview next">
        <div class="card-head">
          <div><h2 class="card-title">Next Step</h2><p class="card-sub">Copy a ready-to-send prompt into Agent chat to continue learning</p></div>
          <div class="card-head-right"><button type="button" class="expand-btn" title="Expand module">⤢</button></div>
        </div>
        <div class="hide-mini">{next_card_html}</div>
      </section>

      <section class="card span-8" data-tilt data-expandable data-groups="overview knowledge">
        <div class="card-head">
          <div><h2 class="card-title">My Knowledge</h2><p class="card-sub">Built strictly from reviewed learner practice</p></div>
          <div class="card-head-right"><button type="button" class="expand-btn" title="Expand module">⤢</button></div>
        </div>
        <div class="hide-mini">{knowledge_html}</div>
      </section>

      <section class="card span-4" data-tilt data-expandable data-groups="overview guide">
        <div class="card-head">
          <div><h2 class="card-title">How it works</h2><p class="card-sub">5-step local learning loop</p></div>
          <div class="card-head-right"><button type="button" class="expand-btn" title="Expand module">⤢</button></div>
        </div>
        <div class="hide-mini">
          <p style="margin:0 0 10px"><strong>Plan → Learn → Practise → Review → Adapt.</strong></p>
          <p class="muted">Return later or switch agents anytime by saying “Let’s continue Daily Learning.”</p>
          <p style="margin:12px 0 6px">Quick guide: <a href="README.md">README.md</a></p>
          <p class="path-note">If preview links do not open, use the file paths shown above or ask an agent to open the named report.</p>
        </div>
      </section>
    </div>

    <footer class="foot-note">
      <span>Daily Learning · Static local dashboard</span>
      <span>Plan → Learn → Practise → Review → Adapt</span>
    </footer>
  </main>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
{JS}
</body>
</html>
'''


def main():
    sprints = []
    parent = ROOT / '01-workspace' / 'sprints'
    for sprint in sorted(p for p in parent.iterdir() if p.is_dir()):
        if (sprint / 'learning-plan.md').is_file():
            (sprint / 'learning-report.html').write_text(report(sprint, False), encoding='utf-8')
            sprints.append(sprint)
    (ROOT / 'dashboard.html').write_text(dashboard(), encoding='utf-8')
    print(f'Refreshed {len(sprints)} user learning reports and dashboard.html.')


if __name__ == '__main__':
    main()
