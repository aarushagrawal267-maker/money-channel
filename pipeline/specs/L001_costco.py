"""Long-form L001: How Costco makes money.

Sources (checked 2026-11-21):
  [R] Costco FY2026 Q4/full-year release (52 weeks ended Aug 30, 2026), dollars in millions.
  [K] Costco FY2026 Form 10-K (filed Oct 2026): members, Executive share of sales, SKUs, warehouses.
  [F] Fee increase effective Sept 1, 2024 (Costco announcement, widely reported): Gold Star $60->$65,
      Executive $120->$130, Executive 2% reward cap $1,000->$1,250. Previous increase: June 2017.
  [H] Company history: Price Club (Sol Price) opened 1976 in San Diego; first Costco opened 1983 in
      Seattle; $1.50 hot dog + soda since 1985; Costco and Price Club merged in 1993.
  Markup caps (14% / 15% Kirkland) are reported by press and analysts, not in filings, so said as "reportedly".
"""
import json, os

# ---- [R] FY2026 and FY2025, $
NET_SALES, NET_SALES_25 = 297_247e6, 269_912e6
FEES, FEES_25 = 5_907e6, 5_323e6
MERCH_COSTS = 264_279e6
SGA = 27_190e6
OP_INC, OP_INC_25 = 11_685e6, 10_383e6
NET_INC = 9_226e6
REVENUE = NET_SALES + FEES
# ---- [K]
PAID = {2024: 76.2e6, 2025: 81.0e6, 2026: 84.1e6}
EXEC_MEMBERS = 42.3e6
EXEC_SALES_SHARE = 0.752
RENEW_US_CA, RENEW_WORLD = 0.923, 0.898
SKUS = 4000                 # "less than 4,000 active SKUs per warehouse"
WAREHOUSES = 939
# ---- [F]
GOLD, EXEC, EXEC_REWARD, EXEC_CAP = 65, 130, 0.02, 1250
GOLD_OLD, EXEC_OLD = 60, 120

# ---- derived numbers (every spoken one is asserted)
assert abs(REVENUE - 303_154e6) < 1                      # matches reported total revenue
assert abs(REVENUE - MERCH_COSTS - SGA - OP_INC) < 1e6   # statement ties out
gross_margin = (NET_SALES - MERCH_COSTS) / NET_SALES     # cents kept per sales $ before running costs
fee_share_rev = FEES / REVENUE
fee_share_op = FEES / OP_INC
merch_margin = (OP_INC - FEES) / NET_SALES               # operating profit from products per sales $
fee_growth = FEES / FEES_25 - 1
exec_member_share = EXEC_MEMBERS / PAID[2026]
breakeven = (EXEC - GOLD) / EXEC_REWARD
gold_breakeven = GOLD / 0.05                              # example: 5% saving vs usual store
cap_spend = EXEC_CAP / EXEC_REWARD
new_members = PAID[2026] - PAID[2024]

assert 302e9 < REVENUE < 304e9            # "just over three hundred and three billion"
assert 297e9 < NET_SALES < 297.5e9        # "almost three hundred billion" / "$297B"
assert 0.110 < gross_margin < 0.112       # "about eleven cents"
assert 0.019 < fee_share_rev < 0.02       # "less than two percent"
assert 0.50 < fee_share_op < 0.51         # "about half"
assert 0.019 < merch_margin < 0.02        # "about two cents"
assert 9.2e9 < NET_INC < 9.3e9            # "over nine billion"
assert 0.10 < fee_growth < 0.12           # "about eleven percent"
assert 0.50 < exec_member_share < 0.51    # "about half"
assert gold_breakeven == 1300            # "about thirteen hundred dollars"
assert 105 < gold_breakeven / 12 < 112    # "roughly a hundred and ten a month"
assert OP_INC - FEES < 6e9                # "under six billion"
assert breakeven == 3250                  # "three thousand two hundred and fifty"
assert cap_spend == 62500                 # "sixty-two thousand five hundred"
assert 7.8e6 < new_members < 8.0e6        # "almost eight million"
print(f"rev {REVENUE/1e9:.1f}B gm {gross_margin:.2%} fees/rev {fee_share_rev:.2%} fees/op {fee_share_op:.1%} "
      f"merch {merch_margin:.2%} fee growth {fee_growth:.1%} exec share {exec_member_share:.1%}")

