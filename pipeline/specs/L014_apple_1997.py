"""Long-form L014 (case study): Apple in 1997, the turnaround that saved the company.

Sources (checked 2026-11-25). Apple's fiscal year ends in late September. Dollar figures in $.
  [K96] Apple Form 10-K for fiscal 1996 (filed Dec 19, 1996): 10,896 regular employees at Sept 27, 1996.
  [K97] Apple Form 10-K for fiscal 1997 (filed Dec 5, 1997): net sales 1995/1996/1997 $11,062M / $9,833M / $7,081M;
        net loss 1996 $816M, 1997 $1,045M; cash, cash equivalents and short-term investments $1,745M (Sept 27,
        1996) -> $1,459M (Sept 26, 1997); NeXT acquired Feb 4, 1997, total price $427M (cash to shareholders $319M,
        1.5M shares ~$25M, options ~$16M, cash to NeXT debtholders $56M, closing costs $9M, net liabilities $2M),
        $375M charged at once as in-process R&D; Q2 1997 net loss $708M (incl. the $375M write-off and a $155M
        restructuring charge); quarterly results 1996-97; S&P cut senior/subordinated debt to B-/CCC (Oct 1997);
        "significant voluntary employee turnover"; Microsoft agreements Aug 1997 (patent cross-licences; for five
        years Microsoft makes Office and Internet Explorer for the Mac OS; Internet Explorer the default browser;
        Microsoft bought $150M of non-voting convertible preferred stock); Aug 6, 1997 new board, all but two
        directors replaced (new: Campbell, Ellison, Jobs, York); Amelio resigned Jul 9, 1997; agreement to buy Power
        Computing's Mac OS licence + customer database, ~$110M total ($100M in stock); 8,437 regular employees.
  [K98] Apple Form 10-K405 for fiscal 1998 (filed Dec 23, 1998): net sales $5,941M, net income $309M; profit in all
        four quarters ($47M, $55M, $101M, $106M); "simplified its product line, moving from approximately 15
        separate individual products to three main product families"; MessagePad (Newton) and eMate discontinued,
        imaging and display products "significantly reduced"; inventory $437M -> $78M, days of supply 31 -> 6;
        cash flow from lower inventories $359M; cash etc. $2,300M; gross margin 19% -> 25%; iMac introduced Aug
        1998, 278,000 iMacs = 33% of Macs shipped in Q4 1998; 6,658 regular employees; restructuring "began in
        1996"; officers: Fred Anderson (CFO, joined Apr 1996), Tim Cook (worldwide operations, joined Mar 1998
        from Compaq), Jon Rubinstein (hardware, joined Feb 1997, ex-NeXT), Avie Tevanian (software, from NeXT).
  [K99] Apple Form 10-K for fiscal 1999 (filed Dec 22, 1999): ~1.8M iMacs sold in fiscal 1999; product lines
        Power Macintosh (pro), PowerBook (pro portable), iMac (consumer), iBook ("iMac to Go", Jul 1999).
  [K01] Apple Form 10-K405 for fiscal 2001: Mac OS X released during 2001.
  [K26] Apple Form 10-K for fiscal 2026 (filed Nov 3, 2026; year ended Sept 26, 2026): net sales $478,834M
        (iPhone $254,098M, Services $123,301M, Mac $37,929M, iPad $27,929M, Wearables/Home/Accessories $35,577M);
        net income $132,175M; ~167,000 full-time equivalent employees.
  [PR96] Apple press release, Dec 20, 1996 (exhibit to 8-K filed Dec 24, 1996): agreement to buy NeXT; Jobs to
        return; NEXTSTEP elements to become part of Mac OS.
  [PR97] Apple press releases Jul 9, 1997 (Amelio resigns) and Sept 16, 1997 (Jobs named interim CEO "until a new
        CEO is named"), exhibits to 8-Ks.
  [MS]  Microsoft press release, Aug 6, 1997 (non-voting stock, Office for Mac, IE default browser, cross-licence).
  [MAC] Maclean's, Aug 18, 1997 (Canadian Encyclopedia archive): announcement at Macworld Boston "initially drew
        boos and jeers"; Jobs: "We have to let go of the notion that for Apple to win, Microsoft has to lose."
        (Stratechery's 2013 transcript of the keynote video has "this notion"; same meaning.)
  [IMAC] Apple press release May 6, 1998 (via MacTech) and CNN (May 6, 1998): iMac $1,299; Apple press release
        Aug 19, 1998 (via MacTech): on shelves Saturday, Aug 15, 1998.
  [IVE] CNN / Macworld (Jun 27, 2019): Jony Ive joined Apple in 1992, led industrial design; the iMac was his
        team's first big project.
  [CHM] Computer History Museum, "The Deep History of Your Apps" (2016): Apple bought NeXT to make NeXTSTEP the
        basis of Mac OS X; OS X in turn became the basis of the iPhone's operating system.
  [POD] Apple press releases Oct 23, 2001 (iPod) and Jan 9, 2007 (iPhone).
  [D8]  The Next Web (Jun 2, 2010): Jobs at the D8 conference: "We were 90 days from going bankrupt." (His
        recollection 13 years later; not in any filing, so we label it as his memory.)
  [ISA] Walter Isaacson, "Steve Jobs" (2011): Jobs drew a two-by-two grid (consumer/pro x desktop/portable). We
        present this as the biographer's account; the four product lines themselves are from [K99].
Left out (not confirmed from a primary or reputable source): Apple's exact share-price moves, the "fifteen to
four" wording (the filing says ~15 products to three families), how many iMacs went to first-time buyers.
"""
import json, os
from collections import Counter

