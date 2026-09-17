# Carolina Gloss Detailing — Instagram highlight system

Handoff brief for Claude Design. Everything below is verified against the
client's live site, logo file and Google Business Profile. Where something is
unverified it says so.

---

## Part 1 — The prompt

Paste this in first.

> You are designing an Instagram story highlight system for **Carolina Gloss
> Detailing**, a mobile car detailing business in North Carolina. Owner is
> Dallas Marzett. The business drives to the customer — home or office — in
> Charlotte, Greensboro and Shelby.
>
> **Objective.** Six highlight sets that turn a profile visit into a booking.
> A stranger lands on the profile, taps a highlight, and within a few slides
> knows what they get, that other people trust it, and how to book. The
> highlights are the sales page. The feed is the ad.
>
> **Format.** Every slide is 1080 × 1920 PNG. Highlight covers are the same
> 1080 × 1920 canvas — Instagram crops the centre 1080 × 1080 and circles it,
> so the cover art has to sit inside that centre square and read at 100px.
>
> **Look.** Three colours, no more: white ground, near-black type, one Carolina
> blue. Big confident type. Flat vector. Nothing that looks generated — no
> gradients pretending to be light, no stock-photo gloss, no AI illustration.
> Think a well-made print job, not a template.
>
> **Voice.** Plain and specific. Short sentences. The way a detailer actually
> talks to a customer standing in their driveway. Never marketing language.
> No em dashes. No "elevate", "transform", "unlock", "experience".
>
> **Copy source.** Pull wording from carolinaglossdetailing.com and the
> client's real Google reviews. Do not invent service names, taglines, prices,
> guarantees, response times or a service radius. If a fact is missing, leave a
> gap and flag it rather than filling it.

---

## Part 2 — Brand spec

### Colour

| Token | Hex | Use |
|---|---|---|
| Ink | `#17181A` | All body and headline type. Logo black, no blue cast. |
| Carolina blue | `#79A9EE` | Sampled from the logo, where it is 35% of the crest. |
| Tint | `#EDF3FD` | Blue washed into white. Cards, bands. |
| Rule | `#D7E5F8` | Dividers, hairlines. |
| Muted | `rgba(23,24,26,0.62)` | Secondary type. Same black, stepped back. |
| Blue deep | `#4F86D9` | Only to give the Most Popular rosette depth. |

**The contrast trap.** `#79A9EE` on white is **2.2:1**. It fails for body
copy. It is legal as a *fill* — a block, pill, bar or rule — with white or
near-black type on top of it, and it is legal for display type at 100px and
up. For blue text at body sizes on white, use `#2B6BCB` (9.15:1).

**Banned:** navy, `#0B1220`, and any second accent colour. The client rejected
navy explicitly and more than once. The live website still uses navy — ignore
the site's palette, the logo is the authority.

### Type

| Role | Face | Notes |
|---|---|---|
| Display | **Archivo Black** | Headlines. `letter-spacing: -0.035em`, `line-height: 0.9`. |
| Body | **Archivo** 400 / 700 | Body copy and labels. |
| Meta | **IBM Plex Mono** 500 | Eyebrows, review counts, dates. `letter-spacing: 0.16em`, uppercase. |

Display headlines run 104–132px. Body 34–46px. Eyebrows 25px.

### Layout

The shipped grid, use it:

- Side margin **84px**, both edges, every slide.
- Header: crest centred, **240–264px** wide, with **66–74px** above it.
- A **10px** Carolina blue bar directly under the header. This bar is the one
  device that ties all six highlights together. Keep it on every slide.
- Body padding `72px 84px 180px`. The bottom **180–250px** is reserved because
  Instagram's own UI sits there.
- Content is centred in the body, biased slightly up out of that bottom UI.

### Covers

One cover per highlight, six total, and they have to read as a set.

- Ring diameter **900px**, stroke **36px** (~4% of the ring).
- Icon box **380px** inside the ring (~42% of the ring). This ratio matters —
  an earlier version at 63% looked cheap and got rejected.
- Icon stroke **6.5** on a 120 × 120 grid.
- Centre the ring in the middle 1080 × 1080 of the canvas. Instagram crops the
  full width, not a tight square.

### Assets

