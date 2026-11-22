"""Long-form L010 (case study): Netflix vs Blockbuster.

Sources (checked 2026-11-22). Dollar figures in $ unless noted.
  [BQ]  Blockbuster Form 10-Q, Q1 2000 (filed 2000): extended viewing fees (late fees) in Q1 1999 were
        $179.4M = 16.1% of total revenues.
  [WP]  UPI, "Late fees key to movie rental business" (Aug 30, 2003), citing the Washington Post: late fees were
        16% of Blockbuster's revenue in 2000, the last year it disclosed them.
  [B00] Blockbuster FY2000 Form 10-K405 (filed Mar 29, 2001): revenue $4,960.1M; 7,677 stores at Dec 31, 2000.
  [B04] Blockbuster FY2004 Form 10-K (filed Mar 29, 2005): revenue $6,053.2M (its highest); 9,094 stores in the US,
        its territories and 24 other countries; ~84,300 employees; BLOCKBUSTER Online US launch Aug 2004;
        late fees dropped Jan 1, 2005 at 4,500+ company-operated US stores; late fees would have contributed an
        estimated $400M-$450M of 2005 revenue.
  [B06] Blockbuster FY2006 Form 10-K (filed Mar 1, 2007): Total Access introduced Nov 1, 2006 (return online
        rentals to a store for a free in-store rental); ~2.2M online subscribers at end of 2006; the no-late-fees
        program addressed "our most prevalent customer complaint".
  [B07] Blockbuster FY2007 Form 10-K (filed Mar 6, 2008): Total Access restructured in Q3 2007 into plans with a
        limited number of in-store exchanges; price increase on all Total Access plans effective Dec 27, 2007.
  [B09] Blockbuster FY2009 Form 10-K (filed Mar 16, 2010): revenue 2005-2009 (as restated there); 2009 net loss
        $558.2M; stores 7,830 / 7,405 / 6,520 at end of 2007 / 2008 / 2009; "substantial doubt about our ability
        to continue as a going concern".
  [KEY] Blockbuster press release, Jul 2, 2007: James W. Keyes named chairman and CEO, succeeding John Antioco.
  [HBR] John Antioco, "Blockbuster's Former CEO on Sparring with an Activist Shareholder", Harvard Business
        Review, April 2011 (his clash with board member Carl Icahn over strategy and spending).
  [S1]  Netflix Form S-1 (filed Mar 6, 2002): incorporated Aug 1997; website launched Apr 1998; subscription
        launched Sept 1999 ($19.95/month, 3 titles out, "no due dates, late fees or shipping charges");
        2000 revenue $35.894M, net loss $57.363M; 292 thousand subscribers at end of 2000.
  [N07] Netflix press release, Jan 16, 2007: "Watch Now" streaming, about 1,000 titles, over 70,000 DVD titles,
        at no additional cost.
  [N09] Netflix FY2009 Form 10-K: revenue 2005-2009; subscribers at year end 2005-2009; 2009 net income $115.86M.
  [N25] Netflix Q4 2025 shareholder letter (Jan 20, 2026): 2025 revenue $45,183,036K; crossed 325M paid
        memberships (Netflix no longer reports member counts every quarter; this is its latest figure).
  [N26] Netflix Q3 2026 shareholder letter (Oct 20, 2026): Q3 2026 income statement; operating margin 34.6%
        (28.2% in Q3 2025); 2026 revenue forecast $51.1B.
  [M]   The 2000 meeting: Marc Randolph, "That Will Never Work" (2019) and Reed Hastings & Erin Meyer,
        "No Rules Rules" (2020), as reported by Marketplace (Sep 8, 2020) and The Independent (Feb 7, 2022);
        Antioco's response in a LinkedIn post, reported by Next TV (Jun 3, 2022) and Newsweek's fact check.
        Accounts differ: the founders say they offered Netflix for $50M and were turned down; Antioco says he
        was not at a meeting where a sale came up, that Netflix came to pitch a partnership and made an
        "off-the-cuff offer", and that serious merger talks came only in early 2007.
  [O]   Origin story: CNBC (May 23, 2017): Hastings' $40 "Apollo 13" late fee; Randolph calls it a
        "convenient fiction".
  [CH]  AFP via phys.org (Sep 23, 2010): Chapter 11 filing, nearly $1B of debt, some 3,000 US stores.
  [D]   AFP via phys.org (Apr 6, 2011) and Bloomberg (Apr 26, 2011): Dish Network won the auction with a
        $320M bid.
  [DVD] NPR (Apr 18, 2023) and CBS News: Netflix's DVD-by-mail service mailed its last discs Sept 29, 2023.
  [BE]  Fortune (Mar 7, 2019): corporate stores closed in 2014; with the Perth, Australia store closing, the
        independently owned store in Bend, Oregon is the last Blockbuster on Earth.
Left out (not confirmed from a primary or reputable source): exact meeting date and floor, the claim that
Netflix itself charged late fees early on, Blockbuster's 2000 net result, Total Access subscriber peak.
"""
import json, os
from collections import Counter

