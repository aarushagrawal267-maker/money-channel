"""Video 042 (global/US): Kodak built a digital camera in 1975, then lost the digital era. Pillar: Case Studies."""
import json, os

# ---------------------------------------------------------------- sourced facts
# IEEE Spectrum, "The First Digital Camera" history piece (Joanna Goodrich, The Institute, Apr 6, 2022): Kodak
# engineer Steven Sasson built the prototype in Rochester in 1975, first photo December 1975; 100 x 100 pixels,
# black and white; 3.6 kg, about the size of a toaster; "It only took 50 milliseconds to capture the image, but it
# took 23 seconds to record it to the tape"; executives saw no market, so it never went into production; US patent
# 1978.
PROTO_YEAR = 1975
PROTO_PIXELS = 100 * 100
PROTO_KG = 3.6
SAVE_SECONDS = 23
LB_PER_KG = 2.20462
# Eastman Kodak Form 10-K for 1996 (SEC EDGAR, filed Mar 14, 1997), consolidated statement of earnings
# ($ millions): Sales 15,968; Cost of goods sold 8,326; net earnings 1,288.
SALES_1996, COGS_1996 = 15_968e6, 8_326e6
# AP via NBC News (Feb 9, 2006), citing IDC: Kodak No. 1 in the US digital-camera market for the second straight
# year in 2005, with a 24.9% share (up from 21% in 2004); digital sales passed film-based sales for the first time
# in 2005. Kodak's own 10-K for 2005 confirms "digital revenues ... exceeded traditional revenues" in 2005.
US_SHARE_2005 = 24.9
TOP_SELLER_YEAR = 2005
# Eastman Kodak Form 10-K for 2011 (SEC EDGAR, filed Feb 29, 2012): total net sales 2011 $6,022 million;
# "Gross profit margin 15%"; Chapter 11 petitions filed "On January 19, 2012"; "As announced on February 9, 2012,
# the Company plans to phase out its dedicated capture devices business, including digital cameras, pocket video
# cameras, and digital picture frames in the first half of 2012."
SALES_2011 = 6_022e6
GROSS_MARGIN_2011 = 15
CH11_YEAR, CH11_MONTH, CH11_DAY = 2012, 1, 19
PHASE_OUT_MONTH, PHASE_OUT_DAY = 2, 9
# Kodak 8-K, Ex. 99.1 (Sept 3, 2013) / 10-Q: plan effective and Kodak emerged from chapter 11 on Sept 3, 2013
# (description only).
EMERGED_YEAR = 2013

# ---------------------------------------------------------------- checks behind spoken / shown claims
assert PROTO_PIXELS == 10_000                                 # "100 × 100 pixels" (shown)
assert round(PROTO_KG * LB_PER_KG) == 8                       # "≈ 8 lb" (shown)
assert SAVE_SECONDS == 23                                     # "twenty-three seconds"
assert 15.9e9 < SALES_1996 < 16e9                             # "almost sixteen billion dollars"
gm_1996 = (SALES_1996 - COGS_1996) / SALES_1996 * 100
assert round(gm_1996) == 48, gm_1996                          # "forty-eight percent"
assert GROSS_MARGIN_2011 == 15                                # "fifteen" (10-K figure)
assert round(SALES_2011 / 1e9) == 6                           # "$6B" (shown)
assert TOP_SELLER_YEAR == 2005 and US_SHARE_2005 > 20         # "number one digital camera seller" (per IDC/AP)
assert (CH11_YEAR, CH11_MONTH) == (2012, 1)                   # "January twenty twelve"
days_to_phase_out = (31 - CH11_DAY) + PHASE_OUT_DAY
assert days_to_phase_out == 21                                # "weeks later" (three weeks)
assert CH11_YEAR - PROTO_YEAR == 37
print(f"1996 gross margin {gm_1996:.1f}% -> 2011 {GROSS_MARGIN_2011}%; sales ${SALES_1996/1e9:.2f}B -> "
      f"${SALES_2011/1e9:.2f}B; phase-out {days_to_phase_out} days after Chapter 11")