- Logo: `design/story-highlights/assets/logo.png` — full-colour crest.
- NC state geometry: `design/story-highlights/assets/us-states.json` —
  public state-boundary GeoJSON, if a map is used.
- Phone: **980·690·5259** — set with middle dots, not hyphens.

---

## Part 3 — Hard rules

Every one of these came from the client rejecting something. They are not
suggestions.

**Do not**

1. Use navy, or any colour outside the six tokens above.
2. Put a background on a slide other than white, black `#17181A`, or a solid
   Carolina blue field. Default is white.
3. Invent copy. No taglines, no package names, no prices, no radius, no
   "24 hour response", no guarantee. Verbatim from the site, or nothing.
4. Put hours or times on any static. They change and the client wants them
   adjustable in Calendly, not baked into an image.
5. Put the website URL on a static.
6. Use AI-generated photography. This was tried and rejected. Real photos from
   the client or flat vector only.
7. Put the crest on every slide of a multi-slide set. Open and close slides
   carry it, interior slides get the blue bar alone.
8. Grey out a word to create hierarchy. It reads as disabled, not as emphasis.
9. Let type or a label clip at the frame edge. Check both edges at 1080 wide.
10. Over-build. The client's most frequent note across this project is that the
    work is overthought. When in doubt ship the simpler version.

**Do**

1. Lead with specifics. "Brake dust out of the barrels" beats "premium wheel
   care" every time.
2. End every set on the phone number in a blue block: `CALL OR TEXT` in mono
   above, the number in Archivo Black below, white type on blue.
3. Fill the frame. Large dead space in the middle of a slide is the single
   thing that made the last round read as bland.
4. Scale display type to its content length so short lines fill the frame and
   long ones still fit.
5. Keep the three packages visually identical siblings — same layout, only the
   name and rows change.

---

## Part 4 — What is already shipped

Two of six highlights are live on the profile. Match them.

### Services — 8 slides, posted

`00-open`, six step slides, `07-close`. Interior slides are headline
(132px Archivo Black, blue, uppercase) over body (46px, bottom-anchored), with
a 132 × 12px blue mark under it. The six steps:

1. **Hand washed, hand finished** — no machines, no brushes, two mitts and clean water
2. **Two buckets, two mitts** — dirt goes in a separate bucket, never back onto the paint
3. **Wheels, tires and trim** — the part every drive-thru wash skips
4. **Clay bar** — pulls embedded grit washing physically cannot
5. **Hot water extraction** — water goes in, comes back out with the stain
6. **Strip, then seal** — old wax off first so new protection bonds

Closes on "Built around your car" plus the phone block.

### Reviews — 7 slides, posted

Opens on **5.0** at 250px in blue, five stars, "from **33 reviews** on Google"
with Google's own four-colour G mark. Five pull-quote slides, one per review,
each with the G mark, the reviewer's real name and review count, and
"5.0 from 33 reviews on Google". Closes on "Your turn. Book it." plus the phone
block.

The five verbatim quotes:

| Quote | Reviewer |
|---|---|
| "They removed deep stains from the seats that I thought were permanent." | Starr Cotton · Local Guide · 30 reviews |
| "It honestly looked better than when I first got it." | Jahmek Bracey · 2 reviews |
| "He arrived on time at my home." | Salena Duffy · 8 reviews |
| "Dealership quality and reasonably priced at that." | biana · 2 reviews |
| "If I could give more than 5 stars I would." | Tyler Spikes · 2 reviews |

Two things that look like mistakes and are not: **biana** is lowercase because
that is her actual Google display name, and the Dealership quote is a sentence
fragment because that is how she wrote it. Leave both.

**Rule for this set:** every pull quote must appear word for word in that
reviewer's actual review text. One quote in an earlier draft was attributed to
Salena Duffy and she never wrote it. Check each one against the source.

### Packages — 3 statics, posted

Header, blue bar, package name (112px Archivo Black, blue), five feature rows
(bold label + muted detail line), a tinted **BEST FOR** card below the rows,
then the blue phone CTA.

| Package | Best for |
|---|---|
| **Standard** | Your everyday fresh. Start the day in a clean car. |
| **Gloss** | The one everybody's actually looking for. A full in and out makeover. |
| **Deluxe** | The final boss. Fresh, sealed, basically a brand new car. |

