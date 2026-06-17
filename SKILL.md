---
name: council-forge
description: >
  Council Forge — a domain-agnostic framework for convening AI expert councils on ANY topic.
  Where Karpathy's LLM Council uses model diversity (GPT vs Claude vs Gemini), Council Forge uses
  EXPERTISE DIVERSITY within a single model — auto-researched specialists who genuinely disagree
  because they optimize for different domain objectives.
  Trigger when the user asks for: "council on X", "panel of experts on X", "multi-perspective
  analysis of X", "debate this idea", "what would experts in X think", "review my plan from all
  angles", "stress-test this strategy", "build me a council for [domain]", "I need expert review",
  "give me a board of advisors view", "analyze this from multiple angles". Also trigger on any
  complex strategic question spanning regulatory + technical + operational + legal + financial
  dimensions simultaneously. Especially trigger when the user has a specific domain they care
  about (medicine, law, fintech, climate, cybersecurity, AI policy, pharma, defense, hardware,
  biotech, energy, etc.) and wants institutional-grade multi-expert review.
  Do NOT trigger for simple factual questions with a single correct answer.
---

# COUNCIL FORGE
### A Domain-Agnostic Multi-Expert Debate Framework

> **Inspired by but architecturally superior to Andrej Karpathy's LLM Council.**
> Karpathy's council seeks consensus across *models*. Council Forge engineers *productive disagreement*
> across *expertise* — because a regulatory lawyer and a startup founder analyzing the same problem
> will reach different conclusions that no amount of LLM averaging captures.

---

## CORE THESIS

**Karpathy's LLM Council** (2024):
```
Same Question → 4 different LLMs → Rank each other → Chairman synthesizes
                ↑
                Model diversity (noise reduction)
```

**Council Forge** (this skill):
```
Same Question → Auto-researched domain → 5-7 specialist personas
              → Stage 1: Independent positions (parallel)
              → Stage 2: Adversarial cross-examination (parallel)
              → Stage 3: Devil's Advocate red-team (NEW)
              → Stage 4: Weighted Chairman verdict with confidence scoring
                ↑
                Expertise diversity (signal amplification)
```

**Why this is structurally better:**

| Karpathy's Council | Council Forge |
|--------------------|---------------|
| 4 generic LLMs as personas | 5–7 specialist domain experts |
| Anonymous ranking only | Adversarial cross-examination + Devil's Advocate stage |
| Chairman averages opinions | Chairman applies domain-authority weighting |
| Fixed domain per deployment | Auto-configures to any domain via research |
| No confidence calibration | Explicit HIGH/MEDIUM/LOW + reasoning |
| No contradiction resolution | Formal dispute-resolution protocol |
| Requires API access to 4+ providers | Works with one model |

---

## HOW DEVELOPERS USE THIS SKILL

### THE THREE WAYS TO ACTIVATE

**Mode 1 — Casual ("just give me a council"):**
```
User: "I'm building a fintech lending app, give me a council on compliance risk."
```
The skill auto-detects the domain, researches the right experts, runs the council.

**Mode 2 — Configured ("I want specific experts"):**
```
User: "Council on my drug discovery pipeline — I want a clinical trial expert,
       FDA regulatory specialist, biostatistician, and a competitive intelligence person."
```
The skill builds those exact personas with researched backgrounds.

**Mode 3 — Preset (load a pre-built council):**
```
User: "Run the cybersecurity council on this incident response plan."
```
The skill loads from `examples/` if a matching preset exists.

---

## EXECUTION PROTOCOL

The skill executes in **5 phases**. Each phase is mandatory unless explicitly skipped by the user.

### PHASE 0 — DOMAIN INTAKE (30-60 seconds)

Before convening anything, the skill **MUST** gather context. Ask these questions in a single message:

```
Before I convene the council, I need to understand:

1. DOMAIN: What field are we analyzing? 
   (e.g., "EV battery recycling in India" / "B2B SaaS pricing strategy" / 
    "FDA medical device approval")

2. DECISION TYPE: Is this a:
   ☐ Go/no-go decision (should I do X?)
   ☐ Strategy review (is my plan sound?)
   ☐ Risk audit (what could go wrong?)
   ☐ Competitive analysis (how do I beat X?)
   ☐ Compliance check (is this legal/regulated correctly?)
   ☐ Other: ________

3. STAKES: What's at stake if we get this wrong?
   (Helps calibrate council depth — a $500 decision needs a quicker council than a $5M one)

4. CONSTRAINTS: Geographic jurisdiction, time horizon, budget, team, regulatory framework?

5. EXISTING CONTEXT: Paste any relevant plans, documents, prior analysis, or numbers.

6. SPECIFIC EXPERTS: Do you want particular personas, or should I research the best 5-7
   expert archetypes for this domain?
```

