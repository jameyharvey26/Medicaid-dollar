# AUTHOR_HELD_SHEILA.md

Held, not deleted. Removed from every artifact on 2026-09-18 by JW's ruling
(D-68) because co-authorship requires CareFirst approval that has not been
given. Nothing here is a judgment about the material; it is parked so it can go
back in one move if the approval comes.

Restoring means reversing four removals, in this order: the byline, the bio
cell, the author-grid geometry, and the disclosure. Each is below in the form it
had when it was removed.

---

## 1. Byline

Cover, `paper_national_v4_1.html` line 138 and `paper_national.typ` line 74.

```
Jamey Harvey and Sheila Yahyazadeh
```

Sub-line beneath it read `Agilian LLC` and did not change when she was removed.
If she returns, that sub-line is wrong as it stands — it attributes both authors
to Agilian, and she is not at Agilian. It was wrong before too. Fix it on
restore.

## 2. Bio, HTML form

Second `<div class="bio">` cell inside `<div class="authgrid">`.

```html
  <div class="bio">
    <div class="nm">Sheila Yahyazadeh</div>
    <div class="rl">Chief External Operations Officer, CareFirst BlueCross BlueShield
      Community Health Plan Maryland</div>
    Sheila Yahyazadeh is the Chief External Operations Officer for CareFirst BlueCross
    BlueShield Community Health Plan Maryland. She has over a decade of experience working
    with government health programs including Marketplace, Medicaid, and Medicare. She
    specializes in business strategy, growth operations, innovation, and partnership
    building. Sheila is passionate about elevating the voice of consumers and the community
    to improve equitable access to care. Through partnerships with providers, community
    stakeholders, startups, and the state, she has built pathways to care access for
    historically underserved and disadvantaged communities. Prior to joining CareFirst
    BCBS, Sheila led strategic campaigns and CX initiatives for Fortune 100 healthcare
    clients. She also spearheaded a health innovation team that brought together
    cross-functional expertise in AI/machine learning, creative services, and UX/UI to
    reimagine how healthcare is delivered. Sheila is committed to innovation as an advisor
    to start-up founders. She has a bachelor's in Human and Global Security as well as a
    Master's degree in Public Administration and Health Policy from American University.
    She is first generation American, daughter to Peruvian and Iranian parents. She is also
    a certified Health Coach, Yoga Instructor, and an avid traveler.
  </div>
```

## 3. Bio, Typst form

Second cell of the `#grid(columns: (1fr, 1fr), gutter: 11mm, ...)` on the
authors page of `paper_national.typ`.

```
  [#text(font: "Jost", size: 11pt, weight: 600, fill: blue)[Sheila Yahyazadeh] \
#text(font: "Jost", size: 8.6pt, fill: mut)[Chief External Operations Officer, CareFirst BlueCross BlueShield Community Health Plan Maryland]

#set text(size: 8.8pt)
Sheila Yahyazadeh is the Chief External Operations Officer for CareFirst BlueCross BlueShield Community Health Plan Maryland. She has over a decade of experience working with government health programs including Marketplace, Medicaid, and Medicare. She specializes in business strategy, growth operations, innovation, and partnership building. Sheila is passionate about elevating the voice of consumers and the community to improve equitable access to care. Through partnerships with providers, community stakeholders, startups, and the state, she has built pathways to care access for historically underserved and disadvantaged communities. Prior to joining CareFirst BCBS, Sheila led strategic campaigns and CX initiatives for Fortune 100 healthcare clients. She also spearheaded a health innovation team that brought together cross-functional expertise in AI/machine learning, creative services, and UX/UI to reimagine how healthcare is delivered. Sheila is committed to innovation as an advisor to start-up founders. She has a bachelor's in Human and Global Security as well as a Master's degree in Public Administration and Health Policy from American University. She is first generation American, daughter to Peruvian and Iranian parents. She is also a certified Health Coach, Yoga Instructor, and an avid traveler.]
```

## 4. Author-grid geometry

Both artifacts carried a two-column grid built for two cells:

- HTML, line 120: `.authgrid{ display:grid; grid-template-columns:1fr 1fr; gap:0 11mm; }`
- Typst: `#grid(columns: (1fr, 1fr), gutter: 11mm, ...)`

With one author the grid was changed to a single column. Restoring her means
restoring `1fr 1fr` in both places as well as the cell.

## 5. Disclosure paragraph

Removed whole from the author page. Its first sentence is the conflict statement
and returns with her. Its second and third sentences are facts about the
diagrams and do not depend on her being an author; their disposition is an open
question at the time of removal.

```html
<p class="disclose"><b>Disclosure.</b> Sheila Yahyazadeh is an officer of a Medicaid
managed care organization. CareFirst BlueCross BlueShield Community Health Plan Maryland
is a nonprofit plan and is therefore not counted in the public-company earnings figure on
either diagram. The plan administration band on both panels is a national aggregate
derived from CMS-64 and MACStats and contains no plan-specific figure.</p>
```

Typst form:

```
#text(size: 8pt, fill: mut)[*Disclosure.* Sheila Yahyazadeh is an officer of a Medicaid managed care organization. CareFirst BlueCross BlueShield Community Health Plan Maryland is a nonprofit plan and is therefore not counted in the public-company earnings figure on either diagram. The plan administration band on both panels is a national aggregate derived from CMS-64 and MACStats and contains no plan-specific figure.]
```

## 6. What this ruling closes

- **S-092** — whether Sheila has seen the author-page disclosure wording. There
  is no author-page disclosure for her to see. Closed by D-68, not answered.
- **D-67** — the 2026-09-11 decision naming her as co-author. Superseded by
  D-68. D-67 itself stands in the record; it is not being rewritten.

## 7. What this ruling does not reach

The working record — `WHITEPAPER_BRIEF.md`, `EDITORIAL_STANDING_NOTES.md`,
`MANIFEST_SESSION.md` and the handoff files — still carries her name, her
employer and the bio verbatim, and the repo is public. Those files are the
project's memory and are append-only by rule. Removing her from them is a
separate decision and has not been taken.
