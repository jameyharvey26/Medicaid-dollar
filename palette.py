"""
palette.py - Single source of truth for Sankey color assignment.

Imported by build_sankey.py, build_sankey_dc.py, and every future state build.
Colors live here and nowhere else. Changing a color changes it everywhere.

THE RULE
    Cool  = money moving.   Payers, capitation, care that still happens.
    Warm  = money stopping. Gaps, cost shift, care that does not happen.
    Slate = structural.     Fee-for-service, which is not a payer at all.

No baseline flow is ever warm. No loss band is ever cool. A reader learns the
legend once and carries it through every diagram in the series.

PAYER ASSIGNMENT IS RESERVED (JW ruling, 2026-08-18)
    Each national parent company holds a fixed cool assignment across every
    state build, so a reader following the series recognizes plans across
    geographies and multi-state comparisons work.

    Collision rule: when two reserved plans co-occur in one state and land
    within COLLISION_DELTA of each other, the SMALLER plan (by capitation)
    shifts to its designated alternate. The swap is logged in that state's
    build notes. Exceptions are visible, never silent.
"""

# ---------------------------------------------------------------------------
# STRUCTURAL — not payers, never on the cool ramp
# ---------------------------------------------------------------------------

STRUCTURAL = {
    "ffs":        "#8494A6",   # fee-for-service: passes through payer column untouched
    "agency":     "#1F7A5A",   # the state agency / the $100 combined
    "federal":    "#3D6E8C",   # federal source band
    "local":      "#A8BFCE",   # state / local source band
    "admin":      "#9AA5AF",   # administration peel
    "premiums":   "#8E9BA6",   # Medicare premiums for duals, back to federal
    "plan_admin": "#7C8894",   # MCO plan admin & margin peel
}

# ---------------------------------------------------------------------------
# PAYER RAMP — cool only. THREE FAMILIES (JW rulings, 2026-08-18).
#
#   CARRIER       blue -> indigo    Commercial and Medicaid carriers.
#   HEALTH_SYSTEM violet -> purple  Provider-sponsored plans from national
#                                   hospital brands (payviders).
#   LOCAL         teal -> green     Genuinely local/regional plans with no
#                                   national brand. Shared FAMILY, ranked by
#                                   size within the state.
#
# Family tells the reader what KIND of payer it is before they read the label.
# Carrier and health-system assignments are RESERVED across every state build.
# ---------------------------------------------------------------------------

PAYER_CARRIER = {
    "Centene":                "#3053A3",
    "CVS / Aetna":            "#3876A3",
    "UnitedHealthcare":       "#3734AE",
    "BCBS (independent)":     "#456F86",
    "CareSource":             "#464EBD",
    "AmeriHealth Caritas":    "#5C68AB",
    "Kaiser Permanente":      "#5789A4",
    "Molina":                 "#6F80C4",
    "Humana":                 "#869AC5",
    "Elevance / Wellpoint":   "#3C3A71",
}

PAYER_HEALTH_SYSTEM = {
    "Mayo Clinic Health Plan":        "#462974",
    "MedStar Family Choice":          "#673479",
    "Henry Ford Health Plan":         "#6B4B91",
    "UPMC Health Plan":               "#6741BE",
    "Johns Hopkins / Priority Ptr":   "#9B3FB8",
    "Presbyterian Health Plan":       "#A039C6",
    "Intermountain / SelectHealth":   "#8261C2",
    "Children's National / HSCSN":    "#A55BC8",
    "Geisinger Health Plan":          "#BC74D1",
    "Sentara / Optima":               "#B48DC3",
}

PAYER_LOCAL_RAMP = [
    "#386F6F",
    "#4C958E",
    "#3AC6B5",
    "#6FB596",
    "#70D2D2",
]

PAYER_TYPE = {
    "PACE":   "#9CACB4",
    "D-SNP":  "#26323C",
}

