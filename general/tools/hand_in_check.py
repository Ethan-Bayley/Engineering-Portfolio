"""Check a deliverable PDF before it is handed in. Prints PASS / WARN / FAIL lines and exits 1 if anything failed.

    python general/tools/hand_in_check.py project/outputs/brochure/brochure_v07.pdf --max-pages 20
    python general/tools/hand_in_check.py --deliverable brochure          # the newest PDF in project/outputs/brochure/

Checks: every font embedded (and which fonts), page count against --max-pages, page size and orientation, placeholder
text left in (<...>, TODO, XX, Still to add, lorem), mentions of AI tools, very small text, file size against
--max-mb, the matching .pptx version exists, and days left until the deadline in project/PROJECT.md.
It cannot judge content: run the marking-loop skill for that.
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:          # older pymupdf
    import fitz

ROOT = Path(__file__).resolve().parents[2]
PLACEHOLDERS = [r"<[a-z][^<>\n]{0,60}>", r"\bTODO\b", r"\bTBC\b", r"\bXX+\b", r"Still to add", r"\blorem\b",
                r"\?\?\?"]
AI_WORDS = [r"\bChatGPT\b", r"\bGPT-\d", r"\bClaude\b", r"\bGemini\b", r"\bCopilot\b", r"AI[- ]generated",
            r"generated (?:by|with) AI", r"\bMidjourney\b", r"\bDALL.?E\b"]
SIZES = {"A4": (595.3, 841.9), "A3": (841.9, 1190.6)}


def deadline(project_md=ROOT / "project" / "PROJECT.md"):
    """The first 'Deadline: YYYY-MM-DD [HH:MM]' in PROJECT.md, as a datetime, or None."""
    if not project_md.exists():
        return None
    m = re.search(r"Deadline:\s*(\d{4}-\d{2}-\d{2})(?:[ T](\d{1,2}:\d{2}))?", project_md.read_text(encoding="utf-8"))
    if not m:
        return None
    return datetime.datetime.strptime(f"{m.group(1)} {m.group(2) or '23:59'}", "%Y-%m-%d %H:%M")


def page_size(w, h):
    for name, (a, b) in SIZES.items():
        if abs(min(w, h) - a) < 3 and abs(max(w, h) - b) < 3:
            return f"{name} {'landscape' if w > h else 'portrait'}"
    if abs(w / h - 16 / 9) < 0.01:
        return "16:9 slides"
    return f"{w:.0f} x {h:.0f} pt"


def check(pdf, max_pages=None, max_mb=None, min_pt=7.0, now=None):
    """Return a list of (level, message); level is PASS, WARN or FAIL."""
    out = []
    doc = fitz.open(pdf)
    n = doc.page_count
    if max_pages:
        out.append(("PASS" if n <= max_pages else "FAIL", f"{n} pages (limit {max_pages})"))
    else:
        out.append(("PASS", f"{n} pages (no limit given: pass --max-pages)"))

    sizes = {page_size(p.rect.width, p.rect.height) for p in doc}
    out.append(("PASS" if len(sizes) == 1 else "WARN", "page size: " + ", ".join(sorted(sizes))))

    fonts, unembedded = set(), set()
    for i in range(n):
        for xref, ext, _type, base, *_ in doc.get_page_fonts(i, full=True):
            name = base.split("+", 1)[-1]
            fonts.add(name)
            if ext == "n/a":
                unembedded.add(name)
    out.append(("FAIL" if unembedded else "PASS",
                f"fonts not embedded: {', '.join(sorted(unembedded))}" if unembedded
                else f"all fonts embedded ({', '.join(sorted(fonts)) or 'no text'})"))
    if any("Calibri" in f or "Arial" in f for f in fonts) and any("Inter" in f for f in fonts):
        out.append(("WARN", "Inter mixed with Calibri/Arial: a text box may have lost its font (export with export_pdf.py)"))

    small, holders, ai = [], [], []
    for i, page in enumerate(doc, 1):
        text = page.get_text()
        for pat in PLACEHOLDERS:
            holders += [(i, m.group(0)) for m in re.finditer(pat, text, 0 if "XX" in pat or "TODO" in pat else re.I)]
        for pat in AI_WORDS:
            ai += [(i, m.group(0)) for m in re.finditer(pat, text, re.I)]
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    if span["text"].strip() and span["size"] < min_pt - 0.05:
                        small.append((i, round(span["size"], 1), span["text"].strip()[:30]))
    out.append(("FAIL" if holders else "PASS", "placeholder text: " + "; ".join(f"p{p} {t!r}" for p, t in holders[:12])
                if holders else "no placeholder text"))
    out.append(("WARN" if ai else "PASS", "AI tools mentioned: " + "; ".join(f"p{p} {t!r}" for p, t in ai[:8])
                if ai else "no AI tools mentioned"))
    out.append(("WARN" if small else "PASS", f"{len(small)} text runs under {min_pt} pt, e.g. "
                + "; ".join(f"p{p} {s} pt {t!r}" for p, s, t in small[:5]) if small else f"no text under {min_pt} pt"))

    mb = Path(pdf).stat().st_size / 1e6
    if max_mb:
        out.append(("PASS" if mb <= max_mb else "FAIL", f"file size {mb:.1f} MB (limit {max_mb} MB)"))
    else:
        out.append(("PASS", f"file size {mb:.1f} MB"))

    pptx = Path(pdf).with_suffix(".pptx")
    out.append(("PASS" if pptx.exists() else "WARN",
                f"source deck {pptx.name} is next to it" if pptx.exists() else f"no {pptx.name} next to the PDF"))

    due = deadline()
    if due:
        left = due - (now or datetime.datetime.now())
        days = left.total_seconds() / 86400
        out.append(("PASS" if days >= 1 else "WARN" if days >= 0 else "FAIL",
                    f"deadline {due:%Y-%m-%d %H:%M}: {days:.1f} days left" if days >= 0 else f"deadline {due:%Y-%m-%d %H:%M} has passed"))
    else:
        out.append(("WARN", "no 'Deadline: YYYY-MM-DD HH:MM' in project/PROJECT.md"))
    return out


def newest_pdf(deliverable):
    folder = ROOT / "project" / "outputs" / deliverable
    pdfs = sorted(folder.glob("*_v*.pdf"), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)", p.stem)] or [0])
    if not pdfs:
        sys.exit(f"no versioned PDF in {folder}; export one with general/tools/export_pdf.py")
    return pdfs[-1]


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):          # Windows consoles are cp1252: PDF text can hold any character
        sys.stdout.reconfigure(errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", nargs="?")
    ap.add_argument("--deliverable", help="use the newest PDF in project/outputs/<deliverable>/")
    ap.add_argument("--max-pages", type=int)
    ap.add_argument("--max-mb", type=float)
    ap.add_argument("--min-pt", type=float, default=7.0, help="smallest text size allowed (default 7 pt)")
    a = ap.parse_args(argv)
    pdf = Path(a.pdf) if a.pdf else newest_pdf(a.deliverable) if a.deliverable else ap.error("give a PDF or --deliverable")
    results = check(pdf, a.max_pages, a.max_mb, a.min_pt)
    print(pdf)
    for level, msg in results:
        print(f"  {level:4}  {msg}")
    fails = sum(level == "FAIL" for level, _ in results)
    print(f"{fails} FAIL, {sum(level == 'WARN' for level, _ in results)} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
