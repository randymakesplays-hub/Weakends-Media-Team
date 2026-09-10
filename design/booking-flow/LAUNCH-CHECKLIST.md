# Launch checklist

Ordered. Each step says who does it, where, and how you know it worked.

---

## Blocking — do these before anyone can book

### 1. Confirm the Calendly event timezone · you, in Calendly · 2 min
Open each of the three event types and check the **availability timezone is
Eastern**. Your laptop is reading as Arizona time, and if the host schedule was
set from it, your 8am–6pm is being offered as 11am–9pm Charlotte time.

Do this first. It is the cheapest check here and the only one that can silently
book customers at the wrong hour.

*Done when:* all three event types show Eastern on the availability tab.

### 2. Rename the site to Standard and Gloss · other Claude session · small
Calendly and Instagram already say Standard / Gloss / Deluxe. The website is the
only surface still saying Basic / Pro Clean. Someone clicking "Book Basic" and
landing on a payment page headed "Standard" will hesitate at the worst moment.

Touches copy **and** routing, so it is not purely additive — keep it as its own
commit, before the booking work:

| Where | From | To |
|---|---|---|
| Hash route + `data-view` | `basic`, `pro` | `standard`, `gloss` |
| `data-quote` | `Basic`, `Pro Clean` | `Standard`, `Gloss` |
| Card headings, hero, endcta headings | Basic, Pro Clean | Standard, Gloss |
| "Everything in Basic" inside Gloss and Deluxe | Basic | Standard |

*Done when:* the site says Standard / Gloss / Deluxe everywhere, all three
package views still open, and the quote form still prefills the right service.

### 3. Add the booking buttons and swap the CTA · other Claude session · small
Per `IMPLEMENTATION-PLAN.md`. Three buttons, one script tag, one branch on the
existing click handler, guarded on `window.Calendly`.

In each `.endcta`, replace the Get my quote button with the booking button and
move the quote path into the paragraph as a `.linkish` text button, keeping its
existing `data-quote` behaviour:

> **Ready to book Gloss?**
> Pick a time that works. $15 holds the slot and comes off your total, and we
> confirm your exact price against your vehicle before we start. *Or get a price first*
>
> **[ Book Gloss · $15 deposit ]**

Deposits: Standard $10, Gloss $15, Deluxe $20.

One CSS line needed — `.endcta .linkish{color:var(--blue)}`. The default
`--blue-ink` sits at 3.47:1 on the navy block and washes out; `--blue` is 9.15:1.

*Done when:* each button opens the matching event at the right deposit, the quote
link still prefills, nav and back still work, and blocking `assets.calendly.com`
in devtools leaves the rest of the page working.

### 4. Move the Zapier hook to an env var · other Claude session · 1 line
`server.js` line 7 hardcodes the catch hook as its default, so anyone with repo
access can post junk leads into the automation. Read from the env var with no
fallback, and set the real value in Railway.

*Done when:* the default is gone from source and a real quote submission still
arrives in Zapier.

---

## Not blocking — worth doing soon after

### 5. Apex redirects over http
`carolinaglossdetailing.com` 301s to `http://www.…`, so anyone typing the bare
domain makes one unencrypted hop before being upgraded. Host config, one line.

### 6. Post the three package statics · you, Instagram
`design/story-highlights/out/` — Standard, Gloss, Deluxe. Names already match
Calendly.

### 7. Upload the six highlight covers · you, Instagram
`design/story-highlights/out/covers/` — Services, Location, Reviews,
Before/After, Book, FAQ. Upload each as a story, set as the highlight cover, type
the title in Instagram.

### 8. Publish the service-detail slides · you, Instagram
`design/story-highlights/out/details/` — eight slides into the Services highlight.

---

## Decide when you have the first few bookings

- Whether the deposit is refundable, and what the cancellation window is
- How far ahead someone can book
- What each vehicle size step adds on top of the starting price
- Whether $10 is enough to deter a no-show, or whether a flat $25–50 works better
