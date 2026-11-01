/* Rocheltex — consentimiento de cookies (vanilla, sin dependencias) */
(function () {
  'use strict';
  var KEY = 'rtx_consent_v1', TTL = 365 * 24 * 3600 * 1000;
  var me = document.currentScript;
  var policy = (me && me.getAttribute('data-policy')) || 'rocheltex-cookies.html';
  var lang = (document.documentElement.lang || 'es').slice(0, 2) === 'en' ? 'en' : 'es';
  var T = {
    es: {
      bTitle: 'Tu privacidad', bText: 'Usamos almacenamiento técnico imprescindible para que la web funcione y, solo si lo permites, contenido de terceros como el mapa de Google. No usamos cookies de publicidad ni de analítica.',
      more: 'Política de cookies', accept: 'Aceptar todo', reject: 'Rechazar todo', config: 'Configurar',
      pTitle: 'Preferencias de cookies', pText: 'Elige qué quieres permitir. Puedes cambiar tu decisión en cualquier momento desde «Configurar cookies», al pie de la página.',
      c1: 'Técnicas (necesarias)', c1d: 'Imprescindibles para el funcionamiento de la web y para recordar tus preferencias de cookies. No se pueden desactivar.', always: 'Siempre activas',
      c2: 'Contenido de terceros (Google Maps)', c2d: 'Permite mostrar el mapa interactivo de Google en la página de Contacto. Google puede instalar cookies y tratar datos de tu navegación.',
      save: 'Guardar preferencias', close: 'Cerrar',
      gate: 'Este mapa lo proporciona Google Maps. Al cargarlo, Google puede instalar cookies y recibir datos de tu navegación.', gateBtn: 'Aceptar y cargar el mapa', gateLink: 'Abrir en Google Maps'
    },
    en: {
      bTitle: 'Your privacy', bText: 'We use strictly necessary technical storage so the website works and, only if you allow it, third-party content such as the Google map. We do not use advertising or analytics cookies.',
      more: 'Cookie policy', accept: 'Accept all', reject: 'Reject all', config: 'Settings',
      pTitle: 'Cookie preferences', pText: 'Choose what you want to allow. You can change your decision at any time from “Cookie settings” at the bottom of the page.',
      c1: 'Technical (necessary)', c1d: 'Essential for the website to work and to remember your cookie preferences. They cannot be disabled.', always: 'Always active',
      c2: 'Third-party content (Google Maps)', c2d: 'Lets us show the interactive Google map on the Contact page. Google may set cookies and process data about your browsing.',
      save: 'Save preferences', close: 'Close',
      gate: 'This map is provided by Google Maps. When loaded, Google may set cookies and receive data about your browsing.', gateBtn: 'Accept and load the map', gateLink: 'Open in Google Maps'
    }
  }[lang];

  function read() {
    try { var v = JSON.parse(localStorage.getItem(KEY) || 'null'); if (v && typeof v.ts === 'number' && Date.now() - v.ts < TTL) return v; } catch (e) {}
    return null;
  }
  function write(maps) {
    var v = { maps: !!maps, ts: Date.now() };
    try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {}
    return v;
  }
  var state = read();

  function el(tag, attrs, html) {
    var n = document.createElement(tag);
    for (var k in (attrs || {})) n.setAttribute(k, attrs[k]);
    if (html) n.innerHTML = html;
    return n;
  }

  /* ---- mapa condicionado ---- */
  function applyMaps() {
    var ok = !!(state && state.maps);
    var frames = document.querySelectorAll('iframe[data-consent="maps"]');
    for (var i = 0; i < frames.length; i++) {
      var f = frames[i], gate = f.parentNode.querySelector('.map-gate');
      if (ok) { if (!f.getAttribute('src')) f.setAttribute('src', f.getAttribute('data-src')); f.hidden = false; if (gate) gate.hidden = true; }
      else { f.removeAttribute('src'); f.hidden = true; if (gate) gate.hidden = false; }
    }
  }
  function buildGates() {
    var frames = document.querySelectorAll('iframe[data-consent="maps"]');
    for (var i = 0; i < frames.length; i++) {
      var f = frames[i];
      if (f.parentNode.querySelector('.map-gate')) continue;
      var href = f.getAttribute('data-link') || 'https://www.google.com/maps';
      var g = el('div', { 'class': 'map-gate' },
        '<p>' + T.gate + '</p><button type="button" class="rtx-btn rtx-accept" data-map-accept>' + T.gateBtn + '</button>' +
        '<a href="' + href + '" target="_blank" rel="noopener noreferrer">' + T.gateLink + ' ↗</a>');
      f.parentNode.insertBefore(g, f);
    }
  }

  /* ---- banner ---- */
  var banner, overlay, lastFocus;
  function buildBanner() {
    banner = el('div', { 'class': 'rtx-cc', role: 'dialog', 'aria-labelledby': 'rtx-cc-t', 'aria-describedby': 'rtx-cc-d', hidden: '' },
      '<h2 id="rtx-cc-t">' + T.bTitle + '</h2><p id="rtx-cc-d">' + T.bText + ' <a href="' + policy + '">' + T.more + '</a>.</p>' +
      '<div class="rtx-cc-row"><button type="button" class="rtx-btn rtx-accept" data-act="accept">' + T.accept + '</button>' +
      '<button type="button" class="rtx-btn" data-act="reject">' + T.reject + '</button>' +
      '<button type="button" class="rtx-link" data-act="config">' + T.config + '</button></div>');
    document.body.appendChild(banner);
  }
  function buildPanel() {
    overlay = el('div', { 'class': 'rtx-overlay', hidden: '' },
      '<div class="rtx-panel" role="dialog" aria-modal="true" aria-labelledby="rtx-p-t">' +
      '<h2 id="rtx-p-t">' + T.pTitle + '</h2><p>' + T.pText + ' <a href="' + policy + '">' + T.more + '</a>.</p>' +
      '<div class="rtx-cat"><div><strong>' + T.c1 + '</strong><span class="d">' + T.c1d + '</span></div><span class="rtx-state">' + T.always + '</span></div>' +
      '<div class="rtx-cat"><div><strong>' + T.c2 + '</strong><span class="d">' + T.c2d + '</span></div>' +
      '<label class="rtx-switch"><input type="checkbox" id="rtx-maps" aria-label="' + T.c2 + '"><span class="rtx-slider"></span></label></div>' +
      '<div class="rtx-cc-row"><button type="button" class="rtx-btn" data-act="reject">' + T.reject + '</button>' +
      '<button type="button" class="rtx-btn rtx-ghost" data-act="save">' + T.save + '</button>' +
      '<button type="button" class="rtx-btn rtx-accept" data-act="accept">' + T.accept + '</button></div></div>');
    document.body.appendChild(overlay);
  }
  function decide(maps) {
    state = write(maps);
    banner.hidden = true; overlay.hidden = true;
    applyMaps();
    if (lastFocus && lastFocus.focus) { try { lastFocus.focus(); } catch (e) {} }
  }
  function openPanel() {
    lastFocus = document.activeElement;
    document.getElementById('rtx-maps').checked = !!(state && state.maps);
    banner.hidden = true; overlay.hidden = false;
    var b = overlay.querySelector('[data-act="accept"]'); if (b) b.focus();
  }
  function onClick(e) {
    var t = e.target;
    var open = t.closest && t.closest('[data-open-cookies]');
    if (open) { e.preventDefault(); openPanel(); return; }
    var mapBtn = t.closest && t.closest('[data-map-accept]');
    if (mapBtn) { decide(true); return; }
    var a = t.closest && t.closest('[data-act]');
    if (!a) { if (t === overlay && state) { overlay.hidden = true; } return; }
    var act = a.getAttribute('data-act');
    if (act === 'accept') decide(true);
    else if (act === 'reject') decide(false);
    else if (act === 'config') openPanel();
    else if (act === 'save') decide(document.getElementById('rtx-maps').checked);
  }
  function onKey(e) {
    if (e.key === 'Escape' && overlay && !overlay.hidden && state) { overlay.hidden = true; }
    if (e.key === 'Tab' && overlay && !overlay.hidden) {
      var f = overlay.querySelectorAll('button, input, a[href]'); if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  }
  function init() {
    buildGates(); buildBanner(); buildPanel(); applyMaps();
    document.addEventListener('click', onClick); document.addEventListener('keydown', onKey);
    if (!state) banner.hidden = false;
    window.rtxConsent = { open: openPanel, get: function () { return state; } };
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
