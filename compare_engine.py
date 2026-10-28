#!/usr/bin/env python3
"""compare_engine.py — the engine's render and the paper's, one panel at a time.

Built because the two were being compared by flipping between a browser tab and
a PNG, which is how a difference gets argued about instead of measured. The
page is generated, never hand-assembled.

Both plates go in the SAME frame. The engine windows its viewBox to its own
content; the paper always draws 0..2200 x 1416. At equal page width they would
otherwise sit at two different scales and every column would appear to have
moved. This rewrites the engine's viewBox to the paper's x extent -- only the
window moves, nothing is stretched -- so a position on one plate is the same
canvas x on the other. That is what the plumb line reads.

The plates are drawn light whatever the page theme. The paper's render is a
fixed-colour artifact and the engine's palette follows the reader's theme;
putting a dark engine plate beside a light paper one compares two things.

    python3 compare_engine.py        writes engine_vs_paper.html

Requires playwright, as `enginecrossings.py` does, and the blessed renders in
reference_renders/ -- run build.py first if they are not there.
"""
import json
import os
import re

REPO = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(REPO, "engine", "explorer_engine.html")
REFS = os.path.join(REPO, "reference_renders")
OUT = os.path.join(REPO, "engine_vs_paper.html")

VB = re.compile(r'viewBox="([-0-9.]+)\s+([-0-9.]+)\s+([-0-9.]+)\s+([-0-9.]+)"')
FRAME = 2200.0

SELECT = {"national_2030_mixed": ("US", "2030"),
          "national_2024": ("US", "2024"),
          "dc_2024": ("DC", "2024")}


def engine_plates(keys):
    """Dump the engine's default view for each panel, reframed to the paper's x."""
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1900, "height": 1300})
        pg.goto("file://" + ENGINE)
        pg.wait_for_timeout(1500)
        for key in keys:
            place, year = SELECT[key]
            pg.evaluate("a=>{document.querySelector(`#place button[data-k=\"${a[0]}\"]`).click();"
                        "document.querySelector(`#year button[data-y=\"${a[1]}\"]`).click();}",
                        [place, year])
            pg.wait_for_timeout(500)
            # the default configuration for the view, which is what the paper
            # draws -- not whatever the last visitor left the controls on
            pg.evaluate("()=>document.getElementById('reset').click()")
            pg.wait_for_timeout(500)
            svg = pg.evaluate("()=>document.querySelector('#plate svg').outerHTML")
            m = VB.search(svg)
            if not m:
                raise SystemExit("compare_engine: %s has no viewBox the engine "
                                 "could draw -- look at the panel before going "
                                 "further" % key)
            _x, y, _w, h = [float(v) for v in m.groups()]
            svg = svg[:m.start()] + 'viewBox="0 0 %.0f %.1f"' % (FRAME, y + h) + svg[m.end():]
            out[key] = svg
        br.close()
    return out


def paper_plate(key):
    s = open(os.path.join(REFS, key + "_combined.svg")).read()
    return s[s.find("<svg"):]


PANELS = [("national_2030_mixed", "US \u00d7 2030"),
          ("national_2024", "US \u00d7 2024"),
          ("dc_2024", "DC \u00d7 2024")]

GEOM = json.load(open(os.path.join(REPO, "engine", "geometry.json")))
COLS = GEOM["cols"]

KEYS = [k for k, _ in PANELS]
_eng = engine_plates(KEYS)
data = {k: {"engine": _eng[k], "paper": paper_plate(k)} for k in KEYS}

HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Engine and paper, side by side</title>
<style>
  :root {
    color-scheme: light;
    --page:#F2F0EB; --chrome:#FFFFFF; --ink:#1A2733; --dim:#5A6B7A;
    --hair:#D8D3C8; --mark:#8B5A5A; --live:#1F7A5A;
    box-sizing:border-box;
    padding-top:env(safe-area-inset-top,0px);
    padding-bottom:env(safe-area-inset-bottom,0px);
  }
  :root:not([data-theme="light"]) { }
  @media (prefers-color-scheme: dark){
    :root:not([data-theme="light"]){
      color-scheme: dark;
      --page:#171C21; --chrome:#1F252B; --ink:#E9E6E0; --dim:#98A5B0;
      --hair:#30383F; --mark:#C9A9A4; --live:#58B894;
    }
  }
  :root[data-theme="dark"]{
    color-scheme: dark;
    --page:#171C21; --chrome:#1F252B; --ink:#E9E6E0; --dim:#98A5B0;
    --hair:#30383F; --mark:#C9A9A4; --live:#58B894;
  }
  *,*::before,*::after{box-sizing:inherit}
  html{scroll-padding-top:calc(58px + env(safe-area-inset-top,0px))}
  body{
    margin:0; background:var(--page); color:var(--ink);
    font:15px/1.45 "Segoe UI", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing:antialiased;
  }
  body::before{content:""; position:fixed; inset:0 0 auto;
    height:env(safe-area-inset-top,0px); background:var(--chrome); z-index:30}

  header{
    position:sticky; top:env(safe-area-inset-top,0px); z-index:20;
    display:flex; flex-wrap:wrap; align-items:baseline; gap:4px 22px;
    padding:12px 20px; background:var(--chrome);
    border-bottom:1px solid var(--hair);
  }
  h1{font-size:15px; font-weight:600; margin:0; letter-spacing:.01em}
  h1 span{color:var(--dim); font-weight:400}
  nav{display:flex; gap:2px; margin-left:auto}
  button{
    font:inherit; font-size:13.5px; color:var(--dim); background:none;
    border:1px solid transparent; border-radius:2px; padding:4px 11px;
    cursor:pointer;
  }
  button:hover{color:var(--ink)}
  button[aria-pressed="true"]{color:var(--ink); border-color:var(--hair);
    background:var(--page); font-weight:600}
  button:focus-visible{outline:2px solid var(--live); outline-offset:1px}
  #where{
    font-size:13px; color:var(--dim); font-variant-numeric:tabular-nums;
    min-width:20ch;
  }
  #where b{color:var(--ink); font-weight:600}

  main{max-width:1680px; margin:0 auto; padding:18px 20px 64px}
  figure{margin:0 0 26px}
  figcaption{
    display:flex; align-items:baseline; gap:12px;
    padding:0 0 7px; font-size:13px; color:var(--dim);
  }
  figcaption em{
    font-style:normal; font-weight:600; font-size:14px; color:var(--ink);
  }
  figcaption i{font-style:normal; margin-left:auto; font-size:12.5px}

  /* The plates are always light. The paper's render is a fixed-colour
     artifact, so putting the engine's dark palette next to it would be
     comparing two different things. */
  .plate{
    position:relative; background:#FAF8F3; border:1px solid var(--hair);
    border-radius:2px; overflow:hidden;
    --ground:#FAF8F3; --ink:#1A2733; --muted:#5A6B7A; --rule:#E4DFD4;
    --panel:#FFFFFF; --warn:#8B5A5A; --vio:#5B21B6;
    color:#1A2733;
  }
  .plate svg{display:block; width:100%; height:auto}
  .plumb{
    position:absolute; top:0; bottom:0; width:1px; background:var(--live);
    opacity:.85; pointer-events:none; left:-10px;
  }
  .plumb::after{
    content:""; position:absolute; inset:0 -3px; background:var(--live);
    opacity:.12;
  }
  @media (prefers-reduced-motion: no-preference){
    .plumb{transition:left 40ms linear}
  }
  @media (max-width:720px){
    main{padding:14px 10px 48px}
    nav{margin-left:0; width:100%}
  }
</style>
</head>
<body>
<header>
  <h1>Engine and paper <span>&mdash; same panel, same frame, same scale</span></h1>
  <div id="where">move across a plate</div>
  <nav id="pick"></nav>
</header>

<main>
  <figure>
    <figcaption><em>Engine</em> explorer_engine.html, default view
      <i id="ecap"></i></figcaption>
    <div class="plate" id="engine"><div class="plumb"></div></div>
  </figure>
  <figure>
    <figcaption><em>Paper</em> reference_renders, blessed render
      <i id="pcap"></i></figcaption>
    <div class="plate" id="paper"><div class="plumb"></div></div>
  </figure>
</main>

<script>
const DATA = __DATA__;
const COLS = __COLS__;
const PANELS = __PANELS__;
const FRAME = 2200;

const pick = document.getElementById('pick');
const where = document.getElementById('where');
const plates = {engine: document.getElementById('engine'),
                paper: document.getElementById('paper')};

function column(x){
  for (const [name, [a, b]] of Object.entries(COLS))
    if (x >= a && x < b) return name.replace(/_/g, ' ').toLowerCase();
  return x < 0 ? '' : 'off the frame';
}

function show(key){
  for (const which of ['engine', 'paper']){
    const el = plates[which];
    const line = el.querySelector('.plumb');
    el.innerHTML = DATA[key][which];
    el.appendChild(line);
  }
  document.getElementById('ecap').textContent =
    DATA[key].engine.length.toLocaleString() + ' bytes';
  document.getElementById('pcap').textContent =
    DATA[key].paper.length.toLocaleString() + ' bytes';
  for (const b of pick.children) b.setAttribute('aria-pressed', b.dataset.k === key);
  history.replaceState(null, '', '#' + key.replace(/_/g, '-'));
}

for (const [key, label] of PANELS){
  const b = document.createElement('button');
  b.textContent = label; b.dataset.k = key;
  b.addEventListener('click', () => show(key));
  pick.appendChild(b);
}

// One plumb line across both plates. The frames are identical, so a position
// on one is the same canvas x on the other, and a column that has moved is
// visible without measuring anything.
function track(ev){
  const host = ev.currentTarget;
  const r = host.getBoundingClientRect();
  const px = ev.clientX - r.left;
  const x = px / r.width * FRAME;
  for (const which of ['engine', 'paper']){
    const el = plates[which];
    const w = el.getBoundingClientRect().width;
    el.querySelector('.plumb').style.left = (x / FRAME * w) + 'px';
  }
  const c = column(x);
  where.innerHTML = 'x&thinsp;<b>' + Math.round(x) + '</b>' + (c ? ' &middot; ' + c : '');
}
function clear(){
  for (const which of ['engine', 'paper'])
    plates[which].querySelector('.plumb').style.left = '-10px';
  where.textContent = 'move across a plate';
}
for (const which of ['engine', 'paper']){
  plates[which].addEventListener('pointermove', track);
  plates[which].addEventListener('pointerleave', clear);
}

const want = location.hash.slice(1).replace(/-/g, '_');
show(DATA[want] ? want : PANELS[0][0]);
</script>
</body>
</html>
"""

html = (HTML
        .replace("__DATA__", json.dumps(data))
        .replace("__COLS__", json.dumps(COLS))
        .replace("__PANELS__", json.dumps(PANELS)))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w").write(html)
print("wrote %s  (%.0f kB)" % (OUT, len(html) / 1024))