# ---- Blockbuster
BB_LATE_SHARE_Q1_99 = 0.161            # [BQ]
BB_LATE_Q1_99 = 179.4e6                # [BQ]
BB_LATE_SHARE_2000 = 0.16              # [WP]
BB_REV = {2000: 4_960.1e6, 2004: 6_053.2e6}                                       # [B00] [B04]
BB_REV_0509 = {2005: 5_551.1e6, 2006: 5_337.6e6, 2007: 5_314.0e6, 2008: 5_065.4e6, 2009: 4_062.4e6}  # [B09]
BB_STORES = {2000: 7_677, 2004: 9_094, 2006: 8_360, 2007: 7_830, 2008: 7_405, 2009: 6_520}  # [B00][B04][B06][B09]
BB_EMPLOYEES_2004 = 84_300             # [B04]
BB_LATE_FEES_2005_EST = (400e6, 450e6) # [B04]
BB_ONLINE_SUBS_2006 = 2.2e6            # [B06]
BB_NET_LOSS_2009 = 558.2e6             # [B09]
BB_DEBT_2010 = 1e9                     # [CH] "nearly one billion"
BB_US_STORES_2010 = 3000               # [CH] "some 3,000"
DISH_BID = 320e6                       # [D]
# ---- Netflix
NF_PRICE_1999 = 19.95                  # [S1]
NF_REV_2000, NF_LOSS_2000 = 35.894e6, 57.363e6   # [S1]
NF_SUBS = {2000: 292e3, 2005: 4_179e3, 2006: 6_316e3, 2007: 7_479e3, 2008: 9_390e3, 2009: 12_268e3}  # [S1] [N09]
NF_REV_0509 = {2005: 682.213e6, 2006: 996.660e6, 2007: 1_205.340e6, 2008: 1_364.661e6, 2009: 1_670.269e6}  # [N09]
NF_NET_INC_2009 = 115.860e6            # [N09]
STREAM_TITLES, DVD_TITLES = 1_000, 70_000          # [N07]
NF_REV_2025 = 45_183_036e3             # [N25]
NF_PAID_MEMBERS = 325e6                # [N25] "crossed 325M"
NF_REV_2026_FCST = 51.1e9              # [N26]
Q3 = dict(rev=12_874_176e3, cor=6_079_016e3, sm=837_051e3, td=1_033_142e3, ga=466_367e3, op=4_458_600e3)  # [N26]
NF_MARGIN_Q3_26, NF_MARGIN_Q3_25 = 0.346, 0.282    # [N26]
OFFER = 50e6                           # [M]

# ---- derived numbers (every spoken one is asserted)
late_2000 = BB_LATE_SHARE_2000 * BB_REV[2000]
size_ratio = BB_REV[2000] / NF_REV_2000
nf_vs_bb_peak = NF_REV_2025 / BB_REV[2004]
rev_per_hour = NF_REV_2025 / (365 * 24)
hours_for_offer = OFFER / rev_per_hour
q3_vs_bb_peak = Q3["rev"] / BB_REV[2004]
q3_margin = Q3["op"] / Q3["rev"]
subs_growth = NF_SUBS[2009] / NF_SUBS[2000]

assert abs(Q3["rev"] - Q3["cor"] - Q3["sm"] - Q3["td"] - Q3["ga"] - Q3["op"]) < 1e3   # statement ties out
assert abs(q3_margin - NF_MARGIN_Q3_26) < 0.001
assert abs(BB_LATE_Q1_99 / BB_LATE_SHARE_Q1_99 - 1.114e9) < 5e6   # Q1 1999 revenue ≈ $1.11B, consistent
assert 790e6 < late_2000 < 800e6         # "nearly eight hundred million dollars"
assert 135 < size_ratio < 140            # "about a hundred and forty times"
assert 7.4 < nf_vs_bb_peak < 7.5         # "more than seven times"
assert 9.5 < hours_for_offer < 10        # "less than ten hours"
assert 2.1 < q3_vs_bb_peak < 2.2         # "more than twice"
assert 6.0e9 < BB_REV[2004] < 6.1e9      # "just over six billion"
assert BB_REV[2004] == max(list(BB_REV.values()) + list(BB_REV_0509.values()))   # best year in our data
assert 45.1e9 < NF_REV_2025 < 45.3e9     # "about forty-five billion"
assert 4.4e9 < Q3["op"] < 4.5e9          # "about four and a half billion"
assert 12.8e9 < Q3["rev"] < 12.9e9       # "twelve point nine billion"
assert 40 < subs_growth < 43             # "about forty times"
assert BB_STORES[2004] - BB_STORES[2009] > 2500
print(f"late fees 2000 ${late_2000/1e6:.0f}M · size {size_ratio:.0f}x · NF/BB peak {nf_vs_bb_peak:.2f}x · "
      f"$50M every {hours_for_offer:.1f} h · Q3/BB peak {q3_vs_bb_peak:.2f}x · subs x{subs_growth:.0f}")