# ---- Apple filings (fiscal years, $)
SALES = {1995: 11_062e6, 1996: 9_833e6, 1997: 7_081e6, 1998: 5_941e6}      # [K97] [K98]
NET = {1996: -816e6, 1997: -1_045e6, 1998: 309e6}                              # [K97] [K98]
CASH = {1996: 1_745e6, 1997: 1_459e6, 1998: 2_300e6}                           # [K97] [K98]
EMPLOYEES = {1996: 10_896, 1997: 8_437, 1998: 6_658}                           # [K96] [K97] [K98]
Q_1997 = [-120e6, -708e6, -56e6, -161e6]       # fiscal 1997 Q1..Q4 net income [K97]
Q_1998 = [47e6, 55e6, 101e6, 106e6]            # fiscal 1998 Q1..Q4 net income [K98]
Q4_1996 = 25e6                                 # last profitable quarter before the turnaround [K97]
NEXT_PARTS = {"Cash to owners": 319e6, "Stock": 25e6, "Options": 16e6, "Debt paid": 56e6,
              "Costs & other": 9e6 + 2e6}      # [K97]
NEXT_TOTAL, NEXT_IPRD = 427e6, 375e6           # [K97]
NEXT_ANNOUNCED = 400e6                         # [PR96] "$400 million" headline price
Q2_1997_LOSS, Q2_1997_RESTRUCT = 708e6, 155e6  # [K97]
MSFT = 150e6                                   # [K97] [MS]
MSFT_YEARS = 5                                 # [K97]
PCC_PRICE, PCC_STOCK = 110e6, 100e6            # [K97] Power Computing deal
PRODUCTS_BEFORE, FAMILIES_AFTER = 15, 3        # [K98] "approximately 15" -> "three main product families"
LINES_1999 = 4                                 # [K99] iMac, iBook, Power Mac, PowerBook
INV = {1997: 437e6, 1998: 78e6}                # [K98]
INV_DAYS = {1997: 31, 1998: 6}                 # [K98]
INV_CASH_1998 = 359e6                          # [K98] cash flow statement, decrease in inventories
GM = {1997: 0.19, 1998: 0.25}                  # [K98]
IMAC_PRICE = 1_299                             # [IMAC]
IMAC_Q4_98, IMAC_SHARE_Q4_98 = 278_000, 0.33   # [K98]
IMAC_FY99 = 1.8e6                              # [K99]
# ---- Apple today [K26]
FY26 = dict(sales=478_834e6, net=132_175e6, iphone=254_098e6, services=123_301e6, mac=37_929e6,
            ipad=27_929e6, wear=35_577e6)
EMP_26 = 167_000

# ---- derived numbers (every spoken one is asserted)
sales_drop_95_97 = 1 - SALES[1997] / SALES[1995]
loss_2y = -(NET[1996] + NET[1997])
cash_drop_97 = CASH[1996] - CASH[1997]
profit_per_day_26 = FY26["net"] / 365
days_to_earn_97_loss = -NET[1997] / profit_per_day_26
msft_share_of_cash = MSFT / CASH[1997]
emp_cut = 1 - EMPLOYEES[1998] / EMPLOYEES[1996]
inv_cut = INV[1997] - INV[1998]
inv_left = INV[1998] / INV[1997]
iphone_share = FY26["iphone"] / FY26["sales"]
sales_mult = FY26["sales"] / SALES[1997]

assert abs(sum(FY26[k] for k in ("iphone", "services", "mac", "ipad", "wear")) - FY26["sales"]) < 1e6  # ties out
assert abs(sum(NEXT_PARTS.values()) - NEXT_TOTAL) < 1e6        # NeXT price parts add up to $427M
assert abs(sum(Q_1997) - NET[1997]) < 1e6 and abs(sum(Q_1998) - NET[1998]) < 1e6   # quarters add up
assert all(q < 0 for q in Q_1997) and all(q > 0 for q in Q_1998) and Q4_1996 > 0   # "four losing quarters in a row"
assert 1.04e9 < -NET[1997] < 1.05e9         # "over a billion dollars" / "one point oh four billion"
assert 0.35 < sales_drop_95_97 < 0.37       # "more than a third"
assert 1.85e9 < loss_2y < 1.9e9             # "nearly one point nine billion"
assert 285e6 < cash_drop_97 < 287e6         # "about two hundred and eighty-six million"
assert 132e9 < FY26["net"] < 132.5e9        # "about a hundred and thirty-two billion"
assert 2.8 < days_to_earn_97_loss < 3       # "in under three days"
assert 0.09 < msft_share_of_cash < 0.11     # "about a tenth"
assert 0.385 < emp_cut < 0.395              # "nearly four in ten"
assert inv_cut == INV_CASH_1998 == 359e6    # "about three hundred and fifty-nine million"
assert inv_cut / MSFT > 2                   # "more than twice what Microsoft invested"
assert 0.17 < inv_left < 0.18 and 1 - inv_left > 0.8   # "more than eighty percent"
assert 0.52 < iphone_share < 0.54           # "over half"
assert 67 < sales_mult < 68                 # "nearly sixty-eight times"
assert NET[1998] > 0 and SALES[1998] < SALES[1997]   # "sales still shrinking in 1998" (balance)
assert 9_000 / 3_000 == 3                   # runway example
print(f"sales -{sales_drop_95_97:.1%} · 2y loss ${loss_2y/1e9:.2f}B · cash -{cash_drop_97/1e6:.0f}M · "
      f"FY26 ${profit_per_day_26/1e6:.0f}M/day -> 1997 loss in {days_to_earn_97_loss:.2f} days · MSFT "
      f"{msft_share_of_cash:.1%} of cash · staff -{emp_cut:.1%} · inventory -{inv_cut/1e6:.0f}M "
      f"({1-inv_left:.0%}) · iPhone {iphone_share:.1%} · sales x{sales_mult:.1f}")