S = []
def scene(say, **visual):
    S.append({"say": say, "visual": visual})

# ---------------------------------------------------------------- Hook
scene("Last year, Costco sold almost three hundred billion dollars worth of stuff. And on all those products, it made almost nothing.",
      type="count", to=297.2, prefix="$", suffix="B", dp=1, label="worth of products sold", sub="fiscal year 2026", color="text")
scene("Yet the company still made over nine billion dollars in profit. So where does the money actually come from?",
      type="stat", value="$9.2B", label="net profit", sub="fiscal year 2026", color="green")
scene("The answer is one of the smartest business models in the world. And once you see it, you'll start spotting it everywhere.",
      type="title", title="How Costco Makes Money", sub="the business model hiding in plain sight")

# ---------------------------------------------------------------- 1
scene("Chapter one. The strange math.", type="chapter", n=1, title="The strange math")
scene("Costco's total revenue last year was just over three hundred and three billion dollars. Almost all of it came from selling products.",
      type="stat_grid", title="Costco, fiscal 2026",
      items=[{"value": "$303B", "label": "total revenue", "color": "text"},
             {"value": "$5.9B", "label": "membership fees", "color": "gold"},
             {"value": "$11.7B", "label": "operating profit", "color": "green"}])
scene("Now follow the money. Start with the revenue. Take away what Costco paid for the products themselves. Then take away the cost of running the business: staff, warehouses, trucks. What's left is operating profit, about eleven point seven billion.",
      type="waterfall", title="Where Costco's revenue goes (fiscal 2026)",
      steps=[{"label": "Revenue", "value": REVENUE, "kind": "start"},
             {"label": "Product costs", "value": MERCH_COSTS, "kind": "minus"},
             {"label": "Running costs", "value": SGA, "kind": "minus"},
             {"label": "Operating profit", "value": OP_INC, "kind": "total"}])
scene("That's a profit of less than four cents on every dollar that comes in. Thin, for a company this famous.",
      type="equation", lines=[{"text": "$1.00 in", "color": "muted", "size": 96},
                              {"text": "↓", "color": "dim", "size": 80},
                              {"text": f"{OP_INC / REVENUE * 100:.1f}¢ operating profit", "color": "green", "size": 110}])
scene("And membership fees? Only five point nine billion dollars. Less than two percent of revenue.",
      type="stat", value=f"{fee_share_rev * 100:.1f}%", label="of revenue came from membership fees",
      sub="$5.9B of $303B", color="gold")
scene("But here's the twist. Those same fees made up about half of Costco's operating profit.",
      type="share", title="Membership fees as a share of...",
      rows=[{"label": "Revenue", "share": fee_share_rev, "color": "gold", "dp": 1},
            {"label": "Operating profit", "share": fee_share_op, "color": "green", "dp": 0}],
      note="Source: Costco FY2026 results")
scene("Split the profit pie and it looks like this. One half from fees. The other half from three hundred billion dollars of shopping.",
      type="donut", title="Costco's operating profit, fiscal 2026",
      segments=[{"label": "Membership fees", "value": FEES, "color": "gold", "display": f"{fee_share_op * 100:.0f}%"},
                {"label": "Selling products", "value": OP_INC - FEES, "color": "blue", "display": f"{(1 - fee_share_op) * 100:.0f}%"}],
      center="$11.7B", center_sub="operating profit")
scene("Try a thought experiment. If Costco stopped charging fees tomorrow and changed nothing else, its operating profit would fall from about eleven point seven billion to under six billion. Half the company's profit, gone.",
      type="columns", title="Operating profit, fiscal 2026", highlight=0,
      items=[{"label": "With fees", "value": OP_INC, "display": "$11.7B", "color": "green"},
             {"label": "Without fees", "value": OP_INC - FEES, "display": f"${(OP_INC - FEES) / 1e9:.1f}B", "color": "red"}])
