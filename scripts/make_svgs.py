"""Generates the animated SVGs in assets/. Run: python3 scripts/make_svgs.py

Everything is plain SVG + CSS/SMIL animation (no JS, no external files),
so GitHub can show it through an <img> tag.
"""

import math
import random
from pathlib import Path

# Kanagawa palette
BG = "#1F1F28"
TEXT = "#DCD7BA"
WAVE = "#7E9CD8"
DEEP = "#2D4F67"
SAKURA = "#D27E99"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# A sakura petal: narrow at the base, notched at the tip.
PETAL = "M0 -9C5 -6 7 0 5 7C3 7.5 1.5 5.5 0 4.2C-1.5 5.5 -3 7.5 -5 7C-7 0 -5 -6 0 -9Z"


def wave_path(width, period, amp, base, bottom, phase=0.0, step=6):
    """A peaky, Hokusai-ish wave: sharp crests, broad troughs.

    The path is one period wider than the canvas so sliding it left by exactly
    one period loops seamlessly.
    """
    pts = []
    x = 0.0
    while x <= width + period + step:
        t = 2 * math.pi * x / period + phase
        y = base - amp * (math.sin(t) + 0.3 * math.sin(2 * t - math.pi / 2))
        pts.append(f"{x:.0f} {y:.1f}")
        x += step
    return f"M0 {bottom}L" + "L".join(pts) + f"L{width + period + step:.0f} {bottom}Z"


def crest_line(width, period, amp, base, phase=0.0, step=6):
    """Just the top edge of a wave, for a thin foam highlight."""
    pts = []
    x = 0.0
    while x <= width + period + step:
        t = 2 * math.pi * x / period + phase
        y = base - amp * (math.sin(t) + 0.3 * math.sin(2 * t - math.pi / 2))
        pts.append(f"{x:.0f} {y:.1f}")
        x += step
    return "M" + "L".join(pts)


def falling_petals(n, width, height, seed, size=(0.8, 1.5), dur=(9, 16)):
    """Petals that fall top to bottom while swaying and spinning.

    Negative delays mean the petals are already mid-fall when the image loads.
    """
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.uniform(20, width - 20)
        s = rnd.uniform(*size)
        fall = rnd.uniform(*dur)
        sway = rnd.uniform(2.5, 4.5)
        spin = rnd.uniform(4, 9)
        opacity = rnd.uniform(0.55, 1.0)
        spin_dir = rnd.choice(["spin", "spinr"])
        out.append(
            f'<g transform="translate({x:.0f} 0)">'
            f'<g class="fall" style="animation-duration:{fall:.1f}s;animation-delay:-{rnd.uniform(0, fall):.1f}s">'
            f'<g class="sway" style="animation-duration:{sway:.1f}s;animation-delay:-{rnd.uniform(0, sway):.1f}s">'
            f'<path class="{spin_dir}" d="{PETAL}" fill="{SAKURA}" opacity="{opacity:.2f}" '
            f'transform="scale({s:.2f})" style="animation-duration:{spin:.1f}s"/>'
            f"</g></g></g>"
        )
    return "".join(out)


def petal_css(height):
    return f"""
.fall{{animation:fall linear infinite}}
.sway{{animation:sway ease-in-out infinite alternate}}
.spin,.spinr{{transform-box:fill-box;transform-origin:center;animation:spin linear infinite}}
.spinr{{animation-direction:reverse}}
@keyframes fall{{from{{transform:translateY(-20px)}}to{{transform:translateY({height + 20}px)}}}}
@keyframes sway{{from{{transform:translateX(-22px)}}to{{transform:translateX(22px)}}}}
@keyframes spin{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
"""


def banner():
    W, H = 1200, 320
    back = wave_path(W, 300, 14, 250, H, phase=1.2)
    mid = wave_path(W, 400, 18, 268, H, phase=0.4)
    front = wave_path(W, 240, 12, 288, H)
    foam = crest_line(W, 240, 12, 288)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="hey, I'm Jimmy. CS @ Penn Engineering '30">
