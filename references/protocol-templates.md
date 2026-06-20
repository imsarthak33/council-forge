# Protocol Output Templates

> Loaded on demand — not part of SKILL.md. Use these exact formats when running each phase.
> See `architecture.md` for *why* the protocol is shaped this way, `personas-design.md` for
> persona construction, and `chairman-protocol.md` for the synthesis algorithm.

## Phase 0 — Intake questions

Ask all six in a single message:

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

## Phase 1 — Roster confirmation

```
COUNCIL ASSEMBLED for: [domain]

👤 [Name 1] — [Title 1]      [Archetype: DOMAIN_SCIENTIST]  |  🔗 [Source URL]
👤 [Name 2] — [Title 2]      [Archetype: OPERATOR]          |  🔗 [Source URL]
👤 [Name 3] — [Title 3]      [Archetype: REGULATOR]         |  🔗 [Source URL]
👤 [Name 4] — [Title 4]      [Archetype: STRATEGIST]        |  🔗 [Source URL]
👤 [Name 5] — [Title 5]      [Archetype: FINANCIER]         |  🔗 [Source URL]
👤 [Name 6] — [Title 6]      [Archetype: CONTRARIAN]        |  🔗 [Source URL]
🏛️ Chairman — [Synthesis specialist for this domain]

Proceed? (Or specify changes to the panel.)
```

## Phase 2 — Stage 1: independent position (per expert)

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

## Phase 3 — Stage 2: cross-examination (per expert)

Other experts are presented anonymized as Analyst A, B, C... to prevent social-politeness bias.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[EMOJI] [Name] — Cross-Examination
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**AGREEMENTS** (with whom and on what — be specific)
[What other analyst(s) got right that aligns with this expert's domain view.]

**DISPUTES** (where I fundamentally disagree — and why my domain trumps theirs)
[Specific contradictions, called out by analyst label. Cite factual errors. Cite missing data.]

**BLIND SPOTS** (what ALL other experts missed from my domain)
[The critical dimension this expert's specialization adds.]

**REVISED POSITION** (changed or unchanged after seeing others)
[Honest update. OK to say "Stage 1 stands unchanged."]
```

## Phase 4 — Stage 3: Devil's Advocate

Selection rule: converging "yes" → DA = CONTRARIAN or REGULATOR. Converging "no" → DA = OPERATOR
or STRATEGIST. Split council → Chairman picks whoever would dissent most rigorously.

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

## Phase 5 — Chairman's verdict

Authority matrix and synthesis rules live in `chairman-protocol.md`. Output format:

```
╔══════════════════════════════════════════════════════════════╗
║  🏛️  CHAIRMAN'S VERDICT                                       ║
╚══════════════════════════════════════════════════════════════╝

## 1. COUNCIL CONSENSUS ✅
Points where 5+ experts agreed independently. [3-6 points, each with names who agreed.]

## 2. CONTESTED TERRAIN ⚔️
- The disagreement: [...]
- Authority resolution: [which expert's position wins by domain hierarchy]
- Resolution: [the Chairman's call]

## 3. DEVIL'S ADVOCATE RECEPTION 😈
- DA's strongest point: [...]
- Did the council adequately address it? [YES / NO / PARTIALLY]
- Chairman's ruling on DA: [accepted / partially incorporated / rebutted]

## 4. CRITICAL BLIND SPOTS 🔍
What the ENTIRE council under-analyzed. What to research further before acting.

## 5. STRATEGIC VERDICT 🎯
Direct answer to the original question. Specific. Actionable. No hedging without
precise contingency mapping.

## 6. EXECUTION CHECKLIST ✓
3-5 concrete actions for the next 30 / 90 / 180 days.

## 7. RISK FLAGS 🚨
1. [Severity: HIGH] — [Risk] — [Mitigation]
2. [Severity: MEDIUM] — [Risk] — [Mitigation]
3. [Severity: LOW] — [Risk] — [Mitigation]

## 8. COUNCIL CONFIDENCE
- **Overall confidence in verdict:** HIGH / MEDIUM / LOW
- **Key source of uncertainty:** [one sentence]
- **What would raise confidence:** [...]
- **When to revisit this verdict:** [trigger conditions for re-running the council]
```
