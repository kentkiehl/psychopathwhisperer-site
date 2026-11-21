# psychopathwhisperer.com — notes for Claude Code

Static site for *The Psychopath Whisperer* (Kent A. Kiehl), rebuilt 21 November 2026 from the WordPress site at
psychopathwhisperer.com using the framework of the Kiehl Lab site (github.com/kentkiehl/kiehl-site; read its CLAUDE.md and
README for the shared design system). `site/assets/app.css` is an unmodified copy of that site's stylesheet; this site's
own styles are in `site/assets/site.css`.

## Decisions
- NOT PUBLISHED. The owner asked for a private preview first: no GitHub repository, no Pages, no DNS change and no change at
  Bluehost until he says so. There is deliberately no `site/CNAME`. See README "Publishing" for the order of steps;
  email for the domain runs through Google, so the MX and TXT records must be left alone when DNS is changed.
- The old site is archived in `Documents/psychopathwhisperer-archive-2026-11-21` (public pages, posts, media, WordPress JSON).
- Pages follow the old menu: The book (about, reviews and praise, figures) · News · Top science (works, scientists, books) ·
  Blog · Awards · Merchandise · Donate · About.
- Blog shows an "Under revision" notice (owner's request, 21 Nov 2026); he decides later what to do with it. The old blog
  text is in the archive (`pages/page_13_blog.html`), not in this repository.
- Home page: the news posts stay on the front page (owner likes them), with newer contributions added from the lab site's
  news and media lists (`"origin": "lab-site"` in `data/news_posts.json`; `"origin": "wordpress"` are the carried-over posts).
- Top scientists: figures come from each scientist's Google Scholar profile (ids in `data/scientists.json`), read on
  21 Nov 2026 and refreshed monthly by `pipeline/update_metrics.py`. The old page's "Citation website" link for Dr. Blair
  pointed at another person's profile and was dropped. Profiles for Viding, Kimonis and Glenn were found by name search.
- Top science and Top books: Google Scholar counts re-read on 21 Nov 2026 (the old page's were from March 2014 and are kept
  as `scholar_2014` for comparison). Per-work Scholar counts cannot be fetched automatically, so the monthly job adds an
  OpenAlex count by DOI instead. The DOIs in `data/works.json` were entered from memory and are confirmed only once the
  first monthly run resolves them.
- About page rewritten from the CV of November 2026 (30+ years, >280 papers, 6,000+ people scanned, 2026 Hare award).
- Donate links to mrn.org/donate, as on the lab site (the old page used a Network for Good form).
- Images: only the owner's own material is used (book figures, cover, merchandise picture, his portrait). Outlet logos,
  Scholar screenshots and photos of other scientists from the old site are not reused. Do not download photos of people.
- Not checked yet: the old external links (CafePress shop, Twitter, Facebook, scientists' faculty pages, older news links).

## Working
- `python3 -m pipeline.build_site`; preview with `python3 -m http.server 8765 --directory site`.
- `python3 -m pipeline.update_metrics --dry-run` to test the monthly refresh.
- Site address lives in pipeline/config.py, site/assets/config.js and the page heads: change with `scripts/set_site_url.py`.
- Bump `?v=` on app.css/site.css/app.js/layout.js when they change.
