/* Shared header/footer, header scroll state, mobile nav, active link, scroll reveals, analytics beacon (as on the Kiehl Lab site). */
(function () {
  const C = window.SITE_CONFIG || {};
  const header = `<header class="site-header solid"><div class="wrap">
    <a class="brand" href="./"><span class="brand-mark" aria-hidden="true"><img src="assets/logo-mark.png" alt="" width="26" height="26"></span><span><b>Psychopath</b> Whisperer</span></a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span></button>
    <nav class="nav" id="nav" aria-label="Main">
      <div class="menu"><a href="book.html" class="menu-btn" aria-haspopup="true" aria-expanded="false">The book ▾</a>
        <div class="menu-list"><a href="book.html">About the book</a><a href="praise.html">Reviews and praise</a><a href="figures.html">Figures in color</a></div></div>
      <a href="news.html">News</a>
      <div class="menu"><a href="science.html" class="menu-btn" aria-haspopup="true" aria-expanded="false">Top science ▾</a>
        <div class="menu-list"><a href="science.html">Top science</a><a href="scientists.html">Top scientists</a><a href="top-books.html">Top books</a></div></div>
      <a href="blog.html">Blog</a>
      <a href="awards.html">Awards</a>
      <a href="merchandise.html">Merchandise</a>
      <a href="donate.html">Donate</a>
      <a href="about.html">About</a>
    </nav></div></header>`;
  const footer = `<footer class="site-footer"><div class="wrap">
    <div><strong>The Psychopath Whisperer</strong>A website dedicated to the science of those without conscience, managed by scientists in the laboratory of Kent A. Kiehl, PhD, at the nonprofit Mind Research Network and the University of New Mexico.</div>
    <div><strong>Site</strong><ul><li><a href="book.html">The book</a></li><li><a href="news.html">News and press</a></li><li><a href="science.html">Top science</a></li><li><a href="scientists.html">Top scientists</a></li><li><a href="top-books.html">Top books</a></li><li><a href="awards.html">Awards</a></li><li><a href="about.html">About</a></li><li><a href="feed.xml">RSS: news</a></li></ul></div>
    <div><strong>Elsewhere</strong><ul><li><a href="https://kentkiehl.com/" target="_blank" rel="noopener">Kiehl Lab</a></li><li><a href="https://www.mrn.org/" target="_blank" rel="noopener">Mind Research Network</a></li><li><a href="https://twitter.com/PsychopathW" target="_blank" rel="noopener">@PsychopathW</a></li><li><a href="https://www.facebook.com/pages/Psychopath-Whisperer/395759497204589" target="_blank" rel="noopener">Facebook</a></li><li><a href="http://www.goodreads.com/book/show/18248486-the-psychopath-whisperer" target="_blank" rel="noopener">Goodreads</a></li><li><a href="mailto:psychopath.whisperer@gmail.com">psychopath.whisperer@gmail.com</a></li><li><a href="donate.html">Support the research</a></li></ul></div>
    <div class="credit-row"><span class="credit">PsychopathWhisperer.com™ · Kiehl Laboratory · Mind Research Network · Albuquerque, NM · Site design after <a href="https://torwager.github.io/canlab/" target="_blank" rel="noopener">Tor Wager's CANlab site</a></span></div>
  </div></footer>`;
  const h = document.getElementById("site-header"); if (h) h.outerHTML = header;
  const f = document.getElementById("site-footer"); if (f) f.outerHTML = footer;

  const hdr = document.querySelector(".site-header");
  const onScroll = () => hdr && hdr.classList.toggle("scrolled", window.scrollY > 8);
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  const here = (location.pathname.split("/").pop() || "index.html");
  document.querySelectorAll(".nav a").forEach(a => { if (a.getAttribute("href") === here) { a.classList.add("active"); const m = a.closest(".menu"); if (m) m.querySelector(".menu-btn").classList.add("active"); } });

  const toggle = document.querySelector(".nav-toggle"), nav = document.getElementById("nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => { const open = nav.classList.toggle("open"); toggle.setAttribute("aria-expanded", String(open)); });
    nav.addEventListener("click", e => { if (e.target.tagName === "A" && !e.target.classList.contains("menu-btn")) nav.classList.remove("open"); });
  }
  document.querySelectorAll(".menu-btn").forEach(b => b.addEventListener("click", e => { const m = b.parentElement; if (!m.classList.contains("open") && window.matchMedia("(hover: none)").matches) { e.preventDefault(); m.classList.add("open"); b.setAttribute("aria-expanded", "true"); } }));

  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const rvs = document.querySelectorAll(".rv");
  if (reduce || !("IntersectionObserver" in window)) { rvs.forEach(el => el.classList.add("in")); }
  else { const io = new IntersectionObserver(entries => { entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } }); }, { threshold: 0.12 }); rvs.forEach(el => io.observe(el)); }

  if (C.cfAnalyticsToken) { const s = document.createElement("script"); s.defer = true; s.src = "https://static.cloudflareinsights.com/beacon.min.js"; s.setAttribute("data-cf-beacon", JSON.stringify({ token: C.cfAnalyticsToken })); document.head.appendChild(s); }
  // Private visit counter (GoatCounter, no cookies). Counts only on the live site, not previews or local copies.
  if (C.goatcounterCode && /(^|\.)psychopathwhisperer\.com$/.test(location.hostname)) { const g = document.createElement("script"); g.async = true; g.src = "https://gc.zgo.at/count.js"; g.setAttribute("data-goatcounter", "https://" + C.goatcounterCode + ".goatcounter.com/count"); document.head.appendChild(g); }
})();