S = []
def scene(say, **visual):
    S.append({"say": say, "visual": visual})

# ---------------------------------------------------------------- Hook
scene("In the year two thousand, Netflix's founders say they offered to sell their company to Blockbuster for fifty million dollars. Blockbuster said no.",
      type="count", to=50, prefix="$", suffix="M", label="the price Netflix's founders say they asked", sub="year 2000, by their account", color="gold")
scene("Ten years later, Blockbuster was bankrupt. Today there is one Blockbuster store left on Earth, in Bend, Oregon.",
      type="stat", value="1", label="Blockbuster store left on Earth", sub="Bend, Oregon", color="red")
scene("And Netflix? Last year it brought in over forty-five billion dollars in revenue. That's more than seven times Blockbuster's best year ever.",
      type="hbars", title="Annual revenue",
      items=[{"label": "Netflix 2025", "value": NF_REV_2025, "display": "$45.2B", "color": "green"},
             {"label": "Blockbuster 2004", "value": BB_REV[2004], "display": "$6.05B", "color": "blue"}])
scene("So how did a small, money-losing startup beat a giant? And what does it teach you about money and business? Let's break it down.",
      type="title", title="Netflix vs Blockbuster", sub="the deal that wasn't, and what it teaches")

# ---------------------------------------------------------------- 1
scene("Chapter one. The giant.", type="chapter", n=1, title="The giant")
scene("At its peak in two thousand four, Blockbuster had about nine thousand one hundred stores across the US and twenty-four other countries, around eighty-four thousand employees, and just over six billion dollars in revenue.",
      type="stat_grid", title="Blockbuster at its peak (2004)",
      items=[{"value": f"{BB_STORES[2004]:,}", "label": "stores", "sub": "US + 24 other countries", "color": "blue"},
             {"value": "$6.05B", "label": "revenue", "sub": "its best year", "color": "gold"},
             {"value": f"{BB_EMPLOYEES_2004:,}", "label": "employees", "sub": "worldwide", "color": "text"}])
scene("The model was simple. You drove to the store, picked a movie off the wall, and rented it for a few nights. Then you drove back to return it. And if you were late, you paid extra.",
      type="bullets", title="How renting worked",
      items=["Drive to the store", "Pick a movie off the wall", "Rent it for a few nights", "Late? Pay a fee"])
scene("Those late fees were a big deal. Blockbuster's own filing shows that in early nineteen ninety-nine, late fees were sixteen percent of its revenue. The Washington Post reported the same share for the year two thousand.",
      type="donut", title="Blockbuster revenue, 2000",
      segments=[{"label": "Late fees", "value": BB_LATE_SHARE_2000, "color": "red"},
                {"label": "Everything else", "value": 1 - BB_LATE_SHARE_2000, "color": "blue"}],
      center="16%", center_sub="from late fees")
scene("Sixteen percent of about five billion dollars is nearly eight hundred million dollars. In one year. From people who brought a movie back late.",
      type="equation", title="Late fees, year 2000 (estimate)",
      lines=[{"text": "$4.96B revenue × 16%", "color": "muted", "size": 84},
             {"text": f"≈ ${late_2000 / 1e6:.0f}M", "color": "red", "size": 130},
             {"text": "from late returns", "color": "text", "size": 56}])
scene("And customers hated them. Blockbuster's own annual report later called late fees its most common customer complaint, in its words, the most prevalent one.",
      type="quote", text="\"Our most prevalent\ncustomer complaint\"", first_color="text", color="gold",
      source="Blockbuster 2006 annual report (10-K), on late fees")

# ---------------------------------------------------------------- 2
scene("Chapter two. The upstart.", type="chapter", n=2, title="The upstart")
scene("Netflix was founded in nineteen ninety-seven by Reed Hastings and Marc Randolph. Its website launched in April nineteen ninety-eight, renting DVDs by mail. The monthly subscription came in September nineteen ninety-nine.",
      type="timeline", title="Netflix's early years",
      events=[{"when": "1997", "text": "Netflix\nfounded"},
              {"when": "1998", "text": "Website launches\nDVDs by mail"},
              {"when": "1999", "text": "Monthly\nsubscription"},
              {"when": "2000", "text": "Pitch to\nBlockbuster"}])
scene("You may have heard Hastings started Netflix after a forty dollar late fee for Apollo Thirteen. He has told that story. But his co-founder, Marc Randolph, calls it a convenient fiction. The real start was two entrepreneurs looking for something to sell online.",
      type="versus", title="The origin story",
      left={"label": "The legend", "value": "$40", "sub": "late fee for Apollo 13", "color": "blue"},
      right={"label": "Co-founder Randolph", "value": "Fiction", "sub": "\"a convenient fiction\"", "color": "gold"},
      verdict="Good story. Disputed history.")
