"""Monthly refresh of the citation figures (run by .github/workflows/monthly.yml on the first of each month).

1. Top scientists (data/scientists.json): reads each scientist's public Google Scholar profile page, one request per
   scientist with a pause between them (profile pages are the part of Scholar that its robots.txt allows). Google
   sometimes refuses automated requests; when a profile cannot be read, that scientist's previous figures are kept
   together with their own "as_of" date, and the run reports it. Nothing is guessed and no check is bypassed.
2. Top science (data/works.json): adds an OpenAlex citation count for every work that has a DOI. Google Scholar has no
   interface for per-paper counts, so the Scholar numbers on that page are dated snapshots, updated by hand
   (or by asking Claude to re-read them).
3. Appends one line per run to data/metrics_history.json.

    python3 -m pipeline.update_metrics [--dry-run]
"""
import json
import re
import sys
import time
import requests
from . import config

UA = f"{config.TOOL_NAME}/1.0 (monthly citation refresh for {config.SITE_URL}; {config.CONTACT_EMAIL or 'no contact set'})"
SCHOLAR = "https://scholar.google.com/citations?hl=en&user={}"
OPENALEX = "https://api.openalex.org/works/doi:{}"
PAUSE = 8  # seconds between Scholar requests


def parse_scholar(html):
    """Return the six numbers of the profile's statistics table, or None if the page is not a profile."""
    table = re.search(r'<table id="gsc_rsb_st".*?</table>', html, re.S)
    if not table:
        return None
    nums = [int(x) for x in re.findall(r'<td class="gsc_rsb_std">(\d+)</td>', table.group(0))]
    if len(nums) != 6:
        return None
    since = re.search(r"Since (\d{4})", table.group(0))
    c, c5, h, h5, i, i5 = nums
    return {"citations": c, "citations_since": c5, "h_index": h, "h_index_since": h5, "i10_index": i, "i10_index_since": i5,
            "since_year": int(since.group(1)) if since else None}


def update_scientists(today):
    path = config.DATA / "scientists.json"
    d = json.loads(path.read_text(encoding="utf-8"))
    ok, failed = 0, []
    for n, s in enumerate(d["scientists"]):
        if n:
            time.sleep(PAUSE)
        try:
            r = requests.get(SCHOLAR.format(s["scholar_id"]), headers={"User-Agent": UA, "Accept-Language": "en"}, timeout=30)
            got = parse_scholar(r.text) if r.status_code == 200 else None
        except requests.RequestException as e:
            got = None
            print(f"  {s['name']}: {e}")
        # sanity check: lifetime citations do not fall by much; a big drop means the wrong page was read
        if got and got["citations"] >= 0.9 * s["scholar"].get("citations", 0):
            s["scholar"] = {**got, "as_of": today}
            ok += 1
            print(f"  {s['name']}: {got['citations']:,} citations, h-index {got['h_index']}")
        else:
            failed.append(s["name"])
            print(f"  {s['name']}: not read; keeping the figures of {s['scholar'].get('as_of')}")
    if ok:
        d["updated"] = today
    return path, d, ok, failed


def update_works(today):
    path = config.DATA / "works.json"
    d = json.loads(path.read_text(encoding="utf-8"))
    ok, failed = 0, []
    params = {"select": "id,cited_by_count", **({"mailto": config.CONTACT_EMAIL} if config.CONTACT_EMAIL else {})}
    for w in [w for s in d["sections"] for w in s["items"]] + d.get("books", []):
        if not w.get("doi"):
            continue
        try:
            r = requests.get(OPENALEX.format(w["doi"]), params=params, headers={"User-Agent": UA}, timeout=30)
            r.raise_for_status()
            w["openalex_citations"], w["openalex_as_of"] = int(r.json()["cited_by_count"]), today
            ok += 1
        except (requests.RequestException, KeyError, ValueError) as e:
            failed.append(w["id"])
            print(f"  {w['id']}: OpenAlex lookup failed ({e})")
        time.sleep(0.3)
    return path, d, ok, failed


def main():
    dry = "--dry-run" in sys.argv
    today = time.strftime("%Y-%m-%d")
    print("Google Scholar profiles:")
    sp, sd, s_ok, s_failed = update_scientists(today)
    print("OpenAlex counts for works with a DOI:")
    wp, wd, w_ok, w_failed = update_works(today)
    hist_path = config.DATA / "metrics_history.json"
    hist = json.loads(hist_path.read_text(encoding="utf-8")) if hist_path.exists() else []
    hist.append({"date": today, "scholar_profiles_read": s_ok, "scholar_profiles_failed": s_failed, "openalex_works_read": w_ok,
                 "scientists": {s["id"]: [s["scholar"]["citations"], s["scholar"]["h_index"], s["scholar"]["as_of"]] for s in sd["scientists"]}})
    print(f"scientists refreshed: {s_ok}/{len(sd['scientists'])}; works refreshed: {w_ok}")
    if not dry:
        for p, obj in ((sp, sd), (wp, wd), (hist_path, hist)):
            p.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    if s_ok == 0:
        # make the failure visible (the workflow opens an issue) but leave the data as it was
        sys.exit("No Google Scholar profile could be read this month; the previous figures were kept.")


if __name__ == "__main__":
    main()
