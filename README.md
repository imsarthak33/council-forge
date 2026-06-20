# Council Forge 🏛️

> **A domain-agnostic multi-expert debate framework for AI assistants.**
> Convene a panel of specialized AI experts on any topic. Get the verdict you'd get from a real board of advisors.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open Source](https://img.shields.io/badge/Open%20Source-Yes-success)]()
[![Inspired by](https://img.shields.io/badge/Inspired%20by-Karpathy's%20LLM%20Council-blue)](https://github.com/karpathy/llm-council)

---

## What is this?

You have a strategic question. You want the kind of multi-perspective review a real board of advisors would give. Today you'd ask ChatGPT or Claude, and you'd get one synthesized opinion that smooths over real disagreements.

**Council Forge convenes 5-7 AI expert personas with deliberately conflicting worldviews, runs them through a 4-stage structured debate, and produces a Chairman's verdict with domain-authority weighting and confidence calibration.**

It works for any domain. Just tell it what you're analyzing.

---

## How is this different from Karpathy's LLM Council?

[Andrej Karpathy's LLM Council](https://github.com/karpathy/llm-council) (2024) is a beautiful exploration of comparing 4 different LLMs (GPT, Claude, Gemini, Grok) on the same question. It uses **model diversity** for noise reduction.

Council Forge uses **expertise diversity** for signal amplification. Same idea taken further:

| Dimension | Karpathy's LLM Council | Council Forge |
|-----------|------------------------|---------------|
| Diversity axis | Model architecture (GPT vs Claude vs Gemini vs Grok) | Domain expertise (lawyer vs operator vs financier vs scientist) |
| Personas | 4 generic LLMs | 5-7 specialized domain experts with researched backgrounds |
| Stage 2 | Anonymous ranking | Adversarial cross-examination with structured headers |
| Stage 3 | None | **Devil's Advocate** — mandatory dissent engineering |
| Synthesis | Chairman averages | Chairman applies **domain-authority weighting** |
| Confidence | None | Per-expert + per-verdict confidence calibration |
| Configurability | Fixed council | Auto-configures to ANY domain |
| Deployment | Requires multi-provider API access | Works with a single model |

**Why does this matter?** When you ask a question like "should I launch this fintech product?" — you don't need GPT's generic perspective and Gemini's generic perspective and Claude's generic perspective. You need a *regulator's* perspective, an *operator's* perspective, and a *contrarian's* perspective. The disagreement between specializations is the signal.

---

## Quick Start

### Option 1: Install as a Claude Code skill (one command)

```bash
curl -fsSL https://raw.githubusercontent.com/council-forge/council-forge/main/install.sh | bash
```

This installs to `~/.claude/skills/council-forge` (available in every project). Add `-- --project`
to install only into the current repo's `.claude/skills/` instead, or `-- --uninstall` to remove it.
Already have the repo cloned? Run `./install.sh` from inside it — same script, no network needed.

```
"give me a council on whether to launch this fintech product in India"

→ Claude Code reads SKILL.md, runs Phase 0 intake (asks about domain, stakes, context),
  generates 5-7 specialized experts, runs the 4-stage debate, and delivers the verdict.
```

### Option 2: Manual install / other Claude products

Copy the `council-forge/` folder (everything in this repo) into your skills directory —
`~/.claude/skills/council-forge/` for Claude Code, or upload it as a Skill in claude.ai/the API.

### Option 3: Run programmatically via Python

```bash
git clone https://github.com/yourname/council-forge
cd council-forge
pip install anthropic  # or openai, or google-genai
export ANTHROPIC_API_KEY="..."

# Interactive intake
python scripts/council_engine.py --interactive

# Direct query
python scripts/council_engine.py \
  --domain "B2B SaaS pricing" \
  --query "Should we move from per-seat to usage-based pricing for our enterprise plan?" \
  --output verdict.json

# Use a preset council
python scripts/council_engine.py \
  --preset examples/biotech-startup.md \
  --query "FDA pathway for our Phase 2-ready oncology asset"
```

### Option 4: Use any LLM provider

```bash
# Claude (default)
export COUNCIL_MODEL_PROVIDER=anthropic
export ANTHROPIC_API_KEY=...

# OpenAI
export COUNCIL_MODEL_PROVIDER=openai
export OPENAI_API_KEY=...

# Google Gemini
export COUNCIL_MODEL_PROVIDER=google
export GOOGLE_API_KEY=...

python scripts/council_engine.py -q "..."
```

---

## Architecture

### The 4-Stage Debate Protocol

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 0: DOMAIN INTAKE                                          │
│ → Ask the user 6 questions: domain, decision type, stakes,      │
│   constraints, context, expert preferences                      │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: AUTO-RESEARCH PERSONAS                                 │
│ → LLM generates 5-7 specialized experts with:                   │
│   - Realistic names, titles, backgrounds                        │
│   - 8-15 domain-specific facts per expert                       │
│   - Explicit worldview + bias                                   │
│   - Genuine disagreement engineered between experts             │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: INDEPENDENT POSITIONS (parallel)                       │
│ → Each expert responds with ZERO knowledge of others            │
│ → 300-450 words per response with BOTTOM LINE + CONFIDENCE      │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 2: ADVERSARIAL CROSS-EXAMINATION (parallel)              │
│ → Each expert reads all others (anonymized as Analyst A-F)      │
│ → Structured headers: AGREEMENTS / DISPUTES / BLIND SPOTS /     │
│   REVISED POSITION                                              │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 3: DEVIL'S ADVOCATE (single expert)                       │
│ → One expert (typically CONTRARIAN archetype) steelmans the    │
│   OPPOSITE conclusion                                           │
│ → Identifies groupthink, 5% failure mode, what would change DA  │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 4: CHAIRMAN'S VERDICT                                     │
│ → Applies domain-authority weighting (not voting)               │
│ → 8 sections: Consensus / Contested / DA Reception / Blind     │
│   Spots / Verdict / Execution Checklist / Risk Flags /         │
│   Confidence Rating                                             │
└─────────────────────────────────────────────────────────────────┘
```

### The 7 Meta-Archetypes

The framework uses 7 reusable archetypes that adapt to any domain:

| Archetype | Role | Example in tech | Example in pharma |
|-----------|------|-----------------|-------------------|
| 🔬 **DOMAIN_SCIENTIST** | Deep technical expert | ML Research Lead | Drug Discovery Chemist |
| ⚙️ **OPERATOR** | Built/ran this for real | Production SRE | Manufacturing Director |
| ⚖️ **REGULATOR** | Policy/legal | FTC Antitrust Lawyer | FDA Reviewer |
| 🎯 **STRATEGIST** | Market/competitive | Industry Analyst | Pharma BD VP |
| 💰 **FINANCIER** | Capital/economics | VC Partner | Healthcare PE |
| 😈 **CONTRARIAN** | Skeptic/risk | Security Red-Teamer | Bioethicist |
| 👤 **CUSTOMER_VOICE** | End-user | Enterprise Buyer | Physician |

---

## Pre-Built Councils

Council Forge ships with example presets in `examples/`:

- **`cybersecurity.md`** — Security architecture, incident response, threat modeling
- **`fintech-india.md`** — RBI compliance, NBFC structuring, Indian payments
- **`biotech-startup.md`** — FDA pathway, clinical trials, biotech finance
- **`climate-tech.md`** — Carbon markets, ESG, climate finance *(coming soon)*
- **`_TEMPLATE.md`** — Blank template for creating new domain councils

Use a preset:
```
"Run the cybersecurity council on this incident response plan: [paste plan]"
```

---

## Build Your Own Council

Create a custom preset in 3 steps:

1. **Copy the template:** `cp examples/_TEMPLATE.md examples/your-domain.md`
2. **Define 5-7 experts** using the meta-archetype framework. Each expert needs:
   - Realistic name + title
   - 8-15 specific knowledge facts
   - Explicit worldview + bias
3. **Specify the domain-specific Chairman hierarchy** — which expert wins on which question type

Once saved, users invoke: `"run the [your-domain] council on X"`

See `references/personas-design.md` for the detailed guide.

---

## Documentation

| File | What it covers |
|------|----------------|
| `SKILL.md` | Main skill definition + execution protocol (kept lean — loads into context on every trigger) |
| `install.sh` | One-command installer for Claude Code (personal or project scope) |
| `references/protocol-templates.md` | Exact output format for every phase (loaded on demand) |
| `references/architecture.md` | Why the 5-phase protocol is engineered this way |
| `references/personas-design.md` | How to craft experts that genuinely disagree |
| `references/chairman-protocol.md` | Synthesis algorithms in detail |
| `examples/` | Pre-built domain councils |
| `scripts/council_engine.py` | Optional Python orchestration engine |

---

## Cost & Performance

Approximate token usage per full council run (5-7 experts):

| Provider | Model | Tokens (approx) | Cost (approx) | Time |
|----------|-------|-----------------|---------------|------|
| Anthropic | claude-sonnet-4-6 | 50,000-80,000 | $0.10-0.25 | 60-90s |
| OpenAI | gpt-4o | 50,000-80,000 | $0.15-0.40 | 50-80s |
| Google | gemini-2.0-flash | 50,000-80,000 | $0.02-0.08 | 40-70s |

Parallel execution of Stage 1 and Stage 2 cuts wall-clock time roughly in half.

---

## What this is NOT

- Not a replacement for actual domain experts on high-stakes decisions
- Not a guarantee of correctness — it's a structured analysis tool
- Not a substitute for primary research — use it AFTER you have data, not instead of getting data
- Not appropriate for simple factual questions (it's overkill)

---

## Comparison to Other Multi-Agent Frameworks

| Framework | Approach | When to use |
|-----------|----------|-------------|
| **AutoGen** (Microsoft) | Multiple agents collaborating on tasks | Complex multi-step task execution |
| **CrewAI** | Role-based agents with workflows | Building agent pipelines |
| **LangGraph** | Stateful multi-agent graphs | Custom agent topologies |
| **Karpathy's LLM Council** | 4 LLMs ranking each other | Model comparison exploration |
| **Council Forge** | Domain-specialized experts debating | Strategic decision analysis |

The frameworks above are *task execution* frameworks. Council Forge is a *decision analysis* framework. Different tools for different jobs.

---

## Origin Story

Council Forge originated as a domain-specific skill called "Kabaddi Council" — built to analyze India's battery recycling and EV policy intersection (6 experts: EPR Policy, EV Industry, Rare Earth Chemistry, Recycling Operations, Indian Environmental Law, NBFC Finance).

It became clear that the architecture was generally applicable: replace the 6 hardcoded experts with auto-researched personas for any domain, and the same pattern works for cybersecurity, biotech, fintech, climate, AI policy, defense, anything.

Council Forge is the generalized open-source version.

---

## Contributing

PRs welcome, especially:

- New preset councils in `examples/`
- Additional LLM provider integrations in `scripts/council_engine.py`
- Improvements to persona generation prompts
- Test cases demonstrating the framework's value across domains

---

## License

MIT License. Use it freely. Commercial use permitted. Attribution appreciated but not required.

---

## Citation

If this framework helped your work, please consider citing:

```
Council Forge: A Domain-Agnostic Multi-Expert Debate Framework for AI Assistants (2026)
Inspired by Karpathy's LLM Council architecture.
https://github.com/yourname/council-forge
```

---

## Acknowledgments

Built on the shoulders of:
- **Andrej Karpathy** for the [LLM Council](https://github.com/karpathy/llm-council) inspiration
- **Anthropic** for the Claude skill system that makes this composable
- The **Multi-Agent AI** research community
