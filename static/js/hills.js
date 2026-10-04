/* Go Sikkim Tours · interactions
   Free libraries (CDN): GSAP + ScrollTrigger, Lenis. Maps are server-drawn SVG (no map API).
   Everything degrades: without JS the site stays readable, navigable and every form submits. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var track = function (name, data) { window.dataLayer = window.dataLayer || []; window.dataLayer.push(Object.assign({ event: name }, data || {})); };
  var store = {
    get: function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  };

  /* analytics hooks: every CTA and form reports itself */
  document.addEventListener("click", function (e) {
    var a = e.target.closest("[data-cta]");
    if (a) track("cta_click", { cta: a.dataset.cta, href: a.getAttribute("href") || "" });
  });
  $$("form[data-cta-form]").forEach(function (f) { f.addEventListener("submit", function () { track("form_submit", { form: f.dataset.ctaForm }); }); });

  /* masthead: compact on scroll */
  var mast = $(".mast");
  var onScroll = function () {
    var y = window.scrollY;
    if (mast) mast.classList.toggle("is-scrolled", y > 24);
    if (fab) fab.classList.toggle("is-on", y > 520);
  };

  /* mega menus: hover on desktop, click anywhere, Esc closes */
  var drops = $$(".nav__drop");
  var closeAll = function (except) { drops.forEach(function (d) { if (d !== except) { d.classList.remove("is-open"); $("button", d).setAttribute("aria-expanded", "false"); } }); };
  drops.forEach(function (drop) {
    var btn = $("button", drop), timer;
    var open = function () { clearTimeout(timer); closeAll(drop); drop.classList.add("is-open"); btn.setAttribute("aria-expanded", "true"); };
    var close = function () { drop.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); };
    btn.addEventListener("click", function (e) { e.stopPropagation(); drop.classList.contains("is-open") ? close() : open(); });
    if (window.matchMedia("(hover: hover)").matches) {
      // one timer per menu: entering cancels a pending close; leaving cancels a pending open
      drop.addEventListener("mouseenter", function () {
        clearTimeout(timer);
        if (!drop.classList.contains("is-open")) timer = setTimeout(open, 80);
      });
      drop.addEventListener("mouseleave", function () { clearTimeout(timer); timer = setTimeout(close, 280); });
    }
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".nav__drop")) closeAll(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeAll(); closeSearch(); closeFab(); } });

  /* mobile sheet */
  var sheet = $(".sheet");
  $$("[data-sheet-open]").forEach(function (b) { b.addEventListener("click", function () { sheet.classList.add("is-open"); document.body.style.overflow = "hidden"; $(".sheet__close", sheet).focus(); }); });
  $$("[data-sheet-close]").forEach(function (b) { b.addEventListener("click", function () { sheet.classList.remove("is-open"); document.body.style.overflow = ""; }); });

  /* search overlay: loads a small JSON index on first open */
  var search = $(".search"), input = $("#q"), results = $(".search__results"), index = null;
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;" }[c]; }); };
  var norm = function (s) { return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };
  function openSearch() {
    if (!search) return;
    if (sheet) { sheet.classList.remove("is-open"); }
    search.hidden = false; document.body.style.overflow = "hidden"; input.focus();
    if (!index) fetch(input.dataset.searchUrl).then(function (r) { return r.json(); }).then(function (d) { index = d.map(function (row) { return { t: row[0], u: row[1], k: row[2], c: row[3], n: norm(row[0] + " " + row[3] + " " + row[2]) }; }); run(); });
    track("search_open");
  }
  function closeSearch() { if (search && !search.hidden) { search.hidden = true; document.body.style.overflow = ""; } }
  function run() {
    if (!index) return;
    var q = norm(input.value.trim());
    if (q.length < 2) { results.innerHTML = ""; return; }
    var words = q.split(/\s+/);
    var hits = index.filter(function (r) { return words.every(function (w) { return r.n.indexOf(w) > -1; }); })
      .sort(function (a, b) { return (norm(a.t).indexOf(words[0]) === 0 ? -1 : 0) - (norm(b.t).indexOf(words[0]) === 0 ? -1 : 0) || a.t.length - b.t.length; })
      .slice(0, 14);
    results.innerHTML = hits.length ? hits.map(function (r) { return '<li><a href="' + esc(r.u) + '"><b>' + esc(r.t) + '</b><small>' + esc(r.k) + (r.c ? " · " + esc(r.c) : "") + "</small></a></li>"; }).join("")
      : '<li class="small muted" style="padding:12px">No match. <a href="/plan/">Ask a planner instead</a>.</li>';
  }
  $$("[data-search-open]").forEach(function (b) { b.addEventListener("click", openSearch); });
  $$("[data-search-close]").forEach(function (b) { b.addEventListener("click", closeSearch); });
  if (search) {
    search.addEventListener("click", function (e) { if (e.target === search) closeSearch(); });
    input.addEventListener("input", run);
    document.addEventListener("keydown", function (e) { if (e.key === "/" && !/input|textarea|select/i.test(document.activeElement.tagName)) { e.preventDefault(); openSearch(); } });
  }

  /* floating CTA */
  var fab = $("[data-fab]"), fabPanel = $("#fab-panel"), fabBtn = $(".fab__toggle");
  function closeFab() { if (fabPanel && !fabPanel.hidden) { fabPanel.hidden = true; fabBtn.setAttribute("aria-expanded", "false"); } }
  if (fab) {
    fabBtn.addEventListener("click", function (e) { e.stopPropagation(); var o = fabPanel.hidden; fabPanel.hidden = !o; fabBtn.setAttribute("aria-expanded", String(o)); if (o) track("fab_open"); });
    document.addEventListener("click", function (e) { if (!e.target.closest("[data-fab]")) closeFab(); });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* journey buy bar: appears once the hero has scrolled away */
  var buybar = $("[data-buybar]");
  if (buybar && "IntersectionObserver" in window) {
    buybar.hidden = false;
    var hero = $(".phead") || $("main section");
    new IntersectionObserver(function (en) {
      var on = !en[0].isIntersecting;
      buybar.classList.toggle("is-on", on);
      document.body.classList.toggle("has-buybar", on);
    }).observe(hero);
  }

  /* planning nudge on long reads: once per visit, after 55% of the page */
  var nudge = $("[data-nudge]");
  if (nudge && !store.get("nudge-closed")) {
    var shown = false;
    window.addEventListener("scroll", function () {
      if (shown) return;
      var h = document.documentElement.scrollHeight - innerHeight;
      if (h > 0 && scrollY / h > 0.55) { shown = true; nudge.hidden = false; track("nudge_shown"); }
    }, { passive: true });
    $("[data-nudge-close]", nudge).addEventListener("click", function () { nudge.hidden = true; store.set("nudge-closed", "1"); });
  }

  /* hero arch fan */
  $$(".fan").forEach(function (fanEl) {
    var items = $$(".fan__item", fanEl);
    var activate = function (it) { items.forEach(function (x) { x.classList.toggle("is-active", x === it); }); };
    items.forEach(function (it) { it.addEventListener("mouseenter", function () { activate(it); }); it.addEventListener("focus", function () { activate(it); }); });
  });

  /* index rows: floating arch preview follows the cursor */
  var peek = $(".toc__peek");
  if (peek && window.matchMedia("(hover: hover)").matches) {
    var pimg = $("img", peek), tx = 0, ty = 0, x = 0, y = 0, raf = null;
    var loop = function () { x += (tx - x) * 0.18; y += (ty - y) * 0.18; peek.style.left = x + "px"; peek.style.top = y + "px"; raf = requestAnimationFrame(loop); };
    $$(".toc__row[data-img]").forEach(function (row) {
      row.addEventListener("mouseenter", function () { pimg.src = row.dataset.img; peek.classList.add("is-on"); if (!raf) loop(); });
      row.addEventListener("mouseleave", function () { peek.classList.remove("is-on"); });
      row.addEventListener("mousemove", function (e) { tx = e.clientX + 170; ty = e.clientY; });
    });
  }

  /* complete rows: show just enough "Shape your own journey" cards to fill the last row of each grid */
  function fillGrid(grid) {
    var fillers = $$(":scope > [data-fill-card]", grid);
    if (!fillers.length) return;
    fillers.forEach(function (f) { f.hidden = true; });
    var cols = getComputedStyle(grid).gridTemplateColumns.split(" ").filter(Boolean).length || 1;
    var visible = $$(":scope > *", grid).filter(function (el) { return !el.hasAttribute("data-fill-card") && !el.hidden; }).length;
    if (!visible || cols < 2) return;
    var need = (cols - (visible % cols)) % cols;
    if (!need) return;
    /* one planner card stretched across the gap reads as intended; several identical cards read as padding */
    var card = fillers[need > 1 ? 1 : 0] || fillers[0];
    card.hidden = false;
    card.style.gridColumn = "span " + need;
    card.classList.toggle("card-fill--wide", need > 1);
  }
  var fillAll = function () { $$("[data-fill]").forEach(fillGrid); };
  fillAll();
  var fillTimer;
  window.addEventListener("resize", function () { clearTimeout(fillTimer); fillTimer = setTimeout(fillAll, 120); });

  /* list filters (journeys, stays, experiences, guides); ?length=short etc. preselects */
  $$("[data-filter-group]").forEach(function (group) {
    var target = $(group.dataset.filterGroup), state = {};
    var count = $("[data-filter-count]", group.parentNode);
    var apply = function () {
      var shown = 0;
      $$("[data-item]", target).forEach(function (el) {
        var ok = Object.keys(state).every(function (k) { return !state[k] || (" " + (el.dataset[k] || "") + " ").indexOf(" " + state[k] + " ") > -1; });
        el.hidden = !ok; if (ok) shown++;
      });
      $$("[data-section]", target).forEach(function (sec) { sec.hidden = !$$("[data-item]", sec).some(function (el) { return !el.hidden; }); });
      if (count) count.textContent = shown;
      fillAll();
    };
    $$("button[data-key]", group).forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.dataset.key;
        $$('button[data-key="' + k + '"]', group).forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
        state[k] = b.dataset.value; apply();
      });
    });
    $$("select[data-key]", group).forEach(function (s) { s.addEventListener("change", function () { state[s.dataset.key] = s.value; apply(); }); });
    var params = new URLSearchParams(location.search);
    $$("select[data-key]", group).forEach(function (s) { var v = params.get(s.dataset.key); if (v) { s.value = v; state[s.dataset.key] = v; } });
    $$("button[data-key]", group).forEach(function (b) { if (params.get(b.dataset.key) === b.dataset.value) b.click(); });
    if (Object.keys(state).length) apply();
  });

  /* plan wizard: three steps, validates the visible step before moving on */
  $$("[data-wizard]").forEach(function (form) {
    var steps = $$(".wizard__step", form), labels = $$(".wizard__steps li", form), bar = $(".wizard__bar span", form), i = 0;
    var errored = $(".errorlist", form);
    if (errored) i = steps.length - 1;
    var show = function (n) {
      i = Math.max(0, Math.min(steps.length - 1, n));
      steps.forEach(function (s, k) { s.classList.toggle("is-on", k === i); });
      labels.forEach(function (l, k) { l.classList.toggle("is-on", k <= i); });
      bar.style.width = ((i + 1) / steps.length * 100) + "%";
      track("wizard_step", { step: i + 1 });
    };
    form.setAttribute("data-ready", "");
    $$("[data-next]", form).forEach(function (b) { b.addEventListener("click", function () {
      var bad = $$("input, select, textarea", steps[i]).filter(function (el) { return !el.checkValidity(); });
      if (bad.length) { bad[0].reportValidity(); return; }
      show(i + 1); steps[i].querySelector("input, select, textarea").focus();
    }); });
    $$("[data-prev]", form).forEach(function (b) { b.addEventListener("click", function () { show(i - 1); }); });
    show(i);
  });

  /* atlas: pins and legend highlight each other */
  $$(".atlas").forEach(function (fig) {
    var pins = $$(".atlas__pin", fig), items = $$(".atlas__legend li", fig);
    var hot = function (n, on) {
      pins.forEach(function (p) { if (p.dataset.n === n) p.classList.toggle("is-hot", on); });
      items.forEach(function (li) { if (li.dataset.n === n) li.classList.toggle("is-hot", on); });
    };
    pins.concat(items).forEach(function (el) {
      el.addEventListener("mouseenter", function () { hot(el.dataset.n, true); });
      el.addEventListener("mouseleave", function () { hot(el.dataset.n, false); });
    });
  });

  /* guide and article contents: highlight the section in view */
  var tocLinks = $$(".toc-side a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) tocLinks.forEach(function (a) { a.classList.toggle("is-on", a.getAttribute("href") === "#" + en.target.id); }); });
    }, { rootMargin: "-30% 0px -60% 0px" });
    tocLinks.forEach(function (a) { var t = document.getElementById(a.getAttribute("href").slice(1)); if (t) io.observe(t); });
  }

  /* smooth scroll + reveals */
  if (!reduce && window.Lenis) {
    var lenis = new Lenis({ lerp: 0.11 });
    if (window.gsap && window.ScrollTrigger) {
      lenis.on("scroll", ScrollTrigger.update);
      gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
    } else {
      var rafL = function (t) { lenis.raf(t); requestAnimationFrame(rafL); };
      requestAnimationFrame(rafL);
    }
  }
  if (!reduce && window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);
    $$(".rv").forEach(function (el) { gsap.to(el, { opacity: 1, y: 0, duration: 1, ease: "power3.out", scrollTrigger: { trigger: el, start: "top 88%", once: true } }); });
    $$(".rv-arch .photo__frame").forEach(function (el) { gsap.to(el, { clipPath: "inset(0% 0 0 0 round 999px 999px 6px 6px)", duration: 1.4, ease: "power3.inOut", scrollTrigger: { trigger: el, start: "top 90%", once: true } }); });
    var title = $(".hero .h-hero");
    if (title) gsap.from(title, { y: 60, opacity: 0, duration: 1.4, ease: "power4.out" });
    var fanEl = $(".fan");
    if (fanEl) gsap.from($$(".fan__item", fanEl), { y: 120, opacity: 0, duration: 1.2, stagger: 0.07, ease: "power4.out", delay: 0.2 });
  } else {
    doc.classList.remove("js");
  }
})();
