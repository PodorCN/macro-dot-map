import json, sys
P = sys.argv[1]
m = json.load(open(P, encoding="utf-8"))
S, N = m["sources"], m["nodes"]
E = {e["id"]: e for e in m["edges"]}
CH = {c["key"]: c for c in m["chains"]}

# Blocker 1 (L-013): name syndicated articles by their real publisher
S["yahoo_chips"].update(name="24/7 Wall St. via Yahoo Finance: chip stocks fall on supply warning", tier=2)
S["inv_nasdaq"].update(name="Investing.com: Nasdaq slides on AI financing worries", publisher="Investing.com")
S["inv_cad"].update(name="Investing.com: CAD and BoC hike bets", publisher="Investing.com")
S.pop("edge_kimi")
S["tnw_kimi"] = {"name": "The Next Web: Kimi K3 and the AI selloff", "url": "https://thenextweb.com/news/kimi-k3-china-ai-tech-rout-selloff", "tier": 2}
k3 = N["cheapai"]["facts"][0]
assert "Kimi K3" in k3["text"]
k3.update(text="Jul 17: Moonshot's Kimi K3 helped fuel a selloff in tech and chip stocks; traders compared it to the DeepSeek shock of early 2025.", src=["tnw_kimi"])

# Blocker 2 (L-014): y10-semis has no tier-1/2 source stating the link for this episode
E["y10-semis"].update(src=[], basis="unsourced")

# Minors from review 2026-10-26-002
N["semis"]["facts"][1]["text"] = "Lam Research also warned that supply constraints for some components will limit chipmakers; its CEO expects the industry to be 'caught up very shortly'."
CH["bonds"]["script"] = CH["bonds"]["script"].replace("When growth fears took over on Oct 22", "When AI-spending worries hit tech on Oct 22")
N["gold"]["say"] = "Gold is near $4,000, far below its January record of $5,608, as higher real yields and Fed hike bets raise the cost of holding it."
h = N["hormuz"]
h["facts"][2] = {"text": "Reports on traffic conflict: Lloyd's List saw 'relatively elevated' transits in early October and Trading Economics cites flows near prewar levels, while Reuters on Oct 26 called Hormuz largely shut.", "src": ["lloyds", "te_brent", "reuters_houthi"], "basis": "sourced"}
h["keepReason"] = "Ongoing: October has the most Hormuz attacks of the war, and claimed Houthi strikes on Saudi export routes lifted Brent to a six-month high on Oct 23."
for x in N["factor"]["facts"]:
    x["text"] = x["text"].replace("when AI euphoria put momentum on top", "when momentum was on top")
CH["canada"]["script"] = CH["canada"]["script"].replace(", which helps an energy-heavy TSX", "")

used = {k for n in N.values() for x in n["facts"] for k in x["src"]} | {k for e in m["edges"] for k in e["src"]}
for k in list(S):
    if k not in used:
        print("removing unused source", k); S.pop(k)
json.dump(m, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(P, "a").write("\n")
