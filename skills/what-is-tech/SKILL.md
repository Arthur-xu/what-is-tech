---
name: what-is-tech
description: Explains what a technology is — quick facts (maintainer, license, current version, maturity), what it fundamentally is, the problem it solves, how it solves it (with an example), alternatives with when-to-use / when-not-to-use guidance, limitations and common misconceptions, and next steps — all grounded in freshly fetched official documentation with cited sources. Use this skill whenever the user asks "what is X", "explain X", "what does X do", "what problem does X solve", "how is X different from Y" (to understand X first), or the same in any other language (e.g. "X 是什么 / X 是干嘛的 / 介绍一下 X"), where X is a technology — a framework, library, protocol, database, middleware, cloud service, architecture pattern, standard, tool, AI model or technical concept — even if they don't ask for docs or invoke /what-is-tech.
---

# What is tech

The user wants to genuinely understand a technology and make decisions with it (whether to learn it, whether to use it, how it compares with what they have) — not hear a description recited from memory. Technology moves fast: APIs get deprecated, licenses change, defaults change, and new versions change the answer to "what problem does it solve". So the core constraint of this skill is: **every claim comes from official material fetched during this run, with a clickable source**. Memory is only for deciding where to look and what to look for, never the answer itself.

## Workflow

### 1. Pin down the subject

First make sure which technology the user means.

**What counts as ambiguous**: in the technical context of the conversation, the name could refer to **two or more different technologies**, and picking the wrong one would make the whole answer wrong. Examples: "Spring" (Spring Framework / Spring Boot / Spring Cloud), "Transformer" (the neural network architecture / the Hugging Face `transformers` library). In that case, **ask the user one question before researching**, listing the candidates you see.

**What does not count**: non-technical meanings (Kafka is also a writer; "Rust" is also corrosion), or names with one overwhelmingly dominant meaning in a technical context ("Kafka" is Apache Kafka; "MCP" in an AI/dev context is the Model Context Protocol). Answer directly — every extra question interrupts the user. If another meaning is worth acknowledging, state your interpretation in one sentence at the top.

### 2. Research (most of the work)

Use WebSearch and WebFetch. If they are deferred tools, load them with ToolSearch first; if WebFetch isn't available, use a `web-fetch` agent instead.

Find these kinds of material:

| Purpose | What to look for |
|---|---|
| Quick facts | Maintainer / governing body (company, foundation); license (the official repo's LICENSE file or the official site — watch for recent license changes); latest stable version and release date (release notes / changelog / GitHub Releases); maturity (GA / beta / experimental / deprecated) |
| Nature, problem, mechanism | Official docs home / Introduction / Overview / Concepts pages; the spec or RFC; the official GitHub README; where it helps explain the motivation, the official launch announcement or design doc ("why we built this") |
| Example | A minimal example from the official Quickstart / Tutorial / Examples |
| Alternatives | Each alternative's **own** official docs; the project's own comparison pages ("X vs Y", "Why X", "When not to use X") |
| Limitations and misconceptions | Official Limitations / Caveats / Known issues / FAQ / Best practices / Production checklist pages; passages in the official docs that explicitly clarify "X is not Y"; official security advisories; known-issue entries in the official issue tracker |

What counts as "official": docs, blogs, specs, repositories, release notes and security advisories published by the technology's maintainers (company, foundation, project team). For academic technologies, the original paper by its authors also counts. Third-party blogs, Stack Overflow, Medium and Wikipedia do not — use them only when no official material exists, and label them explicitly as "unofficial".

**Judging "latest"**: prefer docs for the current version (not pages with an old version number in the URL). If search results point to old docs, find the equivalent page for the latest version. Record the version number or the page's last-updated date; if neither is available, record the access date (today).

**Research in parallel when there is a lot to compare**: when there are three or more main alternatives, or the technology is a large platform or framework, use the Agent tool to launch 2–3 subagents at once, each covering one track — (a) this technology's official docs, version and license, (b) each alternative's own official docs, (c) limitations, known issues, deprecations and security advisories. Each subagent returns: findings + URLs + version/date. This keeps total time close to the slowest track instead of the sum of all tracks. For simple technologies, research directly without subagents.

**When you can't find something**: say "no official statement found", then say what you actually relied on. Do not fill gaps from memory — avoiding exactly that is why the user chose this skill.

### 3. Write the answer

**Language**: reply in the language the user asked in, and translate the section headings in the template below into that language. When replying in a language other than English, keep technical terms in their original English form (e.g. "Raft 共识算法", "Server Components"), optionally with a brief translation on first use.

**Length**: about 600–1000 words of prose in English (about 1000–1800 characters in Chinese), not counting the quick-facts table, code blocks and Sources. The goal is that after reading, the user can explain it to someone else and make an initial judgment — not a manual. If you run over, cut lists of details first; keep the mechanism, the example and the conclusions. Go deeper only when the user asks for more detail.

**What not to give its own section**: history, core terminology and analogies are useful only when they aid understanding, so weave them into existing sections rather than filling slots:
- History: in section 2, one or two sentences on why it appeared when it did.
- Core terms: explain them on first use in section 3; when there are many concepts (e.g. Kafka's topic/partition/offset), a short list inside section 3 is fine.
- Analogies: only use the project's own analogies (e.g. MCP's "USB-C"), or ones that clearly won't mislead.

**Structure** — always use this skeleton, so users can compare technologies side by side:

```markdown
# <Technology name>

> One-line definition: <what it is, in the plainest words>

| Category | Maintainer | License | Current version | Maturity |
|---|---|---|---|---|
| <library/protocol/service/…> | <company or foundation> | <license; note recent changes> | <version (date)> [n] | <GA / beta / …> |

## 1. What it fundamentally is
<What kind of thing it is and its core abstraction. Avoid marketing language; if the official positioning is vague, translate it into something an engineer would understand.> [n]

## 2. What problem it solves
<The pain before it existed; the specific scenarios it targets; where useful, one or two sentences on why it appeared when it did.> [n]

## 3. How it solves it (with an example)
<Core mechanism, 2–4 points, explaining terms on first use.>

**Example**: <A minimal but real example — a code snippet, a config, or a concrete scenario walkthrough, preferably adapted from an official example. Point out which step shows the mechanism above.> [n]

## 4. Alternatives and comparison
<One or two sentences on the dimensions being compared.>

| Option | Approach | Strengths | Weaknesses | Best for |
|---|---|---|---|---|
| <this technology> | ... | ... | ... | ... |
| <alternative A> | ... | ... | ... | ... |

**How to choose**:
- Use <this technology> when: <specific conditions>
- Don't use <this technology> when: <specific conditions, and what to use instead> [n]

## 5. Limitations, common misconceptions and caveats
- <Limitation / pitfall / deprecation / security advisory / version difference — be specific and state the impact.> [n]

**Common misconceptions**:
- ❌ <a common wrong belief> → ✅ <what is actually true> [n]

## Next steps
- Get started: <official Quickstart link, plus prerequisites>
- Go deeper: <the 1–2 official pages most worth reading next, and why>

## Sources
[1] <page title> — <URL> (version x.y / updated YYYY-MM-DD / accessed YYYY-MM-DD)
[2] ...
```

Notes on this structure:
- The **quick-facts table** lets the user judge at a glance whether it's usable in production. License and maturity are the easiest to overlook and the most decision-relevant (Redis, Elasticsearch and Terraform have all changed licenses). If a cell genuinely can't be found, write "no official statement found" — don't guess.
- Sections 1–5 each need at least one `[n]` citation, because every point must be traceable. Use `[1][3]` when a sentence rests on several sources.
- In section 4, describe each alternative using its **own** official docs rather than this technology's comparison page — vendor comparison pages tend to favor themselves. If you do use one, mark it "(<vendor>'s official view)". "How to choose" must give concrete conditions, not an uninformative "each has trade-offs, it depends"; include when *not* to use it, because that's where users most often go wrong.
- In section 5, prioritize limitations the maintainers acknowledge, then problems inferred from official issues/changelogs — label the latter as inferences. List 1–3 **common misconceptions**, choosing ones about the boundaries of the definition that would lead to misuse (e.g. "RSC is just SSR", "MCP calls the model for you"); where possible, base them on statements where the official docs explicitly clarify the point.
- **Next steps** contains only links and a one-line reason, 2–3 lines; also list those links in Sources.
- When citing numbers (performance, limits, prices), give the source and version — these go stale fastest.
- If a fact only comes from an unofficial source, append "(unofficial)" to that entry in Sources.

### 4. Saving (only when asked)

By default, answer only in the conversation. When the user says "save it / write it to a file" (or equivalent), write the same content to `./tech-notes/<technology-name-in-kebab-case>.md` (create the directory if needed) and tell the user the path.

## Example: good vs bad answers

**Bad**: "Kafka is a high-throughput distributed message queue developed at LinkedIn…" (from memory, no sources, no version; may miss recent changes such as KRaft replacing ZooKeeper; never says when *not* to use it.)

**Good**: the quick-facts table shows it is maintained by the Apache Software Foundation under Apache-2.0, with the current version and date; the body says "Apache Kafka is a distributed event streaming platform: its core abstraction is a partitioned, replicated append-only log; producers write to it and consumers read at their own offsets… [1]"; section 4 states plainly "for a simple low-volume task queue, RabbitMQ or SQS is less hassle"; the limitations mention that ZooKeeper mode is no longer supported in new versions, citing the release notes.

(The facts above only illustrate the format; real answers always rely on the official material fetched in that run.)