PAYER_ALTERNATES = {
    "BCBS (independent)":   "#0B3D5E",
    "CVS / Aetna":          "#155471",
    "Centene":              "#1E4478",
    "Kaiser Permanente":    "#1E6B9E",
    "Elevance / Wellpoint": "#8AC0E8",
    "UnitedHealthcare":     "#212B6E",
    "AmeriHealth Caritas":  "#35519E",
    "Molina":               "#6076C4",
    "Humana":               "#B8C8EF",
    "CareSource":           "#2A46A8",
    "MedStar Family Choice":        "#522E7C",
    "Johns Hopkins / Priority Ptr": "#B074D8",
    "UPMC Health Plan":             "#6A3CA0",
    "Children's National / HSCSN":  "#B98CD4",
}

COLLISION_DELTA = 60          # perceptual distance floor; below this, swap

# Back-compat: some callers may still reference the flat national table.
PAYER_NATIONAL = {**PAYER_CARRIER, **PAYER_HEALTH_SYSTEM}

# ---------------------------------------------------------------------------
# LOSS FAMILY — warm only. HR-1 gap bands. Never a baseline flow.
# ---------------------------------------------------------------------------
# Anchor #8B5A5A. Value and texture vary so the five destinations remain
# distinguishable in grayscale print, where hue carries nothing.

LOSS = {
    "care_foregone": {
        "fill":    "#C9A9A4",     # most washed out: the truest absence
        "texture": "hatch_wide",
        "label":   "Care that does not happen",
    },
    "out_of_pocket": {
        "fill":    "#B98A72",
        "texture": "dots",
        "label":   "Paid out of pocket by patients",
    },
    "federal_offset": {
        "fill":    "#A56E63",
        "texture": "hatch_fine",
        "label":   "Absorbed by federal offset programs",
    },
    "state_local_offset": {
        "fill":    "#8B5A5A",     # the anchor
        "texture": "crosshatch",
        "label":   "Unfunded state & local budget pressure",
    },
    "provider_absorbed": {
        "fill":    "#6E4243",     # most saturated: real money, real balance sheets
        "texture": "solid_edge",
        "label":   "Absorbed by providers (bad debt & charity)",
    },
}

LOSS_ANCHOR = "#8B5A5A"

# Counterflow: money arriving to partially defray the gap. Warm but inverted,
# so it reads as related to loss without reading as loss itself.
COUNTERFLOW = {
    "fill":    "#C4A45C",
    "texture": "hatch_reverse",
    "label":   "Rural Health Transformation Program (offset)",
}

INK = "#1A2733"
MUTED = "#5A6B7A"


def payer_color(name, tier=None, local_rank=0, used=None):
    """Return a plan's colour.

    tier        "carrier" | "health_system" | "local" | "type" | None (inferred)
    local_rank  0-based size order among that state's LOCAL plans only.
    used        colours already assigned in this state, for collision swap.

    Returns (hex, warning_or_None).
    """
    used = used or []
    if tier is None:
        tier = infer_tier(name)

    if tier == "type":
        return PAYER_TYPE.get(name, PAYER_LOCAL_RAMP[-1]), None

    if tier in ("carrier", "health_system"):
        table = PAYER_CARRIER if tier == "carrier" else PAYER_HEALTH_SYSTEM
        c = table.get(name)
        if c is None:
            return PAYER_LOCAL_RAMP[min(local_rank, len(PAYER_LOCAL_RAMP) - 1)], (
                f"{name}: declared {tier} but not in the reserved table. "
                f"Add it, or reclassify as local.")
        if c in used:
            alt = PAYER_ALTERNATES.get(name)
            if alt:
                return alt, (f"{name}: reserved {c} already used, "
                             f"swapped to alternate {alt}.")
        return c, None

    if local_rank >= len(PAYER_LOCAL_RAMP):
        return PAYER_LOCAL_RAMP[-1], (
            f"{name}: more local plans than ramp slots "
            f"({len(PAYER_LOCAL_RAMP)}). Extend PAYER_LOCAL_RAMP.")
    return PAYER_LOCAL_RAMP[local_rank], None


