"""Prepare photos for a deliverable: upright (EXIF rotation applied), resized, saved as JPEG in project/assets/photos/ready/.

    python general/tools/photo_prep.py                      # every new photo in project/assets/photos/raw/
    python general/tools/photo_prep.py IMG_1234.jpg --name hand_assembly --max 1600
    python general/tools/photo_prep.py --dates              # list raw/ photos with the date each was taken

Originals in raw/ are never changed. A file already in ready/ is skipped unless --force. HEIC needs pillow-heif.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "project" / "assets" / "photos" / "raw"
READY = ROOT / "project" / "assets" / "photos" / "ready"
EXTS = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".bmp", ".tif", ".tiff"}


def prepare(src, dst, longest=1600, quality=85):
    """Write an upright, resized JPEG copy of src to dst; returns its (width, height)."""
    if src.suffix.lower() == ".heic":
        from pillow_heif import register_heif_opener   # optional dependency
        register_heif_opener()
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((longest, longest))
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, quality=quality)
    return im.size


def taken(src):
    """When the photo was taken: ("YYYY-MM-DD HH:MM", "exif") from EXIF, else the file's modified time and "file"."""
    import datetime
    try:
        with Image.open(src) as im:
            ex = im.getexif()
            raw = ex.get_ifd(0x8769).get(0x9003) or ex.get(0x0132)      # DateTimeOriginal, else DateTime
        if raw:
            return datetime.datetime.strptime(str(raw)[:19], "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d %H:%M"), "exif"
    except (OSError, ValueError):
        pass
    return datetime.datetime.fromtimestamp(src.stat().st_mtime).strftime("%Y-%m-%d %H:%M"), "file"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="photos in raw/ (default: all of them)")
    ap.add_argument("--name", help="output name (one file only), without extension")
    ap.add_argument("--max", type=int, default=1600, help="longest side in pixels")
    ap.add_argument("--force", action="store_true", help="redo files already in ready/")
    a = ap.parse_args(argv)
    files = [RAW / f if not Path(f).is_absolute() else Path(f) for f in a.files] or \
        sorted(f for f in RAW.iterdir() if f.suffix.lower() in EXTS)
    if a.name and len(files) != 1:
        ap.error("--name needs exactly one file")
    for src in files:
        stem = a.name or src.stem.lower().replace(" ", "_").replace("(", "").replace(")", "")
        dst = READY / f"{stem}.jpg"
        if dst.exists() and not a.force:
            print("skip (exists)", dst.name)
            continue
        w, h = prepare(src, dst, a.max)
        print(f"{src.name} -> {dst.relative_to(ROOT)} ({w} x {h})")


if __name__ == "__main__":
    main()
