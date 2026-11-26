# psychopathwhisperer.com — notes for Claude Code

Static site for *The Psychopath Whisperer* (Kent A. Kiehl), rebuilt 21 November 2026 from the WordPress site at
psychopathwhisperer.com using the framework of the Kiehl Lab site (github.com/kentkiehl/kiehl-site; read its CLAUDE.md and
README for the shared design system). `site/assets/app.css` is an unmodified copy of that site's stylesheet; this site's
own styles are in `site/assets/site.css`.

## Decisions
- PUBLISHED 21 Nov 2026 on the owner's instruction: repository github.com/kentkiehl/psychopathwhisperer-site, GitHub Pages
  (source: GitHub Actions), custom domain psychopathwhisperer.com. DNS is at Bluehost (ns1/ns2.bluehost.com): only the `@` A
  record (was 162.241.216.188, the Bluehost server) and the `www` CNAME (was psychopathwhisperer.com) were changed, to GitHub
  Pages. All mail records (MX -> mail.psychopathwhisperer.com at Bluehost, the `mail` A record, SPF) were left alone. To roll
  back, put those two records back. The WordPress site and its files are still on the Bluehost server.
- Google Scholar refuses requests from GitHub's servers (first monthly run, 21 Nov 2026: 0 of 9 profiles read), so the
  Scholar figures only change when someone re-reads them in a browser; NIH RePORTER and OpenAlex refresh fine from GitHub.
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
  OpenAlex count by DOI instead. All seven DOIs in `data/works.json` resolved in OpenAlex on the first run.
- About page rewritten from the CV of November 2026 (30+ years, >280 papers, 6,000+ people scanned, 2026 Hare award).
- Donate links to mrn.org/donate, as on the lab site (the old page used a Network for Good form).
- NIH grants on Top scientists (owner's request): from NIH RePORTER, counting awards on which the scientist is PI or one of
  multiple PIs; one award per core project number; subprojects and intramural (Z) projects are not counted as grants. Matched
  by RePORTER profile ids in `data/scientists.json` (found by name search on 21 Nov 2026 and checked against institution and
  project titles; Dr. Blair has five profile ids). Hare, Viding and Kimonis have no RePORTER profile. Award amounts are not
  shown (the lab site does not publish grant dollar totals). See `pipeline/nih.py`.
- News pictures (owner's request): every carried-over post keeps the picture it had on the old site (`image` /
  `image_source` in `data/news_posts.json`, copied from the archive by `scripts/import_archive_images.py`). Exception: the
  DVD cover on "The Story of God with Morgan Freeman" is not reused (a photo of a public figure). Items without a picture,
  including all the newer ones, show an illustrated panel in the site's own design; the owner can supply photos (set `image`).
- Figures page: on the old page each caption sat ABOVE its image, so Figure 6 = 006.jpg, Figure 8 = 008.jpg, Figure 9 = 009.jpg;
  007.jpg (the paralimbic system) had no caption and was given a short one.
- Do NOT include any media from The Guardian (owner's instruction, 21 Nov 2026). None is on the site.
- Merchandise: the old CafePress shop is gone (404). `site/merchandise.html` is a shop page driven by `data/merch.json`
  (mug, T-shirt, teddy bear, drawn as original illustrations); products show "Coming soon" until `shop_url`/`buy_url` are set.
  A static site cannot take payments itself; a storefront account (the owner's choice) is needed.
- Other images: the book figures, cover, merchandise picture and the owner's portrait. Scholar screenshots and photos of
  other scientists from the old site are not reused. Do not download photos of people from the web.
- Not checked yet: the old external links (CafePress shop, Twitter, Facebook, scientists' faculty pages, older news links).

## Working
- `python3 -m pipeline.build_site`; preview with `python3 -m http.server 8765 --directory site`.
- `python3 -m pipeline.update_metrics --dry-run` to test the monthly refresh.
- Site address lives in pipeline/config.py, site/assets/config.js and the page heads: change with `scripts/set_site_url.py`.
- Bump `?v=` on app.css/site.css/app.js/layout.js when they change.
- Visit counter (owner's request, 26 Nov 2026): GoatCounter, site code `psychopath` (`goatcounterCode` in
  `site/assets/config.js`, loaded by `layout.js` only on the live domain). The owner's private dashboard is
  psychopath.goatcounter.com; the lab site uses the separate code `kkiehl`.
