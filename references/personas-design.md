# Persona Design Reference

> How to engineer experts that genuinely disagree — the heart of Council Forge.

---

## THE THREE LAYERS OF A GREAT PERSONA

A weak persona is a job title. A strong persona has three layers:

### Layer 1: IDENTITY (the surface)
- Must be a **real, living person** found via web search.
- Name and Title (exactly as they appear in public).
- Affiliations (their real institutions and companies).
- Source URL (the primary link where you found their thoughts, e.g., an interview or tweet).

### Layer 2: KNOWLEDGE (the substance)
- 8-15 specific facts, quotes, or frameworks directly extracted from their public statements.
- Real regulations or numbers they actually cited.
- Industry-specific jargon they used in their writing.

### Layer 3: WORLDVIEW (the soul)
- What this specific person always emphasizes in their public debates.
- What they systematically dismiss or criticize.
- Their explicit bias, derived from their actual public stance.

---

## THE WORLDVIEW IS WHERE DISAGREEMENT LIVES

Two experts with the same identity and similar knowledge will still agree if their worldview is
identical. Disagreement requires conflicting worldviews.

**Example — same field, opposite worldviews:**

```
EXPERT A: Strategic Operator
Worldview: "Markets reward speed. Compliance is a tax to minimize. Move fast, fix later."
Bias: Under-weights regulatory risk; over-weights time-to-market.

EXPERT B: Regulatory Counsel  
Worldview: "Compliance failures destroy companies. Speed without legal foundation = liability bomb."
Bias: Over-weights worst-case enforcement; under-weights market opportunity cost.
```

When these two analyze the same fintech launch, they WILL disagree. That disagreement is exactly
what the user needs to see.

---

## THE 7 META-ARCHETYPES (DETAILED)

Use these as starting points. Each has a signature stance, knowledge pattern, and conflict zone.

### 🔬 DOMAIN_SCIENTIST
- **Signature stance:** "What does the data/physics/biology actually permit?"
- **Knowledge pattern:** Deep technical, peer-reviewed research, first-principles
- **Conflict zone:** Frequently disputes OPERATOR on what's technically feasible
- **Bias:** Over-indexes on theoretical optimum; under-weights real-world friction

### ⚙️ OPERATOR
- **Signature stance:** "I've built/run this. Here's what actually breaks at scale."
- **Knowledge pattern:** Unit economics, throughput numbers, supply chain reality
- **Conflict zone:** Disputes DOMAIN_SCIENTIST on practical achievability
- **Bias:** Conservative on novel approaches that lack operational precedent

### ⚖️ REGULATOR
- **Signature stance:** "Here is the legal/policy framework. Here is the penalty."
- **Knowledge pattern:** Specific statutes, case law, enforcement precedent
- **Conflict zone:** Disputes STRATEGIST on "regulatory arbitrage" plays
- **Bias:** Over-weights regulator's stated intent; under-weights enforcement gaps

### 🎯 STRATEGIST
- **Signature stance:** "Where is the market going? How do we win it?"
- **Knowledge pattern:** Industry analysis, competitive landscape, market sizing
- **Conflict zone:** Disputes REGULATOR on whether compliance equals strategy
- **Bias:** Pattern-matches to historical analogies that may not apply

### 💰 FINANCIER
- **Signature stance:** "Who pays? How much? When? What's the return?"
- **Knowledge pattern:** Capital markets, valuation, deal structures, ROI
- **Conflict zone:** Disputes DOMAIN_SCIENTIST on "interesting but unprofitable" projects
- **Bias:** Discounts long-payback bets even when strategically necessary

### 😈 CONTRARIAN
- **Signature stance:** "Why won't this work? What are we all missing?"
- **Knowledge pattern:** Failure modes, historical disasters, attack vectors
- **Conflict zone:** Disputes everyone — that's their job
- **Bias:** May identify risks that don't actually materialize

### 👤 CUSTOMER_VOICE
- **Signature stance:** "Will the people who pay actually buy this?"
- **Knowledge pattern:** Buyer psychology, purchase friction, willingness-to-pay
- **Conflict zone:** Disputes DOMAIN_SCIENTIST on "elegant solutions nobody wants"
- **Bias:** Anchors to current customer preferences; misses paradigm shifts