scene("The subscription was the real idea. For nineteen dollars and ninety-five cents a month, you could keep three DVDs at a time. No due dates. No late fees. No shipping charges.",
      type="stat", value=f"${NF_PRICE_1999}", label="a month · 3 DVDs out at a time",
      sub="no due dates · no late fees · no shipping charges", color="green")
scene("Think about what that did. Keep a movie as long as you like. Send it back when you're ready, and the next one arrives. Netflix still gets paid every month. The customer's biggest annoyance became the selling point.",
      type="flywheel", title="The subscription loop", center="NO LATE FEES",
      steps=["Keep it longer", "Mail it back", "Next DVD arrives", "Pay monthly"])
scene("But Netflix was tiny. At the end of two thousand, it had about two hundred and ninety thousand subscribers and around thirty-six million dollars in revenue.",
      type="count", to=NF_SUBS[2000] / 1e3, suffix="K", label="Netflix subscribers, end of 2000",
      sub="revenue that year: $35.9M", color="green")

# ---------------------------------------------------------------- 3
scene("Chapter three. The meeting.", type="chapter", n=3, title="The meeting")
scene("In two thousand, Hastings and Randolph flew to Blockbuster's headquarters in Dallas. Hastings later wrote that, walking in, he whispered: Blockbuster is a thousand times our size.",
      type="quote", text="\"Blockbuster is a thousand\ntimes our size.\"", first_color="text", color="text",
      source="Reed Hastings, No Rules Rules (2020)")
scene("By revenue, it was more like a hundred and forty times. Still enormous. Blockbuster had nearly five billion dollars in revenue and over seven thousand six hundred stores. Netflix had thirty-six million dollars, and no stores at all.",
      type="table", title="The year 2000",
      header=["", "Blockbuster", "Netflix"],
      rows=[["Revenue", "$4.96B", "$35.9M"], ["Stores", f"{BB_STORES[2000]:,}", "0"], ["Size", f"{size_ratio:.0f}×", "1×"]],
      col_colors={"1": "blue", "2": "green"})
scene("In both founders' books, the pitch went like this. Blockbuster buys Netflix. Netflix runs the online side under Blockbuster's name, and Blockbuster focuses on its stores. The price: fifty million dollars.",
      type="bullets", title="The pitch, per Netflix's founders",
      items=["Blockbuster buys Netflix", "Netflix runs the online side", "Blockbuster runs the stores", "Price: $50 million"])
scene("Randolph wrote that Blockbuster's chief executive, John Antioco, was struggling not to laugh. The answer was no.",
      type="title", title="\"No.\"", sub="per Randolph's book, That Will Never Work (2019)")
scene("But accounts differ. Antioco has said he wasn't at any meeting where a sale came up. In his version, Netflix came to pitch a partnership and made an off-the-cuff offer to sell. No serious talks.",
      type="versus", title="Two versions of the meeting",
      left={"label": "Netflix's founders", "value": "Rejected", "sub": "a $50M offer, laughed off", "color": "green"},
      right={"label": "Blockbuster's CEO", "value": "Not serious", "sub": "an off-the-cuff remark", "color": "blue"},
      verdict="Both agree: Blockbuster passed")
scene("And to be fair, Antioco has a point. Netflix lost fifty-seven million dollars that year. Paying fifty million for a money-losing website, just as the dot-com bubble burst, looked risky.",
      type="stat", value=f"−${NF_LOSS_2000 / 1e6:.0f}M", label="Netflix's net loss in 2000", sub="Netflix S-1 filing, 2002", color="red")
scene("So saying no to one deal wasn't the real mistake. What happened next was.",
      type="equation", lines=[{"text": "Saying no to $50M", "color": "muted", "size": 90},
                              {"text": "≠ the real mistake", "color": "gold", "size": 110}])

# ---------------------------------------------------------------- 4
scene("Chapter four. The fight back.", type="chapter", n=4, title="The fight back")
scene("Blockbuster did fight back, and hard. It launched Blockbuster Online in August two thousand four. On January first, two thousand five, it dropped late fees at its US company stores. In November two thousand six came Total Access: rent online, and return the disc to any store for a free in-store rental.",
      type="timeline", title="Blockbuster's counter-attack",
      events=[{"when": "2004", "text": "Blockbuster Online\nlaunches"},
              {"when": "2005", "text": "Late fees\ndropped (US)"},
              {"when": "2006", "text": "Total Access:\nreturn by mail or store"},
              {"when": "2007", "text": "Netflix starts\nstreaming"}])
scene("Dropping late fees was expensive. In its own annual report, Blockbuster estimated those fees would have brought in four hundred to four hundred and fifty million dollars of revenue in two thousand five. It gave that up on purpose.",
      type="equation", title="Late fees Blockbuster gave up (its own estimate)",
      lines=[{"text": "2005 revenue from late fees", "color": "muted", "size": 72},
             {"text": f"${BB_LATE_FEES_2005_EST[0] / 1e6:.0f}M–${BB_LATE_FEES_2005_EST[1] / 1e6:.0f}M", "color": "red", "size": 130},
             {"text": "given up on purpose", "color": "text", "size": 56}])
