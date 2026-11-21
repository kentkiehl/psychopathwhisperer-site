"""Bundle the whole site into ONE self-contained HTML file for a private preview (for example a Claude artifact).

    python3 -m pipeline.build_site && python3 scripts/make_preview.py [out.html]

Every page becomes a view switched by the address hash (#book, #news, ...); data files, styles, scripts and images are
inlined. The real site in site/ is not changed. Default output: work/preview.html (gitignored).
"""
import base64, json, mimetypes, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
sys.path.insert(0, str(ROOT))
from pipeline import config

out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "work" / "preview.html"
out.parent.mkdir(parents=True, exist_ok=True)

def data_uri(p):
    return f"data:{mimetypes.guess_type(p.name)[0]};base64,{base64.b64encode(p.read_bytes()).decode()}"

images = {str(p.relative_to(SITE)): data_uri(p) for p in (SITE / "assets" / "img").rglob("*") if p.is_file()}
images["assets/logo-mark.png"] = data_uri(SITE / "assets" / "logo-mark.png")
data = {f"data/{p.name}": json.loads(p.read_text(encoding="utf-8")) for p in (SITE / "data").glob("*.json")}
pages = {}
for name in config.PAGES:
    h = (SITE / name).read_text(encoding="utf-8")
    body = re.search(r'<div id="site-header"></div>\s*(.*?)\s*<div id="site-footer"></div>', h, re.S).group(1)
    style = "".join(re.findall(r"<style>(.*?)</style>", h, re.S))
    script = "".join(re.findall(r"<script>(.*?)</script>", h, re.S))
    title = re.search(r"<title>(.*?)</title>", h).group(1)
    pages[name[:-5]] = {"body": body, "style": style, "script": script, "title": title}

js = lambda n: (SITE / "assets" / n).read_text(encoding="utf-8")
css = (SITE / "assets" / "app.css").read_text(encoding="utf-8") + (SITE / "assets" / "site.css").read_text(encoding="utf-8")
safe = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Preview: psychopathwhisperer.com rebuild</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..600,0..100;1,9..144,300..600,0..100&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{css}
.preview-bar {{ position: fixed; left: 0; right: 0; bottom: 0; z-index: 200; background: #1a2332; color: #eef0f3; font: 500 .8rem/1.3 var(--sans); padding: .5rem 1rem; text-align: center; }}
body {{ padding-bottom: 2.4rem; }}
</style>
<style id="page-style"></style>
</head>
<body>
<div id="site-header"></div>
<div id="view"></div>
<div id="site-footer"></div>
<div class="preview-bar">Private preview of the rebuilt psychopathwhisperer.com · not published · built {__import__("time").strftime("%d %b %Y")}</div>
<script>
const __PAGES = {safe(pages)}, __DATA = {safe(data)}, __IMG = {safe(images)};
{js("config.js")}
{js("app.js")}
CL.getJSON = async p => {{ if (!(p in __DATA)) throw new Error(p + ": not in preview"); return JSON.parse(JSON.stringify(__DATA[p])); }};
const __img = h => h.replace(/(src|href)="(assets\\/[^"?]+)(\\?[^"]*)?"/g, (m, a, f) => __IMG[f] ? `${{a}}="${{__IMG[f]}}"` : m);
// images that are probed for (book cover, merchandise) come from the inlined set when present
(function () {{ const NativeImage = window.Image; window.Image = function () {{ const im = new NativeImage(); const d = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, "src");
  Object.defineProperty(im, "src", {{ set(v) {{ d.set.call(im, __IMG[v] || v); }}, get() {{ return d.get.call(im); }} }}); return im; }}; }})();
function __route() {{
  let name = (location.hash || "#index").slice(1); if (!__PAGES[name]) name = "index";
  const p = __PAGES[name];
  document.getElementById("page-style").textContent = p.style;
  document.getElementById("view").innerHTML = __img(p.body);
  document.querySelectorAll("#view img").forEach(im => {{ const s = im.getAttribute("src"); if (__IMG[s]) im.src = __IMG[s]; }});
  document.querySelectorAll("#view .rv").forEach(el => el.classList.add("in"));
  document.querySelectorAll(".nav a").forEach(a => a.classList.toggle("active", a.dataset.page === name));
  window.scrollTo(0, 0);
  try {{ (0, eval)(p.script); }} catch (e) {{ console.error(e); }}
  // images rendered later by the page script
  new MutationObserver(() => document.querySelectorAll("#view img").forEach(im => {{ const s = im.getAttribute("src"); if (__IMG[s]) im.src = __IMG[s]; }})).observe(document.getElementById("view"), {{ childList: true, subtree: true }});
}}
// internal links (book.html, news.html#id, ./) switch views instead of loading a file
document.addEventListener("click", e => {{
  const a = e.target.closest("a[href]"); if (!a) return; const h = a.getAttribute("href");
  const m = /^(?:\\.\\/|([a-z-]+)\\.html)(?:#.*)?$/.exec(h); if (!m) return;
  e.preventDefault(); const name = m[1] || "index"; if (__PAGES[name]) {{ if (location.hash === "#" + name) __route(); else location.hash = name; }}
}});
window.addEventListener("hashchange", __route);
</script>
<script>{js("layout.js")}</script>
<script>
document.querySelectorAll(".site-header img, .site-footer img").forEach(im => {{ const s = im.getAttribute("src"); if (__IMG[s]) im.src = __IMG[s]; }});
document.querySelectorAll(".nav a").forEach(a => {{ const m = /^([a-z-]+)\\.html/.exec(a.getAttribute("href") || ""); if (m) a.dataset.page = m[1]; }});
__route();
</script>
</body>
</html>
"""
out.write_text(html, encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size // 1024} KB, {len(pages)} pages)")
