# Council Forge — Architecture Reference

> Why this is structured the way it is. Read this if you want to modify the protocol.

---

## DESIGN PRINCIPLES

### 1. Specialization Beats Model Diversity for Strategy

Karpathy's hypothesis: different LLMs have different blind spots, so averaging them reduces noise.
**True, but the wrong frame for strategic questions.**

A regulator and an entrepreneur looking at the same fintech proposal will reach different conclusions
not because they have different "blind spots" but because they are **optimizing for different
objectives** — the regulator for systemic risk minimization, the entrepreneur for market capture.
Their disagreement is *signal*, not noise.

Council Forge engineers this disagreement explicitly via persona design.

### 2. Productive Conflict > Polite Consensus

Most LLM-based "expert panel" implementations fail because they default to social politeness — the
experts converge toward agreement to be "helpful." Council Forge breaks this with three mechanisms:

- **Authentic isolation** in Stage 1 (experts cannot reference each other)
- **Adversarial framing** in Stage 2 (experts must call out errors explicitly)
- **Devil's Advocate** in Stage 3 (mandatory dissent even when council agrees)

If a council session produces unanimous agreement with no dissent, something went wrong.
That's why DA is mandatory.

### 3. Domain Authority Trumps Voting

A common failure mode: 4 experts agree, 1 expert with deep domain authority disagrees, the synthesizer
defaults to majority. But on legal questions, the lawyer's lone vote should outweigh four
non-lawyers. On engineering feasibility, the engineer wins.

Chairman applies **domain hierarchy** rather than vote counting. See `chairman-protocol.md` for the
full hierarchy matrix.

### 4. Confidence Calibration as First-Class Citizen

Most AI outputs don't tell you how confident to be. Council Forge mandates explicit confidence
ratings at two levels:
- **Per-expert** (each expert flags their own uncertainty in Stage 1)
- **Per-verdict** (Chairman calibrates overall verdict confidence)

This is critical because high-confidence wrong answers cost more than low-confidence right answers.

### 5. Stages Map to Real Decision-Making

The 5-phase protocol mirrors how real boards/committees actually deliberate:
- Intake → Frame the question (Phase 0)
- Solo expert review → Get independent opinions (Phase 1-2)
- Cross-examination → Surface disagreement (Phase 3)
- Devil's Advocate → Mandatory dissent (Phase 4)
- Final verdict → Authorize action (Phase 5)

This isn't arbitrary — it's the structure used by FDA advisory committees, Supreme Court oral
arguments, corporate boards, and venture capital investment committees.

---

## WHY 5-7 EXPERTS (NOT 3, NOT 10)

**Lower bound (3 experts):** Insufficient diversity. With only 3 perspectives, any single missing
archetype (legal, financial, technical) destroys the council's reliability.

**Upper bound (10+ experts):** Token economics become prohibitive (Stage 2 alone is N² complexity in
context tokens — each expert reads N-1 others). Also, marginal expert adds diminishing perspective.

**Optimal range: 5-7 experts** — covers all 7 meta-archetypes, fits in single-session context budget
(~30K-50K tokens total for the full council), produces diverse enough disagreement to be useful.

**Token math (approximate, Claude Sonnet 4.6 pricing):**
- 5 experts × 4 stages: ~25K input + ~15K output = ~40K tokens
- 7 experts × 4 stages: ~50K input + ~25K output = ~75K tokens
- Cost: ~$0.10-0.25 per full council session

---

## WHY THE DEVIL'S ADVOCATE STAGE EXISTS

Three failure modes that DA prevents:

**1. Convergent Hallucination**
If all experts share a worldview, they can converge on a confidently wrong answer. DA forces an
expert to articulate the dissent that should exist but didn't emerge naturally.

**2. Politeness Drift**
LLMs trained on RLHF tend toward agreement. By the time Stage 2 cross-examination ends, experts
who initially disagreed often soften their positions. DA hardens dissent that may have been lost.

**3. The 5% Catastrophe Blind Spot**
Expert councils tend to optimize for the 95% case (most likely scenario). DA explicitly asks: "if
this fails catastrophically, what's the most likely cause?" — exposing tail risks that consensus
discussion buries.

