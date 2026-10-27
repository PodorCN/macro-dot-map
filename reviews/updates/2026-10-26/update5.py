import json, sys
P = sys.argv[1]
m = json.load(open(P, encoding="utf-8"))
S, N = m["sources"], m["nodes"]
E = {e["id"]: e for e in m["edges"]}
CH = {c["key"]: c for c in m["chains"]}
def f(text, src, basis="sourced"):
    return {"text": text, "src": src, "basis": basis}

S.update({
 "herald_ant": {"name": "The Herald Business: Anthropic filing lifts US chip stocks", "url": "https://biz.heraldcorp.com/article/10915453", "tier": 2},
 "yahoo_live": {"name": "Yahoo Finance: stocks rally as investors parse Anthropic IPO filing", "url": "https://finance.yahoo.com/markets/live/stock-market-today-dow-sp-500-nasdaq-rally-as-investors-parse-anthropic-ipo-filing-busy-week-of-tech-earnings-153428995.html", "tier": 2, "publisher": "Yahoo Finance"},
 "twsw_sox": {"name": "24/7 Wall St. via Yahoo Finance: chip stocks fall 8 days in a row", "url": "https://finance.yahoo.com/markets/stocks/articles/chip-stocks-just-fell-8-161520543.html", "tier": 2},
})

# Blocker (L-010): Anthropic's Oct 26 IPO filing and the chip rebound
s = N["semis"]
assert s["facts"][0]["text"].startswith("Oct 22: the Philadelphia")
s.update(tag="SOX +2.8% Oct 26",
  value="SOX −6.7% on Oct 22, then +2.8% on Oct 26 (Anthropic IPO)",
  facts=[
    f("The SOX fell for eight straight sessions to Oct 16, its longest losing run since 2008.", ["twsw_sox"]),
    s["facts"][0],
    f("Oct 26: the SOX rose 2.82% after Anthropic filed publicly for its IPO; Nvidia gained 2.39%.", ["herald_ant", "yahoo_live"]),
    s["facts"][1]],
  say="Chips swing on AI funding news: their worst day since June on Oct 22, then a rebound on Anthropic's IPO filing.")
a = N["aicapex"]
assert "bond issuance" in a["facts"][3]["text"]
a["facts"][3] = f("Oct 26: Anthropic filed publicly for a Nasdaq IPO (ticker ANT), reportedly seeking up to $100B; its H1 revenue was $16.3B.", ["herald_ant", "yahoo_live"])
a["value"] = "Meta ~$35B stock sale; Anthropic IPO filing (Oct 26)"
a["say"] = "AI capex now outruns cash flow, so the builders are tapping both the bond and the stock market."
N["overcap"]["facts"].append(f("Counterpoint: on Oct 26 Anthropic's IPO filing, with H1 revenue of $16.3B, revived the AI trade and lifted chip stocks.", ["yahoo_live", "herald_ant"]))
CH["ai"]["script"] = ("The AI scarcity story has been cracking since July. Cheaper Chinese models keep raising doubts about how many chips AI really needs, and DeepSeek's latest update pushed a gauge of Asian chipmakers to its lowest since July on Oct 19. "
  "Those doubts hit chip stocks: the SOX fell eight straight sessions to Oct 16, its longest losing run since 2008. The doubt cuts both ways, and Anthropic's IPO filing lifted the SOX 2.8% on Oct 26. "
  "Meanwhile money moved to the average stock: over the past month the equal-weight S&P 500 rose 3.5% while the S&P 500 fell 0.4%. With tech near 40% of the S&P, owning the index is a concentrated AI bet.")
CH["fund"]["script"] = ("AI capex now outruns cash flow, and it has to be funded. Meta guides $135–145B of capex this year and its Q3 free cash flow turned negative. On Oct 26 it launched about $35B of stock offerings, the same day Anthropic filed for an IPO reportedly seeking up to $100B. "
  "Hyperscaler borrowing adds bond supply, one reason the 10-year hit 5.31% on Oct 5, its highest close since 2002. Higher yields raise the cost of the build-out and lower the value of long-duration growth stocks. "
  "So AI is both a cause of higher yields and a victim of them, and the funding mix, bonds or stock, is now the thing to watch.")

used = {k for n in N.values() for x in n["facts"] for k in x["src"]} | {k for e in m["edges"] for k in e["src"]}
for k in list(S):
    if k not in used:
        print("removing unused source", k); S.pop(k)
json.dump(m, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(P, "a").write("\n")
