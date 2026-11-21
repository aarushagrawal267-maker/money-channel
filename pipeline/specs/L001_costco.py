"""Long-form L001: How Costco makes money. Figures: Costco FY2026 results (52 weeks ended Aug 30, 2026)."""
import json, os

NET_SALES = 297_247e6       # Costco FY2026 release
FEES = 5_907e6              # membership fee income
OP_INC = 11_685e6           # operating income
NET_INC = 9_226e6           # net income
REVENUE = NET_SALES + FEES
PAID_MEMBERS = 84.1e6       # reported paid members, year-end (third-party summary of 10-K)
GOLD, EXEC, EXEC_REWARD = 65, 130, 0.02

fee_share_rev = FEES / REVENUE
fee_share_op = FEES / OP_INC
merch_margin = (OP_INC - FEES) / NET_SALES
breakeven = (EXEC - GOLD) / EXEC_REWARD

assert 302e9 < REVENUE < 304e9                 # "over three hundred billion"
assert fee_share_rev < 0.02                    # "less than two percent"
assert 0.50 < fee_share_op < 0.51              # "about half"
assert 0.019 < merch_margin < 0.02             # "about two cents per dollar"
assert 9.2e9 < NET_INC < 9.3e9                 # "over nine billion"
assert breakeven == 3250                        # "$3,250 a year"
print(f"rev {REVENUE/1e9:.1f}B fees/rev {fee_share_rev:.2%} fees/op {fee_share_op:.1%} "
      f"merch margin {merch_margin:.2%} breakeven ${breakeven:,.0f}")

S = []
def scene(say, **visual):
    S.append({"say": say, "visual": visual})

# ---- Hook
scene("Last year, Costco sold almost three hundred billion dollars worth of stuff. And on all those products, it made almost nothing.",
      type="stat", value="$297B", label="worth of products sold", sub="fiscal year 2026", color="text")
scene("Yet the company still made over nine billion dollars in profit. So where does the money actually come from?",
      type="stat", value="$9.2B", label="net profit", sub="fiscal year 2026", color="green")
scene("The answer is one of the smartest business models in the world. And once you see it, you'll spot it everywhere.",
      type="title", title="How Costco Makes Money", sub="the business model hiding in plain sight")

# ---- Chapter 1
scene("The strange math.", type="chapter", n=1, title="The strange math")
scene("Costco's total revenue last year was just over three hundred and three billion dollars. Almost all of that came from selling products.",
      type="stat_grid", title="Costco, fiscal 2026",
      items=[{"value": "$303B", "label": "total revenue", "color": "text"},
             {"value": "$5.9B", "label": "membership fees", "color": "gold"},
             {"value": "$11.7B", "label": "operating profit", "color": "green"}])
scene("Membership fees were only five point nine billion. That's less than two percent of revenue.",
      type="share", title="Membership fees as a share of...",
      rows=[{"label": "Revenue", "share": fee_share_rev, "color": "gold", "dp": 1}])
scene("But here's the twist. Those same fees made up about half of Costco's operating profit.",
      type="share", title="Membership fees as a share of...",
      rows=[{"label": "Revenue", "share": fee_share_rev, "color": "gold", "dp": 1},
            {"label": "Operating profit", "share": fee_share_op, "color": "green", "dp": 0}],
      note="Source: Costco FY2026 results")
scene("In other words, Costco isn't really in the business of selling you groceries. It's in the business of selling you a membership card.",
      type="equation", lines=[{"text": "Not a grocery store", "color": "muted", "size": 80},
                              {"text": "A membership business", "color": "gold", "size": 110}])

# ---- Chapter 2
scene("Why the products barely make money.", type="chapter", n=2, title="Prices on purpose")
scene("Costco reportedly caps its markup at fourteen percent on most brands, and fifteen percent on its own Kirkland brand. Many supermarkets mark items up far more.",
      type="stat_grid", title="Costco's reported markup caps",
      items=[{"value": "14%", "label": "max markup", "sub": "outside brands", "color": "green"},
             {"value": "15%", "label": "max markup", "sub": "Kirkland Signature", "color": "green"}])
scene("After paying for staff, warehouses and shipping, Costco keeps only about two cents of operating profit for every dollar of products it sells.",
      type="equation", lines=[{"text": "$1.00 of products", "color": "muted", "size": 90},
                              {"text": "↓", "color": "dim", "size": 80},
                              {"text": "≈ 2¢ operating profit", "color": "green", "size": 110}])
