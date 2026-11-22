# Shorts editing review (23 Nov 2026)

**Measured:** durations 40.7–55.2 s. Integrated loudness: 018 **-18.8**, 032 **-21.3**, 036 **-23.0**, 029 **-24.3 LUFS** (target -14). True peak -0.6 to -0.9 dBTP. Scene holds: 036 has a 9.3 s scene, 032 10.6 s, 029 **11.4 s** on one static visual.

## Top 8 fixes (ranked by retention impact)

**1. Frame 0 is empty.** In every Short the first frame is background plus one caption. `render()` computes `st = t - (seg["start"] - 0.1)`, which is -0.05 s at t=0, so every `ease()` returns 0. That is the frame where viewers decide to swipe.
- In `render()`: after `st = ...` add `if si == 0: st += 0.6` (the opening visual is fully drawn on frame 0).
- In `build_audio()`: opening silence `int(0.15 * SR)` -> `int(0.05 * SR)`.
- Later scenes also start nearly invisible. Change the lead `- 0.1` to `- 0.25` in both the `si` loop and `st`, so the visual is already in when its first word lands.

**2. Loudness is 5–10 dB too quiet and inconsistent.** `build_audio()` normalises *peak* to 0.9, not loudness. YouTube turns loud videos down but never turns quiet ones up,, so 029 plays about 10 dB quiet. In the `render()` ffmpeg `cmd`, insert before `"-c:a"`:
`"-af", "loudnorm=I=-14:TP=-1.5:LRA=7", "-ar", "48000",`
A two-pass loudnorm, or `pyloudnorm` in `build_audio()`, is more accurate. Target -14 LUFS, true peak ≤ -1.5 dBTP.

**3. Captions spell numbers as words.** On screen you see "NINETY-NINE", "IN TWO THOUSAND,", "THREE HUNDRED / DOLLARS A MONTH", "MADE SIXTY-THREE". The `say` text has to stay in words for Kokoro, but captions should show digits: they are faster to read and are the hook of a money video.
- Add an optional per-scene `"cap_subs": [["three hundred dollars", "$300"], ["ninety-nine percent", "99%"]]`.
- Add a helper `apply_subs(wts, subs)` that merges the matched word tuples into one `(display, start_of_first, end_of_last)`. Call it in `render()` between `align_words()` and `chunk_words()`.
- `tools/voice_check.py` is unaffected.

**4. The ending kills replays.** Every Short ends with the same spoken "Follow for one money lesson every day." (2.2 s), a green button, 0.8 s of padding and a music fade. It then loops back to an empty frame.
- Drop the spoken follow line. Keep "Follow" only as the on-screen `sub` pill.
- Write the last line so it runs into the first line (for 029: "...and it started with one fifty-million-dollar 'no'." The loop restarts on "$50M").
- Make the final visual match the opening visual.
- In `build_audio()`, end padding `0.8` -> `0.25` and remove the `fade` on music.

**5. Static holds of 7–11 s.** At about 1 visual change per 5.5 s, and with nothing moving after the 0.5 s entrance, viewers drop off mid-scene.
- Rule: **no visual held longer than about 4 s.** Split long `say` lines into two scenes.
- Add an assert in each spec (or `preview.py`): `len(sc["say"].split()) <= 14`.
- Add slow motion during holds. In `render()`, scale the `vis` layer from 1.00 to 1.04 over the scene (`vis.resize` around (CX, 840), then crop) before `alpha_composite`.

**6. Too long for the format.** 40–55 s at `speed` 1.05 with 0.22 s gaps. For finance explainers, completion and replay rate are best at **30–40 s (about 85–100 words)**.
- Cut the generic CTA (fix 4) and merge caveat lines into on-screen text where the rules allow. The spoken caveat in 018 scene 4 can be shortened to "Assumed seven percent; real returns vary." and the on-screen disclaimer is kept.
- `spec.get("gap", 0.22)` -> `0.12`. Try `speed` 1.10 and confirm with `voice_check.py`.

**7. Hooks start with setup, not the payoff.** "Two friends invest...", "In two thousand, Netflix's founders say...", "Instagram is free. Yet..." all spend 2–3 s before the stakes. Open on the biggest number or a contradiction, and show it on frame 0 (rewrites below).

**8. Polish.**
- (a) Music is the same 84 bpm Am-F-C-G loop on every Short, a repetition risk. In `make_music()`, seed `bpm` (76–96) and the chord set from `hash(spec["id"])`.
- (b) The disclaimer line (`draw_chrome`, 26 px, `dim`) can't be read on a phone. Use `font(30, "Medium", False)` and `col("muted")`.
- (c) Captions: `CAP_Y` 1430 -> 1340 nearer the visual, clear of the title overlay. Caption font 74 -> 80.
- (d) Remove the progress bar (`render()`, "progress bar" line). It sits under YouTube's own scrubber and announces the end, which works against looping.
- (e) In `v_bars`/`v_compare`, the count-up format jumps ("$88,274" next to "$134K") because `fmt_usd` switches at 1e5. Format the animated value with the final value's unit.

## Rewritten hooks (numbers must be asserted in the spec)

**018_start_early_us**
- Now: "Two friends invest the same three hundred dollars a month. One ends up with more than double."
- New: "Same three hundred dollars a month. Same returns. One friend ends up with over four hundred thousand dollars more, because of one decision."
- Frame 0: the `compare` card ($792K vs $368K), not the M/J circles.

**029_netflix_blockbuster**
- Now: "In two thousand, Netflix's founders say they offered to sell their company to Blockbuster for fifty million dollars. Blockbuster said no."
- New: "Blockbuster said no to buying Netflix for fifty million dollars. Today, Netflix brings in that much in under ten hours."
- Add `assert OFFER_PRICE / (NFLX_REV_2025 / 8760) < 10` (it is 9.7). Keep "the founders say" in scene 2.
- Loop line at the end: "...all from one fifty-million-dollar 'no'."

**036_free_apps**
- Now: "Instagram is free. Yet in just three months, its owner Meta made sixty-three billion dollars from ads."
- New: "Meta makes about six hundred and eighty-five million dollars a day from apps you've never paid a cent for. Here's how."
- Frame 0: "$685M / day". Say Meta, not Instagram alone: the $63.1B is ad revenue across all of Meta's apps.
- Loop line at the end: "...you pay with your time. That's how Meta makes..." (the loop restarts on the number).
