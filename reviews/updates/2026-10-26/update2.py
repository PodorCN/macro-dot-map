import json, sys, runpy
P = sys.argv[1]
# 1) apply the first-pass edits (update1.py), then 2) the fixes for review 2026-10-26-001
import os
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "update1.py"), run_name="__main__")
m = json.load(open(P, encoding="utf-8"))
T = "2026-10-26"
S, N = m["sources"], m["nodes"]
E = {e["id"]: e for e in m["edges"]}
CH = {c["key"]: c for c in m["chains"]}
def f(text, src, basis="sourced"):
    return {"text": text, "src": src, "basis": basis}

# Finding 2: tiers and publishers
S["reuters_houthi"].update(name="Reuters via Investing.com: Houthis claim Saudi pipeline attack", tier=2)
S["ap_week"].update(name="AP via Yahoo Finance: how major US indexes fared Oct 23", tier=2)
S.pop("yahoo_boc")
S.update({
 "reuters_boc": {"name": "Reuters via Yahoo Finance: BoC expected to hike", "url": "https://ca.finance.yahoo.com/news/bank-canada-expected-hike-rate-100130149.html", "tier": 2},
 "il_boc": {"name": "InvestingLive: BoC preview, 81% hike odds", "url": "https://investinglive.com/central-banks/bank-of-canada-preview-81-chance-of-first-hike-in-a-year-to-2-50-economists-split/", "tier": 2},
 "boc_rate": {"name": "Bank of Canada: policy interest rate", "url": "https://www.bankofcanada.ca/core-functions/monetary-policy/key-interest-rate/", "tier": 1},
 "ria": {"name": "Real Investment Advice: stock-bond correlation", "url": "https://realinvestmentadvice.com/resources/blog/stock-bond-correlation-oil-broke-the-hedge-oil-will-fix-it/", "tier": 2},
 "inv_nasdaq": {"name": "Investing.com: Nasdaq's worst day since June", "url": "https://www.investing.com/news/stock-market-news/us-stock-futures-fall-as-investors-weigh-tesla-meta-earnings-4964498", "tier": 2},
 "sa_rsp": {"name": "Seeking Alpha via TradingView: equal weight vs S&P 500", "url": "https://www.tradingview.com/news/seekingalpha:d8ff08a2a094b:0-s-p-500-equal-weight-on-track-for-best-weighted-index-outperformance-since-2009/", "tier": 2},
 "kitco": {"name": "Kitco: Jefferies on real yields and gold", "url": "https://www.kitco.com/news/article/2026-08-07/golds-biggest-headwind-may-finally-be-peaking", "tier": 2},
 "oilprice_q2": {"name": "OilPrice via Yahoo Finance: Big Oil profits", "url": "https://finance.yahoo.com/energy/articles/big-oil-companies-report-record-190000465.html", "tier": 2},
})

# Finding 1: bond hedge regime changed in October
N["sbcorr"].update(tag="Turning negative", asOf=T,
  value="Positive most of 2026; 20-day SPY–TLT −0.24 (Oct 23)",
  facts=[
    f("Since March, SPY and long Treasuries have mostly fallen together as headline CPI rose from 2.4% to 3.7%. The 60-day correlation reached +0.56 in early June.", ["ria"]),
    f("Oct 22: SPY fell 1.2% while long Treasuries rose 1.9%. The 20-day SPY–TLT correlation fell to −0.30, its lowest since early March, and ended the week at −0.24.", ["ria"]),
    f("That day investors 'flocked to the safety of defensive sectors and safe-haven U.S. Treasuries' as the Nasdaq fell 2.6%.", ["inv_nasdaq"]),
    N["sbcorr"]["facts"][2]],
  say="Bonds stopped hedging while oil drove inflation, but the hedge came back on the Oct 22 tech selloff.")
E["y10-sbcorr"]["src"] = ["aqr", "ria"]
N["y10"]["facts"][1] = f("It fell to 4.96% on Oct 22, its first close below 5% since Sep 22, as investors bought Treasuries in the tech selloff. It was 5.00% on Oct 23.", ["fred_dgs10", "inv_nasdaq"])
CH["bonds"]["name"] = "Is the bond hedge back?"
CH["bonds"]["script"] = ("Bonds are starting to hedge again, but only partly. For most of 2026 oil drove inflation: Brent hit a six-month high of $116.72 on Oct 23 after claimed Houthi attacks on Saudi oil sites, and US CPI reached 3.7%. "
  "That pushed the Fed into a September hike and the 10-year to 5.31% on Oct 5, so stocks and bonds fell together. "
  "When growth fears took over on Oct 22, the hedge returned: SPY fell 1.2% while long Treasuries rose 1.9%, and the 20-day correlation dropped to −0.30. "
  "While oil drives inflation the hedge stays unreliable, so I'd keep duration moderate and add other diversifiers. Watch the Fed on Oct 28.")

# Finding 3: oil -> energy needs a source that states the link
E["oil-energy"]["src"] = ["oilprice_q2"]
N["energy"]["facts"][2] = f("FactSet: upward revisions to energy EPS estimates were among the largest contributors to the rise in Q3 blended growth since Sep 30; it is now 29.5%.", ["factset_oct23"])

# Finding 4: Hormuz status sources disagree; say so
N["hormuz"].update(value="Disrupted since Feb 28; October attacks at a war high",
  facts=[N["hormuz"]["facts"][0], N["hormuz"]["facts"][1],
    f("Reports on traffic conflict: Lloyd's List said transits were 'relatively elevated' in early October, while Reuters on Oct 26 called Hormuz largely shut.", ["lloyds", "reuters_houthi"]),
    f("Oct 26: the Houthis said they hit pumping stations on Saudi Arabia's East-West pipeline, an export route around Hormuz. Saudi Arabia did not confirm.", ["reuters_houthi"])],
  say="The root shock is still the Middle East: attacks around Hormuz are at a war high, and the Houthis claim strikes on Saudi export routes.")