def infer_tier(name):
    if name in PAYER_CARRIER:
        return "carrier"
    if name in PAYER_HEALTH_SYSTEM:
        return "health_system"
    if name in PAYER_TYPE:
        return "type"
    return "local"


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def perceptual_distance(a, b):
    """Rough weighted-RGB distance. Good enough to catch collisions."""
    r1, g1, b1 = _hex_to_rgb(a)
    r2, g2, b2 = _hex_to_rgb(b)
    rm = (r1 + r2) / 2
    dr, dg, db = r1 - r2, g1 - g2, b1 - b2
    return (((2 + rm / 256) * dr * dr) +
            (4 * dg * dg) +
            ((2 + (255 - rm) / 256) * db * db)) ** 0.5


def audit_state_palette(plans):
    """Run before any state build.

    `plans` is a list of dicts: {"name": str, "tier": str|None, "size": float}
    Local plans are ranked by size descending to pick their ramp slot.

    Returns (assigned, warnings). The build should REFUSE TO RENDER on any
    COLLISION warning, matching the seven balance checks' behaviour.
    """
    warnings, assigned, used = [], {}, []

    locals_ = sorted(
        [p for p in plans if (p.get("tier") or infer_tier(p["name"])) == "local"],
        key=lambda p: -p.get("size", 0))
    rank = {p["name"]: i for i, p in enumerate(locals_)}

    for p in plans:
        c, w = payer_color(p["name"], p.get("tier"), rank.get(p["name"], 0), used)
        assigned[p["name"]] = c
        used.append(c)
        if w:
            warnings.append(w)

    names = list(assigned)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            d = perceptual_distance(assigned[names[i]], assigned[names[j]])
            if d < COLLISION_DELTA:
                warnings.append(
                    f"COLLISION: {names[i]} and {names[j]} are {d:.0f} apart "
                    f"(floor {COLLISION_DELTA}).")
    return assigned, warnings


def texture_defs():
    """SVG <defs> for the loss-family textures. Absence reads as texture even
    with no color at all, which matters for grayscale print and photocopies."""
    return """
  <defs>
    <pattern id="hatch_wide" patternUnits="userSpaceOnUse" width="8" height="8"
             patternTransform="rotate(45)">
      <rect width="8" height="8" fill="none"/>
      <line x1="0" y1="0" x2="0" y2="8" stroke="#FFFFFF" stroke-width="3" opacity="0.75"/>
    </pattern>
    <pattern id="hatch_fine" patternUnits="userSpaceOnUse" width="5" height="5"
             patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="5" stroke="#FFFFFF" stroke-width="1.6" opacity="0.6"/>
    </pattern>
    <pattern id="hatch_reverse" patternUnits="userSpaceOnUse" width="7" height="7"
             patternTransform="rotate(-45)">
      <line x1="0" y1="0" x2="0" y2="7" stroke="#FFFFFF" stroke-width="2.2" opacity="0.7"/>
    </pattern>
    <pattern id="crosshatch" patternUnits="userSpaceOnUse" width="7" height="7">
      <line x1="0" y1="0" x2="0" y2="7" stroke="#FFFFFF" stroke-width="1.4" opacity="0.55"/>
      <line x1="0" y1="0" x2="7" y2="0" stroke="#FFFFFF" stroke-width="1.4" opacity="0.55"/>
    </pattern>
    <pattern id="dots" patternUnits="userSpaceOnUse" width="6" height="6">
      <circle cx="3" cy="3" r="1.5" fill="#FFFFFF" opacity="0.7"/>
    </pattern>
    <pattern id="solid_edge" patternUnits="userSpaceOnUse" width="10" height="10">
      <rect width="10" height="10" fill="none"/>
      <line x1="0" y1="0" x2="0" y2="10" stroke="#FFFFFF" stroke-width="1" opacity="0.3"/>
    </pattern>
  </defs>"""
