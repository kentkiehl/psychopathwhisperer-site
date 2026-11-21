"""Build the static site's data files from data/ into site/.

Outputs:
  site/data/*.json   copied from data/ (news_posts, scientists, works, praise, figures)
  site/feed.xml      RSS of the news posts
  site/sitemap.xml, site/robots.txt

    python3 -m pipeline.build_site
"""
import json
import re
import shutil
import time
from email.utils import formatdate
from xml.sax.saxutils import escape
from . import config

COPIED = ["news_posts.json", "scientists.json", "works.json", "praise.json", "figures.json"]


def sort_key(d):
    d = str(d or "")
    return d + "-12-31" if len(d) == 4 else d + "-31" if len(d) == 7 else d


def rfc822(d):
    d = str(d or "")
    y, m, day = (d.split("-") + ["1", "1"])[:3]
    return formatdate(time.mktime((int(y), int(m), int(day), 12, 0, 0, 0, 0, 0)), usegmt=True)


def main():
    config.SITE_DATA.mkdir(parents=True, exist_ok=True)
    for name in COPIED:
        json.loads((config.DATA / name).read_text(encoding="utf-8"))  # fail loudly on a broken file
        shutil.copyfile(config.DATA / name, config.SITE_DATA / name)

    posts = json.loads((config.DATA / "news_posts.json").read_text(encoding="utf-8"))
    ids = [p["id"] for p in posts]
    assert len(ids) == len(set(ids)), "duplicate news post id"
    posts.sort(key=lambda p: sort_key(p["date"]), reverse=True)
    items = []
    for p in posts[: config.FEED_CAP]:
        link = p.get("url") or f"{config.SITE_URL}/news.html#{p['id']}"
        text = re.sub(r"<[^>]+>", "", p["html"]).strip()
        items.append(f"<item><title>{escape(p['title'])}</title><link>{escape(link)}</link><guid isPermaLink=\"false\">{escape(p['id'])}</guid>"
                     f"<pubDate>{rfc822(p['date'])}</pubDate><description>{escape(text[:500])}</description></item>")
    (config.SITE / "feed.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>{escape(config.SITE_NAME)}: news</title>'
        f"<link>{config.SITE_URL}/news.html</link><description>News and press about the science of psychopathy.</description>\n"
        + "\n".join(items) + "\n</channel></rss>\n", encoding="utf-8")

    today = time.strftime("%Y-%m-%d")
    urls = "".join(f"<url><loc>{config.SITE_URL}/{'' if p == 'index.html' else p}</loc><lastmod>{today}</lastmod></url>\n" for p in config.PAGES)
    (config.SITE / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    (config.SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {config.SITE_URL}/sitemap.xml\n", encoding="utf-8")
    print(f"built: {len(COPIED)} data files, {len(items)} feed items, {len(config.PAGES)} pages in sitemap")


if __name__ == "__main__":
    main()