S = []
def scene(say, **visual):
    S.append({"say": say, "visual": visual})

# ---------------------------------------------------------------- Hook (retention: payoff in the first 10 s,
# then the promise, then a tease of the best reveal, which pays off in chapter 5: the inventory cut)
scene("In nineteen ninety-seven, Apple lost over a billion dollars in a single year. Its sales had fallen by more than a third in two years.",
      type="count", to=-NET[1997] / 1e9, dp=3, prefix="−$", suffix="B", label="Apple's net loss, fiscal 1997",
      sub="Apple 10-K · sales down 36% in two years", color="red")
scene("In its latest fiscal year, which ended in September, Apple's profit was about a hundred and thirty-two billion dollars. At that pace, it earns back that whole nineteen ninety-seven loss in under three days.",
      type="equation", title="Apple, fiscal 2026",
      lines=[{"text": "$132.2B profit ÷ 365 days", "color": "muted", "size": 80},
             {"text": f"≈ ${profit_per_day_26 / 1e6:.0f}M a day", "color": "green", "size": 120},
             {"text": f"1997's loss: back in {days_to_earn_97_loss:.1f} days", "color": "gold", "size": 64}])
scene("So how did a company with shrinking sales and junk-rated debt turn around? Using Apple's own filings, we'll walk through the deal with its biggest rival, the products it killed, the computer that brought it back, and the team behind it.",
      type="photo", layout="full", file="assets/photos/apple_infinite_loop_hq.jpg", focus=[0.5, 0.45],
      value="Apple in 1997", label="the turnaround, from the filings", color="gold")
scene("And by the end, you'll see the least glamorous fix in those filings. It freed more than twice as much cash as Microsoft's famous investment.",
      type="stat", value="2×", label="more cash than Microsoft put in", sub="the boring fix · chapter five", color="gold")

# ---------------------------------------------------------------- 1
scene("Chapter one. The hole.", type="chapter", n=1, title="The hole")
scene("Start with sales. In fiscal nineteen ninety-five, Apple sold about eleven billion dollars' worth of products. Two years later, about seven billion. And it kept falling, to under six billion in nineteen ninety-eight.",
      type="line", title="Apple net sales by fiscal year", x=list(SALES),
      series=[{"label": "Apple", "values": list(SALES.values()), "color": "red"}])
scene("The losses were huge. Eight hundred and sixteen million dollars in fiscal ninety-six. One point oh four billion in ninety-seven. Nearly one point nine billion dollars gone in two years.",
      type="stat_grid", title="Apple's net losses",
      items=[{"value": "−$816M", "label": "fiscal 1996", "sub": "year to Sept 1996", "color": "red"},
             {"value": "−$1.045B", "label": "fiscal 1997", "sub": "year to Sept 1997", "color": "red"},
             {"value": f"−${loss_2y / 1e9:.2f}B", "label": "two years", "sub": "combined", "color": "gold"}])
scene("Steve Jobs later said, at a conference in twenty ten, that Apple had been ninety days from going bankrupt. That's his memory, thirteen years on. The filings tell a more precise story.",
      type="quote", text="\"We were 90 days from\ngoing bankrupt.\"", first_color="text", color="text",
      source="Steve Jobs, D8 conference, 2010 (his recollection)")
scene("In September nineteen ninety-six, Apple had about one point seven five billion dollars in cash and short-term investments. A year later, one point four six billion. Down about two hundred and eighty-six million dollars, even after a cash injection we'll get to.",
      type="versus", title="Cash & short-term investments",
      left={"label": "Sept 1996", "value": "$1.75B", "sub": "Apple 10-K", "color": "blue"},
      right={"label": "Sept 1997", "value": "$1.46B", "sub": f"down ${cash_drop_97 / 1e6:.0f}M", "color": "red"},
      verdict="Not broke. But bleeding.")
scene("Lenders noticed. In October nineteen ninety-seven, Standard and Poor's cut Apple's debt ratings to B minus and triple C, deep in junk territory. Apple's own filing warned of significant voluntary employee turnover. And its old operating system was falling behind. Back in late nineteen ninety-six, Apple had already gone shopping for a new one.",
      type="bullets", title="Warning signs, 1997", color="red",
      items=["Debt cut to junk (S&P: B− / CCC)", "Staff leaving", "Sales falling every year", "An aging operating system"])

# ---------------------------------------------------------------- 2
scene("Chapter two. The Next bet.", type="chapter", n=2, title="The NeXT bet")
scene("On December twentieth, nineteen ninety-six, Apple, then run by chief executive Gil Uh-mellio, agreed to buy Next, the company Steve Jobs started after he left Apple. The deal closed in February nineteen ninety-seven.",
      type="timeline", title="Apple, 1996–97",
      events=[{"when": "Dec 1996", "text": "Deal to buy\nNeXT"},
              {"when": "Feb 1997", "text": "NeXT deal\ncloses"},
              {"when": "Jul 1997", "text": "CEO Amelio\nresigns"},
              {"when": "Sep 1997", "text": "Jobs named\ninterim CEO"}])