# Finding 5: semis carries both Oct 22 causes; ai chain follows its own edges; retire metacompute
N["semis"].update(tag="SOX −6.7% Oct 22",
  value="Chips' worst day since June on Oct 22 (SOX −6.7%)",
  facts=[
    f("Oct 22: the Philadelphia Semiconductor Index (SOX) fell 6.7%, chip stocks' worst day since June 23, as Meta's negative free cash flow revived AI financing worries.", ["ria", "inv_nasdaq"]),
    f("Lam Research also warned that supply constraints will limit chipmakers, and framed it as a supply squeeze, not weaker demand.", ["yahoo_chips"]),
    N["semis"]["facts"][2]],
  say="Chips had their worst day since June on Oct 22 as AI financing worries returned.")
retired = N.pop("metacompute")
m["edges"] = [e for e in m["edges"] if e["id"] != "metacompute-overcap"]
CH["ai"]["edges"] = [x for x in CH["ai"]["edges"] if x != "metacompute-overcap"]
CH["ai"]["script"] = ("The AI scarcity story has been cracking since July. Cheaper Chinese models keep raising doubts about how many chips AI really needs, and DeepSeek's latest update pushed a gauge of Asian chipmakers to its lowest since July on Oct 19. "
  "Those doubts weigh on chip stocks, and money is moving to the average stock: over the past month the equal-weight S&P 500 rose 3.5% while the S&P 500 fell 0.4%. "
  "With tech near 40% of the S&P, owning the index is a concentrated AI bet, which argues for equal weight and for quality over momentum.")
CH["fund"]["script"] = ("AI capex and rates are pulling against each other. Hyperscalers are spending and borrowing heavily: Meta guides $135–145B of capex this year, and its Q3 free cash flow turned negative. "
  "Bond supply like this is one reason the 10-year hit 5.31% on Oct 5, its highest close since 2002. "
  "Higher yields then raise the cost of funding the build-out and lower the value of long-duration growth stocks. Investors are testing that squeeze: Meta's shares fell nearly 7% on Oct 22 when its cash flow turned negative.")

# Finding 6: equal-weight proxy, named
N["breadth"].update(tag="EW leads (1 month)",
  value="Tech ~40% of S&P 500; equal weight +3.5% vs −0.4% (1M)",
  facts=[N["breadth"]["facts"][0], N["breadth"]["facts"][1],
    f("Over the past month to late October, the equal-weight S&P 500 ETF (RSP) rose 3.5% while the S&P 500 fell 0.4%, on track for its biggest outperformance since April 2009.", ["sa_rsp"])],
  say="Owning the index is a concentrated AI bet: tech is about 40% of it.")

# BoC: rate start date, odds from tier-2 named publishers
N["boc"].update(value="2.25% since Oct 29, 2025 · ~81% hike odds for Oct 28",
  facts=[
    f("The policy rate has been 2.25% since Oct 29, 2025.", ["boc_rate"]),
    f("Markets price about an 81% chance of a hike to 2.50% on Oct 28, and 19 of 34 economists in a Reuters poll expect one.", ["il_boc", "reuters_boc"]),
    N["boc"]["facts"][1], N["boc"]["facts"][2]])
E["inflation-boc"].update(why="Gasoline lifted Canadian CPI to 3.1%; the BoC is expected to hike to stop it spreading.", src=["statcan_cpi", "reuters_boc"])

# Minors
N["credit"]["facts"][2]["text"] = "CoreWeave's bonds yielded near 15% in mid-October on concern about AI borrowing."
N["factor"].update(tag="Quality leads in Q3", value="Q3: value, yield and quality beat momentum",
  facts=[x for x in N["factor"]["facts"] if x["basis"] != "weak"])
N["gold"]["facts"].append(f("Jefferies (Aug): 10-year TIPS yields rising from 1.94% to about 2.41% helped drive gold roughly 25% below its peak.", ["kitco"]))
E["realy-gold"]["src"] = ["kitco", "te_gold"]
CH["gold"]["script"] = ("Gold falling during a war looks odd until you follow the chain. Oil lifts inflation, the Fed tightens, and real yields rise: the 10-year TIPS yield is 2.66%, up from 1.72% the day before the war. "
  "Gold pays no coupon, so higher real yields raise the cost of holding it. That's why gold is near $4,000, far below its January record of $5,608. "
  "The latest leg is Fed pricing rather than real yields, which eased in October: a December hike is more than 80% priced. Watch the Fed on Oct 28.")
CH["canada"]["script"] = ("Oil cuts both ways for Canada. It lifts energy stocks, with XLE up about 58% this year, which helps an energy-heavy TSX. "
  "But gasoline pushed Canadian inflation to 3.1% in September while jobs are falling, down 68,000. That's a stagflation bind for the Bank of Canada: markets price about an 81% chance of an Oct 28 hike. "
  "Hike bets are already supporting the loonie, with USD/CAD back below 1.40. Watch whether the BoC looks through gasoline: inflation excluding it is only 2.2%.")
CH["quality"]["script"] = CH["quality"]["script"].replace("and CoreWeave's bonds yielded near 15%", "and CoreWeave's bonds yielded near 15% in mid-October")

# drop unused sources
used = {k for n in N.values() for x in n["facts"] for k in x["src"]} | {k for e in m["edges"] for k in e["src"]}
for k in list(S):
    if k not in used:
        print("removing unused source", k); S.pop(k)
json.dump(m, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(P, "a").write("\n")
print("retired metacompute:", retired["value"])
