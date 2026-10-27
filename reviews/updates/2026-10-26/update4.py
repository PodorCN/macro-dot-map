import json, sys
P = sys.argv[1]
m = json.load(open(P, encoding="utf-8"))
S, N = m["sources"], m["nodes"]
E = {e["id"]: e for e in m["edges"]}
CH = {c["key"]: c for c in m["chains"]}
def f(text, src, basis="sourced"):
    return {"text": text, "src": src, "basis": basis}

# Blocker (L-010): Meta's Oct 26 equity raise
S["sec_meta"] = {"name": "SEC: Meta free writing prospectus, Oct 26", "url": "https://www.sec.gov/Archives/edgar/data/0001326801/000119312526431036/d116268dfwp.htm", "tier": 1}
S["proactive_meta"] = {"name": "Proactive via Yahoo Finance: Meta launches $35B share offerings", "url": "https://ca.finance.yahoo.com/news/meta-launches-35-billion-share-131100761.html", "tier": 2}
a = N["aicapex"]
assert "bond issuance" in a["facts"][2]["text"]
a["facts"] = [a["facts"][0], a["facts"][1],
  f("Oct 26: Meta launched ~$35B of stock offerings ($22.5B common, ~$12.5B mandatory convertible preferred) and plans a ~$60B at-the-market program, alongside investment-grade debt.", ["sec_meta", "proactive_meta"]),
  a["facts"][2]]
a["value"] = "Meta: $135–145B capex; ~$35B stock sale (Oct 26)"
a["say"] = "AI capex now outruns Meta's cash flow, so it is raising money in both the bond and the stock market."
CH["fund"]["script"] = ("AI capex now outruns cash flow, and it has to be funded. Meta guides $135–145B of capex this year, its Q3 free cash flow turned negative, and on Oct 26 it launched about $35B of stock offerings on top of investment-grade debt. "
  "Hyperscaler borrowing adds bond supply, one reason the 10-year hit 5.31% on Oct 5, its highest close since 2002. "
  "Higher yields then raise the cost of funding the build-out and lower the value of long-duration growth stocks. So AI is both a cause of higher yields and a victim of them, and the funding mix, bonds or stock, is now the thing to watch.")

# Minors from review 2026-10-27-001
o = N["oil"]["facts"][0]
assert o["text"].startswith("Brent settled")
o["text"] = o["text"].replace("Brent settled", "Front-month Brent futures settled")
E["inflation-fed"]["why"] = "Oil-driven inflation pushed the Fed into its first hike in over three years."

used = {k for n in N.values() for x in n["facts"] for k in x["src"]} | {k for e in m["edges"] for k in e["src"]}
for k in list(S):
    if k not in used:
        print("removing unused source", k); S.pop(k)
json.dump(m, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(P, "a").write("\n")
