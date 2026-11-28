"""Draw the counter roller sketch for page 9 (2026-11-28): the pollen is squeezed between the flywheel on one side and
the 2 counter rollers on the other (user, 2026-11-28). The rollers spin the opposite way at the same surface speed, so
both sides push the pollen forward and it leaves without backspin.

    python project/src/counter_roller_diagram.py    # writes project/assets/diagrams/counter_roller.png

A sketch of the idea, not to scale and not the CAD: sizes are the team's (63.5 mm flywheel, 27 mm rollers, 71.12 mm
pollen), positions are made up to show how it works.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import Arc, Circle, FancyArrowPatch  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / "project" / "design" / "fonts"
for f in (FONTS / "Montserrat" / "Montserrat-Regular.ttf", FONTS / "Caveat" / "CaveatStatic-Bold.ttf"):
    font_manager.fontManager.addfont(str(f))
INK, YELLOW, MUTED = "#171616", "#F5E660", "#4D4D4D"
HAND = dict(family="Caveat Static", weight="bold", size=44, color=INK)
OUT = ROOT / "project" / "assets" / "diagrams" / "counter_roller.png"


def turn_arrow(ax, x, y, r, start, end):
    """A curved arrow round a wheel from angle start to angle end (degrees): end > start turns anticlockwise."""
    import math
    lo, hi = min(start, end), max(start, end)
    ax.add_patch(Arc((x, y), 2 * r, 2 * r, theta1=lo, theta2=hi, lw=2.5, color=INK, zorder=4))
    e = math.radians(end)
    ex, ey = x + r * math.cos(e), y + r * math.sin(e)
    d = 1 if end > start else -1
    tx, ty = -math.sin(e) * d, math.cos(e) * d
    ax.add_patch(FancyArrowPatch((ex - 0.05 * tx, ey - 0.05 * ty), (ex + 0.35 * tx, ey + 0.35 * ty),
                                 arrowstyle="-|>", mutation_scale=24, lw=2.5, color=INK, zorder=4))


def main():
    fig, ax = plt.subplots(figsize=(6.4, 4.4), dpi=300)
    ax.set_xlim(-8.6, 7.4)
    ax.set_ylim(-3.4, 6.2)
    ax.set_aspect("equal")
    ax.axis("off")

    s = 0.06                      # mm to sketch units, so the sizes keep the team's proportions
    fr, rr, pr = 63.5 / 2 * s, 27 / 2 * s, 71.12 / 2 * s
    px, py = 0.0, 0.0             # pollen centre; it leaves upwards
    fx, fy = px - pr - fr + 0.3, py   # flywheel on the left
    ax.add_patch(Circle((fx, fy), fr, facecolor="white", edgecolor=INK, lw=3, zorder=3))
    ax.add_patch(Circle((fx, fy), 0.25, facecolor=INK, zorder=4))
    turn_arrow(ax, fx, fy, fr + 0.45, 125, 235)        # anticlockwise: its right side moves up
    rx = px + pr + rr - 0.45      # 2 counter rollers on the right, opposite the flywheel
    for dy in (-1.0, 1.0):
        ax.add_patch(Circle((rx, py + dy), rr, facecolor=YELLOW, edgecolor=INK, lw=3, zorder=3))
        ax.add_patch(Circle((rx, py + dy), 0.12, facecolor=INK, zorder=4))
    turn_arrow(ax, rx, py + 1.0, rr + 0.45, 70, -60)   # clockwise: their left side moves up
    ax.add_patch(Circle((px, py), pr, facecolor="#E8E8E8", edgecolor=INK, lw=2.5, ls="--", zorder=2))

    ax.add_patch(FancyArrowPatch((px, py + pr + 0.3), (px, py + pr + 3.2), arrowstyle="-|>", mutation_scale=28,
                                 lw=3, color=INK, zorder=4))
    ax.text(px + 0.5, py + pr + 2.2, "out, no spin", ha="left", va="center", **HAND)
    ax.text(px, py - pr - 0.3, "pollen", ha="center", va="top", **HAND)
    ax.text(fx - fr - 1.3, fy, "flywheel", ha="right", va="center", linespacing=0.9, **HAND)
    ax.text(rx + rr + 0.9, py - 0.4, "counter\nrollers", ha="left", va="center", linespacing=0.9, **HAND)
    ax.text(-8.5, 6.1, "sketch,\nnot to scale", ha="left", va="top", family="Montserrat", fontsize=30,
            color=MUTED)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, transparent=True, bbox_inches="tight", pad_inches=0.05)
    print(OUT)


if __name__ == "__main__":
    main()
