# Brand & visual review (23 Nov 2026)

Scope: branding_v4/, six long thumbnails (output/L0*_thumb.png), frames from six Shorts and three long videos, render.py / render_long.py. The flat navy/green/gold style is clean and consistent, so these are refinements, not a redesign. Logo gold (250,204,21) and navy (11,18,32) match `COLORS["gold"]`/`bg0` exactly. Good.

## Top 8 recommendations (ranked)

**1. Fix the thumbnail tag: unreadable and off-brand.** White text on the red pill measures **2.5:1 contrast** (fails WCAG), and at 360 px mobile width the 48 px tag shrinks to about 13 px. Red also signals "loss" on every video, even on "NETFLIX VS BLOCKBUSTER". In `render_long.make_thumb`: change `fill=col("red")` to `col(th.get("tag_color", "green"))` and the text to `col("bg0")` (navy on green is about 8:1). Set `f = font(56, "Black")` and the pill to y 590–690 with radius 50. Keep red only for stories that really are about a loss.

**2. Break the one-template look.** At small size all six thumbnails read as one repeating video: a gold number, a white line and a pink pill. Add `th["layout"]` to `make_thumb` and rotate the layouts across the week:
- `"number"`: the current layout.
- `"versus"`: two values at x=340 and x=940, `font(170,"Black")`, left `red` and right `green`, with "VS" between them in `col("muted")` at `font(64,"Black")`. Line text at y=560. Example: Netflix "$50M" vs "$45B".
- `"left"`: the number left-aligned (`anchor="lm"`, x=70, y=280, `font(230)`) and the line at x=70, y=480. In the right third, draw 4 rising (green) or falling (red) rounded bars, x 900–1220, heights 120/200/290/400, bottom at y=640. This reuses the banner's "rising bars" motif.
Also let `th["color"]` be `green` or `red` more often. Gold every time flattens the set.

**3. Auto-fit thumbnail text.** "THE DEAL THEY REJECTED" fills about 1,250 of 1,280 px, so it is nearly touching the edges. In `make_thumb`, shrink the font until it fits: `s=92; while font(s,"Black").getlength(th["line"])>1100: s-=4`. Do the same for `big` with a 1,150 px limit and a 300 px start. A short number then gets bigger, which helps the 168 px search size, where only the number is readable now.

**4. Keep Shorts content clear of the right-hand buttons.** Measured frames have content reaching **x ≈ 940–965 at y 1000–1250**: "$42,963 paid" (031), "of large-cap funds trailed the S&P 500" (020), "= years to 2×" (015) and "petrol pump, clerk" (038). The like/comment buttons cover that area. In `render.py`:
- Composite visuals at `(-30, VIS_SHIFT)` instead of `(0, VIS_SHIFT)` in `render()` and `preview_frame()`.
- Add `def text_fit(d, xy, s, f, fill, max_w=820, **kw)`, which steps the font size down 4 px at a time while `getlength > max_w`. Use it for values in `v_stat`, `v_equation` and `v_pair` labels/subs.
- In `v_pair`, use `x = CX ± 200` instead of ±215.

**5. Make the disclaimers readable.** They carry the "not financial advice" protection, but the `dim` colour (71,85,105) on navy is **2.45:1** at 24–26 px. They can't be read on a phone.
- Shorts, `draw_chrome`: `font(30,"Medium",False)`, `col("muted")` (7.2:1), and wrap to two lines when the width is over 860 px. The 015 disclaimer is currently about 1,000 px wide.
- Long videos, `render()`: `font(28,"Medium",False)`, `col("muted", 0.9)`.

**6. Raise the Shorts captions and drop the duplicate progress bar.** Captions at `CAP_Y = 1430` (74 px, stroke 8) end at about y 1470. That sits right on the edge of YouTube's title/channel block, which grows upward when a title wraps to two lines. Set `CAP_Y = 1370`. Visuals end at about 1230, so there is room. Remove the 10 px green progress bar at `H-10` in `render.py`. YouTube draws its own bar over that strip, and ours just adds clutter. In long videos keep it, but at 4 px.

**7. Show the coin logo inside the content.** The new coin appears nowhere in the videos.
- In `v_cta` (both renderers), draw a simple coin above the lines: `ellipse` r=70 in `gold` with a navy `$` (`font(90,"Black")`, `col("bg0")`). On Shorts put it at (CX-30, 560). This makes the brand mark the last image people see.
- Owner, one-time step: upload `branding_v4/watermark_150.png` in Studio → Customization → Branding → Video watermark, "End of video".
- Long-video badge: draw it as the same green outline pill used on Shorts. Right now it is plain green text (`render_long.render`, y=70).

**8. Fix colour meanings and retire the letter-in-circle avatars.** Use this rule everywhere:
- `green` = growth/good choice
- `red` = cost/loss
- `gold` = the one key number or word
- `muted`/`blue` = neutral comparison

The `v_pair` initials ("I"/"A" for India/Aden, "N"/"B") look like placeholder avatars and are the most dated element. In `v_pair`, if `side` has `"value"` (for example "1949" or "$40"), draw it at `font(96,"Black")` in place of `side["label"][0]`. Drop the circle `fill` and keep the outline only. Never imitate company logos or their brand colours, for trademark safety.

## Shorts safe zones (1080×1920, approximate, varies by phone)
- **Top 0–200 px:** search, camera and menu icons. The badge at y 225–285 is fine.
- **Right x 950–1080, y ≈ 1000–1700:** like, dislike, comment, share, remix and sound buttons. Keep text and values at **x ≤ 920** in this band.
- **Bottom y ≈ 1520–1920:** channel name, subscribe, title (1–2 lines), sound ticker and nav bar. It can reach about y 1480 when the title wraps.
- **Left:** keep a 60 px margin.
- **Always visible box: x 60–920, y 220–1480.** Hook numbers belong in x 90–900, y 300–1400.
- Add this box as a red outline to `pipeline/preview.py`, so every contact sheet flags anything that crosses it.

## What already works (keep)
- Two-colour coin: it reads even at 24 px avatar size.
- Banner text sits inside the 1546×423 safe area.
- Long-video layouts: wide spacing and readable 52 px captions.
- Word-highlight captions with a black stroke: readable on every background tested.
- Green outline pill badge on Shorts.
- One font family (Inter) everywhere.

Minor: `channel_page_preview.png` writes the handle as "@PennytoBillion". The real handle is @PennyToBillion. Cosmetic only.
