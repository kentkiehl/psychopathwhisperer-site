"""Copy the images this site uses out of the archive of the old WordPress site.

    python3 scripts/import_archive_images.py ../psychopathwhisperer-archive-2026-11-21

Takes the archive folder (the one that contains media/2014/03/007.jpg and so on). Only the owner's own material is
copied: the color figures from the book, the book cover and the merchandise picture. Outlet logos and photos of other
people in the archive are not used on the new site.
"""
import shutil, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "site" / "assets" / "img"
WANTED = {
    "media/2014/03/007.jpg": "figures/007.jpg",
    "media/2014/03/006.jpg": "figures/006.jpg",
    "media/2014/03/008.jpg": "figures/008.jpg",
    "media/2014/03/009.jpg": "figures/009.jpg",
    "media/2014/03/PW-book.jpg": "psychopath-whisperer-cover.jpg",
    "media/2019/09/merch.png": "merch.png",
}
if len(sys.argv) != 2:
    sys.exit(__doc__)
src = Path(sys.argv[1])
for a, b in WANTED.items():
    if (src / a).exists():
        (IMG / b).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src / a, IMG / b); print("copied ", b)
    else:
        print("MISSING", a)
