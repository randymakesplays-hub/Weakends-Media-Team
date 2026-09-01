# Weakends — Final Motion Production Prompt (video tier + VSL)

Paste this into a fresh Claude Code session to execute. Repo branch:
`claude/agency-websites-research-hq0zzw`. Base files: `website/motion/motion-lab.html`,
`website/motion/motion-specs.json`. Live lab artifact:
https://claude.ai/code/artifact/dc05f00e-a927-4f90-9873-7f4358e55605

Brand rules: "Weakends"/"Weakend" one word capital W, never split. No invented metrics,
no fake testimonials. CTA: "Book a performance trial".

STEP 0 — BUDGET GATE: estimate_only on every video generation; report total cost before
generating; 1 variation per clip.

## Part 1 — Panel video loops (16:9, 4–6s, loopable, no text, 720p, compressed)
1. HERO LOOP (Born Shipping site face + phone): slow cinematic dolly across flowing glass
   ribbons in sunset orange, magenta and electric blue over warm cream, soft studio light.
2. AD LOOP (Engine Room ad screen): dark premium podium scene, coral-orange and
   electric-blue light streaks sweeping slowly, glossy shapes drifting.
3. SESSION LOOP (One Take screen): Actor 1 at the mic mid-recording, cropped to the
   timeline strip, subtle talking motion.

## Part 2 — The cast (lock a reference portrait per actor with gemini-3-pro-image first;
reuse as reference in every clip for face consistency)
- ACTOR 1 "The Creator" — Black woman, early 20s, natural curls, gold hoops, rust-orange
  knit sweater. Creator desk, podcast mic in frame, warm ring light. Chest-up. Bright,
  fast, credible energy.
- ACTOR 2 "The Operator" — Latino man, late 30s, short dark hair, light stubble, navy
  overshirt over white tee. Service-business back office, morning light. Direct,
  no-nonsense energy.
- ACTOR 3 "The Veteran" — East Asian man, mid 50s, salt-and-pepper hair, thin glasses,
  pressed light-blue shirt. Established storefront office, warm evening light. Calm
  authority, zero hype.

## Part 3 — The VSL (~50s master 16:9 + 9:16 crop; burned captions; hard cuts)
- 0–4s HOOK — A1: "Your business has a Weakend. You already know which one."
- 4–12s AGITATE — A2: "Content you never post. Ads you never test. Follow-ups you never
  send. That's not a you problem — that's an operations problem."
- 12–20s NAME IT — A3: "Weakends is a media and AI agency for business owners. They find
  the weakest part of your operation — and take it over."
- 20–32s HOW — rapid cuts over panel-loop b-roll: A1 "Content, shipped daily." /
  A2 "Leads, on your calendar." / A3 "Systems that run while you sleep."
- 32–42s TRIAL — A2: "And you don't pay a retainer until the numbers prove it. That's the
  performance trial."
- 42–50s CTA — A1: "Fix your Weakends. Book the trial at weakendsagency.com." End card:
  WEAKENDS. wordmark + trial button.
- Switch rhythm: her → him → him → all three fast → him → her.
- Rules: actors are spokespeople in an ad, never framed as real clients; no personal
  result claims; tag AI-generated people where platforms require it.

## Part 4 — Integration
Embed loops into motion-lab.html (muted autoplay playsinline, current stills as poster
fallbacks); VSL as hero media on the prototype with play button; verify page weight +
mobile playback in Chromium; commit to branch.
