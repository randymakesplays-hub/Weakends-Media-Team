# Launch plan — direct booking on each service page

Each service gets its own Calendly booking. Three steps, `index.html` only.

Paste this whole file into the Claude Code session that has the live
carolinaglossdetailing.com codebase.

Out of scope: the Calendly hours (a setting to dial in later, no code) and the
Zapier hook (unrelated).

---

## The live site, verified

Audited by mirroring `www.carolinaglossdetailing.com` and screenshotting every
view — see `live-audit/`. The uploaded zip is a different, older build; ignore it.

| | |
|---|---|
| Host | apex 301s to `www.` |
| Page | one `index.html` |
| CSS | **external**, `/assets/site.css`. Nothing inline |
| JS | **external**, `/assets/quote.js`, plus an inline router in `index.html` |
| Views | `[data-view="home\|basic\|pro\|deluxe"]`, toggled by the **`hidden` attribute** |
| Routes | `#/basic`, `#/pro`, `#/deluxe`; anything else falls back to `home` |
| Handler | one delegated listener already owns `[data-home]`, `[data-nav]`, `[data-quote]` |
| Buttons | `.btn-lg` primary pill (blue fill, navy text) and `.linkish` text button |
| CTA block | each package ends in `.endcta` — a wrapping flex row, navy background |

---

## Step 1 — Rename in the service pages

Basic → **Standard**, Pro Clean → **Gloss**. Deluxe unchanged.

| Where | From | To |
|---|---|---|
| `data-view` + hash route | `basic`, `pro` | `standard`, `gloss` |
| `data-quote` | `Basic`, `Pro Clean` | `Standard`, `Gloss` |
| Card headings, detail hero, `.endcta` headings | Basic, Pro Clean | Standard, Gloss |
| "Everything in Basic" in the Gloss and Deluxe lists | Basic | Standard |
| Quote form service `<option>` values | Basic, Pro Clean | Standard, Gloss |

The form's option values have to match the new `data-quote` values, or
`sendToForm('service', …)` selects nothing.

Own commit — this touches routing, so keep it apart from step 2.

## Step 2 — Add the booking button to each service page

In each `.endcta`, the Get my quote button becomes the booking button. The quote
path moves into the paragraph as a `.linkish` text button, keeping its existing
`data-quote` behaviour.

> **Ready to book Gloss?**
> Pick a time that works. $15 holds the slot and comes off your total, and we
> confirm your exact price against your vehicle before we start.
> *Or get a price first*
>
> **[ Book Gloss · $15 deposit ]**

Standard $10 · Gloss $15 · Deluxe $20. Button reuses `.btn-lg` — do not write a
new button style.

URL on a `data-calendly` attribute, one per page:

- `standard` → `https://calendly.com/carolinaglossdetailing-support/standard-package`
- `gloss` → `https://calendly.com/carolinaglossdetailing-support/gloss-package`
- `deluxe` → `https://calendly.com/carolinaglossdetailing-support/deluxe-package`

Load once at the end of `<body>`:

    <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
    <script src="https://assets.calendly.com/assets/external/widget.js" async></script>

One branch on the existing delegated handler, alongside the three it already has:

    var cal = e.target.closest('[data-calendly]');
    if (cal) {
      e.preventDefault();
      if (window.Calendly) Calendly.initPopupWidget({ url: cal.getAttribute('data-calendly') });
      return;
    }

Two things not to get wrong:

- **Guard on `window.Calendly`.** The listener is shared, so an unguarded throw
  takes nav, back and the quote link down with it.
- **Popup, not the inline embed.** Views toggle on the `hidden` attribute, which
  computes to `display:none`. An inline widget inside one initialises at zero
  height and renders as a collapsed sliver — it looks broken when it is not.

One CSS line in `assets/site.css`: `.endcta .linkish{color:var(--blue)}` —
`--blue-ink` is 3.47:1 on the navy block, `--blue` is 9.15:1.

Nothing else touched: not `server.js`, `quote.js`, `package.json` or `quote.html`.
No calendar UI, no vehicle selector, no extra form field, no new dependency.

## Step 3 — Test, then push

- `#/standard`, `#/gloss`, `#/deluxe` all open
- each button opens its own event at the right deposit
- each *Or get a price first* returns home and prefills the right service
- nav and back still route; reload directly on `#/gloss`
- block `assets.calendly.com` in devtools — the rest of the page still works
- phone width: `.endcta` wraps, overlay usable, no sideways scroll

Two commits: step 1 renames only, step 2 the button work.

---

**Then, separately in Calendly:** rename the event titles from Basic and Pro Clean
to Standard and Gloss. The slugs can stay as they are, so no link breaks. Without
it the site says Gloss and the payment page still says Pro Clean.