scene("And it was working. By the end of two thousand six, Blockbuster had about two point two million online subscribers, against Netflix's six point three million. Antioco says that by early two thousand seven, the two companies were in serious merger talks.",
      type="versus", title="Online subscribers, end of 2006",
      left={"label": "Blockbuster", "value": "2.2M", "sub": "incl. Total Access", "color": "blue"},
      right={"label": "Netflix", "value": f"{NF_SUBS[2006] / 1e6:.1f}M", "sub": "DVD by mail", "color": "green"},
      verdict="The gap was closing")
scene("Then, in January two thousand seven, Netflix quietly launched Watch Now, streaming on computers at no extra cost. It had about a thousand titles. Its DVD library had more than seventy thousand.",
      type="hbars", title="Netflix titles, January 2007", format="num",
      items=[{"label": "DVD by mail", "value": DVD_TITLES, "display": "70,000+", "color": "slate"},
             {"label": "Streaming", "value": STREAM_TITLES, "display": "~1,000", "color": "green"}])
scene("A thousand titles, on a computer screen. Easy to dismiss. That's how disruption usually starts: small, a bit worse, and cheap to try.",
      type="quote", text="Disruption starts small,\nand easy to dismiss.", first_color="text", color="gold")
scene("Then the giant blinked. Antioco had clashed with his board, including the activist investor Carl Icahn, and in July two thousand seven, Jim Keyes replaced him as chief executive. That year, Blockbuster limited the free in-store swaps, and then raised Total Access prices.",
      type="bullets", title="2007: Blockbuster pulls back", color="red",
      items=["CEO John Antioco replaced", "Free in-store swaps limited", "Total Access prices raised"])

# ---------------------------------------------------------------- 5
scene("Chapter five. The fall.", type="chapter", n=5, title="The fall")
scene("Watch the next few years. Blockbuster's revenue slid from about five and a half billion dollars in two thousand five to about four billion in two thousand nine. Netflix grew from under seven hundred million to almost one point seven billion.",
      type="line", title="Annual revenue, 2005–2009", x=list(BB_REV_0509),
      series=[{"label": "Blockbuster", "values": list(BB_REV_0509.values()), "color": "blue"},
              {"label": "Netflix", "values": list(NF_REV_0509.values()), "color": "green"}])
scene("The stores went too. From over nine thousand in two thousand four to six thousand five hundred by the start of two thousand ten.",
      type="columns", title="Blockbuster stores worldwide (year end)", format="num", highlight=0, color="blue",
      items=[{"label": str(y), "value": v, "display": f"{v:,}"} for y, v in BB_STORES.items() if y >= 2004])
scene("In two thousand nine, Blockbuster lost five hundred and fifty-eight million dollars. Netflix made a profit of a hundred and sixteen million. Blockbuster's own filing warned of substantial doubt about its ability to keep going.",
      type="stat_grid", title="Fiscal 2009",
      items=[{"value": f"−${BB_NET_LOSS_2009 / 1e6:.0f}M", "label": "Blockbuster", "sub": "net loss", "color": "red"},
             {"value": f"+${NF_NET_INC_2009 / 1e6:.0f}M", "label": "Netflix", "sub": "net profit", "color": "green"}])
scene("On September twenty-third, two thousand ten, Blockbuster filed for bankruptcy, with nearly a billion dollars of debt and some three thousand US stores left.",
      type="stat", value="2010", label="Blockbuster files for bankruptcy", sub="Sept 23 · nearly $1B of debt", color="red")
scene("In April two thousand eleven, the satellite TV company Dish won Blockbuster's assets at auction, with a three hundred and twenty million dollar bid. The company-owned stores were all closed by two thousand fourteen. And in March two thousand nineteen, when a store in Perth, Australia closed, an independently owned store in Bend, Oregon became the last Blockbuster on Earth.",
      type="table", title="The end of Blockbuster",
      header=["Year", "What happened"],
      rows=[["2010", "Bankruptcy filing"], ["2011", "Dish wins assets ($320M bid)"],
            ["2014", "Company stores closed"], ["2019", "Bend, Oregon: the last one"]],
      col_colors={"1": "text"})
scene("Notice what didn't happen. Blockbuster didn't ignore the internet. It saw the threat, built a real answer, and then pulled back when that answer got expensive while the stores still made money.",
      type="quote", text="It saw the threat.\nThen it pulled back.", first_color="text", color="red")

# ---------------------------------------------------------------- 6
scene("Chapter six. Netflix today.", type="chapter", n=6, title="Netflix today")
scene("At the end of twenty twenty-five, Netflix said it had crossed three hundred and twenty-five million paid memberships. Up from about two hundred and ninety thousand subscribers in two thousand.",
      type="count", to=NF_PAID_MEMBERS / 1e6, suffix="M+", label="Netflix paid memberships", sub="end of 2025 · Netflix Q4 2025 letter", color="green")
