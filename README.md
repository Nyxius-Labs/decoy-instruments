# Decoy Instruments

Code and data for Crainic and Yee, "Decoy Instruments: Do AI Research Agents Act on Documentation That Rules Out an Instrument?" The repository also holds `decoybench`, a package that runs the same test on any agent.

## Install

```
pip install -r requirements.txt
```

To test your own agent, install the package instead and see `decoybench/README.md`:

```
pip install "decoybench[all]"
decoybench --model anthropic:claude-haiku-4-5
decoybench --model anthropic:claude-haiku-4-5 --multiturn
```

## Reproduce the paper's numbers

These scripts read the saved responses and make no API calls.

```
python analyze_v2.py
python reproduce.py
python analyze_nat2.py
```

`analyze_v2.py` is the analysis fixed in the plan: Table 1 and the main hypothesis tests. `reproduce.py` prints the follow-ups, the first held-out set, the file-access run and the coder agreement, and writes Figure 1 to `fig_adoption.pdf`. `analyze_nat2.py` prints the second held-out set.

To check that the prompts match the ones logged before the first call:

```
python abs_v2.py dry --tier B
git diff --stat out5/prompt_hashes_B.tsv
```

The second command should print nothing.

## Rerun the models

These commands call paid APIs.

```
export ANTHROPIC_API_KEY=... OPENAI_API_KEY=... OPENROUTER_API_KEY=...
python abs_v2.py run --tier B --models <model> --cap <model>=<USD>
python reasoning_off.py
python run_nat.py
python fictional.py
python run_nat2.py
```

`run_nat2.py` reads the OpenRouter key from `~/.openrouter_key`. `python make_cases.py` rebuilds the package's cases, and `python build_coding.py sheets` redraws the 240-response coding sample.

## Contents

| Path | Contents |
|---|---|
| `scenarios_v2.py`, `kill2.py`, `kill3.py` | The 20 settings and their codebooks |
| `estimate_v2.py` | Simulated data and regression tables for the estimation step |
| `cost_v2.py`, `abs_v2.py` | Call manifest and runner |
| `scenarios_nat.py`, `run_nat.py`, `fictional.py` | First held-out set, and the same cases with invented programs |
| `scenarios_nat2.py`, `run_nat2.py` | Second held-out set |
| `reasoning_off.py` | Reasoning follow-up (plan in `followup/reasoning_off/PLAN.md`) |
| `build_coding.py`, `coding/` | Coding sample, instructions, both coders' codes and the reconciled codes |
| `out5/`, `out_nat/`, `out_nat2/`, `followup/` | Model responses. `out_nat/v1/` is the first held-out run before calibration |
| `decoybench/`, `make_cases.py` | The package and the script that exports its cases |
| `docs/` | Analysis plan and held-out case rules |
| `frozen/abs_v2.py` | Runner as hashed in the plan |

Files whose SHA-256 is listed in `docs/` are kept byte for byte as hashed.
