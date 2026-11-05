"""Save a picture of a window on screen (for example Onshape in Chrome) to a PNG, with no API and no API credits.

    python general/tools/screen_grab.py --window Onshape --name finger_iso
    python general/tools/screen_grab.py --window Onshape --name finger_iso --crop 0.18,0.12,0.82,0.95
    python general/tools/screen_grab.py --list                     # visible window titles

Finds the first visible window whose title contains --window (case-insensitive), brings it to the front and saves
what is on screen inside it to project/assets/cad/<name>.png (never overwrites: adds _2, _3 ...), logged in
project/assets/cad/SCREEN_GRAB_LOG.md. --crop keeps a part of the window: left,top,right,bottom as fractions of its
width and height (or --crop-px in pixels), so the browser bar and Onshape's panels can be cut away.
--trim then cuts uniform background left round the model.

Windows only (uses the Win32 API through ctypes). The window must be visible and not covered: whatever is on screen
in that rectangle is what is saved. Nothing is sent anywhere.
"""
import argparse
import ctypes
import datetime
import sys
from pathlib import Path

from PIL import Image, ImageChops

if sys.platform == "win32":
    from ctypes import wintypes

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "project" / "assets" / "cad"


def _user32():
    if sys.platform != "win32":
        sys.exit("screen_grab.py works on Windows only")
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)      # real pixels, so the rectangle matches the screen
    except (AttributeError, OSError):
        pass
    return ctypes.windll.user32


def windows():
    """[(hwnd, title)] of visible top-level windows that have a title."""
    u = _user32()
    found = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def cb(hwnd, _lp):
        if u.IsWindowVisible(hwnd) and not u.IsIconic(hwnd):
            n = u.GetWindowTextLengthW(hwnd)
            if n:
                buf = ctypes.create_unicode_buffer(n + 1)
                u.GetWindowTextW(hwnd, buf, n + 1)
                found.append((hwnd, buf.value))
        return True
    u.EnumWindows(cb, 0)
    return found


def window_rect(hwnd):
    """(left, top, right, bottom) of the window as drawn (without the drop shadow)."""
    r = wintypes.RECT()
    try:
        ctypes.windll.dwmapi.DwmGetWindowAttribute(hwnd, 9, ctypes.byref(r), ctypes.sizeof(r))  # extended frame bounds
    except (AttributeError, OSError):
        _user32().GetWindowRect(hwnd, ctypes.byref(r))
    return r.left, r.top, r.right, r.bottom


def crop_box(rect, frac=None, px=None):
    """The part of rect to keep: frac = (l, t, r, b) fractions of the window, px = pixels in from each edge."""
    left, top, right, bottom = rect
    w, h = right - left, bottom - top
    if frac:
        fl, ft, fr, fb = frac
        return (round(left + fl * w), round(top + ft * h), round(left + fr * w), round(top + fb * h))
    if px:
        pl, pt, pr, pb = px
        return (left + pl, top + pt, right - pr, bottom - pb)
    return rect


def trim(im, tolerance=12, margin=16):
    """Cut away the border that matches the top-left pixel's colour (the viewport background), keeping a margin."""
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > tolerance else 0)
    box = diff.getbbox()
    if not box:
        return im
    l, t, r, b = box
    return im.crop((max(0, l - margin), max(0, t - margin), min(im.width, r + margin), min(im.height, b + margin)))


def free_path(name, out=OUT):
    out.mkdir(parents=True, exist_ok=True)
    p, k = out / f"{name}.png", 2
    while p.exists():
        p, k = out / f"{name}_{k}.png", k + 1
    return p


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--window", help="part of the window title, e.g. Onshape")
    ap.add_argument("--name", help="file name without .png")
    ap.add_argument("--crop", help="l,t,r,b fractions of the window to keep, e.g. 0.18,0.12,0.82,0.95")
    ap.add_argument("--crop-px", help="l,t,r,b pixels to cut from each edge")
    ap.add_argument("--trim", action="store_true", help="also cut away plain background round the model")
    ap.add_argument("--note", default="", help="what the picture shows, for the log")
    ap.add_argument("--list", action="store_true", help="list visible window titles and stop")
    ap.add_argument("--out", type=Path, default=OUT, help="folder (default project/assets/cad)")
    a = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if a.list:
        for _h, t in windows():
            print(t)
        return
    if not (a.window and a.name):
        ap.error("--window and --name are needed (or --list)")
    match = [(h, t) for h, t in windows() if a.window.lower() in t.lower()]
    if not match:
        sys.exit(f"no visible window with {a.window!r} in its title; try --list")
    hwnd, title = match[0]
    u = _user32()
    u.SetForegroundWindow(hwnd)
    import time
    time.sleep(0.4)                                   # let it come to the front and redraw
    frac = tuple(float(x) for x in a.crop.split(",")) if a.crop else None
    px = tuple(int(x) for x in a.crop_px.split(",")) if a.crop_px else None
    box = crop_box(window_rect(hwnd), frac, px)
    from PIL import ImageGrab
    im = ImageGrab.grab(bbox=box, all_screens=True).convert("RGB")
    if a.trim:
        im = trim(im)
    path = free_path(a.name, a.out)
    im.save(path)
    log = a.out / "SCREEN_GRAB_LOG.md"
    if not log.exists():
        log.write_text("# Screen grabs\n\n| File | Date | Window | Size | Note |\n|---|---|---|---|---|\n", encoding="utf-8")
    with log.open("a", encoding="utf-8") as fh:
        fh.write(f"| {path.name} | {datetime.date.today()} | {title[:60]} | {im.width} x {im.height} | {a.note} |\n")
    print(f"{path}  ({im.width} x {im.height} px, from {title[:60]!r})")


if __name__ == "__main__":
    main()