scene("The headline price was four hundred million dollars. Apple's annual report puts the full cost at four hundred and twenty-seven million: mostly cash to Next's owners, plus stock, options, and paying off Next's debt.",
      type="waterfall", title="What Apple paid for NeXT",
      steps=[{"label": "Cash", "value": NEXT_PARTS["Cash to owners"], "kind": "start", "display": "$319M"},
             {"label": "Stock", "value": NEXT_PARTS["Stock"], "kind": "plus", "display": "+$25M"},
             {"label": "Options", "value": NEXT_PARTS["Options"], "kind": "plus", "display": "+$16M"},
             {"label": "Debt paid", "value": NEXT_PARTS["Debt paid"], "kind": "plus", "display": "+$56M"},
             {"label": "Costs, other", "value": NEXT_PARTS["Costs & other"], "kind": "plus", "display": "+$11M"},
             {"label": "Total", "value": NEXT_TOTAL, "kind": "total", "display": "$427M"}])
scene("And three hundred and seventy-five million of it was written off straight away, as research still in progress. Add a restructuring charge, and Apple lost seven hundred and eight million dollars in the first three months of nineteen ninety-seven alone.",
      type="stat", value=f"−${Q2_1997_LOSS / 1e6:.0f}M", label="Apple's loss in one quarter (Jan–Mar 1997)",
      sub="incl. $375M NeXT write-off + $155M restructuring", color="red")
scene("So what did Apple really buy? People and software. Avie Tevanian came from Next to run software. Jon Rubinstein, a former Next hardware chief, took over hardware. And to be fair to Uh-mellio, his team had already hired finance chief Fred Anderson, and started the cost cuts in nineteen ninety-six.",
      type="table", title="The team taking shape",
      header=["Who", "Role", "Joined"],
      rows=[["Avie Tevanian", "Software", "1997, NeXT"], ["Jon Rubinstein", "Hardware", "1997, ex-NeXT"],
            ["Fred Anderson", "Finance (CFO)", "April 1996"], ["Steve Jobs", "Adviser", "1997, NeXT"]],
      col_colors={"1": "green", "2": "muted"})
scene("In July nineteen ninety-seven, Uh-mellio resigned. In September, the board named Jobs interim chief executive, in its words, until a new one was found. But new software takes years. Apple needed help sooner, and it came from its fiercest rival.",
      type="photo", layout="side", file="assets/photos/steve_jobs_stage.jpg", focus=[0.55, 0.3],
      value="Interim CEO", label="Steve Jobs, Sept 16, 1997", sub="\"until a new CEO is named\" · Amelio resigned in July", color="gold")

# ---------------------------------------------------------------- 3
scene("Chapter three. The rival's lifeline.", type="chapter", n=3, title="The rival's lifeline")
scene("August sixth, nineteen ninety-seven. On stage at the Macworld show in Boston, Jobs announced that Microsoft would invest one hundred and fifty million dollars in Apple.",
      type="photo", layout="full", file="assets/photos/microsoft_campus_sign.jpg", focus=[0.5, 0.4],
      value="$150M", label="Microsoft's investment in Apple · Aug 6, 1997", sub="announced Aug 6, 1997 · Macworld Boston", color="blue")
scene("Microsoft bought non-voting shares, so it got no say in running Apple. It promised to keep making Office for the Mac for five years. Apple made Internet Explorer the Mac's default browser. And the two companies cross-licensed their patents.",
      type="bullets", title="The 1997 Apple–Microsoft deal",
      items=["$150M of non-voting stock", "Office for Mac, for 5 years", "Internet Explorer as default", "Patent cross-license"])
scene("Here's the surprising part. The cash was small: about a tenth of Apple's cash pile. Apple's own filing calls Microsoft an important developer of Mac software. A five-year promise on Office mattered more than the money.",
      type="share", title="Microsoft's $150M vs Apple's cash (Sept 1997)",
      rows=[{"label": "Share of Apple's $1.46B cash pile", "share": msft_share_of_cash, "color": "blue", "dp": 0}],
      note="Source: Apple 10-K, fiscal 1997")
scene("Not everyone liked it. Maclean's reported that the announcement drew boos and jeers. Jobs told the crowd: We have to let go of the notion that for Apple to win, Microsoft has to lose.",
      type="quote", text="\"We have to let go of the notion\nthat for Apple to win,\nMicrosoft has to lose.\"", first_color="text", color="gold",
      source="Steve Jobs, Macworld Boston, Aug 6, 1997 (via Maclean's)")
scene("The same day, Apple announced a new board. All but two directors were replaced. The money and the promise bought time. What Apple did with that time was cut, hard.",
      type="stat_grid", title="August 1997",
      items=[{"value": "$150M", "label": "from Microsoft", "sub": "non-voting", "color": "blue"},
             {"value": f"{MSFT_YEARS} yrs", "label": "of Office for Mac", "sub": "promised", "color": "green"},
             {"value": "All but 2", "label": "directors replaced", "sub": "new board", "color": "gold"}])

# ---------------------------------------------------------------- 4
scene("Chapter four. Cutting to four boxes.", type="chapter", n=4, title="Cutting to four boxes")
scene("Apple's nineteen ninety-eight annual report says it simplified its product line, from about fifteen separate products to three main product families.",
      type="versus", title="Apple's product line",
      left={"label": "Before", "value": f"~{PRODUCTS_BEFORE}", "sub": "separate products", "color": "red"},
      right={"label": "By 1998", "value": f"{FAMILIES_AFTER}", "sub": "main product families", "color": "green"},
      verdict="Source: Apple 10-K, fiscal 1998")
scene("Out went the Newton handheld and the eMate. Many printers and monitors went too. And Apple ended the Mac clone business, agreeing to buy Power Computing's Mac license and customer list for about a hundred and ten million dollars, mostly in stock.",
      type="photo", layout="side", file="assets/photos/apple_newton_emate.jpg", focus=[0.5, 0.5],
      title="What Apple cut", value="Cut", label="Newton MessagePad and eMate",
      sub="plus many printers and monitors · Mac clones (Power Computing, ~$110M)", color="red")
