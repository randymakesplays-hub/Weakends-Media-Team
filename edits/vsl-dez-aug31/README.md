# VSL cleanup — Dez / e-com essentials (Aug 31 recording)

Source: `Video-Aug-31-2026-11-44-00-PM.mov` — 33:30.06, 1920x1080, ~60 fps (variable), HEVC 10-bit HLG (iPhone), stereo AAC.

## What this is
The recording is a take-by-take read: almost every line was attempted 2-6 times, with the
usable take normally last. This pass keeps the best/last complete take of each line and
removes false starts, restarts, stumbles, self-corrections and dead air.

| | |
|---|---|
| Original runtime | 33:30 |
| Kept | 12:06.2 (87 clips) |
| Removed | 21:23.8 (88 cuts) |

## Files
- `vsl-roughcut.fcpxml` — import into Premiere / Resolve to rebuild this cut against the original file (relink to the .mov).
- `cuts-to-remove.csv` — every removed range (source timecode).
- `keeps.csv` — every kept take, with its transcript line.
- `clean-script.txt` — the kept takes in order, as a script/VO reference.
- `transcript-full.txt` — full timed transcript of the raw recording.

## Notes before you fine-cut
- The source is **variable frame rate** (iPhone). The XML is built on a 60 fps timeline; conform/transcode the .mov to CFR 59.94 or 60 before finishing if you see drift.
- Footage is **HLG / Rec.2020 10-bit**. The review MP4 is tone-mapped to Rec.709; the XML points at the untouched original.
- Cuts are placed inside the pause before/after each take (~0.3s handle in, ~0.45s out), so there is room for L-cuts and cross-dissolves.
- A handful of surviving takes still have a small stumble inside them (flagged below); they were the only version of that line, so they were kept rather than deleted.

## Lines that still need a manual decision

- **0:01:48.870** — take opens on \"and I'm so short\" (misspeak) before the good read — trim the head
- **0:08:33.780** — opens on the word 'little' left over from the previous attempt
- **0:30:34.440** — only take of this line; trails off on 'that's exactly what we help'
- **0:31:11.860** — 'build a business on term' — misspeak, no clean alternate take
- **0:32:58.220** — 'to be cook' — misspeak at head of an otherwise usable take

## Removed ranges (source timecode)

