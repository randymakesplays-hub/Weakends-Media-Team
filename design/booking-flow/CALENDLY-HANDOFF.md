# Handoff prompt — add a Calendly booking button to all three packages

Paste the block below into the Claude Code session that has the live
carolinaglossdetailing.com codebase. It is deliberately additive-only.

---

Task: add a booking button to each of the three package detail views. The button
opens that package's Calendly popup. **Additive only — nothing existing changes,
and nothing new is built beyond the button.**

Context: `index.html` is a single page. The three package detail views are
already in the document and are revealed with `data-open` and `location.hash`.
Each one already ends with a "Ready to book X?" block and a Get my quote button.

**Do not:**
- change, restyle, reorder or reword any existing markup, copy or CSS
- build a calendar, date picker, time-slot list or any booking UI of your own —
  Calendly's popup *is* the whole booking experience
- add a vehicle selector, service dropdown, name/phone/email field or any other
  form input. Calendly's own booking form already collects all of it. Anything
  extra is a second form asking the same questions twice.
- remove or replace the existing Get my quote button — the two sit side by side
- rename the packages; Basic / Pro Clean / Deluxe stay exactly as they are here
- touch `server.js`, `package.json`, the quote form, or anything in `assets/`
- add a dependency, build step, framework or CSS library
- add any third-party script other than Calendly's own

**Do:**

1. Load Calendly once, at the end of `<body>`:

       <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
       <script src="https://assets.calendly.com/assets/external/widget.js" async></script>

   Once for the whole page, not once per package.

2. In each package detail view, next to the existing Get my quote button, add one
   button that opens that package's Calendly popup:

   | Detail view | Calendly URL |
   |---|---|
   | Basic | `https://calendly.com/carolinaglossdetailing-support/standard-package` |
   | Pro Clean | `https://calendly.com/carolinaglossdetailing-support/gloss-package` |
   | Deluxe | `https://calendly.com/carolinaglossdetailing-support/deluxe-package` |

   Wire it with `Calendly.initPopupWidget({ url })` on click, returning false so
   the page does not jump. Attach the handler in JS with the URL on a data
   attribute rather than an inline `onclick`, to match how the rest of the page
   is wired.

3. Style the button with the classes the page already uses for its primary
   button. Do not invent new button styles.

**Why popup and not the inline embed:** the detail views are hidden panels. An
inline `.calendly-inline-widget` inside a `display:none` panel initialises at
zero height and renders as a collapsed sliver — it looks broken when it is not.
The popup renders in its own overlay above the page, so the hidden panel never
touches it. If an always-visible on-page calendar is wanted later, that needs
deferred initialisation on reveal; do not attempt it in this change.

**Verify before pushing:**
- `npm start`, open `http://localhost:3000`
- open each of the three package details, click the button, confirm the correct
  package's calendar opens in the overlay and fills it
- close and reopen, switch packages, and reload with a package hash in the URL
- confirm on a phone width that the overlay is usable and the page behind it does
  not scroll sideways
- confirm nothing else on the page shifted, restyled or changed colour
- `git diff` shows additions only, confined to `index.html`

Then commit and push.

---

## Separate follow-up, not part of the above

`server.js` line 7 hardcodes a Zapier catch hook as its default:

    const LEAD_WEBHOOK_URL = process.env.LEAD_WEBHOOK_URL || 'https://hooks.zapier.com/hooks/catch/27894288/44lfpqm/';

Anyone with repo access can post junk leads straight into the automation. It
should read from the env var with no fallback. Worth doing before launch, but as
its own change so the Calendly diff stays clean.