Gloss carries a **#1 MOST POPULAR** rosette badge. The BEST FOR card has a
`min-height` so Gloss's two-line copy stays aligned with the other two. The
card sits **below** the rows — an earlier version moved it to the top and was
rejected.

### Covers — 6 made

services, location, reviews, before-after, book, faq. Redraw only if the set
gets rebuilt. Note: "packages" was renamed to "services", and the
before/after icon is a **split tile** — a diagonal slash version read as a
no-entry sign.

---

## Part 5 — The four highlights still to build

### 1 · Location — next up, unblocked

**Job:** kill the only question every mobile detailing lead has, which is
whether he comes to them.

**Slides:** 3 to 4.

| Slide | Content |
|---|---|
| Open | "We come to you." Mobile detailing at your home or office. |
| Map | North Carolina with Charlotte, Greensboro and Shelby marked. |
| Cities | The three names at display size. |
| Close | Phone block. |

**This one has failed twice. What went wrong:**

- A pale tinted state outline floating small in a white frame is bland. The
  map has to be large, solid-filled, and cropped by the frame edge.
- Radius halos around the cities blob into one shape, because Charlotte and
  Shelby are only about 40 miles apart. Do not use coverage circles.
- City labels clip off the right edge on a zoomed crop. Greensboro is the one
  that breaks — flip its label to the left side.
- A dead gap between the headline and the map is what made it read as cheap.

The geometry is in `assets/us-states.json`. Project it rather than tracing.
City coordinates: Charlotte `35.2271, -80.8431`, Greensboro `36.0726, -79.7920`,
Shelby `35.2924, -81.5356`.

**Unverified — ask Dallas before designing:** the actual service radius. The
site names three cities and nothing more. "and the Triad", "and the
surrounding metro", "and Cleveland County" were placeholder wording and are
not confirmed.

### 2 · Book — blocked on the website

**Job:** one tap to a real booking.

**Slides:** 3.

| Slide | Content |
|---|---|
| Open | What booking actually involves. |
| How | Pick a time, deposit holds the slot and comes off the total, exact price confirmed against the vehicle first. |
| Close | Phone block plus the link sticker callout. |

Deposits are **10% of the package price**: Standard $10, Gloss $15,
Deluxe $20. Calendly has one event per service and already collects the vehicle
details, so the slides should not ask for them.

**Blocked because** the booking buttons are not on the live site yet. The
implementation plan is in `design/booking-flow/LAUNCH-PLAN.md` and is owned by
a different session. Do not ship a highlight that points at a booking flow
that does not exist.

**Unverified:** package prices. $100 / $150 / $200 is the basis the deposits
were calculated from, but an older copy of the codebase showed different
numbers. Confirm against the live site before putting a price on a slide.

### 3 · Before / After — blocked on photos

**Job:** the highest-converting content type in detailing. Nothing else comes
close.

**Slides:** 2 per car, however many cars there are.

Needs real photos from Dallas: **same car, same angle, same light, before and
after.** Phone photos are fine. Inconsistent angles ruin the effect, and AI
images would be spotted immediately on this specific set — which is exactly why
the client rejected generated photography earlier.

Until those arrive this highlight cannot be built. Chasing the photos is worth
more than any design decision on this list.

### 4 · FAQ — unblocked, lowest priority

**Job:** clear the last few objections.

**Slides:** 4 to 6.

The client's direction on this one, in their words: not all of it needs to be
question-and-answer format, and it should pull exclusively from the services
already offered rather than inventing new questions. Candidates from real
gaps: does he need water and power on site, how long does each package take,
what happens if it rains, does he do interiors only.

All four of those are **unverified**. Get the answers from Dallas before
designing the slides.

---

## Part 6 — Open items outside design

1. **The Google profile is still named DalDeTails Mobile Detailing.** All 33
   reviews and the 5.0 live on that listing. Renaming it keeps them. Creating
   a new listing loses them. The Reviews highlight is already posted and points
   people at a name that does not match the brand, so this is the most
   time-sensitive item here.
2. Calendly availability says Mon–Fri 9–5 while the site says Mon–Sat 8–6.
3. Calendly event display names are still "Basic" and "Pro Clean" and need to
   become Standard and Gloss. The slugs can stay, so no links break.
