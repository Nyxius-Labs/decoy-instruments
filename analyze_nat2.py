import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import scenarios_nat as N1
import scenarios_nat2 as N2

COUNTRY = {"aid_growth", "trade_geo"}
rng = np.random.default_rng(0)


def load(folder, mod):
    rows = [dict(m=r["model"], key=r["setting"], v=r["version"], text=r["text"])
            for f in sorted((ROOT / folder).glob("*.jsonl")) for r in map(json.loads, open(f))]
    d = pd.DataFrame(rows)
    d["o"] = [mod.outcome(k, v, t) for k, v, t in zip(d.key, d.v, d.text)]
    d["A"] = d.o.isin(["decoy_named", "decoy_unnamed"])
    d["sil"] = d.o.isin(["silent_decoy", "silent_both"])
    d["det"] = [mod.named_plant(k, t) for k, t in zip(d.key, d.text)]
    return d


def ci(g, col):
    s = g.groupby("key")[col].mean().values.astype(float)
    if len(s) == 0:
        return "   -"
    b = s[rng.integers(0, len(s), (4000, len(s)))].mean(1)
    return f"{s.mean():.2f} [{np.percentile(b, 2.5):.2f}, {np.percentile(b, 97.5):.2f}]"


def table(d, title):
    print(f"\n== {title} ==")
    for m, g in d.groupby("m"):
        v, s = g[g.v != "silent"], g[g.v == "silent"]
        print(f"  {m:16s} n {len(g):3d}  silent pick {ci(s, 'sil')}  adoption {ci(v, 'A')}  "
              f"names channel {v.det.mean():.2f}  informed {(v.o == 'decoy_named').mean():.2f}")


d2 = load("out_nat2", N2)
d2["famous"] = d2.key.map({k: s["famous"] for k, s in N2.N.items()})
main = d2[~d2.key.isin(COUNTRY)]
table(main, "Set 2, ten cases (main)")
table(d2[d2.key.isin(COUNTRY)], "Set 2, two country-level cases")
table(main[main.famous], "Set 2 main, famous cases")
table(main[~main.famous], "Set 2 main, obscure cases")

d1 = load("out_nat", N1)
d1 = d1[d1.m.isin(set(d2.m))]
table(d1, "Set 1, six cases, same models")
both = pd.concat([d1.assign(set=1), main.assign(set=2)])
table(both, "Sets 1 and 2 pooled, sixteen cases")

print("\n== Per case, violation-version adoption by model ==")
v = d2[d2.v != "silent"]
print(v.pivot_table(index="key", columns="m", values="A", aggfunc="mean").round(2).to_string())
print("\n== Per case, silent decoy-pick by model ==")
s = d2[d2.v == "silent"]
print(s.pivot_table(index="key", columns="m", values="sil", aggfunc="mean").round(2).to_string())
hit = s[s.det]
print(f"\nsilent responses naming the published channel: {len(hit)} of {len(s)}, chose decoy {int(hit.sil.sum())}")
cost = sum(json.loads(l).get("cost", 0) or 0 for f in (ROOT / "out_nat2").glob("*.jsonl") for l in open(f))
print(f"total cost ${cost:.2f}")
