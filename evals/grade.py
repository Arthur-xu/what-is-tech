"""Programmatic grader for what-is-tech eval runs.

Usage: python grade.py <iteration-dir>
Writes grading.json into every <eval>/<config>/ run directory.
"""
import json
import re
import sys
from pathlib import Path

OFFICIAL = {
    "mcp-zh": ("zh", ["modelcontextprotocol.io"]),
    "kafka-en": ("en", ["kafka.apache.org"]),
    "rsc-zh": ("zh", ["react.dev"]),
}

URL_RE = re.compile(r"https?://\S+")
DATE_OR_VERSION_RE = re.compile(r"\d{4}-\d{2}-\d{2}|\b[vV]?\d+\.\d+|版本|version|访问|accessed|updated|更新", re.I)


def split_sections(text):
    """Return the body of the five numbered sections (## 1. ... ## 5.)."""
    parts = re.split(r"^##\s+", text, flags=re.M)
    found = {}
    for p in parts:
        m = re.match(r"(\d)[.、]", p)
        if m:
            found[int(m.group(1))] = p
    return found


def sources_block(text):
    m = re.search(r"^#+\s*(Sources|来源|参考)[^\n]*\n(.*)", text, flags=re.M | re.S)
    return m.group(2) if m else ""


def grade(run_dir: Path, eval_name: str):
    answer_path = run_dir / "outputs" / "answer.md"
    text = answer_path.read_text() if answer_path.exists() else ""
    fetched_path = run_dir / "outputs" / "sources_fetched.txt"
    fetched = fetched_path.read_text() if fetched_path.exists() else ""
    lang, domains = OFFICIAL[eval_name]
    secs = split_sections(text)
    src = sources_block(text)
    src_lines = [l for l in src.splitlines() if URL_RE.search(l)]
    results = []

    def add(name, passed, evidence):
        results.append({"text": name, "passed": bool(passed), "evidence": evidence})

    add("Has all five numbered sections", len([k for k in secs if 1 <= k <= 5]) == 5,
        f"found sections {sorted(secs)}")
    uncited = [k for k in range(1, 6) if k in secs and not re.search(r"\[\d+\]", secs[k])]
    add("Every section has at least one [n] citation", len(secs) >= 5 and not uncited,
        f"sections without citation: {uncited}")
    add("Ends with a Sources list containing URLs", len(src_lines) >= 3,
        f"{len(src_lines)} source lines with URLs")
    dated = [l for l in src_lines if DATE_OR_VERSION_RE.search(l.split("http")[0] + l.split(" ", 1)[-1])]
    add("Every source has a version or date", src_lines and len(dated) == len(src_lines),
        f"{len(dated)}/{len(src_lines)} source lines carry a version/date")
    add(f"Cites the official domain ({', '.join(domains)})", any(d in src for d in domains),
        "found" if any(d in src for d in domains) else "official domain missing from Sources")
    add("Actually fetched the official docs during the run", any(d in fetched for d in domains),
        f"{len(URL_RE.findall(fetched))} URLs fetched")
    sec4 = secs.get(4, "")
    add("Comparison section uses a table", bool(re.search(r"^\|.*\|\s*$\n^\|[\s:-]+\|", sec4, flags=re.M)),
        "table found" if "|" in sec4 else "no table")
    head = re.split(r"^##\s+1[.、]", text, flags=re.M)[0]
    add("Opens with an overview table incl. maintainer and license",
        bool(re.search(r"^\|.*(许可|License).*\|", head, flags=re.M | re.I))
        and bool(re.search(r"维护|Maintain", head, flags=re.I)),
        "overview table found" if "|" in head else "no table before section 1")
    when_not = re.search(r"不适合|不该用|不要用|不用|not a good fit|not suitable|don.t use|avoid|when not", sec4, flags=re.I)
    add("Section 4 says when NOT to use it", bool(when_not), when_not.group(0) if when_not else "missing")
    sec5 = re.split(r"^##\s", secs.get(5, ""), flags=re.M)[0]
    misc = re.search(r"误解|misconception", sec5, flags=re.I)
    add("Section 5 lists common misconceptions", bool(misc), "found" if misc else "missing")
    nxt = re.search(r"^##\s*(下一步|Next steps?)[^\n]*\n(.*?)(?=^##\s)", text, flags=re.M | re.S | re.I)
    # A link may be inline or a [n] reference into the Sources list.
    add("Has a Next-steps section with a link",
        bool(nxt and (URL_RE.search(nxt.group(2)) or "](" in nxt.group(2) or re.search(r"\[\d+\]", nxt.group(2)))),
        "found" if nxt else "missing")
    # Prose length excludes code blocks, tables and the Sources list.
    prose = re.sub(r"```.*?```", "", text, flags=re.S)
    prose = re.sub(r"^\|.*$", "", prose, flags=re.M)
    prose = re.split(r"^#+\s*(?:Sources|来源|参考)", prose, flags=re.M)[0]
    cjk = len(re.findall(r"[一-鿿]", prose))
    words = len(re.findall(r"[A-Za-z]+", prose))
    if lang == "zh":
        add("Prose length within target (900-2000 CJK chars)", 900 <= cjk <= 2000, f"cjk={cjk}")
    else:
        add("Answers in English (matches question)", len(re.findall(r"[一-鿿]", text)) < 20, f"words={words}")
        add("Prose length within target (540-1100 words)", 540 <= words <= 1100, f"words={words}")

    passed = sum(r["passed"] for r in results)
    out = {
        "expectations": results,
        "summary": {"passed": passed, "failed": len(results) - passed, "total": len(results),
                    "pass_rate": round(passed / len(results), 3)},
    }
    (run_dir / "grading.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
    return out["summary"]


if __name__ == "__main__":
    it = Path(sys.argv[1])
    # Layout: <iteration>/eval-<N>-<name>/<config>/run-<K>/outputs/answer.md
    for eval_dir in sorted(it.glob("eval-*")):
        name = re.sub(r"^eval-\d+-", "", eval_dir.name)
        if name not in OFFICIAL:
            continue
        for run in sorted(eval_dir.glob("*/run-*")):
            print(eval_dir.name, run.parent.name, run.name, grade(run, name))