scene("Netflix even shut down the business that beat Blockbuster. It mailed its last DVDs in September twenty twenty-three, after twenty-five years. It replaced its own winner before someone else could.",
      type="stat", value="2023", label="Netflix mails its last DVD", sub="Sept 29, 2023 · after 25 years of DVD by mail", color="gold")
scene("Here's one recent quarter. From July to September twenty twenty-six, Netflix brought in about twelve point nine billion dollars. After the cost of its shows and delivering them, marketing, technology and admin, about four and a half billion was left as operating profit.",
      type="waterfall", title="Netflix, July–September 2026",
      steps=[{"label": "Revenue", "value": Q3["rev"], "kind": "start", "display": "$12.9B"},
             {"label": "Shows & delivery", "value": Q3["cor"], "kind": "minus", "display": "−$6.1B"},
             {"label": "Marketing", "value": Q3["sm"], "kind": "minus", "display": "−$0.8B"},
             {"label": "Technology", "value": Q3["td"], "kind": "minus", "display": "−$1.0B"},
             {"label": "Admin", "value": Q3["ga"], "kind": "minus", "display": "−$0.5B"},
             {"label": "Op. profit", "value": Q3["op"], "kind": "total", "display": "$4.5B"}])
scene("That's an operating margin of about thirty-five percent, up from twenty-eight percent a year earlier.",
      type="share", title="Netflix operating margin",
      rows=[{"label": "July–Sept 2025", "share": NF_MARGIN_Q3_25, "color": "blue", "dp": 1},
            {"label": "July–Sept 2026", "share": NF_MARGIN_Q3_26, "color": "green", "dp": 1}],
      note="Source: Netflix Q3 2026 shareholder letter")
scene("In that one quarter, Netflix brought in more than twice what Blockbuster made in its best full year.",
      type="columns", title="Revenue", highlight=1,
      items=[{"label": "Blockbuster, all of 2004", "value": BB_REV[2004], "display": "$6.05B", "color": "blue"},
             {"label": "Netflix, one quarter", "value": Q3["rev"], "display": "$12.9B", "color": "green"}])
scene("And that fifty million dollar price? At last year's revenue, Netflix now takes in fifty million dollars in less than ten hours.",
      type="equation", title="The $50M price today",
      lines=[{"text": "$45.2B ÷ 8,760 hours", "color": "muted", "size": 84},
             {"text": f"≈ ${rev_per_hour / 1e6:.1f}M an hour", "color": "text", "size": 96},
             {"text": f"$50M ≈ every {hours_for_offer:.1f} hours", "color": "gold", "size": 110}])

# ---------------------------------------------------------------- 7
scene("Chapter seven. The lessons.", type="chapter", n=7, title="The lessons")
scene("Lesson one. A customer's pain is an opportunity. Late fees were Blockbuster's most common complaint. Netflix built a business around removing it.",
      type="quote", text="Find what customers hate.\nThen remove it.", first_color="text", color="gold")
scene("Lesson two. Don't protect a profit stream your customers hate. Sixteen percent of Blockbuster's revenue came from the thing people liked least. Giving it up hurt, so the company waited, and a rival without that baggage promised what Blockbuster couldn't.",
      type="share", title="Blockbuster revenue from late fees (2000)",
      rows=[{"label": "The fee customers hated most", "share": BB_LATE_SHARE_2000, "color": "red", "dp": 0}],
      note="Source: Washington Post, via UPI (2003)")
scene("Lesson three. Disruption starts small. Netflix began with a few hundred thousand subscribers and big losses. By two thousand nine it had about forty times as many. Streaming started with a thousand titles. Both were easy to dismiss, until they weren't.",
      type="columns", title="Netflix subscribers (millions, year end)", format="num", highlight=5,
      items=[{"label": str(y), "value": v / 1e6, "display": f"{v / 1e6:.1f}M"} for y, v in NF_SUBS.items()],
      note="Sources: Netflix S-1 (2002) and 2009 annual report")
scene("And for your own money: notice the fees you pay only because leaving is a hassle. Those are exactly the fees a competitor will remove. And when you look at any business, ask which of its profits depend on customers having no better option.",
      type="bullets", title="Use it yourself",
      items=["Spot fees you pay out of habit", "Expect rivals to remove them", "Ask: which profits need no rival?"])
scene("Netflix isn't guaranteed to win forever, either. The same rules apply to it. Customers stay only while the deal feels fair.",
      type="title", title="No one is too big", sub="the same rules apply to Netflix")
scene("If you learned something, subscribe. We break down how money and business really work, every week.",
      type="cta", lines=["How money", "really works."], sub="Subscribe for weekly breakdowns")

# ---------------------------------------------------------------- checks
types = [s["visual"]["type"] for s in S]
for a, b in zip(S, S[1:]):
    assert a["visual"]["type"] != b["visual"]["type"], ("same visual twice in a row", a["say"][:40])