scene("Jobs' biographer, Walter Isaacson, describes him drawing a simple grid: consumer and pro, desktop and portable. By nineteen ninety-nine, Apple's filing listed four computer lines filling those boxes: iMac, iBook, Power Mac, and PowerBook.",
      type="table", title="Four boxes (Apple's Macs by 1999)",
      header=["", "Desktop", "Portable"],
      rows=[["Consumer", "iMac", "iBook"], ["Pro", "Power Mac", "PowerBook"]],
      col_colors={"1": "green", "2": "gold"})
scene("The cuts hit people, too. Apple had about ten thousand nine hundred regular employees in nineteen ninety-six, eight thousand four hundred a year later, and six thousand seven hundred by nineteen ninety-eight. Nearly four in ten jobs, gone in two years.",
      type="columns", title="Apple regular employees (September each year)", format="num", highlight=2, color="blue",
      items=[{"label": str(y), "value": v, "display": f"{v:,}"} for y, v in EMPLOYEES.items()],
      note="Source: Apple 10-K filings, fiscal 1996–1998")
scene("Fewer products meant every bet had to count. The first big one was a strange-looking, all-in-one computer.",
      type="equation",
      lines=[{"text": "Fewer products", "color": "muted", "size": 90},
             {"text": "= every bet counts", "color": "gold", "size": 110}])

# ---------------------------------------------------------------- 5
scene("Chapter five. The iMac, and the boring fix.", type="chapter", n=5, title="The iMac, and the boring fix")
scene("In May nineteen ninety-eight, Apple unveiled the iMac: an all-in-one computer, built for getting online, for twelve hundred and ninety-nine dollars. It went on sale on August fifteenth.",
      type="photo", layout="side", file="assets/photos/imac_g3_bondi_blue.jpg", focus=[0.4, 0.5],
      value=f"${IMAC_PRICE:,}", label="the iMac", sub="unveiled May 6, 1998 · on sale Aug 15, 1998", color="green")
scene("It came from a team. Jony Ive, at Apple since nineteen ninety-two, led the industrial design group that shaped its look. Jon Rubinstein's engineers built the hardware.",
      type="bullets", title="Who built the iMac",
      items=["Design: Jony Ive's team", "Hardware: Jon Rubinstein's team", "Focus and launch: Steve Jobs"])
scene("In its first quarter on sale, Apple shipped two hundred and seventy-eight thousand iMacs. That was a third of all the Macs it shipped. The next year, it sold about one point eight million.",
      type="donut", title="Macs shipped, July–Sept 1998",
      segments=[{"label": "iMac (278,000)", "value": IMAC_SHARE_Q4_98, "color": "green"},
                {"label": "Other Macs", "value": 1 - IMAC_SHARE_Q4_98, "color": "slate"}],
      center="33%", center_sub="were iMacs")
scene("And Apple was profitable again. After four losing quarters in a row, it made money in every quarter of fiscal ninety-eight. Notice the profits started before the iMac even shipped. Cost cuts came first, helped by a faster Power Mac G3 line launched in late nineteen ninety-seven.",
      type="columns", title="Apple quarterly profit, fiscal 1998", highlight=3,
      items=[{"label": f"Q{i + 1}", "value": q, "display": f"${q / 1e6:.0f}M"} for i, q in enumerate(Q_1998)],
      note="Power Mac G3 from Q1 · iMac shipped in Q4 (Aug 1998) · Source: Apple 10-K, fiscal 1998")
scene("Now the least glamorous fix. Inventory: unsold computers and parts. Apple cut it from four hundred and thirty-seven million dollars to just seventy-eight million in one year. From thirty-one days of supply, to six.",
      type="hbars", title="Apple inventory (end of fiscal year)",
      items=[{"label": "Sept 1997", "value": INV[1997], "display": f"$437M · {INV_DAYS[1997]} days", "color": "red"},
             {"label": "Sept 1998", "value": INV[1998], "display": f"$78M · {INV_DAYS[1998]} days", "color": "green"}])
scene("That released about three hundred and fifty-nine million dollars in cash. More than twice what Microsoft invested. Fewer products made it possible, along with standard parts, fewer warehouses, and a new operations chief hired from Compaq in March nineteen ninety-eight: Tim Cook.",
      type="equation", title="The boring fix",
      lines=[{"text": "$437M − $78M inventory", "color": "muted", "size": 80},
             {"text": f"= ${inv_cut / 1e6:.0f}M of cash freed", "color": "green", "size": 110},
             {"text": f"{inv_cut / MSFT:.1f}× Microsoft's $150M", "color": "gold", "size": 72}])
scene("By September nineteen ninety-eight, Apple had made three hundred and nine million dollars for the year, and its cash had grown to two point three billion. Apple was alive. But it was still a shrinking computer company. Real growth would come later, built on the software it agreed to buy in nineteen ninety-six.",
      type="stat_grid", title="Apple, fiscal 1998",
      items=[{"value": "+$309M", "label": "net profit", "sub": "after −$1.045B", "color": "green"},
             {"value": "$2.3B", "label": "cash & investments", "sub": "up from $1.46B", "color": "gold"},
             {"value": "25%", "label": "gross margin", "sub": "up from 19%", "color": "blue"}])

# ---------------------------------------------------------------- 6
scene("Chapter six. From iMac to iPhone.", type="chapter", n=6, title="From iMac to iPhone")
scene("Next's software became the base of Mac O S Ten, released in two thousand one. That same year, Apple introduced the iPod. In January two thousand seven came the iPhone, whose software, the Computer History Museum notes, was built on Mac O S Ten.",
      type="timeline", title="What the turnaround made possible",
      events=[{"when": "1998", "text": "iMac"},
              {"when": "2001", "text": "Mac OS X\n(NeXT roots)"},
              {"when": "2001", "text": "iPod"},
              {"when": "2007", "text": "iPhone"}])
