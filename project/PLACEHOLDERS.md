# Placeholders in the portfolio (portfolio_v37, 2026-11-12)

Page numbers are the numbers printed on the pages (the cover is not numbered). The hand-in check fails until every
`<...>` in section A is replaced. Section B is empty evidence rather than a placeholder: it says "not finished yet" until
the robot is tested. Question numbers are in [QUESTIONS.md](QUESTIONS.md).

To refresh this list after a new version:
`python -c "import pymupdf,re; d=pymupdf.open('project/outputs/portfolio/portfolio_vNN.pdf'); [print(i, m) for i,p in enumerate(d) for m in re.findall(r'<[^<>]{1,120}>', ' '.join(p.get_text().split()))]"`

## A. Bracketed placeholders (0)

None: the last one (page 5, how we play) was filled on 2026-11-12 from the team's four strategy points.

## B. Results that are in but have no numbers of tries or conditions

| Page | Box | Row | Needs | Question |
|---|---|---|---|---|

## C. Also waiting on you (not placeholders in the text)

- How many shots, from which three distances; what pushed the robot in X-lock; out of how many pickups the 1 jam was; how many auto runs; how the time between shots was measured (QUESTIONS 1-7).

- Page 9: the "instead of" cells for flywheels (one), hood (fixed) and direction (facing forwards) are my reading of your words: QUESTIONS 87.
- Page 3: the 14 November competition line (QUESTIONS 79). Page 5: how many pollen the robot holds, 3 or 4 (QUESTIONS 84).
- No photo of the real robot on any page. See "What the example portfolios have" in NEXT_STEPS.md.
