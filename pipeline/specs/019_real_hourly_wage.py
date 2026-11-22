"""Video 019 (global/USD): your real hourly wage. Example assumptions, all maths computed here."""
import json, os

# --- example assumptions (clearly labelled as an example on screen and in the description)
SALARY, PAID_H = 60_000, 40          # salary per year, paid hours per week
TAX = 0.20                           # example all-in tax rate (income + payroll); varies by person and state
COMMUTE_H, EXTRA_H = 4, 3            # hours/week: commute (~48 min/day) + unpaid extras (early emails, staying late)
COSTS = {"Gas / transit": 30, "Lunches out": 30, "Clothes & other": 10}   # $ per week

week_gross = SALARY / 52
headline = week_gross / PAID_H
take_home_y = SALARY * (1 - TAX)
week_net = week_gross * (1 - TAX)
cost_w = sum(COSTS.values())
real_h = PAID_H + COMMUTE_H + EXTRA_H
real = (week_net - cost_w) / real_h
gadget_h = 300 / real

assert round(headline, 2) == 28.85            # "almost twenty-nine dollars an hour"
assert take_home_y == 48_000                  # "forty-eight thousand"
assert real_h == 47                           # "forty-seven hours"
assert cost_w == 70                           # "seventy dollars a week"
assert 18 < real < 18.5, real                 # "about eighteen dollars"
assert 1 - real / headline > 1 / 3            # "over a third less"
assert 16 < gadget_h < 17, gadget_h           # "over sixteen hours"
assert 10 < 300 / headline < 11               # "doesn't cost ten hours" (10.4 at the paper rate)
print(f"headline ${headline:.2f}/h, real ${real:.2f}/h ({1 - real/headline:.0%} less), $300 = {gadget_h:.1f} h")

spec = {
    "id": "019_real_hourly_wage",
    "currency": "usd", "voice": "af_heart", "speed": 1.05,
    "badge": "EARN MORE",
    "disclaimer": "Example only · 20% tax, 7 extra hrs and $70 costs a week · yours will differ",
    "title": "Your Real Hourly Wage Is Lower Than You Think",
    "description": (
        f"A $60,000 salary for 40 hours a week works out to ${headline:.2f} an hour on paper. "
        f"Add taxes, the commute, unpaid extra time and the cost of going to work, and the real figure in this "
        f"example is about ${real:.2f} an hour, over a third less. Work out your own number before comparing jobs "
        "or big purchases.\n\n"
        "Example assumptions (yours will differ): 20% combined income and payroll tax, 4 hours a week commuting, "
        "3 hours a week of unpaid extra work, $70 a week in work costs ($30 gas or transit, $30 lunches out, "
        "$10 clothes and other). Weeks averaged over the year.\n\n"
        "#personalfinance #salary #careeradvice #moneytips #financialliteracy"
    ),
    "tags": ["real hourly wage", "hourly rate", "salary", "commute cost", "personal finance",
             "career advice", "money tips", "financial literacy", "earn more"],
    "scenes": [
        {"say": "You earn sixty thousand dollars a year. That's almost twenty-nine dollars an hour. Or is it?",
         "visual": {"type": "stat", "value": f"${headline:.2f}", "label": "per hour, on paper",
                    "sub": "$60,000 ÷ (40 hours × 52 weeks)", "color": "gold"}},
        {"say": "First, taxes. In this example, about twenty percent goes to income and payroll tax. You keep forty-eight thousand.",
         "visual": {"type": "equation", "title": "Example: taxes",
                    "lines": [{"text": "$60,000 salary", "color": "text", "size": 88},
                              {"text": "− 20% tax", "color": "red", "size": 80},
                              {"text": "= $48,000 kept", "color": "green", "size": 96}]}},
        {"say": "Next, time. Add four hours a week of commuting, and three hours of unpaid extras, like early emails.",
         "visual": {"type": "bars", "title": "Hours per week", "format": "num",
                    "items": [{"label": "Paid", "value": PAID_H, "color": "slate"},
                              {"label": "Real", "value": real_h, "color": "gold"}]}},
        {"say": "Then the cost of going to work. Gas, lunches out, work clothes. Say seventy dollars a week.",
         "visual": {"type": "equation", "title": "Example: work costs",
                    "lines": [{"text": f"{k}  ${v}", "color": "muted", "size": 68} for k, v in COSTS.items()]
                             + [{"text": f"= ${cost_w} a week", "color": "red", "size": 96}]}},
        {"say": "Put it together, and your real hourly wage is about eighteen dollars. Over a third less than it looked.",
         "visual": {"type": "compare", "title": "Your hourly wage",
                    "left": {"label": "On paper", "value": headline, "color": "slate"},
                    "right": {"label": "Real", "value": real, "color": "green"}}},
        {"say": "Why it matters: a three hundred dollar gadget doesn't cost ten hours of your life. It costs over sixteen.",
         "visual": {"type": "stat", "value": f"{gadget_h:.1f} h", "label": "of your life for a $300 gadget",
                    "sub": f"at ${real:.2f} per real hour", "color": "red"}},
        {"say": "And a job that pays a little less, but with no commute, might actually pay you more per hour.",
         "visual": {"type": "equation", "title": "Compare jobs by",
                    "lines": [{"text": "money kept", "color": "green", "size": 96},
                              {"text": "÷", "color": "dim", "size": 80},
                              {"text": "hours it really takes", "color": "text", "size": 76}]}},
        {"say": "Work out your real number. Follow for one money lesson every day.",
         "visual": {"type": "cta", "lines": ["Know your", "real wage."],
                    "sub": "Follow for daily money lessons"}},
    ],
}
out = os.path.join(os.path.dirname(__file__), "019_real_hourly_wage.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out)