scene("Notice the loop. Focus made better products. Better products brought back profit and cash. And that cash paid for bigger, riskier bets, like a music player, and later a phone. Each turn made the next one possible.",
      type="flywheel", title="The loop 1997 started", center="FOCUS",
      steps=["Fewer products", "Better products", "Profit and cash", "Bigger bets"])
scene("Today, the iPhone alone brought in about two hundred and fifty-four billion dollars in fiscal twenty twenty-six. That's over half of Apple's revenue. Services added another hundred and twenty-three billion.",
      type="donut", title="Apple revenue, fiscal 2026 ($478.8B)",
      segments=[{"label": "iPhone", "value": FY26["iphone"], "color": "green"},
                {"label": "Services", "value": FY26["services"], "color": "gold"},
                {"label": "Mac", "value": FY26["mac"], "color": "blue"},
                {"label": "Wearables, home", "value": FY26["wear"], "color": "slate"},
                {"label": "iPad", "value": FY26["ipad"], "color": "red"}],
      center=f"{iphone_share:.0%}", center_sub="from iPhone")
scene("Put the two years side by side. Before inflation, revenue is up nearly sixty-eight times. A billion-dollar loss became a hundred and thirty-two billion dollar profit. And about eight thousand four hundred regular employees became about a hundred and sixty-seven thousand full-time equivalents.",
      type="table", title="Apple: then and now (not inflation-adjusted)",
      header=["", "Fiscal 1997", "Fiscal 2026"],
      rows=[["Revenue", "$7.08B", "$478.8B"], ["Net result", "−$1.045B", "+$132.2B"],
            ["Staff (regular / FTE)", f"{EMPLOYEES[1997]:,}", f"~{EMP_26:,}"]],
      col_colors={"1": "red", "2": "green"})
scene("A fair warning about hindsight. None of this was guaranteed in nineteen ninety-eight. Apple's sales were still shrinking that year, and the iPhone was nearly a decade away. The turnaround bought a chance, not a result. So what can you take from it?",
      type="photo", layout="side", file="assets/photos/steve_jobs_iphone_keynote.jpg", focus=[0.5, 0.35],
      value="A chance,", label="not a result", sub="the iPhone was nearly a decade away", color="gold")

# ---------------------------------------------------------------- 7
scene("Chapter seven. The lessons.", type="chapter", n=7, title="The lessons")
scene("Lesson one: focus. Fifteen products became a handful. Saying no freed money, people and attention for the few things that mattered. In your own life, list everything that costs you money or time each month, and cut what doesn't earn its place.",
      type="versus", title="Lesson 1: Focus",
      left={"label": "Apple before", "value": f"~{PRODUCTS_BEFORE}", "sub": "products", "color": "red"},
      right={"label": "Apple by 1999", "value": f"{LINES_1999}", "sub": "computer lines", "color": "green"},
      verdict="Say no to most things")
scene("Lesson two: know your runway. That's your cash, divided by what you burn each month. If you have nine thousand dollars saved and three thousand in essential costs each month, your runway is three months. Apple's cash bought it time to fix things. Yours does the same.",
      type="equation", title="Lesson 2: Know your runway",
      lines=[{"text": "Cash ÷ monthly costs = runway", "color": "muted", "size": 72},
             {"text": "$9,000 ÷ $3,000 a month", "color": "text", "size": 96},
             {"text": "= 3 months of runway", "color": "gold", "size": 110}],)
scene("Lesson three: complexity costs cash. Once Apple had fewer products, its inventory fell by more than eighty percent. For you, fewer cards, accounts and subscriptions means fewer fees and fewer surprises.",
      type="share", title="Lesson 3: Complexity costs cash",
      rows=[{"label": "Apple inventory, Sept 1997", "share": 1.0, "color": "red", "dp": 0},
            {"label": "Sept 1998 (as % of 1997)", "share": inv_left, "color": "green", "dp": 0}],
      note="Source: Apple 10-K, fiscal 1998")
scene("And remember who did it. Uh-mellio's team started the cuts and bought Next. Jobs set the focus. Ive, Rubinstein, Tevanian, Anderson and Cook did much of the work. A turnaround is a team effort.",
      type="photo", layout="full", file="assets/photos/apple_infinite_loop_sign.jpg", focus=[0.6, 0.5],
      value="Not one genius. A team.", label="Amelio · Jobs · Ive · Rubinstein · Tevanian · Anderson · Cook", color="gold")
scene("If you learned something, subscribe. We break down how money and business really work, every week.",
      type="cta", lines=["How money", "really works."], sub="Subscribe for weekly breakdowns")

# ---------------------------------------------------------------- checks
types = [s["visual"]["type"] for s in S]
for a, b in zip(S, S[1:]):
    assert a["visual"]["type"] != b["visual"]["type"], ("same visual twice in a row", a["say"][:40])
words = sum(len(s["say"].split()) for s in S)
chapters = [s["visual"]["title"] for s in S if s["visual"]["type"] == "chapter"]
assert 1400 <= words <= 1700, words
assert 40 <= len(S) <= 70, len(S)
assert 6 <= len(chapters) <= 7
assert len(set(types)) >= 10
# retention: payoff number inside the first ~10 s, and the intro (before chapter 1) under ~60 s of speech
assert S[0]["say"].lower().startswith("in nineteen ninety-seven, apple lost over a billion dollars")
intro_words = sum(len(x["say"].split()) for x in S[:next(i for i, x in enumerate(S) if x["visual"]["type"] == "chapter")])
assert intro_words <= 150, intro_words
# every chapter's last scene ends on an open loop into the next chapter (a question or a forward-looking line)
LOOPS = ["Apple had already gone shopping for a new one.", "it came from its fiercest rival.", "What Apple did with that time was cut, hard.",
         "all-in-one computer.", "the software it agreed to buy in nineteen ninety-six.", "So what can you take from it?"]
