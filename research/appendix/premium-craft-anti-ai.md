# Appendix — Premium Visual Craft & the Anti-"AI Look" Playbook

Full research findings (agent pass, Aug 2026). Condensed version in §7 of the main brief.

## 1. Trust data — why the client is right to be paranoid
- NIM ("Transparency Without Trust"): *identical* ads rated less natural/useful/appealing when labeled AI-made; purchase intent drops. Only ~20% trust AI itself.
- Forbes/Harris Poll: consumers saying heavy AI use decreases brand trust doubled 2025→2026 (20%→~40%). ~63% less likely to purchase from brands using AI-generated ads; 73% distrust suspected-AI ads. Half of US consumers prefer brands that don't use genAI in customer-facing content (IAB).
- **The label paradox (Bynder, n=2,000):** 56% *preferred* unlabeled AI copy — but told it was machine-made, 52% disengaged. **Audiences punish detectability, not AI use. Craft goal = zero tells, not zero AI.**
- Cautionary tale: Coca-Cola's AI holiday remake derided as "soulless" despite budget. Hybrid AI+human works best for conventional products (NIM).
- Cars are AI's hardest subject: (1) reflective surfaces must mirror a coherent environment, (2) brand-exact geometry enthusiasts know cold, (3) small badge/plate text. One wrong panel reflection gives everything away — and **reflections are a detailing brand's literal product**.

