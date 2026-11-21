# Decoy Instruments, held-out natural set 2: addendum

Written 2026-11-20, after one smoke call per model on a single case-version (saiz, chain, draw 0; kept, since the main run reuses it) and while the main run was in progress, before any response was scored or read beyond checking that it parsed. Set 2 follows `natural_rules.md` except for the deviations listed here.

## Cases

Twelve cases, chosen from a literature search (36 candidates, `iv_cases.csv`) after the six-case results were known. A candidate was kept if the violation source was verified against Crossref or RePEc, the critique concerns the exclusion restriction of the named instrument, and the design does not duplicate the weather, judge-leniency or draft-lottery families already in the benchmark. Keys: saiz, flow_pressure, mtv, rural_banks, aid_growth, hausman, catholic, twins, school_laws, tax_change, trade_geo, bartik. Citations for each IV study and channel source are in `scenarios_nat2.py` (fields `cite`, `channel_cite`).

## Deviations from natural_rules.md

1. Rule 3 (manipulable treatment). aid_growth and trade_geo have country-level treatments. They are kept, but the main pooled estimate uses the other ten cases, and the two are reported separately.
2. No calibration round. Every alternative is set from the start at the final calibration level of set 1 (a stated subsample and a first-stage F-statistic of about 2). Silent decoy-pick rates are reported per case; no case is changed after any output.
3. Models. A reduced panel: gpt-4o-mini, gpt-5-mini, haiku-4.5, haiku-5.5 and gemma-4-31b with 3 draws, and gemini-4-argon with 1 draw as the only frontier check. All calls go through OpenRouter (provider pinned to the model's maker or to the provider used in set 1).
4. Famous coding. A case is famous if the IV study or the channel source has at least 1,000 citations, from Semantic Scholar or Crossref counts looked up on 2026-11-20. No count was found for Hausman (1996), which is coded famous by judgement because "Hausman instruments" is a textbook term.
5. Channel wording. The implied facts paraphrase the published channel and move it into the dataset's documentation, as in set 1. rural_banks states the channel as concurrent rural anti-poverty programs aimed at the states with few branches, which is the class of policy the critique names, not a specific program.

## Frozen files

scenarios_nat2.py sha256 3d0a624d579d54234090e0b3706e13f089bbec88c0dc550a7eca9ba299a1eb29
run_nat2.py sha256 1bae4ee6d7f1b4d1743e6e01abc4d141d3ab8407476a7df119e0b68dc7d78f15