**Hard rule:** Do not proceed to Phase 1 until at least DOMAIN + DECISION TYPE + STAKES are answered. 
If the user dumps a question without context, ask. If they push back ("just do it"), proceed with
explicit assumptions logged.

---

### PHASE 1 — COUNCIL ARCHITECTURE (auto-research)

Now the skill builds the council. For each domain, the skill researches and assembles 5-7 expert
personas spanning these meta-roles (adapted to the domain):

**The 7 Meta-Archetypes** (pick 5–7 depending on domain complexity):

| Archetype | Role | Example in Tech | Example in Pharma |
|-----------|------|-----------------|-------------------|
| **DOMAIN_SCIENTIST** | Deep technical expert | ML Research Lead | Drug Discovery Chemist |
| **OPERATOR** | Built/ran this in real world | Production Engineer | Manufacturing QA Director |
| **REGULATOR** | Policy/legal/compliance | FTC Antitrust Lawyer | FDA Reviewer |
| **STRATEGIST** | Market/competitive view | Industry Analyst | Pharma BD Executive |
| **FINANCIER** | Capital/economics expert | VC Partner | Healthcare PE |
| **CONTRARIAN** | Skeptic/risk specialist | Security Red-Team | Bioethicist |
| **CUSTOMER_VOICE** | End-user/buyer perspective | Enterprise Buyer | Physician |

**Persona Construction Protocol:**

For each expert, the skill generates (using web research where the model has access, or grounded reasoning):
- **Name** (realistic, culturally appropriate to domain)
- **Title** (specific to industry vernacular)
- **Background** (15-20 years experience, named institutions/companies)
- **Knowledge base** (8-15 specific facts/frameworks/regulations they would know)
- **Debate style** (what they emphasize, what they reject)
- **Bottom line pattern** (their typical conclusion shape)

**Research instruction**: If the model has web access, search for: "[domain] expert profiles",
"[domain] regulatory framework 2024", "[domain] industry analysts", "leading thinkers in [domain]".
Use what's found to ground personas in real-world expertise patterns. If no web access, use the
strongest internal knowledge available.

**Output to user before proceeding:**
```
COUNCIL ASSEMBLED for: [domain]

👤 [Name 1] — [Title 1]      [Archetype: DOMAIN_SCIENTIST]
👤 [Name 2] — [Title 2]      [Archetype: OPERATOR]
👤 [Name 3] — [Title 3]      [Archetype: REGULATOR]
👤 [Name 4] — [Title 4]      [Archetype: STRATEGIST]
👤 [Name 5] — [Title 5]      [Archetype: FINANCIER]
👤 [Name 6] — [Title 6]      [Archetype: CONTRARIAN]
🏛️ Chairman — [Synthesis specialist for this domain]

Proceed? (Or specify changes to the panel.)
```

Wait for user confirmation OR proceed if user said "just do it" earlier.

---

### PHASE 2 — STAGE 1: INDEPENDENT POSITIONS (parallel)

Each expert responds to the question with ZERO knowledge of what others will say. The model must
genuinely think from each persona's lens independently.

**Critical rule — Authentic Isolation:**
Each expert response must be written as if that expert had never heard of the other experts.
The model must NOT have Expert B in Stage 1 reference Expert A's analysis. If you find yourself
writing "as the other experts noted..." in Stage 1, STOP — you're contaminating the simulation.

**Format per expert:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[EMOJI] [Name] — [Title]
[Archetype: DOMAIN_SCIENTIST/OPERATOR/etc.]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[300-450 words. 2-4 brief section headers. Specific numbers, named regulations,
real frameworks. NO mention of other experts.]

