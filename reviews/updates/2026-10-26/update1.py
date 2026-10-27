import json, sys
P = sys.argv[1]
m = json.load(open(P, encoding="utf-8"))
T = "2026-10-26"
S, N, E = m["sources"], m["nodes"], {e["id"]: e for e in m["edges"]}
CH = {c["key"]: c for c in m["chains"]}

S.update({
 "fred_dgs10": {"name": "FRED: 10-year Treasury yield (DGS10)", "url": "https://fred.stlouisfed.org/series/DGS10", "tier": 1},
 "fred_tips": {"name": "FRED: 10-year TIPS yield (DFII10)", "url": "https://fred.stlouisfed.org/series/DFII10", "tier": 1},
 "fred_ccc": {"name": "FRED: ICE BofA CCC & lower OAS", "url": "https://fred.stlouisfed.org/series/BAMLH0A3HYC", "tier": 1},
 "fred_cad": {"name": "FRED: USD/CAD (DEXCAUS)", "url": "https://fred.stlouisfed.org/series/DEXCAUS", "tier": 1},
 "national_oil": {"name": "The National: oil at six-month high", "url": "https://www.thenationalnews.com/business/energy/2026/10/23/oil-prices-rise-as-houthis-launch-another-wave-of-attacks-on-saudi-arabia/", "tier": 2},
 "reuters_houthi": {"name": "Reuters: Houthis claim Saudi pipeline attack", "url": "https://za.investing.com/news/world-news/houthis-say-they-attacked-saudi-oil-pumping-stations-riyadh-airport-as-fighting-intensifies-4524874", "tier": 1},
 "lloyds": {"name": "Lloyd's List Intelligence: Hormuz brief Oct 22", "url": "https://www.lloydslistintelligence.com/resources/blog/strait-of-hormuz-brief-22-october-2026", "tier": 1},
 "bls_cpi": {"name": "BLS: CPI, September 2026", "url": "https://www.bls.gov/news.release/cpi.nr0.htm", "tier": 1},
 "umich": {"name": "University of Michigan: consumer survey", "url": "https://www.sca.isr.umich.edu/", "tier": 1},
 "statcan_cpi": {"name": "Statistics Canada: CPI, September 2026", "url": "https://www150.statcan.gc.ca/n1/daily-quotidien/261019/dq261019a-eng.htm", "tier": 1},
 "statcan_lfs": {"name": "Statistics Canada: Labour Force Survey, Sept", "url": "https://www150.statcan.gc.ca/n1/daily-quotidien/261009/dq261009a-eng.htm", "tier": 1},
 "fed_sep": {"name": "Federal Reserve: Sep 16 statement", "url": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm", "tier": 1},
 "fed_cal": {"name": "Federal Reserve: FOMC calendar", "url": "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm", "tier": 1},
 "fx_gold": {"name": "FXStreet: gold off three-month low", "url": "https://www.fxstreet.com/news/gold-rebounds-from-three-month-low-and-retakes-4-000-on-weak-usd-focus-remains-on-fomc-202610260434", "tier": 2},
 "yahoo_boc": {"name": "Yahoo Finance: BoC expected to hike Oct 28", "url": "https://ca.finance.yahoo.com/news/bank-canada-expected-raise-rates-140600608.html", "tier": 2},
 "yahoo_xle": {"name": "Yahoo Finance: XLE performance", "url": "https://finance.yahoo.com/quote/XLE/performance/", "tier": 2},
 "yahoo_chips": {"name": "Yahoo Finance: chip stocks fall on supply warning", "url": "https://finance.yahoo.com/technology/articles/chip-stocks-fall-supply-warning-154508313.html", "tier": 2},
 "ap_week": {"name": "AP: how major US indexes fared Oct 23", "url": "https://finance.yahoo.com/markets/world-indices/articles/major-us-stock-indexes-fared-201458598.html", "tier": 1},
 "factset_oct23": {"name": "FactSet: earnings season update Oct 23", "url": "https://insight.factset.com/sp-500-earnings-season-update-october-23-2026", "tier": 1},
 "meta_ir": {"name": "Meta: Q3 2026 results", "url": "https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Third-Quarter-2026-Results/default.aspx", "tier": 1},
 "cnbc_metaq3": {"name": "CNBC: Meta free cash flow negative", "url": "https://www.cnbc.com/2026/10/22/meta-stock-q3-earnings-free-cash-flow.html", "tier": 1},
 "cnbc_cw": {"name": "CNBC: CoreWeave bond yields near 15%", "url": "https://www.cnbc.com/2026/10/14/coreweave-stock-bond-yields-ai-debt.html", "tier": 1},
})

def node(nid, **kw):
    N[nid].update(kw); N[nid]["asOf"] = T

def f(text, src, basis="sourced"):
    return {"text": text, "src": src, "basis": basis}

node("hormuz",
  value="Hormuz largely shut since Feb 28; attacks at a peak",
  facts=[N["hormuz"]["facts"][0],
    f("Lloyd's List counted at least 28 confirmed attacks around Hormuz in October as of Oct 22, the most in any month since the war began.", ["lloyds"]),
    f("Oct 26: the Houthis said they hit pumping stations on Saudi Arabia's East-West pipeline, a key export route while Hormuz is largely shut. Saudi Arabia did not confirm.", ["reuters_houthi"])],
  say="The root shock is still the Middle East: Hormuz is largely shut, and the Houthis are now targeting Saudi Arabia's bypass pipeline.",
  keepReason="Ongoing: October has the most Hormuz attacks of the war, and Houthi strikes on Saudi export routes lifted Brent to a six-month high on Oct 23.")

node("oil", tag="Brent ~$115",
  value="Brent ~$115 (Oct 26) · settled $116.72 on Oct 23",
  facts=[
    f("Brent settled at $116.72 on Oct 23, a six-month high, up 6.24% on the week. WTI closed at $103.27.", ["national_oil"]),
    f("Still below the 2026 intraday peak of $126.41 set on Apr 30.", ["il_gs"]),
    f("Brent eased to about $115 on Oct 26 as Saudi Arabia held talks with Iran. It is up about 18% over the past month and 77% over the year.", ["te_brent"])],
  say="Brent is near $115, a six-month high, but still below the April peak of $126.")

node("inflation", tag="US CPI 3.7%",
  value="US CPI 3.7% (Sept) · UMich 1-yr 4.7% · Canada 3.1%",
  facts=[
    f("US CPI rose 3.7% over the year to September. Gasoline rose 9.1% in the month, over half of the monthly increase; core rose 0.3%.", ["bls_cpi"]),
    f("University of Michigan year-ahead inflation expectations rose to 4.7% in October, from 4.6% in September.", ["umich"]),
    f("Canadian CPI rose 3.1% in September, led by gasoline (+27.8%). Excluding gasoline it rose 2.2%.", ["statcan_cpi"])],
  say="Oil is pushing headline inflation up on both sides of the border, while core is calmer.")

node("fed", tag="Decides Oct 28",
  value="3.75–4.00% after the Sept hike · next decision Oct 28",
  facts=[
    f("On Sep 16 the Fed raised its target range by a quarter point to 3.75–4.00%, its first hike in more than three years.", ["fed_sep", "james"]),
    f("Next decision Oct 28. Markets expect a hold; CME FedWatch odds of a December hike are above 80%.", ["te_gold", "fed_cal"])],
  say="The Fed hiked in September and is expected to hold on Oct 28, with a December hike largely priced.")

node("y10", tag="5.00% · peak 5.31%",
  value="5.00% (Oct 23), off the 5.31% 2026 high of Oct 5",
  facts=[
    f("The 10-year closed at 5.31% on Oct 5, its highest close since May 2002. It started 2026 at 4.19%.", ["fred_dgs10"]),
    f("It closed at 5.00% on Oct 23, down from 5.13% on Oct 21.", ["fred_dgs10"]),
    f("Drivers: inflation, Fed hikes, and heavy bond supply including AI-related borrowing.", ["cnbc_10y"])],
  say="The 10-year hit 5.31% in early October, its highest since 2002, and is now about 5%.")

node("realy", tag="TIPS 2.66%",
  value="10-yr TIPS 2.66% (Oct 23), up from 1.72% before the war",
  facts=[
    f("The 10-year TIPS yield was 2.66% on Oct 23, up from 1.72% on Feb 27, the day before the war began. It peaked at 2.95% on Oct 5.", ["fred_tips"]),
    N["realy"]["facts"][1]],
  say="Real yields are up almost a point since February, so this isn't only an inflation-expectations story.")

node("gold", tag="~$4,000 · 3-mo low",
  value="About $4,000, near a three-month low",
  facts=[
    f("Gold was about $4,017 on Oct 26, down 2.4% over the past month. Its record was $5,608 in January 2026.", ["te_gold"]),
    f("It hit a three-month low just below $4,000 before recovering on Oct 26, ahead of the Fed decision.", ["fx_gold"]),
    f("Traders say high oil makes a higher-for-longer Fed more likely, which weighs on non-yielding gold.", ["te_gold"])],
  say="Gold is near $4,000, far below its January record of $5,608, which tells you real yields are in charge.")

node("credit", tag="HY OAS 3.38%",
  value="HY OAS 3.38% (338 bp, Oct 23) · CCC 13.56%",
  facts=[
    f("HY spreads rose from 2.66% on Sep 21 to 3.40% on Oct 22, the widest since Mar 30 (3.46%, the 2026 high). They were 3.38% on Oct 23.", ["fred"]),
    f("CCC-and-lower spreads reached 13.56% on Oct 23, up from 10.75% on Sep 22 and wider than at any time since at least 2023.", ["fred_ccc"]),
    f("CoreWeave's bonds yielded near 15% on Oct 14 on concern about AI borrowing.", ["cnbc_cw"])],
  say="Credit is widening fast at the weak end: CCC spreads are the widest in years, and AI borrowers are in focus.")

node("semis", tag="SOXX −6% Oct 22",
  value="SOXX fell about 6% on Oct 22 on Lam's supply warning",
  facts=[
    f("Oct 22: Lam Research said supply constraints for some components will limit chipmakers, and the iShares Semiconductor ETF (SOXX) fell about 6%.", ["yahoo_chips"]),
    f("Lam framed it as a supply squeeze, not weaker demand, and expects the industry to catch up soon.", ["yahoo_chips"]),
    N["semis"]["facts"][1]],
  say="Chips fell about 6% on Oct 22, this time on a supply squeeze rather than demand doubts.")

node("aicapex", tag="Meta $135–145B",
  value="Meta guides $135–145B of 2026 capex (Oct 21)",
  facts=[
    f("Meta now guides 2026 capex of $135–145B, mostly for AI infrastructure. Q3 capex was $34.91B.", ["meta_ir"]),
    f("Meta's free cash flow turned negative (−$2.1B) in Q3, and its shares fell nearly 7% on Oct 22.", ["cnbc_metaq3"]),
    N["aicapex"]["facts"][1]],
  say="AI capex keeps rising, and at Meta it now exceeds the cash the business generates.")

node("boc", tag="2.25% · Oct 28",
  value="2.25% since Oct 2025 · ~78% hike odds for Oct 28",
  facts=[
    f("Futures put the odds of a quarter-point hike on Oct 28 at 78%, and most economists in a Reuters poll expect one.", ["yahoo_boc"]),
    f("Employment fell by 68,000 in September and unemployment rose to 6.5%.", ["statcan_lfs"]),
    f("Inflation excluding gasoline was only 2.2% in September.", ["statcan_cpi"])],
  say="The BoC is in a stagflation bind: 3.1% inflation, falling jobs, and a likely hike on Oct 28.")
# say-line number 3.1 must be in its own facts
N["boc"]["facts"][2]["text"] = "Headline CPI was 3.1% in September, but only 2.2% excluding gasoline."

node("energy", tag="XLE +58% YTD",
  value="XLE +58.1% YTD through Oct 23",
  facts=[
    f("The Energy Select Sector SPDR (XLE) is up 58.14% this year through Oct 23.", ["yahoo_xle"]),
    N["energy"]["facts"][1],
    f("FactSet: higher energy EPS estimates are among the biggest reasons Q3 S&P 500 earnings growth rose to 29.5%.", ["factset_oct23"])],
  say="Energy is up nearly 60% this year as oil climbs.")

node("cad", tag="USD/CAD ~1.40",
  value="USD/CAD 1.3993 (Oct 23), down from 1.4273 on Oct 14",
  facts=[
    f("USD/CAD fell from 1.4273 on Oct 14, its 2026 high, to 1.3993 on Oct 23 (Fed H.10 rates).", ["fred_cad"]),
    N["cad"]["facts"][0], N["cad"]["facts"][1]],
  say="Hike bets and oil have pushed the loonie back below 1.40 per US dollar.")

node("breadth", tag="Tech ~40% of S&P",
  value="Tech ~40% of the S&P 500; small caps led last week",
  facts=[N["breadth"]["facts"][0], N["breadth"]["facts"][1],
    f("Week to Oct 23: the Russell 2000 rose 2% while the S&P 500 fell 0.5% and the Nasdaq Composite 0.7%.", ["ap_week"])],
  say="Owning the index is a concentrated AI bet: tech is about 40% of it.")

E["inflation-boc"].update(why="Gasoline lifted Canadian CPI to 3.1%, so markets price a hike on Oct 28.", src=["statcan_cpi", "yahoo_boc"])
E["oil-inflation"]["src"] = ["bls_cpi", "cnbc_real"]
E["hormuz-oil"]["src"] = ["politis", "national_oil"]

CH["bonds"]["script"] = ("The key portfolio issue is that bonds aren't hedging equities. The shock is oil: attacks in the Gulf lifted Brent to a six-month high of $116.72 on Oct 23. "
  "Gasoline drove US inflation to 3.7% in September, and the Fed, which hiked in September, decides again on Oct 28. The 10-year hit 5.31% in early October. "
  "When inflation drives rates, a bad day for stocks is often a bad day for bonds too: Nationwide notes the 40-day correlation is the most positive since 1999. "
  "I wouldn't abandon bonds. I'd keep duration short and add diversifiers with genuinely low equity beta, such as real assets.")
CH["gold"]["script"] = ("Gold falling during a war looks odd until you follow the chain. Oil lifts inflation, the Fed responds by tightening, and real yields rise: "
  "the 10-year TIPS yield is 2.66%, up from 1.72% the day before the war. Gold pays no coupon, so higher real yields raise the cost of holding it. "
  "That's why gold is near $4,000, far below its January record of $5,608, even with the Middle East unresolved. In this regime, real rates beat the safe-haven story. "
  "Watch the Fed on Oct 28: a December hike is already more than 80% priced.")
CH["fund"]["script"] = ("AI capex and rates are pulling against each other. Hyperscalers are borrowing heavily to build data centres: Meta alone guides $135–145B of capex this year, and its free cash flow turned negative. "
  "That bond supply is one reason the 10-year hit 5.31% on Oct 5, its highest close since 2002. "
  "But higher yields raise the cost of funding the same build-out and lower the value of long-duration growth stocks. So AI is both a cause of higher yields and a victim of them.")
CH["ai"]["script"] = ("The AI scarcity story cracked in July. Meta said it would rent out spare compute, which the market read as overbuilding, and cheaper Chinese models raised doubts about how many chips AI needs. "
  "The latest leg was different: on Oct 22 SOXX fell about 6% after Lam Research warned of supply constraints, a supply squeeze rather than weaker demand. "
  "Last week small caps rose 2% while the S&P 500 fell. With tech near 40% of the S&P, owning the index is a concentrated AI bet, which argues for equal weight and for quality over momentum.")
CH["canada"]["script"] = ("Oil cuts both ways for Canada. It lifts energy stocks, with XLE up about 58% this year, which helps an energy-heavy TSX. "
  "But gasoline pushed Canadian inflation to 3.1% in September while jobs are falling, down 68,000. That's a stagflation bind for the Bank of Canada, and futures put the odds of an Oct 28 hike at 78%. "
  "Hike bets are already supporting the loonie, with USD/CAD back below 1.40. Watch whether the BoC looks through gasoline: inflation excluding it is only 2.2%.")
CH["quality"]["script"] = ("Expensive money is sorting companies by balance sheet. High-yield spreads widened from 2.66% in September to 3.40% on Oct 22, the widest since March. "
  "The weak end is worse: CCC spreads reached 13.56%, wider than at any time since at least 2023, and CoreWeave's bonds yielded near 15%. Leveraged borrowers feel higher rates first. "
  "In equities the same logic shows up as quality and value beating momentum, as they did in Q3. I'd favour strong balance sheets in both credit and equity.")

for k in ["lite", "disp", "mitrade", "tt_credit", "cnn_10y", "yahoo_hike", "mt_wti", "oilprice", "cnbc_hy", "bnn"]:
    used = any(k in x["src"] for n in N.values() for x in n["facts"]) or any(k in e["src"] for e in m["edges"])
    if not used: S.pop(k)
    else: print("still used:", k)

m["meta"]["asOf"] = T
m["meta"]["version"] = 3
json.dump(m, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(P, "a").write("\n")
