# Handoff prompt — add Calendly to the package detail views

Paste the block below into the Claude Code session that has the live
carolinaglossdetailing.com codebase. It is deliberately additive-only.

---

Task: add Calendly booking to the three package detail views. **Additive only —
nothing existing changes.**

Context: `index.html` is a single page. The package detail views are already in
the document and are revealed with `data-open` and `location.hash`. Each detail
view already ends with a "Ready to book X?" block and a Get my quote button.

**Do not:**
- change, restyle, reorder or reword any existing markup, copy or CSS
- build a custom calendar, date picker or time-slot UI — the Calendly iframe *is*
  the calendar
- rename the packages; Basic / Pro Clean / Deluxe stay exactly as they are in
  this task
- touch `server.js`, `package.json`, the quote form, or any file in `assets/`
- add a dependency, build step, framework or CSS library
- add any third-party script other than Calendly's `widget.js`

**Do:**

1. In each package detail view, directly after the existing "Ready to book X?"
   block, append one booking container using that package's URL:

   | Detail view | Calendly URL |
   |---|---|
   | Basic | `https://calendly.com/carolinaglossdetailing-support/standard-package` |
   | Pro Clean | `https://calendly.com/carolinaglossdetailing-support/gloss-package` |
   | Deluxe | `https://calendly.com/carolinaglossdetailing-support/deluxe-package` |

2. Load `https://assets.calendly.com/assets/external/widget.js` **once**, at the
   end of `<body>`, `async`. Not three times.

3. **Do not rely on Calendly's auto-init.** A `.calendly-inline-widget` that is
   inside a `display:none` panel when the script runs initialises at zero height
   and renders collapsed — this is the one thing that will actually break here.
   Instead, give each container a `data-url` but withhold the
   `calendly-inline-widget` class until its view is revealed, or call
   `Calendly.initInlineWidget({ url, parentElement })` the first time that view
   is shown. Guard it so each package initialises at most once.

4. Container sizing: `min-width:320px; height:700px; width:100%`.

**Verify before pushing:**
- `npm start`, open `http://localhost:3000`
- open each of the three package details and confirm the calendar renders at full
  height, not collapsed
- navigate between packages and back — confirm each still loads
- reload with a package hash directly in the URL — confirm it loads
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
