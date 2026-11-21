# The Psychopath Whisperer website

Website for *The Psychopath Whisperer: The Science of Those Without Conscience* by Kent A. Kiehl, PhD, and for news and
rankings in the science of psychopathy. Planned address: **https://psychopathwhisperer.com**. Not published yet.

It uses the same open-source framework as the [Kiehl Lab site](https://github.com/kentkiehl/kiehl-site) (built by Tor Wager
for the CANlab and Jakubzick Lab sites): a static site with plain JSON data and an automated update job. Content was
carried over from the WordPress site psychopathwhisperer.com in November 2026.

- **Static site** in `site/` (no build step for the HTML; `pipeline/build_site.py` copies the data into `site/data/` and
  writes `feed.xml`, `sitemap.xml` and `robots.txt`).
- **Data** as plain JSON in `data/`:
  `news_posts.json` (news and press; newest first on the home page and the News page),
  `scientists.json` (Top scientists, with Google Scholar figures), `works.json` (Top science and Top books),
  `praise.json` (reviews), `figures.json` (color figures from the book), `metrics_history.json` (one line per monthly run).
- **Monthly workflow** (`.github/workflows/monthly.yml`, first of each month): re-reads every scientist's Google Scholar
  profile, adds OpenAlex citation counts for the listed papers, commits the new figures, rebuilds and deploys.
  If Google refuses the automated request for a profile, that scientist keeps the previous figures and date, and the
  workflow opens an issue when no profile could be read at all.

## Pages

Home · The book · Reviews and praise · Figures in color · News and press · Top science · Top scientists · Top books ·
Blog (under revision) · Awards · Merchandise · Donate · About.

## Everyday edits

- **Add a news item**: add an entry at the top of `data/news_posts.json` (`id`, `date` as `YYYY-MM-DD`, `title`, `source`,
  `kind`: press, tv, podcast, interview, talk, award, book or essay; `url`; `html`).
- **Add a scientist**: add an entry to `data/scientists.json` with the `scholar_id` from the profile address
  (`scholar.google.com/citations?user=<scholar_id>`); the figures fill in at the next monthly run.
- **Re-read the per-paper Google Scholar counts** on Top science and Top books: edit `scholar_citations` and `scholar_as_of`
  in `data/works.json`.
- **Blog**: `site/blog.html` shows an "Under revision" notice. Replace it when a decision is made.

## Things still to add by hand

- **Images from the old site**: `python3 scripts/import_archive_images.py <archive folder>` copies the four color figures,
  the book cover and the merchandise picture into `site/assets/img/`. Until then the pages show placeholders.
- **Old external links** (merchandise shop, Twitter, Facebook, faculty pages, some news links from 2014 to 2015) have not
  been checked.

## Local use

```bash
pip install -r requirements.txt
python3 -m pipeline.build_site                 # writes site/data, feed.xml, sitemap.xml
(cd site && python3 -m http.server 8765)       # http://localhost:8765
python3 -m pipeline.update_metrics --dry-run   # test the monthly refresh without saving
```

## Publishing (only when the owner says so)

1. Create the GitHub repository (`psychopathwhisperer-site`) and push this folder to its `main` branch.
2. For a test address first: `python3 scripts/set_site_url.py <github-username> psychopathwhisperer-site`, push, then
   Settings → Pages → Source "GitHub Actions". The site appears at `https://<username>.github.io/psychopathwhisperer-site`.
3. Variables (Settings → Secrets and variables → Actions → Variables): `PW_SITE_URL` (the site address) and
   `PW_CONTACT_EMAIL` (sent to OpenAlex with the monthly lookups).
4. To move the real domain: `python3 scripts/set_site_url.py --domain psychopathwhisperer.com`, push, set the custom
   domain under Settings → Pages, then at Bluehost (where the DNS is) change only the web records: the `A` records for
   `psychopathwhisperer.com` to GitHub Pages' addresses and the `www` `CNAME` to `<username>.github.io`.
   **Leave the MX and TXT records exactly as they are: email for the domain runs through Google.**
5. Keep the WordPress site and its files at Bluehost until the new site has been checked at the real address.

## Licences

Code: MIT (framework by Tor Wager). Text and figures: © Kent A. Kiehl. Quoted reviews remain the property of their authors.