spec = {
    "id": "042_kodak",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "CASE STUDY",
    "disclaimer": "Sources: Kodak 10-Ks, IEEE Spectrum, AP/IDC · see description",
    "title": "Kodak Invented the Digital Camera. Then It Lost to It",
    "description": (
        "Kodak built a digital camera in 1975, when engineer Steven Sasson made a prototype that took 23 seconds "
        "to save one black-and-white photo. It never went into production, and film kept paying the bills: Kodak's "
        f"sales were almost $16 billion in 1996. Kodak did go digital and was America's No. 1 digital camera "
        "seller in 2005, but its gross margin fell from about 48% (1996) to 15% (2011). Kodak filed for Chapter 11 "
        "on January 19, 2012, and weeks later said it would stop making digital cameras. It emerged from "
        "bankruptcy in September 2013 as a smaller company focused on printing and imaging for business. The "
        "lesson: don't let today's profits decide whether you build tomorrow's business.\n\n"
        "Sources: IEEE Spectrum, 'The First Digital Camera' (Apr 6, 2022); Eastman Kodak Form 10-K for 1996 "
        "(sales $15,968M, cost of goods sold $8,326M; gross margin computed); Associated Press via NBC News "
        "(Feb 9, 2006), citing IDC (24.9% US share in 2005); Eastman Kodak Form 10-K for 2011 (sales $6,022M, "
        "gross profit margin 15%, Chapter 11 filing and Feb 9, 2012 phase-out of digital cameras); Kodak 8-K "
        "(Sept 3, 2013) on emerging from Chapter 11. Educational content, not investment advice.\n\n"
        "#kodak #business #casestudy #innovation #photography"
    ),
    "tags": ["kodak", "kodak digital camera", "why kodak failed", "kodak bankruptcy", "steve sasson",
             "business case study", "business lessons", "disruption", "innovator's dilemma"],
    "localizations": {
        "es": {"title": "Kodak inventó la cámara digital. Y luego perdió",
               "summary": "Kodak construyó una cámara digital en 1975, pero el cine fotográfico seguía pagando las cuentas. En 2012 se declaró en quiebra (Capítulo 11). Por qué los beneficios de hoy pueden frenar el futuro."},
        "pt": {"title": "A Kodak inventou a câmera digital. E depois perdeu",
               "summary": "A Kodak construiu uma câmera digital em 1975, mas o filme ainda pagava as contas. Em 2012 entrou com pedido de recuperação judicial (Chapter 11). Por que o lucro de hoje pode travar o futuro."},
        "hi": {"title": "Kodak ने डिजिटल कैमरा बनाया, फिर उसी से हार गया",
               "summary": "Kodak ने 1975 में डिजिटल कैमरा बना लिया था, पर कमाई फ़िल्म से हो रही थी। 2012 में कंपनी ने दिवालियापन (Chapter 11) के लिए आवेदन किया। आज का मुनाफ़ा कल के बिज़नेस को कैसे रोक सकता है।"},
        "id": {"title": "Kodak Menemukan Kamera Digital, Lalu Kalah Olehnya",
               "summary": "Kodak membuat kamera digital pada 1975, tetapi film masih menjadi sumber uang. Pada 2012 Kodak mengajukan kebangkrutan (Chapter 11). Mengapa laba hari ini bisa menghambat masa depan."},
        "de": {"title": "Kodak erfand die Digitalkamera – und verlor gegen sie",
               "summary": "Kodak baute 1975 eine Digitalkamera, doch das Geld kam vom Film. 2012 meldete Kodak Insolvenz nach Chapter 11 an. Warum die Gewinne von heute das Geschäft von morgen bremsen können."},
        "fr": {"title": "Kodak a inventé l'appareil numérique, puis a perdu",
               "summary": "Kodak a construit un appareil photo numérique en 1975, mais la pellicule payait les factures. En 2012, Kodak s'est placé sous la protection du Chapter 11. Pourquoi les profits d'aujourd'hui peuvent freiner l'avenir."},
    },
    "scenes": [
        # hook: the contradiction on frame 0 + open loop ("why did Kodak lose?")
        {"say": "In nineteen seventy-five, Kodak built a digital camera. Why did Kodak lose?",
         "visual": {"type": "stat", "value": str(PROTO_YEAR), "label": "Kodak builds a digital camera",
                    "sub": f"then Chapter 11 in {CH11_YEAR}", "color": "gold"}},
        {"say": "Steve Sasson's prototype took twenty-three seconds to save one photo.",
         "visual": {"type": "equation", "title": "Steve Sasson's prototype",
                    "lines": [{"text": "100 × 100 pixels", "color": "text", "size": 84},
                              {"text": f"≈ {round(PROTO_KG * LB_PER_KG)} lb ({PROTO_KG} kg)", "color": "text", "size": 84},
                              {"text": f"{SAVE_SECONDS} s to save a photo", "color": "gold", "size": 84}]}},
        {"say": "It never went into production. Film still paid the bills.",
         "visual": {"type": "pair", "title": "Kodak's choice",
                    "left": {"label": "Digital", "sub": "a prototype", "color": "slate"},
                    "right": {"label": "Film", "sub": "the cash machine", "color": "gold"}}},
        {"say": "By nineteen ninety-six, sales hit almost sixteen billion dollars.",
         "visual": {"type": "stat", "value": f"${SALES_1996 / 1e9:.2f}B", "label": "Kodak sales in 1996",
                    "sub": "Kodak annual report (10-K)", "color": "green"}},
        # mid-video re-hook: opens a second loop (if it went digital, why did it fail?)
        {"say": "Now the twist: Kodak did go digital.",
         "visual": {"type": "equation", "title": "The twist",
                    "lines": [{"text": "Kodak went digital.", "color": "text", "size": 96},
                              {"text": "And led the market.", "color": "gold", "size": 96}]}},
        {"say": "By two thousand five, it was America's top digital camera seller.",
         "visual": {"type": "stat", "value": "No. 1", "label": "US digital camera seller, 2005",
                    "sub": f"{US_SHARE_2005}% share · IDC, via AP", "color": "green"}},
        {"say": "The catch: Kodak's gross margin fell from forty-eight percent to fifteen.",
         "visual": {"type": "bars", "title": "Kodak gross margin (%)", "format": "num",
                    "items": [{"label": "1996", "value": round(gm_1996), "color": "green"},
                              {"label": "2011", "value": GROSS_MARGIN_2011, "color": "red"}]}},
        {"say": "In January twenty twelve, Kodak filed for bankruptcy.",
         "visual": {"type": "compare", "title": f"Before Chapter 11 (Jan {CH11_YEAR})",
                    "left": {"label": "Sales 1996", "value": SALES_1996, "color": "slate"},
                    "right": {"label": "Sales 2011", "value": SALES_2011, "color": "red"}}},
        {"say": "Weeks later, it announced an exit from digital cameras.",
         "visual": {"type": "equation", "title": f"Feb {PHASE_OUT_DAY}, {CH11_YEAR}",
                    "lines": [{"text": "Kodak phases out", "color": "text", "size": 96},
                              {"text": "its digital cameras", "color": "red", "size": 96}]}},
        {"say": "The lesson: protect tomorrow's business, not just today's profits.",
         "visual": {"type": "pair", "title": "The lesson",
                    "left": {"label": "Profits", "sub": "today's", "color": "slate"},
                    "right": {"label": "Future", "sub": "build it anyway", "color": "green"}}},
        # loop line: runs back into "In nineteen seventy-five, Kodak built a digital camera..."
        {"say": "Inventing the future isn't enough. Ask Kodak.",
         "visual": {"type": "cta", "lines": ["Invent it.", "Then sell it."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
# ---------------------------------------------------------------- retention checks (AUTOPILOT "Retention rules")
words = [len(s["say"].split()) for s in spec["scenes"]]
for s in spec["scenes"]:
    assert len(s["say"].split()) <= 14, s["say"]                        # one visual per ~4 s
assert len(spec["scenes"][0]["say"].split()) <= 12                         # hook: payoff first, ~2 s
for a, b in zip(spec["scenes"], spec["scenes"][1:]):
    assert a["visual"]["type"] != b["visual"]["type"], a["say"]           # never the same visual twice in a row
assert 80 <= sum(words) <= 105, sum(words)                                 # ~30-40 s
assert "follow" not in spec["scenes"][-1]["say"].lower()                   # loop line, not a spoken CTA
assert len(spec["title"]) < 60, len(spec["title"])
print(f"{len(words)} scenes, {sum(words)} words (~{sum(words) / 2.9:.0f} s)")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "042_kodak.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