scene("In other words, Costco isn't really in the business of selling you groceries. It's in the business of selling you a membership card.",
      type="quote", text="Not a grocery store.\nA membership business.", first_color="muted", color="gold")

# ---------------------------------------------------------------- 2
scene("Chapter two. Prices on purpose.", type="chapter", n=2, title="Prices on purpose")
scene("Costco reportedly caps its markup at fourteen percent on most brands, and fifteen percent on its own Kirkland brand.",
      type="stat_grid", title="Costco's reported markup caps",
      items=[{"value": "14%", "label": "max markup", "sub": "outside brands", "color": "green"},
             {"value": "15%", "label": "max markup", "sub": "Kirkland Signature", "color": "green"}])
scene("You can see it in the numbers. For every dollar of products Costco sold, it paid about eighty-nine cents to buy them. It kept only about eleven cents to run the entire company.",
      type="hbars", title="Every $1 of Costco sales",
      items=[{"label": "Paid to suppliers", "value": 1 - gross_margin, "display": f"{(1 - gross_margin) * 100:.0f}¢", "color": "slate"},
             {"label": "Kept by Costco", "value": gross_margin, "display": f"{gross_margin * 100:.0f}¢", "color": "green"}])
scene("Costco's own annual report says it runs on significantly lower margins than most other retailers. That's not an accident. It's the strategy.",
      type="quote", text="\"Significantly lower gross margins\nthan most other retailers\"", first_color="text", color="text",
      source="Costco FY2026 annual report (10-K)")
scene("After paying for staff, buildings and shipping, the products themselves leave Costco about two cents of operating profit per dollar sold.",
      type="equation", lines=[{"text": "$1.00 of products", "color": "muted", "size": 90},
                              {"text": "↓", "color": "dim", "size": 80},
                              {"text": "≈ 2¢ operating profit", "color": "green", "size": 110}])
scene("That's why the famous one dollar fifty hot dog and soda combo hasn't changed price since nineteen eighty-five. Cheap prices aren't a mistake. They're the marketing.",
      type="title", title="$1.50", sub="hot dog + soda · same price since 1985")
scene("Every time a news story says the hot dog is still a dollar fifty, Costco gets free advertising. It tells you, before you walk in, that prices here are fair.",
      type="bullets", title="What a $1.50 hot dog buys Costco",
      items=["Free headlines every year", "A reputation for fair prices", "A reason to visit (and stay)", "Trust that sells everything else"])

# ---------------------------------------------------------------- 3
scene("Chapter three. The membership machine.", type="chapter", n=3, title="The membership machine")
scene("Costco now has about eighty-four million paid members. A basic Gold Star membership in the US costs sixty-five dollars a year. Executive costs one hundred and thirty.",
      type="stat_grid", title="Who pays Costco to shop there",
      items=[{"value": "84M", "label": "paid members", "color": "text"},
             {"value": "$65", "label": "Gold Star / year", "sub": "US", "color": "gold"},
             {"value": "$130", "label": "Executive / year", "sub": "US", "color": "gold"}])
scene("And that number keeps climbing. In just two years, Costco added almost eight million paid members.",
      type="columns", title="Paid members (millions, fiscal year end)", format="num", highlight=2,
      items=[{"label": str(y), "value": v / 1e6, "display": f"{v / 1e6:.1f}M"} for y, v in PAID.items()],
      note="Source: Costco 10-K")
scene("Membership fees are almost pure profit. There's no product to buy, no shelf to stock. And members pay upfront, before they've bought a single thing.",
      type="bullets", title="Why fees are the perfect revenue",
      items=["Almost pure profit", "No inventory needed", "Paid upfront, every year", "Collected before you shop"])