words = sum(len(s["say"].split()) for s in S)
chapters = [s["visual"]["title"] for s in S if s["visual"]["type"] == "chapter"]
assert 1400 <= words <= 1700, words
assert 45 <= len(S) <= 70, len(S)
assert 6 <= len(chapters) <= 7
assert len(set(types)) >= 10

SOURCES = [
    "Blockbuster Form 10-Q, Q1 2000 (late fees 16.1% of Q1 1999 revenue): https://www.sec.gov/Archives/edgar/data/1085734/000093066100001267/0000930661-00-001267.txt",
    "UPI, Late fees key to movie rental business (Aug 30, 2003), citing the Washington Post: https://www.upi.com/Business_News/2003/08/30/Late-fees-key-to-movie-rental-business/16201062257151/",
    "Blockbuster Form 10-K405 for 2000 (revenue, stores): https://www.sec.gov/Archives/edgar/data/1085734/000093066101000794/0000930661-01-000794-0001.txt",
    "Blockbuster Form 10-K for 2004 (revenue, stores, employees, Blockbuster Online, late-fee estimate): https://www.sec.gov/Archives/edgar/data/1085734/000119312505063510/d10k.htm",
    "Blockbuster Form 10-K for 2006 (Total Access, online subscribers, \"most prevalent customer complaint\"): https://www.sec.gov/Archives/edgar/data/1085734/000119312507044360/d10k.htm",
    "Blockbuster Form 10-K for 2007 (Total Access plan and price changes): https://www.sec.gov/Archives/edgar/data/1085734/000119312508048757/d10k.htm",
    "Blockbuster Form 10-K for 2009 (revenue 2005-2009, 2009 loss, stores, going-concern warning): https://www.sec.gov/Archives/edgar/data/1085734/000119312510058339/d10k.htm",
    "Netflix Form S-1 (Mar 2002; founding, subscription terms, 2000 results): https://www.sec.gov/Archives/edgar/data/1065280/000101287002001044/ds1.txt",
    "Netflix, Netflix offers subscribers the option of instantly watching movies on their PCs (Jan 16, 2007): https://about.netflix.com/en/news/netflix-offers-subscribers-the-option-of-instantly-watching-movies-on-their",
    "Netflix Form 10-K for 2009 (revenue, subscribers, profit 2005-2009): https://www.sec.gov/Archives/edgar/data/1065280/000119312510036181/d10k.htm",
    "Netflix Q4 2025 shareholder letter (Jan 20, 2026): https://s22.q4cdn.com/959853165/files/doc_financials/2025/q4/FINAL-Q4-25-Shareholder-Letter.pdf",
    "Netflix Q3 2026 shareholder letter (Oct 20, 2026): https://s22.q4cdn.com/959853165/files/doc_financials/2026/q3/FINAL-Q3-26-Shareholder-Letter.pdf",
    "Marc Randolph, That Will Never Work (2019); Reed Hastings & Erin Meyer, No Rules Rules (2020); see Marketplace (Sep 8, 2020): https://www.marketplace.org/story/2020/09/08/ceo-reed-hastings-on-how-netflix-beat-blockbuster",
    "John Antioco's response, Next TV (Jun 3, 2022): https://www.nexttv.com/news/blockbusters-famous-netflix-2002-rebuff-that-didnt-happen-says-video-chains-former-ceo",
    "John Antioco, Blockbuster's Former CEO on Sparring with an Activist Shareholder, Harvard Business Review (April 2011)",
    "CNBC, Reed Hastings on how Netflix was born (May 23, 2017): https://www.cnbc.com/2017/05/23/netflix-ceo-reed-hastings-on-how-the-company-was-born.html",
    "AFP, Blockbuster files for bankruptcy (Sep 23, 2010): https://phys.org/news/2010-09-blockbuster-bankruptcy.html",
    "AFP, Dish Network buys Blockbuster for $320mn (Apr 6, 2011): https://phys.org/news/2011-04-dish-network-blockbuster-320mn.html",
    "NPR, Netflix ends DVD-by-mail service (Apr 18, 2023): https://www.npr.org/2023/04/18/1170740799/netflix-ends-dvd-by-mail-service",
    "Fortune, The last Blockbuster on Earth (Mar 7, 2019): https://fortune.com/2019/03/07/last-blockbuster-on-earth/",
]

DESCRIPTION = (
    "In 2000, Netflix's founders say they offered to sell the company to Blockbuster for $50 million, and "
    "Blockbuster said no. Ten years later Blockbuster was bankrupt, and Netflix now brings in over $45 billion a "
    "year. This case study follows Blockbuster's late-fee business, Netflix's no-late-fee subscription, the "
    "disputed meeting, Blockbuster's fight back with Total Access, the bankruptcy, and three business lessons you "
    "can use.\n\n"
    "Accounts of the 2000 meeting differ: both Netflix co-founders describe a $50M offer that was turned down; "
    "Blockbuster's former CEO John Antioco says no serious talks took place. We show both.\n"
    "The late-fee total for 2000 is an estimate: 16% (as reported by the Washington Post) x Blockbuster's 2000 "
    "revenue of $4.96B.\n\n"
    "Sources:\n" + "\n".join("- " + s for s in SOURCES) + "\n\n"
    "For education only. Not financial advice.\n\n"
    "#netflix #blockbuster #casestudy #business #businessstrategy"
)