---

## WHY CHAIRMAN COMES LAST (NOT FIRST)

In some frameworks, a Chairman or moderator frames the question before experts speak. Council Forge
deliberately does NOT do this. Reason: a moderator's framing **biases the experts**. Experts who
hear "this is a legal question" filter through legal lenses. Experts who hear "this is a market
question" filter through market lenses.

Better: let each expert decide what kind of question this is from their own domain perspective. The
disagreement about *what kind of question this even is* is often the most valuable output.

Chairman only synthesizes AFTER all experts have spoken — when their independent framings can be
compared.

---

## TOKEN OPTIMIZATION TRICKS

For developers running Council Forge at scale:

**Parallel stages where possible:**
- Stage 1: All 5-7 experts run in parallel (no dependency between them)
- Stage 2: All 5-7 experts run in parallel (each reads all others' Stage 1)
- Stage 3 (DA): Single sequential call after Stage 2
- Stage 4 (Chairman): Single sequential call after Stage 3

**Truncation strategy when context overflows:**
1. Compress Stage 1 responses to bullet points before feeding to Stage 2
2. Have Chairman read full Stage 1+2 only for experts whose positions diverged most
3. Use summary buffers if the same council runs multiple questions

**Caching for preset councils:**
The system prompts for each expert persona are static — cache them as Anthropic prompt caching
breakpoints. ~70% cost reduction for repeated council runs on different questions in the same domain.

---

## COMMON FAILURE MODES & FIXES

### Failure 1: Experts sound the same
**Symptom:** All 5-7 experts produce similar analyses with minor variations.
**Cause:** Personas not specialized enough; knowledge bases overlap too much.
**Fix:** Ensure each expert has 8-15 *domain-specific* facts that NO other expert has. Strengthen
the "what this expert will NOT discuss" boundary.

### Failure 2: Devil's Advocate is too weak
**Symptom:** DA writes "well, here are some risks" instead of steelmanning the opposite.
**Cause:** DA prompt isn't adversarial enough.
**Fix:** Reframe — "you are a skeptical investor who believes this entire plan will fail. Write
the email to the founder explaining why."

### Failure 3: Chairman averages instead of weighting
**Symptom:** Chairman verdict says "considering all views, perhaps..."
**Cause:** Chairman prompt is too diplomatic.
**Fix:** Force domain hierarchy in Chairman prompt. "If experts conflict on X, [specific expert]
wins. Apply this rule. Do not equivocate."

### Failure 4: Stage 1 contamination
**Symptom:** Expert 3 in Stage 1 references Expert 1's reasoning.
**Cause:** Model writing all stages in single context loses isolation.
**Fix:** Either run Stage 1 experts in parallel API calls, OR reset context between each Stage 1
expert, OR include explicit "you have not seen any other expert's response" reminder per persona.

### Failure 5: User dumps question without context
**Symptom:** Council runs on insufficient information, produces generic verdict.
**Cause:** Phase 0 intake skipped.
**Fix:** Hard-enforce Phase 0. Refuse to proceed without DOMAIN + DECISION TYPE + STAKES answered.

---

## EXTENDING COUNCIL FORGE

### Adding New Archetypes

Current 7 archetypes cover most domains. To add a new archetype:

1. Define its "signature question" — what does this archetype always ask?
2. Define its domain authority — when does it win conflicts?
3. Define its blind spot — what does this archetype systematically miss?

Example: ETHICIST archetype
- Signature question: "What are the externalities and second-order harms?"
- Domain authority: Wins on questions involving ethics, public good, AI safety, bioethics
- Blind spot: Systematically over-weights theoretical harms vs. realistic adoption rates

### Multi-Round Councils

For complex decisions, run the council multiple times:
- Round 1: Strategic direction
- Round 2: Implementation plan (informed by Round 1 verdict)
- Round 3: Risk audit on the implementation plan

Each round's Chairman verdict becomes the user's question for the next round.

### Agentic Mode

Future extension: have experts ask each other follow-up questions in Stage 2, with the model
generating questions one expert would ask another. This produces deeper debate but ~3x token cost.