scene("They also renew. In the US and Canada, about ninety-two percent of members renew. Worldwide, about ninety percent.",
      type="share", title="Members who renew",
      rows=[{"label": "US & Canada", "share": RENEW_US_CA, "color": "green", "dp": 1},
            {"label": "Worldwide", "share": RENEW_WORLD, "color": "green", "dp": 1}],
      note="Source: Costco FY2026 10-K")
scene("Put another way: out of every hundred members in the US and Canada, about ninety-two come back the next year and pay again. Most subscription businesses would love a number like that.",
      type="stat", value="92 of 100", label="US & Canada members who renew", sub="Costco FY2026 10-K", color="green")
scene("Then there's the upgrade. About half of paid members now pay for Executive. And those Executive members account for about three quarters of all Costco sales.",
      type="versus", title="Executive members",
      left={"label": "Share of paid members", "value": f"{exec_member_share * 100:.0f}%", "sub": "42.3M of 84.1M", "color": "blue"},
      right={"label": "Share of Costco sales", "value": f"{EXEC_SALES_SHARE * 100:.0f}%", "sub": "fiscal 2026", "color": "gold"},
      verdict="The biggest shoppers pay the biggest fee")
scene("Because people renew so reliably, Costco can even raise the fee. In September twenty twenty-four, Gold Star went from sixty to sixty-five dollars, and Executive from one twenty to one thirty. Most members simply paid it.",
      type="table", title="The 2024 fee increase (US & Canada)",
      header=["Membership", "Before", "After"],
      rows=[["Gold Star", f"${GOLD_OLD}", f"${GOLD}"], ["Executive", f"${EXEC_OLD}", f"${EXEC}"]],
      col_colors={"1": "muted", "2": "gold"})
scene("Partly as a result, membership fee income grew about eleven percent last year, to five point nine billion dollars.",
      type="columns", title="Membership fee income", highlight=1,
      items=[{"label": "Fiscal 2025", "value": FEES_25, "display": "$5.3B"},
             {"label": "Fiscal 2026", "value": FEES, "display": "$5.9B"}])
scene("That means Costco knows, a year in advance, where roughly half of its operating profit will come from. Investors pay a lot for that kind of predictability.",
      type="share", title="Profit Costco can count on before the year starts",
      rows=[{"label": "Membership fees", "share": fee_share_op, "color": "green", "dp": 0}])

# ---------------------------------------------------------------- 4
scene("Chapter four. The flywheel.", type="chapter", n=4, title="The flywheel")
scene("Low prices attract more members. More members means Costco buys in enormous volume. Huge volume lets it negotiate lower costs from suppliers. And lower costs mean even lower prices. Then the loop starts again.",
      type="flywheel", title="The Costco flywheel", center="REPEAT",
      steps=["Low prices", "More members", "Huge volume", "Lower costs"])
scene("Costco also keeps its range tiny. Fewer than four thousand items per warehouse, while a typical supermarket carries tens of thousands.",
      type="hbars", title="Products on the shelves (approx.)", format="num",
      items=[{"label": "Costco", "value": SKUS, "display": "<4,000", "color": "green"},
             {"label": "Typical supermarket", "value": 30000, "display": "tens of thousands", "color": "slate"}])
scene("Fewer items means much bigger orders of each one. That gives Costco enormous bargaining power, and it makes the warehouses simpler and cheaper to run.",
      type="bullets", title="Why fewer items wins",
      items=["Giant orders → better prices", "Faster-selling stock", "Simpler warehouses", "Less waste"])
scene("And the stores themselves are bare warehouses. Concrete floors, products on pallets, no fancy displays. Every saving goes back into lower prices, which feeds the flywheel again.",
      type="equation", title="Where the savings go",
      lines=[{"text": "Cheaper to run", "color": "muted", "size": 84},
             {"text": "↓", "color": "dim", "size": 80},
             {"text": "Lower prices", "color": "green", "size": 110},
             {"text": "↓ more members", "color": "gold", "size": 64}])
