"""Draw the team's autonomous route on the blank field (page 14).

    python project/src/trace_auto_route.py      # writes project/assets/auto/auto_route.png

The user's sketch (project/assets/auto/source/auto_route_hand_drawn.jpg) only shows where the robot goes, so the route is
drawn as horizontal and vertical lines on the grid, with corners on grid lines or tile midpoints (user, 2026-11-11). The
sketch's field is the blank field turned 90 degrees anticlockwise (the four flowers, both gardens and both loading zones
line up), and the route is reversed from how the sketch is drawn.

The seven steps (user, 2026-11-11), each with a numbered circle on the route:
  1 shoot (causing a HIVE TIP)   2 get pollen from the flower   3 go to the shooting position on the other side
  4 shoot   5 collect pollen from the flower   6 shoot   7 park
The robot goes into each flower and back out along the SAME line.

Grid: the field is 554 px square with 6 tiles, so grid lines are every 92.3 px; tile midpoints (allowed) are 46.2 px inside
them. The bottom flower is on x = 369 and the left flower on y = 369.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# blank-field pixels (554 x 554)
ROUTE = [
    (540, 323),    # start, right wall, y = midpoint of a tile row            (step 1: shoot)
    (369, 323),    # left along y = 323 to the grid line x = 369
    (369, 525),    # straight down into the bottom flower                      (step 2: get pollen)
    (369, 415),    # straight back up the same line
    (92, 415),     # left along y = 415 to the grid line x = 92                (steps 3 and 4: shooting position, shoot)
    (92, 369),     # up to the left flower's line
    (24, 369),     # straight left into the left flower                        (step 5: collect pollen)
    (92, 369),     # straight back along the same line
    (138, 369),    # right to x = 138, midpoint of the 2nd column              (step 6: shoot)
    (138, 523),    # straight down into the red loading zone                   (step 7: park)
]
ARROWS = [((450, 323), math.pi), ((369, 380), math.pi / 2), ((369, 470), -math.pi / 2), ((300, 415), math.pi),
          ((62, 369), math.pi), ((138, 445), math.pi / 2)]       # (middle of the arrow, direction)
STEPS = [(1, (540, 323)), (2, (369, 525)), (3, (230, 415)), (4, (92, 415)), (5, (24, 369)), (6, (138, 369)),
         (7, (138, 523))]

K = 3
blank = Image.open("project/assets/auto/source/field_blank.png").convert("RGB")
size = blank.width * K
canvas = blank.resize((size, size), Image.LANCZOS).convert("RGBA")
pts = [(x * K, y * K) for x, y in ROUTE]
d = ImageDraw.Draw(canvas)
W_OUT, W_IN = 9 * K, 5 * K
DARK, YEL = (23, 22, 22, 255), (245, 230, 96, 255)
FONT = ImageFont.truetype("project/design/fonts/Montserrat/Montserrat-Bold.ttf", 15 * K)


def dot(p, r, fill, outline=None, w=0):
    d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=fill, outline=outline, width=w)


def head(mid, ang, length=15 * K, half=9 * K):
    ux, uy = math.cos(ang), math.sin(ang)
    nx, ny = -uy, ux
    tip = (mid[0] + ux * length / 2, mid[1] + uy * length / 2)
    base = (mid[0] - ux * length / 2, mid[1] - uy * length / 2)
    tri = [tip, (base[0] + nx * half, base[1] + ny * half), (base[0] - nx * half, base[1] - ny * half)]
    d.polygon(tri, fill=YEL)
    d.line(tri + [tri[0]], fill=DARK, width=2 * K, joint="curve")


d.line(pts, fill=DARK, width=W_OUT, joint="curve")
for p in pts:
    dot(p, W_OUT / 2, DARK)
d.line(pts, fill=YEL, width=W_IN, joint="curve")
for p in pts:
    dot(p, W_IN / 2, YEL)
for (x, y), ang in ARROWS:
    head((x * K, y * K), ang)
for n, (x, y) in STEPS:                                           # numbered circles, one per step
    c = (x * K, y * K)
    dot(c, 13 * K, YEL, DARK, 2 * K)
    box = d.textbbox((0, 0), str(n), font=FONT)
    d.text((c[0] - (box[0] + box[2]) / 2, c[1] - (box[1] + box[3]) / 2), str(n), font=FONT, fill=DARK)
out = Path("project/assets/auto"); out.mkdir(parents=True, exist_ok=True)
old = out / "auto_elims_route.png"
if old.exists():
    old.unlink()
canvas.convert("RGB").save(out / "auto_route.png", optimize=True)
print("saved", canvas.size)