ch_idx = [i for i, x in enumerate(S) if x["visual"]["type"] == "chapter"]
for i, loop in zip(ch_idx[1:], LOOPS):
    assert S[i - 1]["say"].endswith(loop), (S[i - 1]["say"][-60:], loop)

SOURCES = [
    "Apple Form 10-K for fiscal 1996 (employees): https://www.sec.gov/Archives/edgar/data/320193/0000320193-96-000023.txt",
    "Apple Form 10-K for fiscal 1997 (1997 results, NeXT, Microsoft deal, debt ratings): https://www.sec.gov/Archives/edgar/data/320193/0001047469-97-006960.txt",
    "Apple Form 10-K405 for fiscal 1998 (return to profit, product line, inventory, iMac): https://www.sec.gov/Archives/edgar/data/320193/0001047469-98-044981.txt",
    "Apple Form 10-K for fiscal 1999 (iMac sales, four product lines): https://www.sec.gov/Archives/edgar/data/320193/0000912057-99-010244.txt",
    "Apple Form 10-K405 for fiscal 2001 (Mac OS X released): https://www.sec.gov/Archives/edgar/data/320193/000091205701544436/a2066171z10-k405.htm",
    "Apple Form 10-K for fiscal 2026: https://www.sec.gov/Archives/edgar/data/320193/000032019326000026/aapl-20260926.htm",
    "Apple press release, Apple to acquire NeXT (Dec 20, 1996; 8-K exhibit): https://www.sec.gov/Archives/edgar/data/320193/0000320193-96-000027.txt",
    "Apple 8-K press releases: Amelio resigns (Jul 9, 1997), Jobs interim CEO (Sept 16, 1997): https://www.sec.gov/Archives/edgar/data/320193/0000320193-97-000012.txt and https://www.sec.gov/Archives/edgar/data/320193/0000320193-97-000018.txt",
    "Microsoft press release (Aug 6, 1997): https://news.microsoft.com/1997/08/06/microsoft-and-apple-affirm-commitment-to-build-next-generation-software-for-macintosh/",
    "Maclean's, Microsoft rescues Apple (Aug 18, 1997): https://thecanadianencyclopedia.ca/en/article/microsoft-rescues-apple",
    "Stratechery, Steve Jobs at Macworld Boston in 1997 (transcript): https://stratechery.com/2013/steve-jobs-at-macworld-boston-in-1997/",
    "Apple press release, Apple unveils iMac (May 6, 1998), via MacTech: https://www.mactech.com/1998/05/06/md1-apples-imac/",
    "Apple press release, record iMac demand (Aug 19, 1998), via MacTech: https://www.mactech.com/1998/08/20/md1-apple-pr-retailers-experience-record-consumer-demand-for-imac/",
    "Macworld, Apple design guru Jony Ive to leave Apple (Jun 27, 2019): https://www.macworld.com/article/232955/apple-design-guru-jony-ive-to-leave-apple.html",
    "Computer History Museum, Steve Jobs and NeXTSTEP: https://computerhistory.org/blog/the-deep-history-of-your-apps-steve-jobs-nextstep-and-early-object-oriented-programming/",
    "Apple press releases: iPod (Oct 23, 2001) https://www.apple.com/newsroom/2001/10/23Apple-Presents-iPod/ and iPhone (Jan 9, 2007) https://www.apple.com/newsroom/2007/01/09Apple-Reinvents-the-Phone-with-iPhone/",
    "The Next Web, Steve Jobs: We were 90 days from going bankrupt (Jun 2, 2010): https://thenextweb.com/news/steve-jobs-90-days",
    "Walter Isaacson, Steve Jobs (Simon & Schuster, 2011): the two-by-two product grid",
]

DESCRIPTION = (
    "Apple in 1997 lost over $1 billion, its sales had fallen by more than a third in two years, and its debt was "
    "rated junk. This case study uses Apple's own 10-K filings to show how the company turned around: the NeXT "
    "acquisition and Steve Jobs' return, the $150 million Microsoft deal, cutting the product line, the iMac, a "
    "huge inventory cut, and how it set up the iPod and iPhone era. Plus three business lessons you can use: "
    "focus, cash runway and cutting complexity.\n\n"
    "Apple's fiscal year ends in late September; years in the video are fiscal years. Dollar figures are not adjusted "
    "for inflation; US prices roughly doubled between 1997 and 2026. Staff: 1997 = regular employees (excl. 1,739 "
    "temporary staff and contractors), 2026 = full-time equivalents. \"Under three days\" = "
    "Apple's fiscal 1997 net loss ($1.045B) / its fiscal 2026 net income per day ($132.2B / 365). The \"90 days\" "
    "line is Steve Jobs' own later recollection (2010), not a figure from Apple's filings. The two-by-two product "
    "grid is as described by biographer Walter Isaacson; the four product lines are from Apple's 1999 10-K. The "
    "$9,000 runway example is illustrative.\n\n"
    "Sources:\n" + "\n".join("- " + s for s in SOURCES) + "\n\n"
    "For education only. Not financial or investment advice.\n\n"
    "#apple #stevejobs #casestudy #business #businessstrategy"
)