scene("Kirkland Signature, Costco's own brand, adds another turn. Costco controls the product, so it can sell high quality at a lower price, and build loyalty no other store can copy.",
      type="stat", value="Kirkland", label="Costco's own brand", sub="a growing share of sales, per the 10-K", color="gold")

# ---------------------------------------------------------------- 5
scene("Chapter five. How it started.", type="chapter", n=5, title="How it started")
scene("The idea is older than Costco. In nineteen seventy-six, Sol Price opened Price Club in San Diego, one of the first membership warehouses.",
      type="timeline", title="From one warehouse to 939",
      events=[{"when": "1976", "text": "Price Club opens\nSan Diego"},
              {"when": "1983", "text": "First Costco\nSeattle"},
              {"when": "1985", "text": "$1.50 hot dog\n+ soda"},
              {"when": "1993", "text": "Costco merges\nwith Price Club"},
              {"when": "2026", "text": "939\nwarehouses"}])
scene("His insight was simple. Charge a small fee to join, keep prices barely above cost, and the people who pay to get in will come back again and again to get their money's worth.",
      type="flywheel", title="Sol Price's idea", center="FEE",
      steps=["Pay to join", "Low prices", "Shop often", "Renew"])
scene("Costco opened its first warehouse in Seattle in nineteen eighty-three, copying the model and pushing it further. Ten years later, the two companies merged.",
      type="versus", title="Two founders, one idea",
      left={"label": "Price Club", "value": "1976", "sub": "San Diego", "color": "blue"},
      right={"label": "Costco", "value": "1983", "sub": "Seattle", "color": "green"},
      verdict="Merged in 1993")
scene("Today, Costco runs nine hundred and thirty-nine warehouses. Most are in the United States, but there are more than a hundred in Canada and more than a hundred and seventy in other countries.",
      type="hbars", title="Costco warehouses, end of fiscal 2026", format="num",
      items=[{"label": "US & Puerto Rico", "value": 647, "color": "green"},
             {"label": "Other countries", "value": 177, "color": "blue"},
             {"label": "Canada", "value": 115, "color": "gold"}])

# ---------------------------------------------------------------- 6
scene("Chapter six. What could go wrong?", type="chapter", n=6, title="What could go wrong")
scene("No model is bulletproof. The biggest risk is simple. If members stop renewing, half the profit is at stake.",
      type="share", title="Profit that depends on renewals",
      rows=[{"label": "Membership fees", "share": fee_share_op, "color": "red", "dp": 0}])
scene("There's also competition. Rival warehouse clubs, and online stores that deliver bulk goods to your door, all fight for the same shoppers.",
      type="bullets", title="Pressure points", color="red",
      items=["Members stop renewing", "Rival warehouse clubs", "Online bulk delivery", "Fee hikes that go too far"])
scene("Growth is the other question. Costco grows mainly by opening new warehouses and signing up new members. That works for decades, but every new building costs money, and the best locations get taken first.",
      type="columns", title="Paid members (millions)", format="num", highlight=2, color="blue",
      items=[{"label": str(y), "value": v / 1e6, "display": f"{v / 1e6:.1f}M"} for y, v in PAID.items()],
      note="Growth so far is steady, but it must be earned year after year")
scene("And Costco can only push the fee so far. Raise it too much, and the deal stops feeling like a deal. That's why increases have been small and years apart.",
      type="quote", text="The fee only works\nwhile the deal feels fair.", first_color="text", color="gold")

# ---------------------------------------------------------------- 7
scene("Chapter seven. What it means for you.", type="chapter", n=7, title="What it means for you")
scene("First, as a shopper. Is a basic membership even worth it? It depends on how much you save. Say Costco saves you five percent compared with your usual store. That's just an example; your savings could be higher or lower.",
      type="stat", value="5%", label="example saving vs your usual store", sub="an assumption, not a Costco figure", color="gold")
