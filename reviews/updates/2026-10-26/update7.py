import json, sys
P = sys.argv[1]
m = json.load(open(P, encoding="utf-8"))
N = m["nodes"]
CH = {c["key"]: c for c in m["chains"]}

# Blocker (L-017, V20): SpaceX's deal (talks reported Oct 6, closed Oct 25) cannot explain the Oct 5 peak
CH["fund"]["script"] = ("AI capex now outruns cash flow, and it has to be funded. Meta guides $135–145B of capex this year and its Q3 free cash flow turned negative. "
  "Heavy borrowing for the build-out is one reason the 10-year hit 5.31% on Oct 5, its highest close since 2002. "
  "Since then the funding has widened: on Oct 25 SpaceX said it closed $40B of GPU debt, and on Oct 26 Meta launched about $35B of stock offerings while Anthropic filed for an IPO reportedly seeking up to $100B. "
  "Higher yields raise the cost of the build-out and lower the value of long-duration growth stocks. So AI is both a cause of higher yields and a victim of them; watch the funding mix.")

# Minor: SpaceX is private debt, not bonds, and not a hyperscaler
i = N["issuance"]
i["say"] = "Part of the yield move is plain supply: heavy Treasury issuance and AI-related borrowing all need buyers."
i["value"] = "Heavy Treasury issuance and AI-related borrowing"
sp = [x for x in i["facts"] if x["text"].startswith("Oct 25: Musk said SpaceX")][0]
sp["text"] = "Oct 25: Musk said SpaceX closed $40B of mainly callable debt to buy GPUs arriving in the first half of 2027; talks were first reported on Oct 6."

# Minor: Musk's exact wording, and his reason (revenue concentration) kept apart from rates
c = [x for x in N["credit"]["facts"] if x["text"].startswith("Oct 25: Musk")][0]
c["text"] = "Oct 25: Musk, who competes with neoclouds, said debt markets have 'almost entirely shut off' money for firms without substantial revenue outside AI data centers."
CH["quality"]["script"] = ("Expensive money is sorting companies by balance sheet. High-yield spreads widened from 2.66% in September to 3.40% on Oct 22, the widest since March. "
  "The weak end is worse: CCC spreads reached 13.56%, wider than at any time since at least 2023, and CoreWeave's bonds yielded near 15% in mid-October. Leveraged borrowers feel higher rates first. "
  "Lenders are also getting choosier about AI: on Oct 25 Musk, a competitor, said debt markets have almost shut for firms without substantial revenue outside AI data centers. "
  "In equities the same logic shows up as quality and value beating momentum, as they did in Q3. I'd favour strong balance sheets in both credit and equity.")

# Minors: ai script keeps causes to the streak they describe, and states the semis-factor mechanism
CH["ai"]["script"] = ("The AI scarcity story has been cracking since July. Cheaper Chinese models keep raising doubts about how many chips AI needs, and DeepSeek's latest update pushed a gauge of Asian chipmakers to its lowest since July on Oct 19. "
  "Oil, rates and doubts about whether AI spending will pay off drove the SOX's eight straight losses to Oct 16. It was down 12.2% for October through Oct 26, though Anthropic's IPO filing lifted it 2.8% that day. "
  "Money moved to the average stock: over the past month the equal-weight S&P 500 rose 3.5% while the S&P 500 fell 0.4%. "
  "With tech near 40% of the S&P, the index is a concentrated AI bet. Momentum is crowded in AI winners, so I'd lean to equal weight and quality as it unwinds.")

json.dump(m, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(P, "a").write("\n")