| # | In | Out | Length |
|---|---|---|---|
| 1 | 0:00:00.000 | 0:00:36.428 | 36.4s |
| 2 | 0:00:43.030 | 0:00:52.487 | 9.5s |
| 3 | 0:01:03.920 | 0:01:24.400 | 20.5s |
| 4 | 0:01:35.861 | 0:01:48.870 | 13.0s |
| 5 | 0:02:11.413 | 0:02:23.523 | 12.1s |
| 6 | 0:02:31.850 | 0:02:36.372 | 4.5s |
| 7 | 0:02:41.670 | 0:03:21.586 | 39.9s |
| 8 | 0:03:30.520 | 0:03:39.524 | 9.0s |
| 9 | 0:03:44.974 | 0:03:54.854 | 9.9s |
| 10 | 0:04:12.730 | 0:04:25.689 | 13.0s |
| 11 | 0:04:32.400 | 0:04:43.030 | 10.6s |
| 12 | 0:04:51.003 | 0:05:32.260 | 41.3s |
| 13 | 0:05:41.380 | 0:05:51.656 | 10.3s |
| 14 | 0:06:00.230 | 0:06:10.200 | 10.0s |
| 15 | 0:06:18.320 | 0:06:45.690 | 27.4s |
| 16 | 0:07:03.050 | 0:08:05.453 | 62.4s |
| 17 | 0:08:16.508 | 0:08:23.389 | 6.9s |
| 18 | 0:08:32.300 | 0:08:33.780 | 1.5s |
| 19 | 0:08:48.950 | 0:08:50.675 | 1.7s |
| 20 | 0:08:57.730 | 0:09:32.490 | 34.8s |
| 21 | 0:09:48.530 | 0:09:49.175 | 0.6s |
| 22 | 0:09:58.360 | 0:10:03.293 | 4.9s |
| 23 | 0:10:10.210 | 0:10:31.111 | 20.9s |
| 24 | 0:10:37.484 | 0:10:41.647 | 4.2s |
| 25 | 0:10:53.650 | 0:10:58.010 | 4.4s |
| 26 | 0:11:05.090 | 0:11:33.320 | 28.2s |
| 27 | 0:11:39.874 | 0:11:51.870 | 12.0s |
| 28 | 0:11:56.270 | 0:12:05.000 | 8.7s |
| 29 | 0:12:13.130 | 0:12:20.480 | 7.4s |
| 30 | 0:12:30.200 | 0:12:41.229 | 11.0s |
| 31 | 0:12:48.400 | 0:12:54.446 | 6.0s |
| 32 | 0:12:57.564 | 0:13:37.200 | 39.6s |
| 33 | 0:13:47.880 | 0:13:56.912 | 9.0s |
| 34 | 0:14:03.150 | 0:14:12.861 | 9.7s |
| 35 | 0:14:18.533 | 0:14:19.698 | 1.2s |
| 36 | 0:14:27.227 | 0:14:43.888 | 16.7s |
| 37 | 0:14:49.220 | 0:15:07.964 | 18.7s |
| 38 | 0:15:19.257 | 0:15:24.635 | 5.4s |
| 39 | 0:15:32.802 | 0:15:36.563 | 3.8s |
| 40 | 0:15:42.980 | 0:15:47.344 | 4.4s |
| 41 | 0:15:53.902 | 0:16:11.790 | 17.9s |
| 42 | 0:16:19.386 | 0:16:31.600 | 12.2s |
| 43 | 0:16:35.040 | 0:16:45.973 | 10.9s |
| 44 | 0:16:52.220 | 0:17:02.930 | 10.7s |
| 45 | 0:17:12.819 | 0:17:20.310 | 7.5s |
| 46 | 0:17:33.181 | 0:17:40.930 | 7.7s |
| 47 | 0:17:48.250 | 0:17:49.719 | 1.5s |
| 48 | 0:18:05.180 | 0:18:41.806 | 36.6s |
| 49 | 0:18:58.930 | 0:19:03.099 | 4.2s |
| 50 | 0:19:14.931 | 0:19:30.354 | 15.4s |
| 51 | 0:19:37.360 | 0:20:22.430 | 45.1s |
| 52 | 0:20:32.640 | 0:20:36.460 | 3.8s |
| 53 | 0:20:41.732 | 0:20:54.192 | 12.5s |
| 54 | 0:21:04.668 | 0:21:13.087 | 8.4s |
| 55 | 0:21:27.747 | 0:21:49.021 | 21.3s |
| 56 | 0:21:51.942 | 0:22:10.590 | 18.6s |
| 57 | 0:22:15.209 | 0:22:50.990 | 35.8s |
| 58 | 0:23:03.653 | 0:23:09.063 | 5.4s |
| 59 | 0:23:17.310 | 0:23:19.910 | 2.6s |
| 60 | 0:23:26.190 | 0:23:31.941 | 5.8s |
| 61 | 0:23:41.000 | 0:24:19.422 | 38.4s |
| 62 | 0:24:29.080 | 0:24:36.921 | 7.8s |
| 63 | 0:24:44.510 | 0:25:01.993 | 17.5s |
| 64 | 0:25:07.210 | 0:25:28.230 | 21.0s |
| 65 | 0:25:36.300 | 0:25:53.540 | 17.2s |
| 66 | 0:25:57.049 | 0:26:06.015 | 9.0s |
| 67 | 0:26:13.481 | 0:26:20.016 | 6.5s |
| 68 | 0:26:23.860 | 0:26:47.176 | 23.3s |
| 69 | 0:26:52.869 | 0:27:17.848 | 25.0s |
| 70 | 0:27:23.867 | 0:27:36.022 | 12.2s |
| 71 | 0:27:47.129 | 0:28:04.680 | 17.6s |
| 72 | 0:28:09.812 | 0:28:15.188 | 5.4s |
| 73 | 0:28:28.602 | 0:28:42.332 | 13.7s |
| 74 | 0:28:47.624 | 0:28:53.427 | 5.8s |
| 75 | 0:28:59.800 | 0:29:18.397 | 18.6s |
| 76 | 0:29:22.989 | 0:29:33.017 | 10.0s |
| 77 | 0:29:42.174 | 0:30:10.850 | 28.7s |
| 78 | 0:30:17.910 | 0:30:21.890 | 4.0s |
| 79 | 0:30:31.910 | 0:30:34.440 | 2.5s |
| 80 | 0:30:39.240 | 0:30:57.217 | 18.0s |
| 81 | 0:31:04.960 | 0:31:11.860 | 6.9s |
| 82 | 0:31:16.080 | 0:31:33.867 | 17.8s |
| 83 | 0:31:42.313 | 0:32:05.975 | 23.7s |
| 84 | 0:32:11.677 | 0:32:26.067 | 14.4s |
| 85 | 0:32:33.024 | 0:32:47.700 | 14.7s |
| 86 | 0:32:50.520 | 0:32:58.220 | 7.7s |
| 87 | 0:33:04.960 | 0:33:24.587 | 19.6s |
| 88 | 0:33:28.440 | 0:33:30.060 | 1.6s |

