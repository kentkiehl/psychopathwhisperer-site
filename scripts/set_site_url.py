"""Point the site at a different address (for example a github.io address while testing).

    python3 scripts/set_site_url.py <github-username> [repo-name]     -> https://<username>.github.io/<repo-name>
    python3 scripts/set_site_url.py --domain psychopathwhisperer.com  -> https://psychopathwhisperer.com (also writes site/CNAME)

Rewrites the address in the HTML pages, site/assets/config.js and pipeline/config.py. site/CNAME is what tells GitHub
Pages to serve the custom domain; it is deliberately absent until the owner decides to publish there.
"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
args = sys.argv[1:]
domain = None
if args[:1] == ["--domain"]:
    domain, args = args[1], args[2:]
user = args[0] if args else None
repo = args[1] if len(args) > 1 else "psychopathwhisperer-site"
if not (user or domain):
    sys.exit(__doc__)
new_url = f"https://{domain}" if domain else f"https://{user}.github.io/{repo}"
cfg = (ROOT / "pipeline" / "config.py").read_text()
old_url = re.search(r'or "(https://[^"]+)"\)\.rstrip', cfg).group(1)
files = list((ROOT / "site").glob("*.html")) + [ROOT / "site" / "assets" / "config.js", ROOT / "pipeline" / "config.py"]
n = 0
for f in files:
    s = f.read_text(); t = s.replace(old_url, new_url)
    if t != s:
        f.write_text(t); n += 1
cname = ROOT / "site" / "CNAME"
if domain:
    cname.write_text(domain + "\n")
elif cname.exists():
    cname.unlink()
print(f"{old_url} -> {new_url} in {n} files. Now run: python3 -m pipeline.build_site")
