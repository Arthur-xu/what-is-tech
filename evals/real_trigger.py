"""Measure triggering of the *installed* what-is-tech skill via claude -p.

Usage: python real_trigger.py <trigger_eval.json>
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor


def first_skill(query):
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    p = subprocess.run(
        ["claude", "-p", query, "--model", "claude-opus-5-5", "--output-format", "stream-json",
         "--verbose", "--max-turns", "1"],
        capture_output=True, text=True, cwd=os.path.expanduser("~/Documents"), env=env, timeout=240,
    )
    tools = []
    for line in p.stdout.splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("type") == "assistant":
            for c in e["message"].get("content", []):
                if c.get("type") == "tool_use":
                    tools.append((c["name"], c.get("input", {}).get("skill", "")))
    return any(n == "Skill" and s == "what-is-tech" for n, s in tools), tools[:2]


items = json.load(open(sys.argv[1]))
with ThreadPoolExecutor(8) as ex:
    results = list(ex.map(lambda it: (it, *first_skill(it["query"])), items))
tp = sum(1 for it, t, _ in results if t and it["should_trigger"])
fp = sum(1 for it, t, _ in results if t and not it["should_trigger"])
pos = sum(it["should_trigger"] for it in items)
for it, t, tools in results:
    ok = t == it["should_trigger"]
    print("PASS" if ok else "FAIL", "expect" if it["should_trigger"] else "avoid", t, tools, it["query"][:50])
print(f"recall={tp}/{pos} false_positives={fp}/{len(items) - pos}")