## Kept takes

| # | In | Out | Line |
|---|---|---|---|
| 1 | 0:00:36.428 | 0:00:43.030 | My name is Dez and I run a multi six figure e -commerce business out of my storage unit and my entire marketing team |
| 2 | 0:00:52.487 | 0:01:03.920 | two years ago I was stuck at zero guessing spending money on things that I thought will work just like everybody else an |
| 3 | 0:01:24.400 | 0:01:35.861 | you probably tried this yourself you probably tried to make a couple products You probably tried to make a website and y |
| 4 | 0:01:48.870 | 0:02:11.413 | and I'm so short And I'm for sure that at some point in that journey that you probably start to ask yourself Is this for |
| 5 | 0:02:23.523 | 0:02:31.850 | because I made every single one of those mistakes the most slowest and expensive way possible because I was doing it alo |
| 6 | 0:02:36.372 | 0:02:41.670 | I spent so much time and money and it's all down to drain because I didn't know what I was doing. |
| 7 | 0:03:21.586 | 0:03:30.520 | My name is Dez I'm 20 years old and I run a brand called Cribit Centrals at my storage unit and just this year alone we' |
| 8 | 0:03:39.524 | 0:03:44.974 | We also have multiple products that brought us tens of thousands of dollars just by themselves. |
| 9 | 0:03:54.854 | 0:04:12.730 | In the one part that people never believe me when I say is that I'm using AI to actually help me run and the one part th |
| 10 | 0:04:25.689 | 0:04:32.400 | the biggest reason to my success right now and none of this would be possible without AI. |
| 11 | 0:04:43.030 | 0:04:51.003 | I used to waste so much time recording content that just end up never converting. And it's just like I was wasting so mu |
| 12 | 0:05:32.260 | 0:05:41.380 | And matter of fact, that same content that used to take me hours if not days to create takes me seconds to create now us |
| 13 | 0:05:51.656 | 0:06:00.230 | And on top of not just marketing, there's a lot of AI systems that I'm using right now to actually be able to help me sc |
| 14 | 0:06:10.200 | 0:06:18.320 | keep in mind I'm only one person I don't have a big team around me helping me it's just me and some simple AI systems he |
| 15 | 0:06:45.690 | 0:07:03.050 | the thing that kept me stuck for those two years while I wasn't getting any results is I was stuck trying to find anothe |
| 16 | 0:08:05.453 | 0:08:16.508 | Even when I started to get a couple sales here and there for my business, I was never able to actually get to that next  |
| 17 | 0:08:23.389 | 0:08:32.300 | And the part is it wasn't even my fault. There's actually a lot of people out here right now giving a lot of different i |
| 18 | 0:08:33.780 | 0:08:48.950 | little, and the fact is that it wasn't even my fault. There's a lot of people out here giving e -commerce game and knowl |
| 19 | 0:08:50.675 | 0:08:57.730 | nobody's teaching you the proper systems to actually be placed inside your business so that you can actually take someth |
| 20 | 0:09:32.490 | 0:09:48.530 | And the thing is it wasn't even my fault. There's a lot of people out here giving a lot of information and knowledge abo |
| 21 | 0:09:49.175 | 0:09:58.360 | They're only giving you, people are only giving you pieces of the puzzle, people are only giving you pieces of the puzzl |
| 22 | 0:10:03.293 | 0:10:10.210 | And there's so much contradicting information that you probably don't know where to start, or maybe you already started  |
| 23 | 0:10:31.111 | 0:10:37.484 | And that's the very thing that's causing you to miss out on this opportunity right now. |
| 24 | 0:10:41.647 | 0:10:53.650 | AI is becoming more and more popular and it's only so long before everybody starts to hop on this trend on how people ar |
| 25 | 0:10:58.010 | 0:11:05.090 | even in the past the barrier to entry to get into e -commerce or drop shipping was so small it was basically free |
| 26 | 0:11:33.320 | 0:11:39.874 | and now in 2026 going into 2027 AI has made that even easier |
| 27 | 0:11:51.870 | 0:11:56.270 | what you're missing is the proper information and the proper AI systems |
| 28 | 0:12:05.000 | 0:12:13.130 | and that is the difference between what me and that's the difference between what had me stuck at two years not having a |
| 29 | 0:12:20.480 | 0:12:30.200 | and that same thing is what had me stuck at two years not having any results versus me now being able to grow my busines |
| 30 | 0:12:41.229 | 0:12:48.400 | And that's the difference from, and that's exactly the difference from me being stuck for two years not having any resul |
| 31 | 0:12:54.446 | 0:12:57.564 | And that's the same thing that kept me stuck for two years. |
| 32 | 0:13:37.200 | 0:13:47.880 | that is the exact difference that kept me stuck for a couple of years not having any results to me now being able to wal |
| 33 | 0:13:56.912 | 0:14:03.150 | and there is four mechanism and there's only four mechanisms that build a real brand |
| 34 | 0:14:12.861 | 0:14:18.533 | first you have the offer and this is the perceive value that the customer has while they're viewing your product. |
| 35 | 0:14:19.698 | 0:14:27.227 | How much value do they think? How much value does the customer sees while they're viewing your product? |
| 36 | 0:14:43.888 | 0:14:49.220 | then you have your storefront on your website. This is what's gonna actually be converting people into sales. |
| 37 | 0:15:07.964 | 0:15:19.257 | think about your website like an actual store when people come into a store everything that they see what are in those f |
| 38 | 0:15:24.635 | 0:15:32.802 | then you have the engine this is what's actually driving the sales this is your content and this is your marketing and w |
| 39 | 0:15:36.563 | 0:15:42.980 | this is one of the key parts that I was able to use AI to help me market my brand and get more sales |
| 40 | 0:15:47.344 | 0:15:53.902 | because your content and your marketing is what's actually getting people to be aware of your product |
| 41 | 0:16:11.790 | 0:16:19.386 | this is one of the key things that allowed me to have the success that I have now because AI made marketing my brand ten |
| 42 | 0:16:31.600 | 0:16:35.040 | I don't have to send my products to influencers and they end up ghosting |
| 43 | 0:16:45.973 | 0:16:52.220 | I'm doing all of this from behind my computer. |
| 44 | 0:17:02.930 | 0:17:12.819 | the last part is the operations in another very important one This is your fulfillment your manufacturers your customer  |
| 45 | 0:17:20.310 | 0:17:33.181 | lastly you have your operations. This is your manufacturer. This is your fulfillment. This is your customer service This |
| 46 | 0:17:40.930 | 0:17:48.250 | you have the operations This is your inventory, your cash flow, your fulfillment, your customer service, your manufactur |
| 47 | 0:17:49.719 | 0:18:05.180 | And last you have your operations. This is the fulfillment, your cash flow, finances, manufacturer, suppliers, your cust |
| 48 | 0:18:41.806 | 0:18:58.930 | Most people trying to teach ecommerce right now are showing you some fake results about a store that they never had, or  |
| 49 | 0:19:03.099 | 0:19:14.931 | A lot of these people are coming results that they actually never even had and what makes me different is that I'm actua |
| 50 | 0:19:30.354 | 0:19:37.360 | I'm currently in my storage unit right now as I see I got a lot of orders behind me and these are not fake orders I just |
| 51 | 0:20:22.430 | 0:20:32.640 | I'm gonna be so honest with you guys there's a lot of things in my business that I'm still automating and growing but as |
| 52 | 0:20:36.460 | 0:20:41.732 | is because I'm building something long -term, not something that's going to die out in a couple of months. |
| 53 | 0:20:54.192 | 0:21:04.668 | And if you work with me, this is something that you're going to actively be watching me as I grow, and you're going to b |
| 54 | 0:21:13.087 | 0:21:27.747 | Because let's be honest, you don't just learn from a course, you learn from somebody who's doing this in real time. And  |
| 55 | 0:21:49.021 | 0:21:51.942 | what I'm calling this is ecom essentials |
| 56 | 0:22:10.590 | 0:22:15.209 | is where you get direct access to me and my private channel and all of my knowledge. |
| 57 | 0:22:50.990 | 0:23:03.653 | this is where we come into your business and actually help you scale. We look at what's working, what's not working, you |
| 58 | 0:23:09.063 | 0:23:17.310 | We're helping with your website, your funnels, your offers, everything. We're helping you with everything from your webs |
| 59 | 0:23:19.910 | 0:23:26.190 | we're working with you help you optimize your website, increase your conversion rate, your funnels, your offers, your ad |
| 60 | 0:23:31.941 | 0:23:41.000 | You'll also have a community for like -minded people who you could connect with. You also have a community for like -min |
| 61 | 0:24:19.422 | 0:24:29.080 | You also have direct access to the key modules we have packed with information going over the four pillars that you need |
| 62 | 0:24:36.921 | 0:24:44.510 | But most importantly, this is where you're getting direct access to the AI systems that I'm using right now to help me s |
| 63 | 0:25:01.993 | 0:25:07.210 | And also the prompts that I'm using from my images and my videos that's, |
| 64 | 0:25:28.230 | 0:25:36.300 | you'll also get access to the exact prompts that I'm using to create images and videos that's helping me market my brand |
| 65 | 0:25:53.540 | 0:25:57.049 | and I'm gonna let you in on a little secret. These E |
| 66 | 0:26:06.015 | 0:26:13.481 | I'm I'll let you in on a little secret. These AI ads that I'm using right now are so exclusive that I cannot just give t |
| 67 | 0:26:20.016 | 0:26:23.860 | That's why I'm giving you access to them into my private group, e -com essentials. |
| 68 | 0:26:47.176 | 0:26:52.869 | And these are things that other people couldn't give you access to because I'm the only one who's doing it right now. |
| 69 | 0:27:17.848 | 0:27:23.867 | You'll also get access to the live calls that we'll be having weekly to go over all of these things that we have mention |
| 70 | 0:27:36.022 | 0:27:47.129 | And a couple quick answers to some questions that you might be having one is oh I don't want to show my face what AI has |
| 71 | 0:28:04.680 | 0:28:09.812 | helped solve that problem for me and that's the first thing that we're going to be helping you get set up |
| 72 | 0:28:15.188 | 0:28:28.602 | you may be thinking oh e -commerce is saturated well the truth is e -commerce itself isn't saturated and it's something  |
| 73 | 0:28:42.332 | 0:28:47.624 | It's saturated with people guessing, don't know what they're doing and just trying to make quick money. |
| 74 | 0:28:53.427 | 0:28:59.800 | What is not saturated with people who are actually running and operating a real business. |
| 75 | 0:29:18.397 | 0:29:22.989 | or you may be thinking, Dez, I tried this already and I feel, what's gonna be different? |
| 76 | 0:29:33.017 | 0:29:42.174 | And to be honest, that's one of the best things because that means that you already tried, you failed, and you already p |
| 77 | 0:30:10.850 | 0:30:17.910 | most people never even start. They never even get a product. They never do any research. They're just stuck consuming in |
| 78 | 0:30:21.890 | 0:30:31.910 | the truth is you don't need to start over. You just need the proper knowledge, the proper information and the proper sys |
| 79 | 0:30:34.440 | 0:30:39.240 | that's exact and it's in an ecom essentials that's exactly what we help |
| 80 | 0:30:57.217 | 0:31:04.960 | and I'm gonna be I'm gonna be so honest if you're looking for a store by tomorrow and 10 grand by the next two weeks I a |
| 81 | 0:31:11.860 | 0:31:16.080 | but if you're trying to build a business on term that's exactly what we help |
| 82 | 0:31:33.867 | 0:31:42.313 | ecom essentials this is a one -on -one program where we work closely with you one -on -one. This is not something where  |
| 83 | 0:32:05.975 | 0:32:11.677 | We're looking for people who are ready to put into work, take action and build a business long -term. |
| 84 | 0:32:26.067 | 0:32:33.024 | I'm still I'm making multiple six figures running my brand out of my storage unit So you don't need a lot to start |
| 85 | 0:32:47.700 | 0:32:50.520 | don't need a big 5 ,000 square foot warehouse |
| 86 | 0:32:58.220 | 0:33:04.960 | to be cook to be completely honest now with AI and with the right system You don't even need to hold any inventory |
| 87 | 0:33:24.587 | 0:33:28.440 | I only take a couple calls a week because I'm not trying to work with everybody. |
