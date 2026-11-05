"""Charts as PNG files in the design system's look, drawn at the exact size they are placed, so chart text matches the
page text (brochure 8.5 pt, poster 9 pt, slides 13 pt: the format's table size).

    import charts
    charts.bars("project/assets/charts/speed.png", ["Detect", "Outline", "Plan"], [397, 1896, 9],
                size=(4.2, 1.6), fmt="brochure", unit=" ms", kept=[2])      # size in inches as placed
    box.picture(r, "project/assets/charts/speed.png", "Bar chart: time per stage")

Colours by meaning, as in the boxes: green = what we kept / the result, red = before / the problem, grey = the rest,
slate text. Every number on a chart must come from project/logs/ (say which section in the build script).
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from design_system import FORMATS, GREEN, ORANGE, PURPLE, RED, SLATE  # noqa: E402

for _f in (Path(__file__).resolve().parent / "fonts" / "Inter").glob("Inter-*.ttf"):
    font_manager.fontManager.addfont(str(_f))

GREY, LINE = "#AAB6C2", "#D0D8E0"
KEPT, BEFORE, CAUTION, OTHER = "#" + GREEN, "#" + RED, "#" + ORANGE, "#" + PURPLE
TEXT = "#" + SLATE


def _style(fmt):
    size = FORMATS[fmt].table
    plt.rcParams.update({"font.family": "Inter", "font.size": size, "text.color": TEXT, "axes.labelcolor": TEXT,
                         "xtick.color": TEXT, "ytick.color": TEXT, "axes.edgecolor": LINE, "figure.dpi": 220,
                         "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": size,
                         "axes.titleweight": "bold"})
    return size


def _save(fig, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=220, transparent=False, facecolor="white")
    plt.close(fig)
    return path


def bars(path, labels, values, size, fmt="brochure", unit="", kept=(), before=(), title=None, xmax=None,
         value_labels=None):
    """Horizontal bars, one per label, value written at the end of each bar. kept / before: indexes coloured green / red."""
    s = _style(fmt)
    fig, ax = plt.subplots(figsize=size, layout="constrained")
    colours = [KEPT if i in kept else BEFORE if i in before else GREY for i in range(len(values))]
    y = range(len(values))[::-1]
    ax.barh(list(y), values, color=colours, height=0.62)
    ax.set_yticks(list(y), labels)
    top = xmax or max(values) * 1.22
    ax.set_xlim(0, top)
    for yi, v, lab in zip(y, values, value_labels or [f"{v:,}{unit}" for v in values]):
        ax.text(v + top * 0.015, yi, lab, va="center", fontsize=s, fontweight="bold")
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="x", length=0, labelbottom=False)
    ax.tick_params(axis="y", length=0)
    if title:
        ax.set_title(title, loc="left")
    return _save(fig, path)


def before_after(path, panels, size, fmt="brochure", unit=""):
    """Small multiples, one panel per measure: panels = [(title, before, after)]; before red, after green."""
    s = _style(fmt)
    fig, axes = plt.subplots(1, len(panels), figsize=size, layout="constrained", squeeze=False)
    for ax, (title, b, a) in zip(axes[0], panels):
        ax.bar([0, 1], [b, a], color=[BEFORE, KEPT], width=0.6)
        ax.set_xticks([0, 1], ["Before", "After"])
        ax.set_ylim(0, max(b, a) * 1.25)
        for x, v in ((0, b), (1, a)):
            ax.text(x, v + max(b, a) * 0.03, f"{v:,}{unit}", ha="center", fontsize=s, fontweight="bold")
        ax.set_title(title)
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0, labelleft=False)
        ax.tick_params(axis="x", length=0)
    return _save(fig, path)


def lines(path, x, series, size, fmt="brochure", xlabel="", ylabel="", target=None):
    """Line chart: series = [(name, ys, kind)] with kind "kept", "before", "caution", "other" or "grey".
    target: optional (value, label) drawn as a dashed line."""
    _style(fmt)
    col = {"kept": KEPT, "before": BEFORE, "caution": CAUTION, "other": OTHER, "grey": GREY}
    fig, ax = plt.subplots(figsize=size, layout="constrained")
    for name, ys, kind in series:
        ax.plot(x, ys, color=col[kind], lw=2, marker="o", ms=3.5, label=name)
    if target:
        ax.axhline(target[0], color=TEXT, lw=1, ls="--")
        ax.text(x[0], target[0], " " + target[1], va="bottom", fontsize=FORMATS[fmt].small)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", color=LINE, lw=0.6)
    if len(series) > 1:
        ax.legend(frameon=False, loc="best")
    return _save(fig, path)