## 2. AI-tells checklist
**Car-specific (fatal):** melted/garbled badges (#1 tell — see Autoblog's G-Wagen clone case where the car changed between AI "press photos") · wheel geometry (mismatched spoke counts, ovalized rims, wrong calipers, missing lugs) · nonsense plates · grille mesh/trim pattern breakdown, wandering panel gaps · incoherent paint reflections (two panels reflecting different worlds) · shadow contradicting light source · **missing tire contact shadow ("floating car")**.

**General:** plastic/waxy poreless texture on paint/tires/concrete · garbled text anywhere · uniform fake bokeh, melted foliage, misaligned architecture · the generic "epic moody garage" look (volumetric god-rays, teal-orange, wet floor with no water source) — now instantly pattern-matched as slop · crushed blacks + HDR oversaturation (AI's default grade) · impossible perfection (no grain/dust/flaws, dead-center symmetry) · hands/hair/jewelry fails · the unnameable "uncanny" gestalt (assume car people feel it 3× faster).

Trend note: text/hand tells are shrinking as models improve; **reflective-surface coherence and brand geometry remain unsolved** — exactly what detailing content is made of.

## 3. Using AI without detection
**Hard rules:**
1. Never let AI render badges, wheels, plates, or paint reflections. Those pixels come from a camera.
2. AI for environments only — real car cut out and composited (how the dealership industry does it at scale: vehicle pixels untouched, backdrop swapped).
3. img2img/inpainting off real client photos with the vehicle masked; never full-frame img2img of a car at high denoise.
4. Inpaint small problem regions; creative upscale 2–4×; sharpen.

**Compositing craft:** match light direction first (generate background specifying the photo's light: "window light from left," "overcast afternoon"); background slightly darker than subject; **single soft contact shadow under tires = the single biggest believability fix**; one unifying curves/LUT pass over the whole composite; reflection sanity check — quiet backgrounds (dusk sky, dark studio, plain wall) hide reflection mismatch best (another argument for the dark-studio style).

**De-AI-ing pass (numbers):** add noise 2–4% Gaussian monochromatic (highest-impact single step) · desaturate 10–15% · lift blacks slightly · crop imperfectly (off-center, clip an edge) · prompt-side: "shot on Sony A7IV, 50mm f/1.8," "35mm film grain," "Kodak Portra 400"; negatives: smooth, airbrushed, perfect lighting, HDR, oversaturated, centered composition, bokeh balls, stock photo.

**Consistency:** an AI image that changes the "same" van's details between posts torches credibility — lock references of the actual vehicle/rig and never regenerate them.

**Safe-use ladder:** ① real photo + retouch (hero, always safe) → ② real photo + AI cleanup (bins, sky, background extend) → ③ real car cutout + AI quiet background, graded as one → ④ AI atmosphere backplates behind typography (no car) → ⑤ full AI car beauty shots: **never**.

## 4. Photography & retouch fundamentals to mimic
- **Golden hour:** soft diffuse light flatters paint; f/8–f/11 (to f/16), low ISO, sun raking across body lines; position for deliberate reflections on paint/glass.
- **Polarizer (CPL) look:** kills glare so "true depth of the paint comes through — reds richer, blacks deeper"; ~90° to sun, rotate to taste; **don't over-polarize** (fully stripped reflections make gloss look matte — opposite of detailing content). Keep the desirable reflection (sky gradient, body-line highlight streak), remove the ugly one. Digital mimicry: selective dehaze/clarity on paint, darken windows, deepen sky, preserve the specular streak.
- **Hero angle:** low front/rear three-quarter, camera at/below headlight height; reflective panels at 35–45° to camera.
- **Detailing money shots:** backlit/side-lit water-beading macro (each bead gets a specular ping — the ceramic/coating proof); wet-look gloss photographed right after application with one defined light source creating a long clean highlight streak; before/after under identical light/framing or it reads cheated.
- **Dark-studio light painting:** pitch-dark space, tripod, 10s+ exposures, walk an LED tube around the car, blend exposures. Achievable in a garage with a ~$50 LED wand; very hard for AI to fake → doubles as an authenticity signal. Commercial reality: pro finals are multi-exposure composites; ~85% of commercial car photographers outsource retouch — budget real retouch time.

## 5. Design craft that reads premium
**DO:** 2–3 colors max (dominant near-black/charcoal/navy neutral + brand accent + highlight) · generous negative space ("we don't need to overwhelm you to impress you" — Apple/Mercedes model; clutter = cheap/shouty) · one display face + one workhorse sans with 3–4× size jumps; attend to kerning/tracking/leading · consistent grid/margins/logo position across every post (consistency IS the brand) · subtle texture (fine grain, faint carbon/asphalt at low opacity) over layer effects.

**DON'T (amateur markers):** bevel & emboss, outer glows, dramatic drop shadows · rainbow/overcooked gradients; >1–2 layer effects · stretched/squashed type or logos · >2 typefaces · low-res raster logos · fear-of-whitespace clutter · everything-bold no-hierarchy · cliché stock (handshakes, generic supercar renders that aren't the client's work).

**Feed legibility:** 1080×1350 (4:5) primary; story safe zones top ~250px / bottom ~340–350px clear; text contrast ≥4.5:1 (WCAG AA — survives sunlight); a *subtle* shadow/thin outline on overlay text is the one acceptable shadow; ~125 caption chars before "more"; test every graphic at thumbnail size on a phone.

## 6. Typography
**Luxury-auto code (Monotype):** ~80% of luxury car brands set logos/headings in ALL CAPS with wide letter-spacing; sans-serif dominates. Motorsport = condensed bold sharp (speed); luxury = wide spaced light-medium caps (calm confidence). A detailing brand can blend: condensed bold for offers/energy + wide spaced caps for the premium layer.

**Free/Google font system:**

| Role | Font | Notes |
|---|---|---|
| Impact headline (condensed) | **Anton**, **Oswald**, **Barlow Condensed Bold** | Barlow is a superfamily → one-family system |
| Premium wide caps | **Archivo** (Expanded), **Space Grotesk** | Wide grotesk = modern luxury |
| Body/UI | **Inter**, **Archivo**, **Montserrat** | Sharp at small mobile sizes |
| Semi-condensed sport alt | **Saira** (+ Condensed variants) | Racing-designed, 9 weights |
| Techy accent (sparingly) | Exo 2; **avoid Orbitron** | Orbitron reads sci-fi/gamer = cheap risk |

Pairing recipe: condensed grotesque headline + neutral modern sans body (e.g. **Anton caps + Inter**), or all-Barlow/all-Archivo superfamily (hardest to get wrong in templates). Micro-rules: all-caps headlines +5–15% tracking; never track out lowercase body; never fake-condense by scaling; 2 families max.

## 7. Template systems ("swappable variables" architecture)
- **Central kit file:** color tokens, type styles (H1/H2/body/CTA), logo components, texture assets — referenced, never rebuilt.
- **Master components with variants** per format (4:5, 1:1, 9:16, flyer) × content type (before/after, offer, testimonial, booking CTA, educational).
- **Photo zones as placeholder/smart-object slots** — the photo is the variable; layout, margins, logo lockup, type never move. In PSD: grain + color-grade adjustment layers ABOVE the photo slot so every swapped photo inherits the house look.
- **Governance:** Canva Brand Templates with element locks (team can only swap photos/edit copy — can't move the logo or break the grid; draft/republish approval flow). Figma equivalent: publish-locked libraries.
- **Practical set:** 6–8 locked masters (before/after split, single hero, 3-photo process, offer/price, review card, story CTA) × swappable real-photo zones = infinite feed, one system.
- Why it solves the AI question: **AI never touches layout or type** (where "cheap" is most visible); every photo zone is fed by real client shots. The locked system is the anti-slop insurance.

## 8. Print & QR craft
- Bleed ~3mm past trim for edge-touching elements; text/logos/QR ≥3mm inside trim; export PDF w/ bleed + crop marks; CMYK-aware (rich black mix, not 100K; no unprintable RGB neons).
- One offer, one CTA, arm's-length readability — flyers get glanced, not read.
- **QR:** min ~2cm handheld; ~5cm at poster distance (rule: scan distance ÷ 10); ≥4-module quiet zone; dark-on-light, high contrast (brand-colored dark modules fine); framed into the grid with "Scan to book" caption, bottom third — branded codes get up to ~40% more scans than default black squares. Print a physical proof on the actual stock and scan-test it.
- Digital adaptation: bump contrast and type size vs print; re-check 4.5:1 on-screen.

## Key sources
imagera.ai + whichoneis.ai + GIJN + Fox News (AI tells) · autoblog.com G-Wagen-clone case · nim.org "Transparency Without Trust" · Forbes/Harris Poll · iab.com "AI Ad Gap" · Bynder survey (via JIAD/tandfonline) · koinsights.com authenticity premium · upsampler/pixova/imagera (de-AI workflows) · Adobe compositing · getimg.ai/photoroom/stable-diffusion-art (background replacement) · autopix.no + kasefilters.eu (CPL) · proedu.com (golden hour) · fstoppers + machineswithsouls + andrewlinkphotography (light painting) · studiometrodesk (retouch) · drbeasleys.com (beading) · 99designs + companyfolders + atomicsocial (amateur markers) · ixdf.org + graphically.io (negative space) · monotype.com (luxury auto type) · fontalternatives + fontfabric + creativeboom + groteskly.xyz (type trends) · canva.com brand-template locks · mokudigital + usevisuals (Figma systems) · paperlust (print checklist) · adobe.com/express + qr-insights + cgamedia (QR) · coinis + admanage.ai (overlay/dimensions).

*Verification note: Autoblog, Curbside Classic, and GIJN resisted direct fetch (403s) — those findings came via search extracts; Harris Poll stats are secondhand via Forbes. Re-verify before quoting in client-facing decks.*
