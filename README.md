# what-is-tech

A Claude skill that answers "what is X?" for any technology, grounded in freshly fetched **official documentation**, with every point cited.

Each answer follows the same structure, so technologies are easy to compare:

- **Quick facts**: category, maintainer, license, current version, maturity
1. **What it fundamentally is**
2. **What problem it solves**
3. **How it solves it**, with a concrete example
4. **Alternatives and comparison**, with when to use it and when not to
5. **Limitations, common misconceptions and caveats**
- **Next steps** and a numbered **Sources** list (with version or access date)

It replies in the language you ask in (e.g. "Kafka 是什么" gets a Chinese answer, keeping technical terms in English), asks first only when a name could mean different technologies, and saves the answer to `./tech-notes/<name>.md` on request.

## Install

**Claude Code**

```bash
git clone https://github.com/Arthur-xu/what-is-tech.git
mkdir -p ~/.claude/skills
ln -s "$PWD/what-is-tech/skills/what-is-tech" ~/.claude/skills/what-is-tech
```

**Claude.ai**: upload `dist/what-is-tech.skill` in the skills settings.

Then ask something like "what is ClickHouse?" or run `/what-is-tech ClickHouse`.

## Repository layout

| Path | Purpose |
|---|---|
| `skills/what-is-tech/SKILL.md` | The skill itself |
| `dist/what-is-tech.skill` | Packaged skill for upload |
| `evals/evals.json` | Content test prompts and expected outcomes |
| `evals/grade.py` | Grades answers against structural checks (sections, citations, overview table, length…) |
| `evals/trigger_eval.json` | 20 queries labelled should / shouldn't trigger |
| `evals/real_trigger.py` | Runs those queries against the installed skill with `claude -p` and reports triggering |

## License

MIT