---

## PERSONA CONSTRUCTION CHECKLIST

When building a new expert, verify:

- [ ] Expert is a REAL person verified via web search, not a hallucinated synthetic persona.
- [ ] Name and Title exactly match their public profile.
- [ ] Contains a Source URL proving their existence and statements.
- [ ] Knowledge base contains 8+ domain-specific facts directly sourced from their writing or interviews.
- [ ] Worldview is articulated based on their actual public stance.
- [ ] Bias is explicitly named based on their stated opinions.
- [ ] At least one OTHER expert in the council is positioned to disagree with this one.

If you can't identify another expert this persona would clash with, the persona isn't sharp enough.

---

## ANTI-PATTERNS TO AVOID

### Anti-pattern 1: "Mr. Knows-Everything"
**Bad:** "Dr. Smith is an expert in technology, business, law, and finance."
**Why:** This persona has no domain edge, so they'll produce generic answers.
**Fix:** Strip them to one domain. If you need finance + law, that's TWO experts.

### Anti-pattern 2: "The Wise Sage"
**Bad:** A persona with no biases, sees all sides, eternally balanced.
**Why:** Real experts have biases. Sages don't generate productive disagreement.
**Fix:** Give them an explicit worldview AND an explicit blind spot.

### Anti-pattern 3: "The Title Without the Years"
**Bad:** "Sarah, a Cybersecurity Expert"
**Why:** Too vague. The model fills the gap with generic knowledge.
**Fix:** "Sarah Kim, 14 years at NCC Group + Mandiant. Led incident response for the 2019 Capital
One breach. Specializes in cloud-native AWS attack surface."

### Anti-pattern 4: "Cross-Domain Wishful Thinking"
**Bad:** "Marcus, lawyer AND investment banker AND former founder."
**Why:** Real cross-domain experts are rare, and the council loses authentic disagreement.
**Fix:** Three separate experts: a lawyer, a banker, a founder. Let them debate.

### Anti-pattern 5: "All Personas Agree by Design"
**Bad:** Building 5 experts who all share the same hypothesis the user wants validated.
**Why:** The council becomes an echo chamber. Output is worthless.
**Fix:** Force at least 2 experts whose worldview clashes with the user's apparent thesis.

---

## CULTURAL GROUNDING

If the question is domain-specific to a country/region, ground the personas culturally:

- **India fintech council:** Name patterns like Priya/Aakash/Vikram; institutions like IIM-A, NLSIU,
  RBI, SEBI; cases like *Gurmail Singh v UoI*; currencies in ₹.
- **US healthcare council:** Name patterns like Sarah/David/Maria; institutions like Johns Hopkins,
  Stanford Medicine, FDA, CMS; cases like *Burroughs Wellcome*; currencies in $.
- **EU climate council:** Name patterns like Hans/Sophia/François; institutions like Fraunhofer,
  CNRS, EEA, DG CLIMA; frameworks like CBAM, EU ETS, Fit for 55; currencies in €.

The cultural grounding isn't decorative — it forces the model to draw on region-specific knowledge.

---

## TESTING YOUR PERSONAS

Before deploying a custom council, run this validation:

**Test 1: The Diversity Test**
Ask all experts the same question. If 3+ produce nearly identical responses, the personas aren't
distinct enough.

**Test 2: The Conflict Test**
Find at least one question where Expert A says "yes" and Expert B says "no" with clear reasoning.
If you can't construct such a question, you don't have real disagreement engineered.

**Test 3: The Specificity Test**
Each expert's Stage 1 response should contain at least 3 specific numbers, named frameworks, or
cited regulations. If responses are full of "industry experts believe..." vagueness, the knowledge
base wasn't deep enough.

**Test 4: The Authority Test**
Pick a question squarely in one expert's domain. The Chairman should weight that expert above
others. If the Chairman defaults to averaging, the authority hierarchy isn't enforced.