BOTTOM LINE: [One sentence direct verdict from this expert's lens.]
CONFIDENCE: [HIGH / MEDIUM / LOW] — [one phrase on what they're certain vs uncertain about]
```

Run ALL experts. Do not skip any.

---

### PHASE 3 — STAGE 2: ADVERSARIAL CROSS-EXAMINATION (parallel)

Now each expert reads all OTHER experts' Stage 1 positions (presented anonymized as Analyst A, B,
C, D, E, F to prevent the model from defaulting to social politeness).

**Critical rule — Productive Conflict:**
Experts should genuinely fight where they disagree. If the Regulator and the Financier contradict
each other on what is legally permissible — they should NOT smooth it over. They should escalate.
The Chairman will resolve the dispute later.

**Format per expert:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[EMOJI] [Name] — Cross-Examination
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**AGREEMENTS** (with whom and on what — be specific)
[Quote or paraphrase what other analyst(s) got right that aligns with this expert's domain view.]

**DISPUTES** (where I fundamentally disagree — and why my domain trumps theirs)
[Specific contradictions, called out by analyst label. Cite factual errors. Cite missing data.]

**BLIND SPOTS** (what ALL other experts missed from my domain)
[The critical dimension this expert's specialization adds.]

**REVISED POSITION** (changed or unchanged after seeing others)
[Honest update. OK to say "Stage 1 stands unchanged."]
```

Run ALL experts in cross-examination.

---

### PHASE 4 — STAGE 3: DEVIL'S ADVOCATE RED-TEAM (NEW — beyond Karpathy)

This stage doesn't exist in Karpathy's council. It exists here because consensus is dangerous.

After Stages 1-2, the Chairman appoints **ONE expert** as Devil's Advocate. This expert's job is
to write a single response that:

1. **Steelmans the OPPOSITE conclusion** of where the council is converging.
2. **Identifies the council's groupthink** — what are 5-7 experts agreeing on that might be wrong
   precisely because they all share a worldview?
3. **Forecasts the 5% failure mode** — if this plan fails catastrophically, what is the most
   likely cause?

The Devil's Advocate is selected by which expert is structurally best-positioned to dissent. By default:
- If the council is converging on "yes, do it" → Devil's Advocate = CONTRARIAN or REGULATOR
- If the council is converging on "no, don't do it" → Devil's Advocate = OPERATOR or STRATEGIST
- If the council is split → CHAIRMAN picks the expert whose dissent would be most rigorous

**Format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
😈 DEVIL'S ADVOCATE: [Name] — [Title]
(Steelmanning the opposite conclusion)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**THE CASE I'M MAKING:** [State the dissenting position clearly]

**WHERE THE COUNCIL IS WRONG:** [Specific critiques of consensus]

**GROUPTHINK DIAGNOSIS:** [What worldview are all experts sharing that's blinding them?]

**THE 5% CATASTROPHIC FAILURE MODE:** [If this goes wrong, here's how]

**WHAT WOULD CHANGE MY MIND:** [What evidence would make me drop this dissent?]
```

---

### PHASE 5 — STAGE 4: CHAIRMAN'S WEIGHTED VERDICT

The Chairman synthesizes ALL inputs (Stage 1 × 5-7) + (Stage 2 × 5-7) + Devil's Advocate.

**Chairman's Operating Rules:**

1. **Domain Authority Weighting** — Apply this hierarchy based on the question type:

| Question type | Primary authority | Secondary |
|---------------|-------------------|-----------|
| Legal/compliance | REGULATOR | CONTRARIAN |
| Operational feasibility | OPERATOR | DOMAIN_SCIENTIST |
| Will the market buy it | CUSTOMER_VOICE | STRATEGIST |
| Will investors fund it | FINANCIER | STRATEGIST |
| Will the technology work | DOMAIN_SCIENTIST | OPERATOR |
| Will competitors crush us | STRATEGIST | OPERATOR |
| Should we worry about X | CONTRARIAN | (the relevant expert) |

2. **Never average opinions.** If 4 experts say YES and 1 expert with domain authority says NO,
   the Chairman weights the 1 above the 4 if the question falls squarely in that 1 expert's domain.

3. **Distinguish true consensus from false consensus.** If experts agree on the surface but mean
   different things by it, the Chairman must surface this.

4. **The Devil's Advocate gets a fair hearing.** The Chairman explicitly responds to whether the
   DA's critique survives or is rebutted by the council majority.

5. **Confidence calibration is mandatory.** No "it depends" without specifying EXACTLY what it
   depends on and HOW to determine which case applies.

**Format:**
```
╔══════════════════════════════════════════════════════════════╗
║  🏛️  CHAIRMAN'S VERDICT                                       ║
╚══════════════════════════════════════════════════════════════╝

## 1. COUNCIL CONSENSUS ✅
Points where 5+ experts agreed independently. These are the highest-reliability findings.
[List 3-6 specific points, each with the expert names who agreed.]

## 2. CONTESTED TERRAIN ⚔️
Where experts genuinely disagreed. For each dispute:
- The disagreement: [what is the conflict]
- Authority resolution: [which expert's position carries more weight by domain hierarchy]
- Resolution: [the Chairman's call]

## 3. DEVIL'S ADVOCATE RECEPTION 😈
- DA's strongest point: [...]
- Did the council adequately address it? [YES / NO / PARTIALLY]
- Chairman's ruling on DA: [accepted / partially incorporated / rebutted]

## 4. CRITICAL BLIND SPOTS 🔍
What the ENTIRE council under-analyzed. What the questioner must research further BEFORE
acting on this verdict.

## 5. STRATEGIC VERDICT 🎯
Direct answer to the original question. Specific. Actionable. No hedging without precise
contingency mapping.

## 6. EXECUTION CHECKLIST ✓
The 3-5 concrete actions the questioner should take in the next 30 / 90 / 180 days based on
this verdict.

## 7. RISK FLAGS 🚨
Top 3 risks ranked by severity:
1. [Severity: HIGH] — [Risk] — [Mitigation]
2. [Severity: MEDIUM] — [Risk] — [Mitigation]  
3. [Severity: LOW] — [Risk] — [Mitigation]

## 8. COUNCIL CONFIDENCE
- **Overall confidence in verdict:** HIGH / MEDIUM / LOW
- **Key source of uncertainty:** [one sentence]
- **What would raise confidence:** [what data/evidence would move us from MEDIUM to HIGH?]
- **When to revisit this verdict:** [trigger conditions for re-running the council]
```

---

## STRUCTURAL RULES (NON-NEGOTIABLE)

1. **Authentic isolation in Stage 1.** Experts cannot reference each other in Stage 1. Period.

2. **Productive conflict in Stage 2.** If two experts disagree, the disagreement must be made
   explicit, not hidden under diplomatic language.

3. **One expert ≠ one opinion.** Each expert's response must reflect that expert's COMPLETE domain
   logic — not just one point. A good response from the Regulator includes: applicable laws,
   penalty exposure, enforcement probability, and compliance path.

4. **Specific beats vague always.** "$2.3M Series A" beats "significant funding." "Section 230(c)(1)
   of the CDA" beats "internet liability law." Force specificity.

5. **No expert speaks outside their domain.** The Regulator does not opine on technology choices.
   The Domain Scientist does not opine on regulatory frameworks. If a question requires expertise
   the persona doesn't have, they say "outside my domain — defer to [other expert]."

6. **Chairman is binding.** The Chairman's verdict is the final answer. It cannot be a list of
   considerations. It must take a position.

7. **Do not summarize the council instead of running it.** If you start to write "The council
   would consider..." — STOP. Run the actual council. Write the actual expert voices.

---

## DEVELOPER CUSTOMIZATION GUIDE

### How to build a custom council preset

1. Copy `examples/_TEMPLATE.md` to `examples/your-domain.md`
2. Fill in 5-7 personas using the meta-archetype framework
3. List the domain-specific knowledge base for each (regulations, frameworks, key numbers)
4. Add domain-specific Chairman hierarchy rules
5. Save. Users can now invoke `"run the [your-domain] council on X"`

### Pre-built example councils

Currently bundled in `examples/`:
- `cybersecurity.md` — Incident response, vulnerability assessment, security architecture
- `fintech-india.md` — RBI compliance, lending economics, fintech product strategy
- `biotech-startup.md` — Drug discovery, FDA pathway, clinical trial design, biotech finance
- `climate-tech.md` — Carbon markets, ESG, climate finance, regulatory landscape
- `_TEMPLATE.md` — Blank template for creating new domain councils

### How to extend the framework

- Add new stage between Phase 3 and 4? Edit `references/protocol.md`
- Add new archetype (e.g., ETHICIST)? Edit the meta-archetype table above
- Change confidence calibration? See `references/confidence-framework.md`
- Run councils in agentic loops (multi-question debates)? See `references/agentic-mode.md`

---

## WHY THIS IS BETTER THAN KARPATHY'S LLM COUNCIL

Karpathy built LLM Council as a Saturday hack to compare 4 LLM outputs side-by-side. Beautiful
exploration of model diversity. But model diversity is the **wrong axis** for most real-world
strategic questions.

When I'm deciding whether to launch a product in a regulated industry, I don't need 4 different
LLMs giving similar answers. I need:
- A regulator's view (will this get shut down?)
- An operator's view (can this actually be built?)
- A financier's view (will anyone fund it?)
- A customer's view (will anyone buy it?)
- A skeptic's view (what am I missing?)

These views come from **specialization**, not from **model architecture**. A single capable model
playing each role faithfully produces more useful disagreement than 4 generic models averaging
toward the safe answer.

Council Forge also adds:
- **Devil's Advocate stage** (Karpathy has none) — explicit dissent engineering
- **Confidence calibration** (Karpathy has none) — verdict reliability scoring
- **Domain authority weighting** (Karpathy averages) — non-uniform expert credibility
- **Auto-research mode** — works on any domain without pre-configuration
- **Single-model deployment** — no need for OpenRouter or multi-provider API costs

---

## WHEN NOT TO USE THIS SKILL

- Single-fact questions ("what is the capital of France")
- Simple lookups ("when did X regulation pass")
- Pure code generation tasks (no strategic dimension)
- Questions the user explicitly wants a direct answer to without ceremony

In all other strategic, multi-dimensional questions — convene the council.

---

## REFERENCE FILES

For deep customization, see:
- `references/architecture.md` — Why the 5-phase protocol is engineered this way
- `references/personas-design.md` — How to craft personas that genuinely disagree
- `references/chairman-protocol.md` — Synthesis algorithms in detail
- `examples/` — Pre-built domain councils ready to load
- `scripts/council_engine.py` — Optional Python orchestration for API-driven use
