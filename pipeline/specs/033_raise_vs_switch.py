"""Video 033 (global/USD): staying for yearly raises vs. switching jobs every few years, over 10 years.
Clearly labelled example raise sizes; one sourced real-data check (Atlanta Fed) shows the real gap is smaller.
All maths computed here."""
import json, os

# --- example assumptions (labelled as an example on screen and in the description)
START = 60_000          # year-1 salary
STAY_RAISE = 0.03       # example yearly raise for staying
SWITCH_RAISE = 0.10     # example pay bump when switching jobs
SWITCH_EVERY = 3        # switch at the start of years 4, 7 and 10
YEARS = 10

# --- sourced real data: Federal Reserve Bank of Atlanta, Wage Growth Tracker (3-month moving average of median
#     year-over-year wage growth), data to September 2026, released Oct 8, 2026:
#     job switchers 4.7%, job stayers 3.4%. https://www.atlantafed.org/chcs/wage-growth-tracker
REAL_SWITCHER, REAL_STAYER = 0.047, 0.034

def path(switch, stay_raise=STAY_RAISE, switch_raise=SWITCH_RAISE):
    sal, out = START, [START]
    for year in range(2, YEARS + 1):
        bump = switch_raise if switch and (year - 1) % SWITCH_EVERY == 0 else stay_raise
        sal *= 1 + bump
        out.append(sal)
    return out

stay, move = path(False), path(True)
yrs = list(range(1, YEARS + 1))
S10, M10 = stay[-1], move[-1]
S_tot, M_tot = sum(stay), sum(move)
gap_year, gap_tot = M10 - S10, M_tot - S_tot
switches = sum(1 for y in range(2, YEARS + 1) if (y - 1) % SWITCH_EVERY == 0)
# same model, but with the Atlanta Fed medians in place of the example raises
real_gap_tot = sum(path(True, REAL_STAYER, REAL_SWITCHER)) - sum(path(False, REAL_STAYER, REAL_SWITCHER))

assert switches == 3                            # "three switches in ten years"
assert 78_000 < S10 < 78_500, S10               # "about seventy-eight thousand"
assert 95_000 < M10 < 95_500, M10               # "about ninety-five thousand"
assert 17_000 < gap_year < 17_500, gap_year     # year-10 pay gap (shown via the bars)
assert 687_000 < S_tot < 688_500, S_tot
assert 749_000 < M_tot < 750_500, M_tot
assert 61_500 < gap_tot < 62_500, gap_tot       # "about sixty-two thousand dollars" (hook + scene 4)
assert (REAL_SWITCHER, REAL_STAYER) == (0.047, 0.034)   # "four point seven" vs "three point four percent"
assert 10_500 < real_gap_tot < 11_500, real_gap_tot     # "shrinks to about eleven thousand"
assert real_gap_tot < gap_tot / 5                       # real-world gap is much smaller than the example
print(f"year10 stay ${S10:,.0f} move ${M10:,.0f} gap ${gap_year:,.0f} | 10y stay ${S_tot:,.0f} "
      f"move ${M_tot:,.0f} gap ${gap_tot:,.0f} | real-data gap ${real_gap_tot:,.0f}")

