"""Save shaded-view PNGs of an Onshape Part Studio or Assembly, for brochure and poster pages.

    python general/tools/onshape_images.py <onshape element URL> --name finger --views isometric front top
    python general/tools/onshape_images.py <URL> --name finger --views isometric --size 2400 1800 --no-edges

Writes project/assets/cad/onshape_<name>_<view>.png (never overwrites: adds _2, _3 ...) and a line per image
in project/assets/cad/ONSHAPE_LOG.md (URL, view, size, date).

API keys: create them yourself at https://dev-portal.onshape.com/keys with **read** permission only, then either set
the environment variables ONSHAPE_ACCESS_KEY and ONSHAPE_SECRET_KEY, or save
    {"access_key": "...", "secret_key": "..."}
as %USERPROFILE%\\.onshape\\keys.json (outside the repo). The keys are sent only to the onshape.com address in the URL and never printed.
Uses the Onshape REST API (shadedviews endpoints, HTTP Basic auth with API keys) and only reads the document.
Checked against the API reference on 2026-10-19: viewMatrix = a named view (front/back/top/bottom/left/right) or 12
numbers; pixelSize 0 = fit the model to the image. The `edges` and `useAntiAliasing` options are not yet confirmed
on a real call. Not yet run against a real document (needs the user's keys).
"""
import argparse
import base64
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "project" / "assets" / "cad"
KEY_FILE = Path.home() / ".onshape" / "keys.json"
NAMED_VIEWS = ("front", "back", "top", "bottom", "left", "right")      # the API's own named views
# "isometric" is not a named view in the API, so it is sent as a view matrix (3 x 4, row-major, last column = pan in m)
MATRICES = {"isometric": "0.707,0.707,0,0,-0.409,0.409,0.816,0,0.577,-0.577,0.577,0"}
URL_RE = re.compile(r"https://(?P<host>[\w.-]*onshape\.com)/documents/(?P<did>[0-9a-f]{24})/(?P<wvm>[wvm])/"
                    r"(?P<wvmid>[0-9a-f]{24})/e/(?P<eid>[0-9a-f]{24})")


def parse_url(url):
    """Onshape element URL -> dict(did, wvm, wvmid, eid). Raises ValueError for anything else."""
    m = URL_RE.match(url.strip())
    if not m:
        raise ValueError("expected an Onshape element URL like https://cad.onshape.com/documents/<id>/w/<id>/e/<id>")
    return {k: m.group(k) for k in ("host", "did", "wvm", "wvmid", "eid")}


def load_keys():
    a, s = os.environ.get("ONSHAPE_ACCESS_KEY"), os.environ.get("ONSHAPE_SECRET_KEY")
    if a and s:
        return a, s
    if KEY_FILE.exists():
        d = json.loads(KEY_FILE.read_text(encoding="utf-8"))
        return d["access_key"], d["secret_key"]
    raise SystemExit(f"No Onshape API keys: set ONSHAPE_ACCESS_KEY / ONSHAPE_SECRET_KEY or create {KEY_FILE} "
                     "(read-only keys from https://dev-portal.onshape.com/keys).")


def _get(host, path, params, keys):
    api = f"https://{host}/api"     # cad.onshape.com, or a school/company address such as x.onshape.com
    url = f"{api}{path}?{urllib.parse.urlencode(params)}" if params else f"{api}{path}"
    token = base64.b64encode(f"{keys[0]}:{keys[1]}".encode()).decode()
    req = urllib.request.Request(url, headers={"Authorization": f"Basic {token}",
                                              "Accept": "application/json;charset=UTF-8; qs=0.09"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Onshape API error {e.code} for {path}: {e.read().decode(errors='replace')[:300]}") from None


def element_kind(ids, keys):
    """'partstudios' or 'assemblies' for the element in the URL."""
    els = _get(ids["host"], f"/documents/d/{ids['did']}/{ids['wvm']}/{ids['wvmid']}/elements", {"elementId": ids["eid"]}, keys)
    kind = (els[0].get("elementType") if els else "") or ""
    if kind == "PARTSTUDIO":
        return "partstudios"
    if kind == "ASSEMBLY":
        return "assemblies"
    raise SystemExit(f"element type {kind!r} has no shaded view (needs a Part Studio or an Assembly)")


def shaded_view_params(view, width, height, edges):
    matrix = MATRICES.get(view, view)
    if matrix not in NAMED_VIEWS and not re.fullmatch(r"(-?[\d.]+,){11}-?[\d.]+", matrix):
        raise ValueError(f"view must be one of {NAMED_VIEWS + tuple(MATRICES)} or 12 comma-separated numbers")
    return {"viewMatrix": matrix, "outputWidth": width, "outputHeight": height, "pixelSize": 0,
            "edges": "show" if edges else "hide", "useAntiAliasing": "true"}


def free_path(name, view):
    base = OUT / f"onshape_{name}_{view if view in NAMED_VIEWS or view in MATRICES else 'custom'}"
    path, n = base.with_suffix(".png"), 2
    while path.exists():
        path, n = Path(f"{base}_{n}.png"), n + 1
    return path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", help="Onshape Part Studio or Assembly URL (copy it from the browser address bar)")
    ap.add_argument("--name", required=True, help="short file-name label, e.g. finger")
    ap.add_argument("--views", nargs="+", default=["isometric"], help="named views or 12-number view matrices")
    ap.add_argument("--size", nargs=2, type=int, default=[2000, 1500], metavar=("W", "H"))
    ap.add_argument("--no-edges", action="store_true", help="hide black edge lines")
    a = ap.parse_args(argv)
    if not re.fullmatch(r"[\w-]+", a.name):
        ap.error("--name: letters, digits, _ and - only")

    ids = parse_url(a.url)
    keys = load_keys()
    kind = element_kind(ids, keys)
    OUT.mkdir(parents=True, exist_ok=True)
    log = OUT / "ONSHAPE_LOG.md"
    if not log.exists():
        log.write_text("# Onshape images (saved by tools/onshape_images.py)\n\n| File | Element URL | View | Size | Date |\n"
                       "|---|---|---|---|---|\n", encoding="utf-8")
    for view in a.views:
        params = shaded_view_params(view, *a.size, edges=not a.no_edges)
        res = _get(ids["host"], f"/{kind}/d/{ids['did']}/{ids['wvm']}/{ids['wvmid']}/e/{ids['eid']}/shadedviews", params, keys)
        images = res.get("images") or []
        if not images:
            raise SystemExit(f"Onshape returned no image for view {view!r}")
        path = free_path(a.name, view)
        path.write_bytes(base64.b64decode(images[0]))
        with log.open("a", encoding="utf-8") as f:
            f.write(f"| {path.name} | {a.url.strip()} | {view} | {a.size[0]} x {a.size[1]} | {datetime.date.today()} |\n")
        print(path)


if __name__ == "__main__":
    sys.exit(main())
