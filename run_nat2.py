import os
import sys
from pathlib import Path

import abs_v2 as A
import scenarios_nat2 as N

os.environ.setdefault("OPENROUTER_API_KEY", Path("~/.openrouter_key").expanduser().read_text().strip())

ANTH = {"provider": {"only": ["anthropic"], "allow_fallbacks": False}}
A.MODELS.update({
    "haiku-4.5": ("openrouter", "anthropic/claude-haiku-4.5", dict(ANTH)),
    "haiku-5.5": ("openrouter", "anthropic/claude-haiku-5.5", dict(ANTH, reasoning={"effort": "medium"})),
    "gpt-4o-mini": ("openrouter", "openai/gpt-4o-mini", {"provider": {"only": ["openai"], "allow_fallbacks": False}}),
    "gpt-5-mini": ("openrouter", "openai/gpt-5-mini",
                   {"provider": {"only": ["openai"], "allow_fallbacks": False}, "reasoning": {"effort": "medium"}}),
})

A.OUT = Path(__file__).resolve().parent / "out_nat2"
A.OUT.mkdir(exist_ok=True)
A.V = N

CAPS = {"gpt-4o-mini": 0.8, "gpt-5-mini": 2.0, "haiku-4.5": 3.5, "haiku-5.5": 0.8, "gemma-4-31b": 0.8,
        "gemini-4-argon": 2.0}
DRAWS = {"gemini-4-argon": 1}


def rows_for(m, smoke=False):
    keys = N.ORDER[:1] if smoke else N.ORDER
    vers = ("chain",) if smoke else ("silent", "implied", "chain")
    draws = 1 if smoke else DRAWS.get(m, 3)
    return [(m, "agent", k, v, "neutral", True, i) for k in keys for v in vers for i in range(draws)]


if __name__ == "__main__":
    import concurrent.futures as cf
    smoke = "--smoke" in sys.argv
    models = [a for a in sys.argv[1:] if not a.startswith("--")] or list(CAPS)
    with cf.ThreadPoolExecutor(len(models)) as ex:
        list(ex.map(lambda m: A.run_sync(m, rows_for(m, smoke), 0.1 if smoke else CAPS[m], 3), models))
    print("ALLDONE")