spec = {
    "id": "L014_apple_1997", "currency": "usd", "voice": "af_heart", "speed": 1.0, "gap": 0.35,
    "badge": "CASE STUDY",
    "caption_fix": {"Uh-mellio": "Amelio"},   # Kokoro says "Emilio"
    "disclaimer": "Figures: Apple 10-K filings & press releases · for education, not investment advice",
    "title": "Apple in 1997: How a $1 Billion Loss Became a Comeback",
    "intro_chapter": "The $1B loss",
    "thumbnail": {"big": f"${MSFT / 1e6:.0f}M", "line": "Not what saved Apple", "tag": "APPLE IN 1997", "color": "gold",
                  "photo": {"file": "assets/photos/steve_jobs_iphone_keynote.jpg", "focus": [0.52, 0.4], "cutout": True}},
    "description": DESCRIPTION,
    "tags": ["apple 1997", "apple turnaround", "how apple was saved", "steve jobs return to apple",
             "microsoft apple 150 million", "apple next acquisition", "imac 1998", "business case study",
             "apple history", "tim cook inventory", "business strategy", "corporate turnaround"],
    "localizations": {
        "es": {"title": "Apple en 1997: de perder $1.000 M a la gran remontada",
               "summary": "En 1997 Apple perdió más de 1.000 millones de dólares, sus ventas habían caído más de "
                          "un tercio en dos años y su deuda era calificada como basura. Con los informes 10-K de "
                          "Apple vemos cómo se recuperó: la compra de NeXT y el regreso de Steve Jobs, el acuerdo de "
                          "150 millones con Microsoft, el recorte de productos, el iMac y un enorme recorte de "
                          "inventario. Y tres lecciones de negocio: enfoque, margen de caja y menos complejidad."},
        "pt": {"title": "Apple em 1997: do prejuízo de US$ 1 bi à grande virada",
               "summary": "Em 1997 a Apple perdeu mais de US$ 1 bilhão, suas vendas tinham caído mais de um terço "
                          "em dois anos e sua dívida era considerada lixo. Com os relatórios 10-K da Apple, mostramos "
                          "a virada: a compra da NeXT e a volta de Steve Jobs, o acordo de US$ 150 milhões com a "
                          "Microsoft, o corte de produtos, o iMac e um enorme corte de estoque. E três lições de "
                          "negócios: foco, fôlego de caixa e menos complexidade."},
        "hi": {"title": "Apple 1997: $1 अरब के घाटे से वापसी तक",
               "summary": "1997 में Apple को 1 अरब डॉलर से ज़्यादा का घाटा हुआ, दो साल में बिक्री एक-तिहाई से "
                          "ज़्यादा गिर गई और उसके कर्ज़ को जंक रेटिंग मिली। Apple की अपनी 10-K फ़ाइलिंग से देखिए "
                          "कंपनी कैसे संभली: NeXT की ख़रीद और Steve Jobs की वापसी, Microsoft का 15 करोड़ डॉलर "
                          "($150M) का सौदा, प्रोडक्ट्स में कटौती, iMac और इन्वेंटरी में भारी कमी। साथ में बिज़नेस "
                          "के तीन सबक: फ़ोकस, कैश रनवे और कम जटिलता।"},
        "id": {"title": "Apple 1997: Dari Rugi $1 Miliar Menjadi Kebangkitan",
               "summary": "Pada 1997 Apple rugi lebih dari 1 miliar dolar AS, penjualannya turun lebih dari "
                          "sepertiga dalam dua tahun, dan utangnya berperingkat sampah. Dengan laporan 10-K Apple "
                          "sendiri, kita lihat cara Apple bangkit: akuisisi NeXT dan kembalinya Steve Jobs, "
                          "kesepakatan 150 juta dolar dengan Microsoft, pemangkasan produk, iMac, dan pemangkasan "
                          "persediaan besar-besaran. Plus tiga pelajaran bisnis: fokus, runway kas, dan "
                          "mengurangi kerumitan."},
        "de": {"title": "Apple 1997: Wie aus 1 Mrd. $ Verlust ein Comeback wurde",
               "summary": "1997 verlor Apple über 1 Milliarde Dollar, der Umsatz war in zwei Jahren um mehr als "
                          "ein Drittel gefallen und die Schulden galten als Ramsch. Anhand von Apples eigenen "
                          "10-K-Berichten zeigen wir die Wende: die Übernahme von NeXT und Steve Jobs' Rückkehr, "
                          "der 150-Millionen-Deal mit Microsoft, weniger Produkte, der iMac und ein riesiger "
                          "Lagerabbau. Dazu drei Business-Lektionen: Fokus, finanzieller Spielraum und weniger "
                          "Komplexität."},
        "fr": {"title": "Apple en 1997 : d'une perte de 1 Md$ au grand retour",
               "summary": "En 1997, Apple a perdu plus d'un milliard de dollars, ses ventes avaient chuté de plus "
                          "d'un tiers en deux ans et sa dette était classée « pourrie ». À partir des rapports 10-K "
                          "d'Apple, on suit le redressement : le rachat de NeXT et le retour de Steve Jobs, "
                          "l'accord de 150 millions avec Microsoft, la gamme réduite, l'iMac et une énorme baisse "
                          "des stocks. Et trois leçons de business : se concentrer, connaître sa trésorerie, "
                          "simplifier."},
    },
    "scenes": S,
}
assert len(spec["title"]) < 60, len(spec["title"])
assert spec["title"].startswith("Apple in 1997")
assert len(spec["thumbnail"]["big"]) <= 6 and len(spec["thumbnail"]["line"]) <= 22
assert all(len(l["title"]) <= 60 for l in spec["localizations"].values())

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "L014_apple_1997.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out, len(S), "scenes,", words, "words,", len(chapters), "chapters, intro", intro_words, "words, title",
      len(spec["title"]), "chars")
print("types:", dict(Counter(types)))
