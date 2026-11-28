"""Draw the auto-aim vector diagram for page 13 (2026-11-28): the aim vector runs from the goal to where the robot
will be 0.4 s from now, and the robot turns so its rear-facing shooter points back along that line.

    python project/src/auto_aim_diagram.py      # writes project/assets/diagrams/auto_aim_vector.png

A sketch of the idea, not to scale: positions are made up to show the geometry, not measured.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / "project" / "design" / "fonts"
for f in (FONTS / "Montserrat" / "Montserrat-Regular.ttf", FONTS / "Montserrat" / "Montserrat-Bold.ttf",
          FONTS / "Caveat" / "CaveatStatic-Bold.ttf"):
    font_manager.fontManager.addfont(str(f))
INK, YELLOW, MUTED = "#171616", "#F5E660", "#4D4D4D"
HAND = dict(family="Caveat Static", weight="bold", size=24, color=INK)
OUT = ROOT / "project" / "assets" / "diagrams" / "auto_aim_vector.png"


def robot(ax, x, y, angle_deg, dashed=False):
    """A square robot seen from above, rotated, with a short bar on its back edge for the shooter."""
    t = matplotlib.transforms.Affine2D().rotate_deg_around(x, y, angle_deg) + ax.transData
    ax.add_patch(Rectangle((x - 0.6, y - 0.6), 1.2, 1.2, transform=t, fill=not dashed, facecolor="white",
                           edgecolor=INK, lw=2, ls="--" if dashed else "-", zorder=3))
    ax.add_patch(Rectangle((x - 0.6, y - 0.18), 0.22, 0.36, transform=t, facecolor=YELLOW, edgecolor=INK, lw=1.5,
                           zorder=4, alpha=0.5 if dashed else 1))


def main():
    fig, ax = plt.subplots(figsize=(6.4, 4.4), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.2)
    ax.set_aspect("equal")
    ax.axis("off")

    goal = (10.6, 6.9)
    now = (2.6, 2.0)
    ahead = (5.0, 2.6)                       # where the robot will be 0.4 s from now
    # goal: a hexagon
    ax.add_patch(Polygon([(goal[0] + 0.55 * c, goal[1] + 0.55 * s) for c, s in
                          [(1, 0), (0.5, 0.87), (-0.5, 0.87), (-1, 0), (-0.5, -0.87), (0.5, -0.87)]],
                         facecolor=YELLOW, edgecolor=INK, lw=2, zorder=3))
    ax.text(goal[0], goal[1] + 0.85, "goal", ha="center", va="bottom", **HAND)

    import math
    ang = math.degrees(math.atan2(goal[1] - ahead[1], goal[0] - ahead[0]))
    robot(ax, *now, ang + 180 - 18)         # still turning
    robot(ax, *ahead, ang + 180, dashed=True)  # back edge (shooter) faces the goal
    ax.text(now[0], now[1] - 1.05, "robot now", ha="center", va="top", **HAND)
    ax.text(ahead[0] + 0.3, ahead[1] - 1.05, "robot in 0.4 s", ha="center", va="top", **HAND)

    # velocity: now -> ahead
    ax.add_patch(FancyArrowPatch(now, ahead, arrowstyle="-|>", mutation_scale=16, lw=2, color=MUTED,
                                 shrinkA=22, shrinkB=22, zorder=2))
    ax.text((now[0] + ahead[0]) / 2 - 0.2, (now[1] + ahead[1]) / 2 + 0.35, "velocity × 0.4 s", ha="center",
            va="bottom", family="Montserrat", fontsize=13, color=MUTED, rotation=14)

    # aim vector: goal -> robot 0.4 s ahead
    ax.add_patch(FancyArrowPatch(goal, ahead, arrowstyle="-|>", mutation_scale=22, lw=4, color=INK, shrinkA=18,
                                 shrinkB=26, zorder=2))
    ax.add_patch(FancyArrowPatch(goal, ahead, arrowstyle="-", lw=2.2, color=YELLOW, shrinkA=18, shrinkB=34, zorder=2))
    mx, my = (goal[0] + ahead[0]) / 2, (goal[1] + ahead[1]) / 2
    ax.text(mx + 0.5, my - 0.55, "aim vector", rotation=ang, rotation_mode="anchor", ha="center", va="top", **HAND)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, transparent=True, bbox_inches="tight", pad_inches=0.05)
    print(OUT)


if __name__ == "__main__":
    main()
