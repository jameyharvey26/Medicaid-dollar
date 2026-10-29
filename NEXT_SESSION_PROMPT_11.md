# Next session — controls and UI for the demo. Engine only.

## Start here and nowhere else

The repo is in my Documents folder, `GitHub/Medicaid-dollar`. Ask for that
folder and nothing else.

**Do not run the gates.** Not `gates.py`, not `build.py`, not `renderproof`.
They take minutes, they rebuild the paper, and none of it is what I'm doing.
`renderproof` is red on purpose and `RENDER_DEFECTS.md` says why — if you find
yourself reading about it, you have gone the wrong way.

**Do not install anything** unless something actually fails. The whole job is
one HTML file.

Read these two, in this order, and then start:

    git log -1 --stat          what landed last session
    DC_ENGINE_TODO.md          every assumption currently on the plate

Skip `MANIFEST_SESSION.md` unless something confuses you. It is long.

## Where things are

`engine/explorer_engine.html` is the whole app. One file, four panels — US
and DC, FY2024 and FY2030 — fonts inside it, no network needed. Open it in a
browser to see it.

Two rules about that file:

- `const DATA = {...};` must stay on ONE line. `engine_data_export.py`
  rewrites it with a regex and will refuse if it has been reformatted.
- Everything else in it is hand-written and safe to edit.

If you change a ledger, `python3 engine_data_export.py` is the one command
that puts it back in the engine. That is fast. Nothing else needs to run.

## What I want to do

Build the controls and the UI for driving this in a room. I have not decided
what they are yet — that is the conversation. Right now there is one slider,
for work reporting, and five zoom buttons.

Come with options and your recommendation, as usual, and show me pictures
rather than describing things. Ask me one thing at a time.

## Things to know before you suggest anything

- The only assumption wired to a control is work reporting. The seniors lane
  has a published band too — the figure drawn is an upper bound and the band
  runs down to zero — so it could take a slider tomorrow.
- Two lanes on the DC FY2030 panel are national numbers wearing District
  labels. They are drawn behind a switch called `assumed_levers`, and I want
  to be able to flip that in front of people and show the difference.
- No District figure is signed. Any demo I give says so.

## How I work

One question at a time. Show me the picture before any layout claim. Recommend
on methodology, ask on direction — and when you ask, give me the options and
your recommendation, not a bare question. Derive in code, never type an
output. Commit at close, not mid-session. Challenge me if a request does not
make sense; I would rather be told no than agreed with.

Talk to me in plain English about what I would see. Not counters, not metrics,
not tool names. I am not a computer.