spec = {
    "id": "033_raise_vs_switch",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "EARN MORE",
    "disclaimer": "Example raises only · 3% a year vs 10% per switch · yours will differ",
    "title": "Ask for a Raise or Switch Jobs? The 10-Year Math",
    "description": (
        "Should you stay for yearly raises or switch jobs for a bigger bump? In this example, two people start on "
        f"$60,000. Staying with 3% raises reaches about ${S10/1e3:,.0f}K in year ten; switching every three years "
        f"for a 10% bump reaches about ${M10/1e3:,.0f}K, about ${gap_tot/1e3:,.0f}K more earned over the decade.\n\n"
        "Real raises are often smaller. In the Atlanta Fed's Wage Growth Tracker (data to September 2026), median "
        f"pay growth was {REAL_SWITCHER:.1%} a year for job switchers vs {REAL_STAYER:.1%} for people who stayed. "
        f"Using those numbers in the same example, the 10-year gap shrinks to about ${real_gap_tot/1e3:,.0f}K.\n\n"
        "Source: Federal Reserve Bank of Atlanta, Wage Growth Tracker (3-month moving average of median wage growth, "
        "released Oct 8, 2026): https://www.atlantafed.org/chcs/wage-growth-tracker\n\n"
        "Example assumptions (real raises vary by job, field and year): $60,000 starting salary, "
        "3% yearly raise when staying, 10% raise at each switch in years 4, 7 and 10 and 3% in the other years, "
        "no gaps between jobs, salary only (no bonuses, benefits or retirement matching). Switching has costs too: "
        "risk, a learning curve and benefits you may lose. This is not career or financial advice.\n\n"
        "#careeradvice #salary #personalfinance #moneytips #jobsearch"
    ),
    "tags": ["ask for a raise", "switch jobs", "job hopping salary", "salary negotiation", "career advice",
             "how to earn more", "personal finance", "money tips", "pay raise"],
    "localizations": {
        "es": {"title": "¿Pedir aumento o cambiar de trabajo? Cálculo a 10 años",
               "summary": "Ejemplo: dos personas empiezan con $60,000. Quedarse con aumentos del 3% vs cambiar cada "
                          f"tres años con un 10% más: unos ${gap_tot/1e3:,.0f}K de diferencia en 10 años."},
        "pt": {"title": "Pedir aumento ou trocar de emprego? A conta de 10 anos",
               "summary": "Exemplo: duas pessoas começam com $60,000. Ficar com aumentos de 3% vs trocar a cada três "
                          f"anos com 10% a mais: cerca de ${gap_tot/1e3:,.0f}K de diferença em 10 anos."},
        "hi": {"title": "रेज़ मांगें या नौकरी बदलें? 10 साल का हिसाब",
               "summary": "उदाहरण: दोनों की शुरुआती सैलरी $60,000। हर साल 3% बढ़ोतरी बनाम हर तीन साल में 10% बढ़त "
                          f"के साथ नौकरी बदलना: 10 साल में करीब ${gap_tot/1e3:,.0f}K का फर्क।"},
        "id": {"title": "Minta Naik Gaji atau Pindah Kerja? Hitungan 10 Tahun",
               "summary": "Contoh: dua orang mulai dengan gaji $60,000. Bertahan dengan kenaikan 3% vs pindah tiap tiga "
                          f"tahun dengan kenaikan 10%: selisih sekitar ${gap_tot/1e3:,.0f}K dalam 10 tahun."},
        "de": {"title": "Gehaltserhöhung oder Jobwechsel? Die 10-Jahres-Rechnung",
               "summary": "Beispiel: Zwei Personen starten mit $60,000. Bleiben mit 3% pro Jahr vs. Wechsel alle drei "
                          f"Jahre mit 10% mehr: rund ${gap_tot/1e3:,.0f}K Unterschied in 10 Jahren."},
        "fr": {"title": "Demander une hausse ou changer de job ? Le calcul sur 10 ans",
               "summary": "Exemple : deux personnes débutent à $60,000. Rester avec 3 % par an ou changer tous les trois "
                          f"ans avec 10 % de plus : environ ${gap_tot/1e3:,.0f}K d'écart en 10 ans."},
    },
    "thumbnail": {"photo": {"file": "assets/photos/business_meeting_coworkers.jpg", "focus": [0.45, 0.5]},
                  "big": f"${gap_tot/1e3:,.0f}K?", "line": "The price of staying", "color": "gold"},
    "scenes": [
        {"say": "In this example, staying loyal costs about sixty-two thousand dollars over ten years. Here's the math, and the catch.",
         "visual": {"type": "equation", "title": "Stay or switch?",
                    "lines": [{"text": "10-year example", "color": "text", "size": 96},
                              {"text": "↓", "color": "dim", "size": 80},
                              {"text": f"${gap_tot/1e3:,.0f}K gap", "color": "gold", "size": 140}]}},
        {"say": "Two people start at sixty thousand dollars. Sara stays and gets three percent a year. Leo switches every three years for a ten percent bump.",
         "visual": {"type": "pair", "title": "Example: both start at $60K",
                    "left": {"label": "Sara", "sub": "stays · 3% a year", "color": "slate"},
                    "right": {"label": "Leo", "sub": "switches · +10%", "color": "green"}}},
        {"say": "Each switch resets Leo's pay higher. By year ten, Sara earns about seventy-eight thousand; Leo, about ninety-five thousand.",
         "visual": {"type": "bars", "title": "Salary in year 10",
                    "items": [{"label": "Sara", "value": S10, "color": "slate"},
                              {"label": "Leo", "value": M10, "color": "green"}]}},
        {"say": "Over the decade, Leo earns about sixty-two thousand dollars more.",
         "visual": {"type": "photo", "file": "assets/photos/office_workers_desks.jpg",
                    "title": "Example: 3 switches at +10%",
                    "value": f"+${gap_tot/1e3:,.0f}K", "color": "green", "label": "more earned over 10 years",
                    "focus": [0.6, 0.4]}},
        {"say": "But real bumps are often smaller. In US data, switchers' pay recently grew four point seven percent a year, versus three point four for stayers. At those rates, Leo's lead shrinks to about eleven thousand.",
         "visual": {"type": "pair", "title": "Real US pay growth · Atlanta Fed",
                    "left": {"label": "Stayers", "sub": f"{REAL_STAYER:.1%} a year", "color": "slate"},
                    "right": {"label": "Switchers", "sub": f"{REAL_SWITCHER:.1%} a year", "color": "green"}}},
        {"say": "Switching has costs too: risk, and lost bonuses or benefits.",
         "visual": {"type": "photo", "file": "assets/photos/business_meeting_coworkers.jpg",
                    "title": "The catch",
                    "label": "New-job risk · lost bonuses · benefits reset", "focus": [0.5, 0.5]}},
        {"say": "So know your market value: ask for a raise first, and move if the answer is no.",
         "visual": {"type": "pair", "title": "Your two moves",
                    "left": {"label": "Ask", "sub": "with market data", "color": "gold"},
                    "right": {"label": "Move", "sub": "if the answer is no", "color": "green"}}},
        {"say": "Follow for a new one every day.",
         "visual": {"type": "cta", "lines": ["Know your", "market value."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(__file__), "033_raise_vs_switch.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
