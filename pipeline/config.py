import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SITE = ROOT / "site"
SITE_DATA = SITE / "data"

SITE_URL = (os.environ.get("PW_SITE_URL") or "https://kentkiehl.github.io/psychopathwhisperer-site").rstrip("/")
SITE_NAME = "The Psychopath Whisperer"
CONTACT_EMAIL = os.environ.get("PW_CONTACT_EMAIL", "")   # polite-pool address for OpenAlex (repository variable)
TOOL_NAME = "psychopathwhisperer-site"
FEED_CAP = 30
PAGES = ["index.html", "book.html", "praise.html", "figures.html", "news.html", "science.html", "scientists.html",
         "top-books.html", "blog.html", "awards.html", "merchandise.html", "donate.html", "about.html"]
