# Calendly booking — implementation plan, verified against the live site

Audited `www.carolinaglossdetailing.com` on 10 Sep 2026 by mirroring it locally
and screenshotting every view. Screenshots in `live-audit/`. Everything below is
what the live site actually does, not what the uploaded zip does — the zip is a
different, older build.

## What the live site is

| | |
|---|---|
| Host | apex 301s to **`www.`** — and it redirects to `http://`, not https |
| Page | one `index.html`, 28 KB |
| CSS | **external**, `/assets/site.css`, 17 KB. Nothing is inline |
| JS | **external**, `/assets/quote.js`, 4 KB, exposes `CarolinaQuote`, binds the form |
| Routing | an inline `<script>` in `index.html` |
| Third party | `weakendsapp-production.up.railway.app/pixel.js` |

## How the package views work

Four views, `[data-view="home|basic|pro|deluxe"]`, toggled by the **`hidden`
attribute** in the inline script. Hash routes are `#/basic`, `#/pro`, `#/deluxe`;
anything else falls back to `home`.

A delegated click handler already owns three attributes — `[data-home]`,
`[data-nav]`, `[data-quote]`. `[data-quote]` returns to home and prefills the
quote form's `service` field via `window.sendToForm`.

**This confirms the popup decision.** `hidden` computes to `display:none`. A
Calendly *inline* widget inside a hidden view initialises at zero height and
renders as a collapsed sliver. The popup renders in its own overlay and never
touches the hidden view.

## The insertion point

Each package view ends with the same block:

    <section class="section wash"><div class="wrap">
      <div class="endcta">
        <div><h2>Ready to book Basic?</h2><p>Tell us where you are…</p></div>
        <button class="btn-lg" type="button" data-quote="Basic">Get my quote</button>
      </div>
    </div></section>

`.endcta` is `display:flex; justify-content:space-between; gap:32px; flex-wrap:wrap`,
so a second button placed beside the existing one flows and wraps on its own. No
layout change is needed to fit it.

`.btn-lg` is `background:var(--blue); color:#0B1220; border-radius:999px`. The
site already pairs a blue fill with dark text, which is the same call we made on
the story frames. **Reuse `.btn-lg` — do not write a new button style.**

## The change

Three buttons and one script tag. Nothing else.

1. In each of the three `.endcta` blocks, add one sibling button after the
   existing Get my quote button, carrying its URL on a data attribute:

   | View | `data-calendly` |
   |---|---|
   | `basic` | `https://calendly.com/carolinaglossdetailing-support/standard-package` |
   | `pro` | `https://calendly.com/carolinaglossdetailing-support/gloss-package` |
   | `deluxe` | `https://calendly.com/carolinaglossdetailing-support/deluxe-package` |

2. Load Calendly once, at the end of `<body>`:

       <link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">
       <script src="https://assets.calendly.com/assets/external/widget.js" async></script>

3. Extend the **existing** delegated click handler in the inline script with one
   more branch, matching how `[data-home]`, `[data-nav]` and `[data-quote]`
   are already handled:

       var cal = e.target.closest('[data-calendly]');
       if (cal) {
         e.preventDefault();
         if (window.Calendly) Calendly.initPopupWidget({ url: cal.getAttribute('data-calendly') });
         return;
       }

   Guard on `window.Calendly` so a slow or blocked script cannot throw inside the
   shared handler and break `[data-home]`, `[data-nav]` and `[data-quote]` with it.

## What could break, and why it will not

| Risk | Why it is contained |
|---|---|
| Breaking the existing quote funnel | The new branch is added after the existing ones and returns early. `[data-quote]` is untouched. |
| Calendly script fails to load | The `window.Calendly` guard makes the button a no-op instead of throwing. Every other handler keeps working. |
| Collapsed calendar | Avoided entirely by using the popup rather than the inline embed. |
| Layout shift in `.endcta` | It is already a wrapping flex row. A second button is exactly what it is built for. |
| New CSS colliding with `site.css` | None is added. `.btn-lg` is reused as-is. |
| Breaking the router | The router is not touched. No new `data-view`, no new hash route. |

## Files touched

`index.html` only — three button elements, one link tag, one script tag, one
click branch. **Not touched:** `assets/site.css`, `assets/quote.js`, `server.js`,
`package.json`, `quote.html`, anything in `assets/`.

## Verify

- `npm start`, then walk `#/basic`, `#/pro`, `#/deluxe`
- click each new button: the correct event opens, showing the right deposit —
  $10 Standard, $15 Gloss, $20 Deluxe
- click Get my quote on each: still returns home and still prefills `service`
- click a nav link and the back arrow: routing still works
- reload directly on `#/deluxe`: the view opens and its button still works
- phone width: `.endcta` wraps, the overlay is usable, no sideways scroll
- block `assets.calendly.com` in devtools and confirm the rest of the page still
  behaves — this proves the guard
- `git diff` shows additions only, confined to `index.html`

## Two things to fix separately, not in this change

1. **The apex redirects to `http://www.`**, not https. Anyone typing the bare
   domain makes one unencrypted hop before being upgraded. It is a one-line host
   config change and does not belong in this diff.
2. **`server.js` hardcodes a Zapier catch hook** as its default value, so anyone
   with the repo can post junk leads into the automation. It should read the env
   var with no fallback.