spec = {
    "id": "L010_netflix_blockbuster", "currency": "usd", "voice": "af_heart", "speed": 1.0, "gap": 0.35,
    "badge": "CASE STUDY",
    "disclaimer": "Figures: company filings & reports · for education, not investment advice",
    "title": "Netflix vs Blockbuster: The $50M Deal That Got Away",
    "intro_chapter": "The $50M deal",
    "thumbnail": {"big": "$50M", "line": "THE DEAL THEY REJECTED", "tag": "NETFLIX VS BLOCKBUSTER", "color": "gold"},
    "description": DESCRIPTION,
    "tags": ["netflix vs blockbuster", "netflix", "blockbuster", "blockbuster netflix 50 million",
             "why blockbuster failed", "business case study", "disruptive innovation", "late fees",
             "netflix history", "reed hastings", "business strategy", "subscription business"],
    "localizations": {
        "es": {"title": "Netflix vs Blockbuster: el trato de $50M que se les escapó",
               "summary": "En el año 2000, los fundadores de Netflix dicen que ofrecieron vender la empresa a "
                          "Blockbuster por 50 millones de dólares, y Blockbuster dijo que no. Diez años después, "
                          "Blockbuster estaba en quiebra y hoy Netflix ingresa más de 45.000 millones de dólares al "
                          "año. Te contamos la historia, las versiones que no coinciden y tres lecciones de negocio."},
        "pt": {"title": "Netflix vs Blockbuster: o negócio de US$50 mi que escapou",
               "summary": "Em 2000, os fundadores da Netflix dizem que ofereceram vender a empresa à Blockbuster "
                          "por US$ 50 milhões, e a Blockbuster recusou. Dez anos depois, a Blockbuster faliu, e hoje "
                          "a Netflix fatura mais de US$ 45 bilhões por ano. Contamos a história, as versões que não "
                          "batem e três lições de negócios."},
        "hi": {"title": "Netflix बनाम Blockbuster: $50M की डील जो हाथ से निकल गई",
               "summary": "साल 2000 में Netflix के संस्थापकों के मुताबिक़ उन्होंने अपनी कंपनी Blockbuster को 5 करोड़ "
                          "डॉलर ($50M) में बेचने की पेशकश की, और Blockbuster ने मना कर दिया। दस साल बाद Blockbuster "
                          "दिवालिया हो गई, और आज Netflix की सालाना कमाई 45 अरब डॉलर से ज़्यादा है। पूरी कहानी, "
                          "दोनों पक्षों का दावा, और बिज़नेस के तीन सबक।"},
        "id": {"title": "Netflix vs Blockbuster: Kesepakatan $50 Juta yang Lepas",
               "summary": "Pada tahun 2000, para pendiri Netflix mengatakan mereka menawarkan perusahaannya kepada "
                          "Blockbuster seharga 50 juta dolar AS, dan Blockbuster menolak. Sepuluh tahun kemudian "
                          "Blockbuster bangkrut, sementara Netflix kini meraup lebih dari 45 miliar dolar AS per "
                          "tahun. Inilah kisahnya, versi yang saling berbeda, dan tiga pelajaran bisnis."},
        "de": {"title": "Netflix vs. Blockbuster: Der verpasste 50-Millionen-Deal",
               "summary": "Im Jahr 2000 boten die Netflix-Gründer ihre Firma nach eigener Aussage Blockbuster für "
                          "50 Millionen Dollar an, und Blockbuster lehnte ab. Zehn Jahre später war Blockbuster "
                          "pleite, und Netflix setzt heute über 45 Milliarden Dollar im Jahr um. Die Geschichte, die "
                          "widersprüchlichen Versionen und drei Lehren fürs Business."},
        "fr": {"title": "Netflix vs Blockbuster : le deal à 50 M$ qui leur a échappé",
               "summary": "En 2000, les fondateurs de Netflix disent avoir proposé de vendre leur entreprise à "
                          "Blockbuster pour 50 millions de dollars, et Blockbuster a refusé. Dix ans plus tard, "
                          "Blockbuster faisait faillite, et Netflix réalise aujourd'hui plus de 45 milliards de "
                          "dollars de chiffre d'affaires par an. L'histoire, les versions qui divergent et trois "
                          "leçons de business."},
    },
    "scenes": S,
}
assert len(spec["title"]) < 60, len(spec["title"])
assert len(spec["thumbnail"]["big"]) <= 6 and len(spec["thumbnail"]["line"]) <= 22
assert all(len(l["title"]) <= 60 for l in spec["localizations"].values())

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "L010_netflix_blockbuster.json")
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out, len(S), "scenes,", words, "words,", len(chapters), "chapters, title", len(spec["title"]), "chars")
print("types:", dict(Counter(types)))
