import json, sys
P = sys.argv[1]
m = json.load(open(P, encoding="utf-8"))
S, N = m["sources"], m["nodes"]
CH = {c["key"]: c for c in m["chains"]}
T = "2026-10-26"
def f(text, src, basis="sourced"):
    return {"text": text, "src": src, "basis": basis}

S.update({
 "inv_sox": {"name": "Investing.com: PHLX Semiconductor Index historical data", "url": "https://www.investing.com/indices/phlx-semiconductor-historical-data", "tier": 2},
 "il_spacex": {"name": "InvestingLive: SpaceX closes $40B GPU debt deal", "url": "https://investinglive.com/stocks/musk-says-spacex-closed-40-billion-gpu-debt-deal-predicts-neocloud-shakeout/", "tier": 2},
 "tnw_spacex": {"name": "The Next Web: SpaceX raises $40bn in debt for AI chips", "url": "https://thenextweb.com/news/spacex-40bn-debt-ai-chips-musk", "tier": 2},
 "il_2y": {"name": "InvestingLive: $69B 2-year auction, Oct 26", "url": "https://investinglive.com/news/us-treasury-sells-69-billion-of-2-year-notes-at-a-high-yield-of-4-708/", "tier": 2},
})

# Blocker (L-010): the debt side of AI funding on Oct 25-26
i = N["issuance"]
i.update(asOf=T, value="Heavy Treasury and AI debt, incl. SpaceX's $40B GPU deal",
  facts=i["facts"] + [
    f("Oct 25: Musk said SpaceX closed $40B of mainly callable debt to buy GPUs arriving in the first half of 2027.", ["il_spacex", "tnw_spacex"]),
    f("Oct 26: a $69B 2-year auction tailed 0.3 bp, with indirect bidders at 45.7% vs a 58.3% average (graded C−).", ["il_2y"])],
  say="Part of the yield move is plain supply: more bonds, including AI-related debt like SpaceX's $40B GPU deal, need buyers.")
N["credit"]["facts"].append(f("Oct 25: Musk said debt markets have 'almost entirely shut off' money for firms without revenue outside AI data centers.", ["tnw_spacex"]))

# Major (L-017): the SOX streak's stated causes; plus a period return (minor, 5th time)
s = N["semis"]
assert s["facts"][0]["text"].startswith("The SOX fell for eight")
s["facts"][0] = f("The SOX fell 12.2% from Sep 30 to Oct 26. It lost 15.7% in eight straight sessions to Oct 16, its longest losing run since 2008, on oil, rates and doubts that AI spending will pay off.", ["inv_sox", "twsw_sox"])
s.update(tag="SOX −12.2% in Oct", value="SOX −12.2% Oct 1–26; +2.8% on Oct 26 (Anthropic IPO)")

# overcap: re-verified with the new counterpoint; say line reflects both sides
N["overcap"].update(asOf=T, say="The scarcity story cracked, but the doubt cuts both ways: Anthropic's IPO filing on Oct 26 revived the AI trade.")

# Major (L-018): ai script covers all four edges and ends with an implication
CH["ai"]["script"] = ("The AI scarcity story has been cracking since July. Cheaper Chinese models keep raising doubts about how many chips AI needs, and DeepSeek's latest update pushed a gauge of Asian chipmakers to its lowest since July on Oct 19. "
  "Doubts about whether AI spending will pay off, along with oil and rates, drove the SOX down 12.2% in October through Oct 26, though Anthropic's IPO filing lifted it 2.8% that day. "
  "Money moved to the average stock: over the past month the equal-weight S&P 500 rose 3.5% while the S&P 500 fell 0.4%. "
  "With tech near 40% of the S&P, owning the index is a concentrated AI bet, so I'd lean to equal weight and to quality over momentum, which led in Q3.")
CH["fund"]["script"] = ("AI capex now outruns cash flow, and it has to be funded. Meta guides $135–145B of capex this year and its Q3 free cash flow turned negative. "
  "On the equity side, Meta launched about $35B of stock offerings on Oct 26 and Anthropic filed for an IPO reportedly seeking up to $100B. "
  "On the debt side, SpaceX closed $40B of GPU debt, adding to bond supply that helped push the 10-year to 5.31% on Oct 5, its highest close since 2002. "
  "Higher yields raise the cost of the build-out and lower the value of long-duration growth stocks. So AI is both a cause of higher yields and a victim of them; watch the funding mix.")
CH["quality"]["script"] = ("Expensive money is sorting companies by balance sheet. High-yield spreads widened from 2.66% in September to 3.40% on Oct 22, the widest since March. "
  "The weak end is worse: CCC spreads reached 13.56%, wider than at any time since at least 2023, CoreWeave's bonds yielded near 15% in mid-October, and on Oct 25 Musk said debt markets have almost shut for firms without revenue outside AI data centers. "
  "Leveraged borrowers feel higher rates first. In equities the same logic shows up as quality and value beating momentum, as they did in Q3. I'd favour strong balance sheets in both credit and equity.")

# Minor: The National does not name the contract
o = N["oil"]["facts"][0]
o["text"] = o["text"].replace("Front-month Brent futures settled", "Brent settled")

used = {k for n in N.values() for x in n["facts"] for k in x["src"]} | {k for e in m["edges"] for k in e["src"]}
for k in list(S):
    if k not in used:
        print("removing unused source", k); S.pop(k)
json.dump(m, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(P, "a").write("\n")