<style>
{petal_css(H)}
.w1{{animation:slide1 18s linear infinite}}
.w2{{animation:slide2 24s linear infinite}}
.w3{{animation:slide3 12s linear infinite}}
@keyframes slide1{{to{{transform:translateX(-300px)}}}}
@keyframes slide2{{to{{transform:translateX(-400px)}}}}
@keyframes slide3{{to{{transform:translateX(-240px)}}}}
.title{{font:700 68px {SANS};fill:{TEXT};animation:rise 1s ease-out both}}
.sub{{font:500 24px {SANS};fill:{WAVE};letter-spacing:3px;animation:rise 1s .35s ease-out both}}
@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
</style>
<defs>
<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{DEEP}" stop-opacity=".55"/>
</linearGradient>
<linearGradient id="gMid" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{DEEP}"/><stop offset=".6" stop-color="{WAVE}"/><stop offset="1" stop-color="{SAKURA}"/>
</linearGradient>
<linearGradient id="gFront" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{DEEP}"/><stop offset="1" stop-color="{BG}"/>
</linearGradient>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<circle cx="1050" cy="92" r="30" fill="{SAKURA}" opacity=".9"/>
<path d="M860 262L970 150Q980 141 990 150L1100 262Z" fill="{DEEP}"/>
<path d="M946 174L970 150Q980 141 990 150L1014 174L1002 169L992 180L982 166L970 180L958 169Z" fill="{TEXT}" opacity=".9"/>
<g class="w1"><path d="{back}" fill="{DEEP}" opacity=".8"/></g>
<g class="w2"><path d="{mid}" fill="url(#gMid)" opacity=".75"/></g>
<g class="w3"><path d="{front}" fill="url(#gFront)"/><path d="{foam}" fill="none" stroke="{TEXT}" stroke-opacity=".55" stroke-width="2"/></g>
{falling_petals(8, W, H, seed=3, size=(0.9, 1.4))}
<text class="title" x="{W / 2}" y="136" text-anchor="middle">hey, I'm Jimmy</text>
<text class="sub" x="{W / 2}" y="182" text-anchor="middle">CS @ PENN ENGINEERING '30</text>
</g>
</svg>"""


def typing():
    lines = [
        "CS student at Penn Engineering",
        "building small, useful things for the web",
        "learning to ride the wave",
        "one project at a time",
    ]
    W, H = 640, 56
    fs = 20
    cw = fs * 0.6  # monospace advance; textLength below enforces it
    type_s, hold_s, erase_s, gap_s = 0.07, 2.2, 0.03, 0.5

    # One timeline of (time, line index, visible chars).
    events = []
    t = 0.0
    for i, line in enumerate(lines):
        for c in range(len(line) + 1):
            events.append((t, i, c))
            t += type_s
        t += hold_s
        for c in range(len(line) - 1, -1, -1):
            events.append((t, i, c))
            t += erase_s
        t += gap_s
    total = t

    def x0(i):
        return (W - len(lines[i]) * cw) / 2

    def keyframes(name, frames):
        body = "".join(f"{100 * tt / total:.3f}%{{transform:translateX({x:.1f}px)}}" for tt, x in frames)
        return f"@keyframes {name}{{{body}}}"

    # Each line sits under a background-colored cover that slides right to
    # reveal one character at a time (step-end = no smooth sliding).
    css, shapes = [], []
    for i, line in enumerate(lines):
        mine = [(tt, c) for tt, li, c in events if li == i]
        frames = [(0, 0)] + [(tt, c * cw) for tt, c in mine] + [(total, 0)]
        css.append(keyframes(f"k{i}", frames))
        # Only the active line is visible; the rest are faded out.
        on, off = 100 * mine[0][0] / total, 100 * (mine[-1][0] + erase_s) / total
        css.append(f"@keyframes v{i}{{0%{{opacity:0}}{on:.3f}%{{opacity:1}}{off:.3f}%{{opacity:0}}}}")
        css.append(f".c{i}{{animation:k{i} {total:.2f}s step-end infinite}}")
        css.append(f".l{i}{{opacity:0;animation:v{i} {total:.2f}s step-end infinite}}")
        tw = len(line) * cw
        shapes.append(
            f'<g class="l{i}"><text x="{x0(i):.1f}" y="{H / 2 + fs * 0.35:.1f}" textLength="{tw:.1f}" '
            f'lengthAdjust="spacingAndGlyphs">{line}</text>'
            f'<rect class="c{i}" x="{x0(i) - 1:.1f}" y="6" width="{tw + 4:.1f}" height="{H - 12}" fill="{BG}"/></g>'
        )
    css.append(keyframes("kc", [(tt, x0(li) + c * cw + 2) for tt, li, c in events] + [(total, x0(0) + 2)]))

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{' / '.join(lines)}">
<style>
text{{font:500 {fs}px {MONO};fill:{SAKURA}}}
{chr(10).join(css)}
.cur{{animation:kc {total:.2f}s step-end infinite}}
.blink{{animation:blink 1s step-end infinite}}
@keyframes blink{{50%{{opacity:0}}}}
</style>
<defs><clipPath id="pill"><rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="{H / 2 - 2}"/></clipPath></defs>
<rect width="{W}" height="{H}" rx="{H / 2}" fill="{BG}"/>
<rect width="{W - 2}" height="{H - 2}" x="1" y="1" rx="{H / 2 - 1}" fill="none" stroke="{DEEP}" stroke-width="2"/>
<g clip-path="url(#pill)">{''.join(shapes)}</g>
<g class="cur"><rect class="blink" y="{H / 2 - fs * 0.6:.1f}" width="2.5" height="{fs * 1.1:.1f}" fill="{WAVE}"/></g>
</svg>"""


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for name, fn in [("banner", banner), ("typing", typing)]:
        path = ASSETS / f"{name}.svg"
        path.write_text(fn())
        print(f"{path.name}: {path.stat().st_size / 1024:.1f} KB")
