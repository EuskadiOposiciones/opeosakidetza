/* OPE Osakidetza — PostHog EU, privacidad por diseño.
 * Medición cookieless: sin cookies, localStorage ni sessionStorage de PostHog.
 * Requiere activar Cookieless tracking también en los ajustes del proyecto PostHog.
 */
(function () {
  'use strict';

  var POSTHOG_TOKEN = 'phc_nyXj9NDnjEt7ngcrAuSZT8jPN9mkqW5ySCBNtLp6SMWH';
  var API_HOST = 'https://eu.i.posthog.com';
  var UI_HOST = 'https://eu.posthog.com';
  var CATEGORY_SLUGS = {
    'celador': 'celador',
    'operario': 'operario',
    'tcae': 'tcae',
    'auxiliar-administrativo': 'auxiliar_administrativo',
    'administrativo': 'administrativo',
    'enfermeria': 'enfermeria',
    'radiodiagnostico': 'radiodiagnostico',
    'laboratorio': 'laboratorio'
  };

  function cleanPath(pathname) {
    return (pathname || '/').replace(/\/index\.html$/i, '/').replace(/\/+$/, '') || '/';
  }

  function pageContext() {
    var path = cleanPath(window.location.pathname);
    var parts = path.split('/').filter(Boolean);
    var last = parts.length ? parts[parts.length - 1] : '';
    var pageType = 'other';
    var category = null;

    if (last === 'opeosakidetza' || path === '/') pageType = 'home';
    else if (CATEGORY_SLUGS[last]) { pageType = 'category'; category = CATEGORY_SLUGS[last]; }
    else if (last === 'baterias-oficiales') pageType = 'batteries';
    else if (last === 'respuestas-bateria-osakidetza') pageType = 'responses';
    else if (last === 'simulacro-osakidetza') pageType = 'simulacro';
    else if (last === 'ope-osakidetza-2026') pageType = 'ope_overview';
    else if (last === 'fase-2-osakidetza-2026') pageType = 'phase_2';
    else if (last === 'it-txartela-osakidetza') pageType = 'it_txartela';
    else if (last === 'resultados-ope-osakidetza-2026') pageType = 'results';
    else if (last === 'privacy.html') pageType = 'privacy';
    else if (last === 'legal.html') pageType = 'legal';
    else if (last === '404.html') pageType = '404';

    return {
      page_type: pageType,
      category: category || 'none',
      page_path: path
    };
  }

  function positionOf(el) {
    if (!el) return 'unknown';
    if (el.closest && el.closest('.mobile-cta')) return 'mobile_sticky';
    if (el.closest && el.closest('header')) return 'header';
    if (el.closest && (el.closest('.hero') || el.closest('.category-hero'))) return 'hero';
    if (el.closest && el.closest('footer')) return 'footer';
    if (el.closest && el.closest('main')) return 'content';
    return 'other';
  }

  function labelOf(el) {
    return ((el && el.textContent) || '').replace(/\s+/g, ' ').trim().slice(0, 120) || 'unlabeled';
  }

  function capture(name, props) {
    if (!window.posthog || typeof window.posthog.capture !== 'function') return;
    var base = pageContext();
    window.posthog.capture(name, Object.assign(base, props || {}));
  }

  // Current PostHog HTML loader (array.js), adapted to EU Cloud.
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog&&window.posthog.__loaded)||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split('.');2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}p||((p=t.createElement('script')).type='text/javascript',p.crossOrigin='anonymous',p.async=!0,p.src=s.api_host.replace('.i.posthog.com','-assets.i.posthog.com')+'/static/array.js',p.onerror=function(){p=null},(r=t.getElementsByTagName('script')[0]).parentNode.insertBefore(p,r));var u=e;for(void 0!==a?u=e[a]=[]:a='posthog',u.people=u.people||[],u.toString=function(t){var e='posthog';return'posthog'!==a&&(e+='.'+a),t||(e+=' (stub)'),e},u.people.toString=function(){return u.toString(1)+'.people (stub)'},o='init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagResult isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug'.split(' '),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

  window.posthog.init(POSTHOG_TOKEN, {
    api_host: API_HOST,
    ui_host: UI_HOST,
    defaults: '2026-05-30',
    cookieless_mode: 'always',
    person_profiles: 'never',
    autocapture: false,
    capture_pageview: false,
    capture_pageleave: true,
    capture_dead_clicks: false,
    capture_heatmaps: false,
    capture_performance: false,
    capture_exceptions: false,
    disable_session_recording: true,
    disable_surveys: true,
    respect_dnt: true
  });

  // Keep Google Play attribution useful without adding browser persistence.
  document.querySelectorAll('a[href*="play.google.com/store/apps/details"]').forEach(function (a) {
    try {
      var url = new URL(a.href, window.location.href);
      var referrer = new URLSearchParams(url.searchParams.get('referrer') || '');
      var ctx = pageContext();
      referrer.set('utm_source', 'github_pages');
      referrer.set('utm_medium', 'web');
      referrer.set('utm_campaign', 'ope_osakidetza');
      referrer.set('utm_content', positionOf(a));
      referrer.set('utm_term', ctx.category !== 'none' ? ctx.category : ctx.page_type);
      url.searchParams.set('referrer', referrer.toString());
      a.href = url.toString();
    } catch (e) {}
  });

  // Standard PostHog pageview enriched with the site's SEO/content taxonomy.
  capture('$pageview', { page_title: document.title });

  document.addEventListener('click', function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    var abs;
    try { abs = new URL(a.href, window.location.href); } catch (e) { return; }

    if (abs.hostname === 'play.google.com' && abs.pathname.indexOf('/store/apps/details') !== -1) {
      capture('google_play_clicked', {
        cta_position: positionOf(a),
        cta_label: labelOf(a),
        destination: 'google_play'
      });
      return;
    }

    if (abs.hostname === 'www.osakidetza.euskadi.eus' || abs.hostname === 'osakidetza.euskadi.eus' || abs.hostname === 'www.euskadi.eus' || abs.hostname === 'euskadi.eus') {
      var isPdf = /\.pdf(?:$|\?)/i.test(abs.pathname + abs.search);
      capture('official_source_clicked', {
        link_position: positionOf(a),
        link_label: labelOf(a),
        resource_type: isPdf ? 'pdf' : 'portal',
        source_kind: isPdf ? 'official_battery_or_document' : (abs.hostname.indexOf('euskadi.eus') !== -1 && abs.hostname.indexOf('osakidetza') === -1 ? 'official_bopv_or_euskadi' : 'official_ope_portal'),
        source_path: abs.pathname.slice(0, 300)
      });
      return;
    }

    if (abs.hostname === window.location.hostname) {
      var targetPath = cleanPath(abs.pathname);
      var targetLast = targetPath.split('/').filter(Boolean).pop() || '';
      if (CATEGORY_SLUGS[targetLast]) {
        capture('category_link_clicked', {
          target_category: CATEGORY_SLUGS[targetLast],
          link_position: positionOf(a),
          link_label: labelOf(a)
        });
      }
    }
  }, { passive: true });

  // Coarse scroll goals only; no continuous scroll telemetry.
  var reached = {50: false, 90: false};
  function onScroll() {
    var doc = document.documentElement;
    var max = Math.max(1, doc.scrollHeight - window.innerHeight);
    var pct = Math.round((window.scrollY / max) * 100);
    [50, 90].forEach(function (threshold) {
      if (!reached[threshold] && pct >= threshold) {
        reached[threshold] = true;
        capture('scroll_depth_reached', { depth_percent: threshold });
      }
    });
    if (reached[50] && reached[90]) window.removeEventListener('scroll', onScroll);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
})();