scene("That's why the famous one dollar fifty hot dog and soda combo hasn't changed price in decades. Cheap prices aren't a mistake. They're the marketing.",
      type="title", title="$1.50", sub="hot dog + soda · same price for decades")

# ---- Chapter 3
scene("The membership machine.", type="chapter", n=3, title="The membership machine")
scene("Costco has about eighty-four million paid members. A basic membership in the US costs sixty-five dollars a year. Executive costs one hundred and thirty.",
      type="stat_grid", title="Who pays Costco to shop there",
      items=[{"value": "84M", "label": "paid members", "color": "text"},
             {"value": "$65", "label": "Gold Star / year", "sub": "US", "color": "gold"},
             {"value": "$130", "label": "Executive / year", "sub": "US", "color": "gold"}])
scene("Here's why this is so powerful. Membership fees are almost pure profit. There's no product to buy, no shelf to stock. And around nine in ten members renew every year.",
      type="bullets", title="Why fees are the perfect revenue",
      items=["Almost pure profit", "No inventory needed", "Paid upfront, every year", "~9 in 10 members renew"])
scene("That means Costco knows, a year in advance, where roughly half its operating profit will come from. Investors love that kind of predictability.",
      type="share", title="Profit Costco can count on before the year starts",
      rows=[{"label": "Membership fees", "share": fee_share_op, "color": "green", "dp": 0}])

# ---- Chapter 4
scene("The flywheel.", type="chapter", n=4, title="The flywheel")
scene("Low prices attract more members. More members means Costco buys in enormous volume. Huge volume lets it squeeze suppliers for lower costs. And lower costs mean even lower prices. Then the loop starts again.",
      type="flywheel", title="The Costco flywheel", center="REPEAT",
      steps=["Low prices", "More members", "Huge volume", "Lower costs"])
scene("Costco also stocks only around four thousand items, while a typical supermarket carries tens of thousands. Fewer items means bigger orders of each one, and even better deals.",
      type="hbars", title="Products on the shelves (approx.)", format="num",
      items=[{"label": "Costco", "value": 4000, "display": "~4,000", "color": "green"},
             {"label": "Typical supermarket", "value": 30000, "display": "30,000+", "color": "slate"}])

# ---- Chapter 5
scene("What this means for you.", type="chapter", n=5, title="What it means for you")
scene("First, as a shopper. The Executive membership gives two percent back on purchases. The upgrade costs sixty-five dollars more, so it only pays off if you spend over three thousand two hundred and fifty dollars a year.",
      type="equation", title="Is Executive worth it?",
      lines=[{"text": "$65 extra ÷ 2% back", "color": "muted", "size": 84},
             {"text": "= $3,250 / year", "color": "gold", "size": 120},
             {"text": "about $270 a month at Costco", "color": "text", "size": 56}])
scene("Second, as an investor or a business builder. The best businesses often don't profit from what they sell. They profit from the relationship. Think Amazon Prime, Netflix, or your phone plan.",
      type="bullets", title="Same model, different companies",
      items=["Amazon Prime", "Netflix", "Gym memberships", "Phone plans"])
scene("Costco gives away the products almost at cost, and charges you for the right to shop. That's the secret.",
      type="equation", lines=[{"text": "Sell products at cost.", "color": "text", "size": 96},
                              {"text": "Charge for access.", "color": "gold", "size": 110}])
scene("If you learned something, subscribe. We break down how money really works, every week.",
      type="cta", lines=["How money", "really works."], sub="Subscribe for weekly breakdowns")

spec = {
    "id": "L001_costco", "currency": "usd", "voice": "af_heart", "speed": 1.02, "gap": 0.35,
    "badge": "BUSINESS BREAKDOWN",
    "disclaimer": "Figures: Costco FY2026 results · for education, not investment advice",
    "title": "How Costco Makes $9 Billion While Barely Profiting From Products",
    "thumbnail": {"big": "$5.9B", "line": "COSTCO'S REAL BUSINESS", "tag": "IT'S NOT GROCERIES", "color": "gold"},
    "description_sources": [
        "Costco FY2026 Q4 and full-year results: https://investor.costco.com/news/news-details/2026/Costco-Wholesale-Corporation-Reports-Fourth-Quarter-and-Fiscal-Year-2026-Operating-Results/default.aspx",
    ],
    "tags": ["costco", "business model", "how costco makes money", "membership business", "business breakdown",
             "investing", "kirkland", "costco stock", "economics explained"],
    "scenes": S,
}
out = os.path.join(os.path.dirname(__file__), "L001_costco.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out, len(S), "scenes,", sum(len(s["say"].split()) for s in S), "words")