scene("At five percent, you'd need to spend about thirteen hundred dollars a year, roughly a hundred and ten a month, just to win back the sixty-five dollar fee.",
      type="equation", title="Gold Star break-even (at a 5% saving)",
      lines=[{"text": "$65 fee ÷ 5% saved", "color": "muted", "size": 84},
             {"text": f"= ${gold_breakeven:,.0f} / year", "color": "gold", "size": 120},
             {"text": f"about ${gold_breakeven / 12:,.0f} a month", "color": "text", "size": 56}])
scene("And watch out for the bulk trap. A cheaper price per unit only saves you money if you actually use it all. Thirty-six rolls you need is a deal. A giant tub of food you throw away is not.",
      type="versus", title="The bulk-buying trap",
      left={"label": "Bought in bulk, all used", "value": "Saved", "sub": "lower price per unit", "color": "green"},
      right={"label": "Bought in bulk, half wasted", "value": "Lost", "sub": "paid for what you binned", "color": "red"},
      verdict="Price per unit used is what counts")
scene("Now the upgrade. Executive gives two percent back on most purchases. The upgrade costs sixty-five dollars more, so it only pays off if you spend over three thousand two hundred and fifty dollars a year at Costco.",
      type="equation", title="Is Executive worth it?",
      lines=[{"text": "$65 extra ÷ 2% back", "color": "muted", "size": 84},
             {"text": "= $3,250 / year", "color": "gold", "size": 120},
             {"text": f"about ${breakeven / 12:,.0f} a month at Costco", "color": "text", "size": 56}])
scene("Here's how that plays out. Spend two thousand a year, and you get forty dollars back. Not worth it. Spend six thousand, and you get one hundred and twenty. That's fifty-five dollars ahead.",
      type="table", title="Executive upgrade: $65 extra per year",
      header=["You spend / yr", "2% back", "Net"],
      rows=[["$2,000", "$40", "−$25"], ["$3,250", "$65", "$0"], ["$6,000", "$120", "+$55"]],
      highlight_row=1, col_colors={"1": "green"})
scene("The reward is capped at one thousand two hundred and fifty dollars a year, which you'd only hit by spending sixty-two thousand five hundred. Most households are nowhere near that.",
      type="count", to=cap_spend, prefix="$", label="spend needed to hit the $1,250 reward cap", sub="Executive · US", color="gold")
scene("Second, as someone learning how business works. The best businesses often don't profit from what they sell. They profit from the relationship. Think Amazon Prime, gyms, or software subscriptions.",
      type="bullets", title="Same idea, different companies",
      items=["Amazon Prime", "Warehouse clubs", "Gym memberships", "Software subscriptions"])
scene("So next time you see a business with surprisingly low prices, ask: what are they really selling? Often, it's access.",
      type="quote", text="Low prices?\nAsk what they're really selling.", first_color="text", color="gold")
scene("Costco sells products at almost no profit, and charges you for the right to shop. That's the whole secret.",
      type="equation", lines=[{"text": "Sell products at cost.", "color": "text", "size": 96},
                              {"text": "Charge for access.", "color": "gold", "size": 110}])
scene("If you learned something, subscribe. We break down how money really works, every week.",
      type="cta", lines=["How money", "really works."], sub="Subscribe for weekly breakdowns")

for a, b in zip(S, S[1:]):
    assert a["visual"]["type"] != b["visual"]["type"], ("same visual twice in a row", a["say"][:40])

