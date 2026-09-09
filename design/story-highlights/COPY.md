# Carolina Gloss — Package Statics

Three 1080×1920 images, one layout, only the package content changes.
Source copy: carolinaglossdetailing.com package pages, shortened for story reading.

Rendered files live in `out/`. Rebuild with `python3 build.py`
(`--measure` to check fit, `--canvas` to regenerate the .dc.html).

## Shared on all three

- Header: crest logo on white, Carolina blue bar. Service area lives in its own highlight, not here
- Best-for card, then the CTA: `CALL OR TEXT` + `980·690·5259`. No hours, website or prices, so nothing on the image goes stale
- Price line: "Priced on your vehicle size and condition. We lock that number in before we touch the car."

## STANDARD

**Best for** Your everyday fresh. Start the day in a clean car.


| Item | Payoff |
|---|---|
| Hand wash, top to bottom | Two mitts and clean water. No brushes, no swirl marks. |
| Wheels, tires and trim | Brake dust out of the barrels, trim back to black. |
| Full interior vacuum | Seats, rails, under the mats, and the trunk. |
| Glass, inside and out | Streak free on both sides. You notice it driving at night. |
| Vinyl sanitized, leather refreshed | Dash, doors, console and every vent wiped down. |


## GLOSS  (carries the #1 rosette)

**Best for** The one everybody’s actually looking for. A full in and out makeover.


| Item | Payoff |
|---|---|
| Light clay bar | Pulls the grit washing cannot reach. Run your hand over the hood after. |
| Hot water extraction | Coffee, dog, kids, gym bag. Gone, not covered up. |
| Two bucket wash | Dirt goes in its own bucket, never back onto your paint. |
| Leather and vinyl conditioned | So it stops drying out and cracking in the Carolina sun. |
| Wheels and tires, second pass | Faces, barrels and lug seats done properly, then dressed. |


## DELUXE

**Best for** The final boss. Fresh, sealed, basically a brand new car.


| Item | Payoff |
|---|---|
| Full clay bar | The whole body decontaminated panel by panel, not a spot treatment. |
| Chemical strip wash | Old wax and road film off so the new protection bonds. |
| Ceramic soap | Lays down a slick layer. Water sheets straight off your paint. |
| Hand wax and spray sealant | Months of protection against pollen, sun and road salt. |
| Interior shampooed and conditioned | Comes back looking like a lease return. |


## Palette

Sampled from the pixels of `assets/logo.png`. Three colors, nothing else.

| Role | Hex | Where it appears |
|---|---|---|
| White | `#FFFFFF` | the ground everywhere, and the type inside the blue CTA |
| Black | `#17181A` | body type. Neutral, no blue cast |
| Carolina blue | `#79A9EE` | 35% of the crest. Package name, CTA block, divider bar, the Gloss rosette |
| Deep blue | `#4F86D9` | a darker tone of the same blue, only to give the rosette depth |

`#EDF3FD` and `#D7E5F8` are that same blue washed into white for the card and the
dividers. The blue is too light for small text on white, so it only ever appears as a
fill with black on top of it. The one exception is the package name, which is set in
blue at 112px where the size carries it.

## Source alignment

Checked against carolinaglossdetailing.com and the @carolinaglossdetails grid.

**Open item for the client:** the website still lists the packages as
**Basic / Pro Clean / Deluxe**. Instagram and these statics use
**Standard / Gloss / Deluxe**. Anyone who taps from a post to the quote form
meets a different set of names, and the form dropdown offers the old ones.
One side has to change before these go up.

Everything else traces to the site: the sub lines, the row payoffs and the
best-for lines are the site's own wording, tightened. Two claims were
corrected against it: the Gloss clay bar is the site's "light" clay bar, not
the full one, and Deluxe now states that it contains Gloss.

Dropped from the site lists to fit five rows per frame, all under-promises,
never over: Standard's "cloth seats, light pass"; Standard's leather and vinyl
rows merged into one; Deluxe's shampoo and interior-condition rows merged.

## Story highlight covers

`covers.py` renders the set to `out/covers/`, plus `00-row-preview.png` showing
how the six read side by side on the profile.

Six covers, one system: Standard / Gloss / Deluxe live under **Services**, and
the rest are the row a detailer needs.

| File | Highlight title to type in Instagram | Icon |
|---|---|---|
| `services.png` | Services | stacked layers |
| `location.png` | Location | map pin |
| `reviews.png` | Reviews | star |
| `before-after.png` | Before / After | split tile |
| `book.png` | Book | calendar with a check |
| `faq.png` | FAQ | question mark in a circle |

**How they are built.** White ground, black icon, Carolina blue ring. Each is
1080×1920. Instagram crops the centre 1080×1080 and circles it, so the visible
disc is the full width of the image — checked against the live profile. The ring
is 900px, which fills that crop with a margin that reads as padding. An earlier
pass used 520px on the theory that the crop was tighter, and on the phone the
ring floated in a sea of white.

Ring stroke is about 4% of the ring diameter and the icon about 42% of it, the
proportions signed off on the treatment sheet. `covers_compare.py` renders that
sheet if the other two grounds ever need revisiting.

**Adding a seventh.** Add a tuple to `COVERS` in `covers.py` with a slug, a label
and the icon markup on the same 120×120 grid, then re-run. Nothing else changes.
Keep the set at six or seven — past that the row scrolls and the last ones are
never seen.
