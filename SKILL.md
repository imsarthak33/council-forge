---
name: council-forge
description: "Convene a council of 5-7 auto-researched domain-expert AI personas who independently analyze a question, cross-examine each other, produce a mandatory Devil's Advocate dissent, then receive a Chairman's verdict with domain-authority weighting and confidence calibration. Works for ANY field — fintech, biotech, climate, cybersecurity, defense, hardware, energy, AI policy, law, medicine. Trigger on: \"council on X\", \"panel of experts on X\", \"multi-perspective analysis of X\", \"debate this idea\", \"stress-test this strategy\", \"build me a council for [domain]\", \"board of advisors view\", \"review this from all angles\", \"what would experts in X think\", \"I need expert review\", or any strategic question spanning regulatory + technical + financial + operational dimensions at once. Do NOT trigger for single-fact lookups or questions with one correct answer."
license: MIT
---

# Council Forge

Domain-agnostic multi-expert debate framework. Where Karpathy's LLM Council gets diversity from
*different models*, Council Forge gets it from *different expertise* inside one model — personas
that genuinely disagree because they optimize for different objectives. Full pitch and comparison
table: `README.md`.

## Activation modes

- **Casual** — "give me a council on X." Auto-detect the domain, research the right experts, run it.
- **Configured** — user names the specific experts they want. Build exactly those, with researched backgrounds.
- **Preset** — "run the cybersecurity council on X." Load a matching file from `examples/` if one exists.

## Execution protocol

Five phases (plus a live research step), each mandatory unless the user explicitly skips it. Exact output formats for every
phase are in `references/protocol-templates.md` — read it before Phase 0 and follow the formats
precisely.

1. **Domain intake.** Ask the six intake questions (template: `protocol-templates.md`) in one
   message. Do not proceed until DOMAIN + DECISION TYPE + STAKES are answered. If the user pushes
   back ("just do it"), proceed with explicit assumptions logged instead.

2. **Live Expert Research.** BEFORE generating personas, you MUST use your built-in web search tools (or URL readers) to identify 5-7 REAL, living experts in this specific domain. Search for their recent interviews, publications, or public stances. Do NOT hallucinate synthetic experts.

3. **Council architecture.** Construct the 5-7 personas based ENTIRELY on the real experts you just researched. Map them to the closest meta-archetype — DOMAIN_SCIENTIST, OPERATOR, REGULATOR, STRATEGIST, FINANCIER, CONTRARIAN, CUSTOMER_VOICE. Each persona needs their actual name, real title, and 8-15 factual nuggets synthesized from their real public worldview. Construction details: `references/personas-design.md`. Present the roster (including source URLs) and wait for confirmation before continuing (skip the wait if the user already said "just do it").

4. **Stage 1 — independent positions.** Each expert answers in total isolation: no expert may
   reference another's analysis at this stage. Synthesize their public worldview into their own voice for the debate. Run every expert, none skipped.

5. **Stage 2 — adversarial cross-examination.** Each expert reads the others, presented anonymized
   as Analyst A/B/C... Real disagreements must be escalated explicitly, never smoothed over. 

6. **Stage 3 — Devil's Advocate.** One expert (selection rule in `protocol-templates.md`) steelmans
   the opposite conclusion, diagnoses the council's groupthink, and names the most likely
   catastrophic failure mode.

7. **Stage 4 — Chairman's verdict.** Synthesizes every prior stage. Domain-authority weighting, not
   averaging: a lone domain-relevant expert can outweigh a majority outside their domain. Full
   authority matrix and synthesis rules: `references/chairman-protocol.md`.

## Structural rules (non-negotiable)

1. No expert references another's analysis during Stage 1.
2. Disagreements in Stage 2 are made explicit, not diplomatically hidden.
3. Each expert response reflects their full domain logic, not one isolated point.
4. Specificity beats vagueness — named regulations, real numbers, not generic claims.
5. No expert opines outside their domain; they defer explicitly when asked to.
6. The Chairman's verdict is binding and takes a position — never a list of considerations.
7. Don't summarize what the council "would" say — run it and write the actual expert voices.

## When NOT to use this skill

Single-fact lookups, simple regulation-date questions, pure code generation with no strategic
dimension, or when the user explicitly wants a direct answer without ceremony.

## Reference files

- `references/protocol-templates.md` — exact output format for every phase (read first)
- `references/personas-design.md` — how to craft personas that genuinely disagree
- `references/chairman-protocol.md` — domain-authority matrix and synthesis algorithm
- `references/architecture.md` — why the 5-phase protocol is engineered this way
- `examples/` — pre-built domain councils (cybersecurity, fintech-india, biotech-startup, climate-tech)
- `scripts/council_engine.py` — optional standalone Python orchestrator (multi-provider API use, outside Claude Code)