spec = {
    "id": "L001_costco", "currency": "usd", "voice": "af_heart", "speed": 1.0, "gap": 0.35,
    "badge": "BUSINESS BREAKDOWN",
    "disclaimer": "Figures: Costco FY2026 results & 10-K · for education, not investment advice",
    "title": "How Costco Makes Money (It's Not the Groceries)",
    "intro_chapter": "Intro",
    "thumbnail": {"big": "$5.9B", "line": "COSTCO'S REAL BUSINESS", "tag": "IT'S NOT GROCERIES", "color": "gold"},
    "description": (
        "Costco sold about $297 billion of products in fiscal 2026, yet the products themselves earned it only "
        "about 2 cents of operating profit per dollar. The real engine is membership: $5.9 billion in fees, less "
        "than 2% of revenue but about half of operating profit. Here's how the model works, how it started, what "
        "could break it, and what it means for you as a shopper.\n\n"
        "Sources:\n"
        "- Costco FY2026 Q4 and full-year results (52 weeks ended Aug 30, 2026): https://investor.costco.com\n"
        "- Costco FY2026 Form 10-K (members, renewal rates, Executive share of sales, SKUs, warehouses): "
        "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000909832\n"
        "- Membership fee increase effective Sept 1, 2024 (Costco announcement)\n"
        "Markup caps are as reported by press and analysts, not company filings.\n\n"
        "For education only. Not financial or investment advice.\n\n"
        "#costco #businessmodel #businessbreakdown #howcompaniesmakemoney #personalfinance"
    ),
    "tags": ["costco", "business model", "how costco makes money", "membership business", "business breakdown",
             "costco executive membership", "kirkland signature", "economics explained", "retail business"],
    "localizations": {
        "es": {"title": "Cómo gana dinero Costco (no es vendiendo comida)",
               "summary": "Costco vendió unos $297 mil millones en productos en el año fiscal 2026, pero esos productos le dejaron solo unos 2 centavos de beneficio operativo por dólar. "
                          "El verdadero motor son las membresías: $5.9 mil millones en cuotas, menos del 2% de los ingresos pero cerca de la mitad del beneficio operativo."},
        "pt": {"title": "Como a Costco ganha dinheiro (não é vendendo comida)",
               "summary": "A Costco vendeu cerca de $297 bilhões em produtos no ano fiscal de 2026, mas esses produtos renderam só uns 2 centavos de lucro operacional por dólar. "
                          "O verdadeiro motor é a assinatura: $5.9 bilhões em taxas, menos de 2% da receita, mas cerca de metade do lucro operacional."},
        "hi": {"title": "Costco पैसा कैसे कमाती है (किराने से नहीं)",
               "summary": "वित्त वर्ष 2026 में Costco ने करीब $297 अरब का सामान बेचा, पर इन प्रोडक्ट्स से हर डॉलर पर सिर्फ़ करीब 2 सेंट का ऑपरेटिंग मुनाफ़ा हुआ। "
                          "असली इंजन है मेंबरशिप: $5.9 अरब की फीस, जो कमाई का 2% से भी कम है पर ऑपरेटिंग मुनाफ़े का करीब आधा।"},
        "id": {"title": "Cara Costco Cari Untung (Bukan dari Jualan Makanan)",
               "summary": "Costco menjual produk senilai sekitar $297 miliar pada tahun fiskal 2026, tapi produk itu hanya menghasilkan sekitar 2 sen laba operasi per dolar. "
                          "Mesin sebenarnya adalah keanggotaan: $5.9 miliar dari iuran, kurang dari 2% pendapatan tapi sekitar separuh laba operasi."},
        "de": {"title": "Wie Costco Geld verdient (nicht mit Lebensmitteln)",
               "summary": "Costco verkaufte im Geschäftsjahr 2026 Waren für rund $297 Milliarden, verdiente daran aber nur etwa 2 Cent operativen Gewinn pro Dollar. "
                          "Der eigentliche Motor sind die Mitgliedschaften: $5.9 Milliarden an Gebühren, weniger als 2% des Umsatzes, aber etwa die Hälfte des operativen Gewinns."},
        "fr": {"title": "Comment Costco gagne de l'argent (pas avec les courses)",
               "summary": "Costco a vendu environ $297 milliards de produits sur l'exercice 2026, mais ces produits ne lui ont rapporté qu'environ 2 cents de bénéfice d'exploitation par dollar. "
                          "Le vrai moteur, ce sont les abonnements : $5.9 milliards de cotisations, moins de 2 % du chiffre d'affaires mais environ la moitié du bénéfice d'exploitation."},
    },
    "scenes": S,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "L001_costco.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out, len(S), "scenes,", sum(len(s["say"].split()) for s in S), "words")
