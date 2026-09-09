# Handoff prompt — Calendly booking button, in three gated stages

Paste the block below into the Claude Code session that has the live
carolinaglossdetailing.com codebase.

It is deliberately staged. Nothing in the existing site is touched until stage 3,
and stage 3 does not start until the preview in stage 2 has been approved.

---

Task: add a booking button to each of the three package detail views, opening
that package's Calendly popup. Work in three stages and **stop at the end of each
one for approval**. Do not run ahead.

## Stage 1 — plan only, zero edits

Read `index.html`, `server.js` and `quote.html`. Do not modify any file. Report:

- exactly where each of the three package detail views is defined, by line range
- how they are shown and hidden (`data-open`, `location.hash`, whichever it is),
  and whether a hidden panel is `display:none` or offscreen
- the class names the page already uses for its primary and secondary buttons
- where the existing "Ready to book X?" block and Get my quote button sit inside
  each detail view
- where scripts are currently loaded at the end of `<body>`
- the exact insertion point you propose for each button, and the one-line diff
  shape you intend

Then stop and wait.

## Stage 2 — live preview in a new file, still zero edits to the site

Create **one new file**, `preview-booking.html`, at the repo root. Do not modify
any existing file. Do not add a route for it in `server.js`.

The preview must:

- reproduce the three package detail views closely enough to judge the placement,
  reusing the site's real classes and copying its `<style>` block or linking it if
  it is external
- load Calendly for real:

      <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
      <script src="https://assets.calendly.com/assets/external/widget.js" async></script>

- carry one working button per package, wired with
  `Calendly.initPopupWidget({ url })`:

  | Detail view | Calendly URL |
  |---|---|
  | Basic | `https://calendly.com/carolinaglossdetailing-support/standard-package` |
  | Pro Clean | `https://calendly.com/carolinaglossdetailing-support/gloss-package` |
  | Deluxe | `https://calendly.com/carolinaglossdetailing-support/deluxe-package` |

Open it directly in a browser as a `file://` URL — Calendly loads over https from
a local file, so the popup, the booking form and the deposit all work for real.

Note: do not try to publish this preview as a Claude Artifact. Artifacts run under
a CSP that only permits scripts from a small CDN allowlist, and
`assets.calendly.com` is not on it, so the popup would silently never open. A
local file is the only way to preview the real widget.

Report the file path and what you confirmed working. Then stop and wait.

## Stage 3 — apply to the site, additive only

Only after the preview is approved. Port the same button into each of the three
detail views in `index.html`, and load Calendly's `widget.css` and `widget.js`
**once** at the end of `<body>` — once for the page, not once per package.

**Do not:**
- change, restyle, reorder or reword any existing markup, copy or CSS
- build a calendar, date picker, time-slot list or any booking UI of your own —
  Calendly's popup is the entire booking experience
- add a vehicle selector, service dropdown, name/phone/email field or any other
  form input. Calendly's booking form already collects all of it, and its event
  description already carries the pricing and prep copy. Anything added here asks
  the same questions twice.
- remove or replace the existing Get my quote button — the two sit side by side
- rename the packages; Basic / Pro Clean / Deluxe stay exactly as they are here
- touch `server.js`, `package.json`, `quote.html`, or anything in `assets/`
- add a dependency, build step, framework or CSS library
- add any third-party script other than Calendly's own
- delete `preview-booking.html` unless asked

Attach the click handler in JS with the URL on a data attribute rather than an
inline `onclick`, matching how the rest of the page is wired. Style the button
with the classes the page already uses. Do not invent new button styles.

**Why popup and not the inline embed:** the detail views are hidden panels. An
inline `.calendly-inline-widget` inside a `display:none` panel initialises at zero
height and renders as a collapsed sliver — it looks broken when it is not. The
popup renders in its own overlay above the page, so the hidden panel never touches
it. If an always-visible on-page calendar is wanted later, that needs deferred
initialisation on reveal; do not attempt it in this change.

**Verify before pushing:**
- `npm start`, open `http://localhost:3000`
- open each of the three package details, click the button, confirm the correct
  package's calendar opens and fills the overlay
- close and reopen, switch packages, reload with a package hash in the URL
- on a phone width, confirm the overlay is usable and the page behind it does not
  scroll sideways
- confirm nothing else on the page shifted, restyled or changed colour
- `git diff` shows additions only, in `index.html` plus the new preview file

Then commit and push.

---

## Already done inside Calendly — do not rebuild any of it

Confirmed on the live Deluxe event type:

- the **$20 deposit is already collecting**, so Stripe is connected
- the event description already carries the pricing and prep copy: base from $200,
  10% deposit applied to the total, final price confirmed after seeing the vehicle,
  clear personal items, park with access to all sides, keys ready
- duration is set (5 hr on Deluxe)

The site needs the button and nothing else.

## Two separate follow-ups, not part of the above

**1. Check the event timezone.** Confirm each event type's availability timezone
is Eastern. If the host schedule is set to anything else, 8am–6pm will be offered
at the wrong hours for Charlotte customers.

**2. Zapier hook is hardcoded.** `server.js` line 7:

    const LEAD_WEBHOOK_URL = process.env.LEAD_WEBHOOK_URL || 'https://hooks.zapier.com/hooks/catch/27894288/44lfpqm/';

Anyone with repo access can post junk leads into the automation. It should read
from the env var with no fallback. Worth doing before launch, but as its own
change so the Calendly diff stays clean.
