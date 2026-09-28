# v8.0 — commit package

D-104 through D-116. Copy the top-level files into the repo root, replacing
files of the same name, and replace `render_register/` wholesale.

On `DELETE OLD FILES.command`: `medicaid_dollar_explorer.html`,
`render_v7_1.py`, `paper_national_v7_1.html`,
`Medicaid_Dollars_National_v7.1.pdf`.

## What goes to the webmaster

| File | |
|---|---|
| `medicaid_dollar_explorer_v8.0.html` | The explorer. 2.3 MB, opens on a phone. |
| `Medicaid_Dollars_National_v8.0.html` | The whitepaper for the web. |
| `Medicaid_Dollars_National_v8.0.pdf` | The whitepaper for download. |
| `MHPA_Board_Deck_v8.0.html` | The deck for the web. |
| `MHPA_Board_Deck_v8.0.pdf` | The deck for download. |

All five are self-contained: fonts and figures inlined, nothing fetched at
runtime. They can sit in one directory and be served as static files.

**One dependency.** The explorer's whitepaper thumbnail and Download button
both point at the landing URL, so the paper has to be reachable from that page
or the explorer's download is a dead end. Easiest fix for the webmaster is to
put `Medicaid_Dollars_National_v8.0.pdf` at that URL, or tell me the final
path and I will point the button straight at it.

## Build

```
python3 gates.py          # everything, in order
python3 publish.py        # the five artifacts alone
```

14 gates green. `render_v8_0.py` honestly red: page 9 strands seven lines,
three leaders on `fig6_taper_all.svg` run through a label.

## One thing that needs you

**`views.V_DC.strap` is false.** It says the DC MCO service mix is a national
proxy; the panel no longer draws a service mix at all. Proposed:

> REDUCED FIDELITY. CMS-64 / MACStats FY2024 DC spine; payer peel DHCF
> CY2023. The panel stops at claims: no DC service allocation is published
> and none has been estimated. Vintages need re-checking.
