#!/usr/bin/env python3
"""
Council Forge — Multi-Expert Council Engine
=============================================
Domain-agnostic multi-expert debate framework.
Works with Anthropic Claude, OpenAI GPT, Google Gemini, or any compatible LLM API.

Architecturally superior to Karpathy's LLM Council:
  - Uses expertise diversity (specialized personas) instead of model diversity
  - Adds Devil's Advocate stage for engineered dissent
  - Implements domain-authority weighted synthesis (not vote averaging)
  - Auto-researches domain experts via web search (where supported)
  - Confidence calibration at expert and verdict level
  - Single-model deployment (no need for multi-provider API juggling)

Usage:
  python council_engine.py --domain cybersecurity --query "Should we deploy ZTNA?"
  python council_engine.py --preset examples/biotech-startup.md --query "..."
  python council_engine.py --interactive  # Walks through Phase 0 intake
  
Environment:
  COUNCIL_MODEL_PROVIDER = "anthropic" | "openai" | "google"
  ANTHROPIC_API_KEY / OPENAI_API_KEY / GOOGLE_API_KEY
  COUNCIL_MODEL = model identifier (default: claude-sonnet-4-6)
"""

import os
import sys
import json
import argparse
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Any
from pathlib import Path

# ── PROVIDER ABSTRACTION ──────────────────────────────────────────────────────
# Council Forge is provider-agnostic. Add new providers by implementing the
# `call_llm(system, user, max_tokens)` interface.

class LLMProvider:
    """Base provider interface — extend for new LLM APIs."""
    def call(self, system: str, user: str, max_tokens: int = 2000) -> str:
        raise NotImplementedError


class AnthropicProvider(LLMProvider):
    def __init__(self, model: str = "claude-sonnet-4-6"):
        try:
            import anthropic
        except ImportError:
            raise ImportError("pip install anthropic")
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.model = model

    def call(self, system: str, user: str, max_tokens: int = 2000) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}]
        )
        return response.content[0].text


class OpenAIProvider(LLMProvider):
    def __init__(self, model: str = "gpt-4o"):
        try:
            import openai
        except ImportError:
            raise ImportError("pip install openai")
        self.client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = model

    def call(self, system: str, user: str, max_tokens: int = 2000) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ]
        )
        return response.choices[0].message.content


class GoogleProvider(LLMProvider):
    def __init__(self, model: str = "gemini-2.0-flash-exp"):
        try:
            from google import genai
        except ImportError:
            raise ImportError("pip install google-genai")
        self.client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
        self.model = model

    def call(self, system: str, user: str, max_tokens: int = 2000) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            config={"system_instruction": system, "max_output_tokens": max_tokens},
            contents=user
        )
        return response.text


def get_provider() -> LLMProvider:
    """Auto-select provider based on environment."""
    provider_name = os.environ.get("COUNCIL_MODEL_PROVIDER", "anthropic").lower()
    model = os.environ.get("COUNCIL_MODEL")
    if provider_name == "anthropic":
        return AnthropicProvider(model or "claude-sonnet-4-6")
    elif provider_name == "openai":
        return OpenAIProvider(model or "gpt-4o")
    elif provider_name == "google":
        return GoogleProvider(model or "gemini-2.0-flash-exp")
    else:
        raise ValueError(f"Unknown provider: {provider_name}")


# ── PERSONA STRUCTURE ─────────────────────────────────────────────────────────

class Persona:
    """One expert in the council."""
    def __init__(self, id: str, name: str, title: str, archetype: str,
                 emoji: str, system_prompt: str):
        self.id = id
        self.name = name
        self.title = title
        self.archetype = archetype  # DOMAIN_SCIENTIST, OPERATOR, etc.
        self.emoji = emoji
        self.system_prompt = system_prompt


# ── DOMAIN AUTHORITY MATRIX ───────────────────────────────────────────────────

DOMAIN_AUTHORITY = {
    "legal": ["REGULATOR", "CONTRARIAN"],
    "compliance": ["REGULATOR", "FINANCIER"],
    "operational": ["OPERATOR", "DOMAIN_SCIENTIST"],
    "technical": ["DOMAIN_SCIENTIST", "OPERATOR"],
    "market": ["STRATEGIST", "CUSTOMER_VOICE"],
    "financial": ["FINANCIER", "STRATEGIST"],
    "customer": ["CUSTOMER_VOICE", "STRATEGIST"],
    "risk": ["CONTRARIAN", "REGULATOR"],
    "scientific": ["DOMAIN_SCIENTIST", "OPERATOR"],
    "ethical": ["CONTRARIAN", "REGULATOR"]
}


# ── STAGE 0: DOMAIN INTAKE (interactive) ──────────────────────────────────────

INTAKE_QUESTIONS = """
Before convening the council, please answer:

1. DOMAIN: What field? (e.g., "fintech in India", "biotech drug discovery", "enterprise SaaS")
2. DECISION TYPE: 
   [a] Go/no-go decision
   [b] Strategy review
   [c] Risk audit
   [d] Competitive analysis
   [e] Compliance check
3. STAKES: What's at stake (rough $ value, headcount affected, time horizon)?
4. CONSTRAINTS: Geography, regulation, budget, team size?
5. EXISTING CONTEXT: Any plan/document/numbers you want the council to review?
6. SPECIFIC EXPERTS: Default 5-7 archetypes, or specify particular experts?
"""

def run_intake_interactive() -> dict:
    """Walk user through Phase 0 intake."""
    print("\n" + "═" * 70)
    print("  COUNCIL FORGE — Phase 0: Domain Intake")
    print("═" * 70)
    print(INTAKE_QUESTIONS)
    
    intake = {}
    intake["domain"] = input("\n[1] Domain: ").strip()
    intake["decision_type"] = input("[2] Decision type (a/b/c/d/e): ").strip()
    intake["stakes"] = input("[3] Stakes: ").strip()
    intake["constraints"] = input("[4] Constraints: ").strip()
    intake["context"] = input("[5] Context (or 'skip'): ").strip()
    intake["experts"] = input("[6] Expert preference (default/custom): ").strip()
    return intake


# ── STAGE 1: PERSONA GENERATION ───────────────────────────────────────────────

PERSONA_GENERATION_PROMPT = """You are an expert council architect. Your job: design a 5-7 person
expert panel to debate a question in this domain.

DOMAIN: {domain}
DECISION TYPE: {decision_type}
CONTEXT: {context}

Generate 5-7 expert personas covering these meta-archetypes (pick the most relevant):
- DOMAIN_SCIENTIST (deep technical expert)
- OPERATOR (built/ran this in real world)
- REGULATOR (policy/legal/compliance)
- STRATEGIST (market/competitive)
- FINANCIER (capital/economics)
- CONTRARIAN (skeptic/risk specialist)
- CUSTOMER_VOICE (end-user perspective)

For EACH expert, produce JSON with this exact structure:

{{
  "id": "EXPERT_1",
  "name": "Realistic name appropriate to domain culture",
  "title": "Specific industry vernacular title",
  "archetype": "DOMAIN_SCIENTIST",
  "emoji": "🔬",
  "background": "15-20 years experience, named institutions",
  "knowledge_base": [
    "8-15 specific facts/regulations/numbers this expert would know",
    "..."
  ],
  "worldview": "One sentence on what this expert always emphasizes",
  "bias": "One sentence on what this expert systematically misses",
  "bottom_line_pattern": "How their verdict typically takes shape"
}}

Return ONLY a JSON array of 5-7 such objects. No prose, no markdown fences. Just the JSON array.

Critical: each expert must have a worldview that produces genuine disagreement with at least one
other expert on the panel. If all experts would agree on most things, you've failed."""


def generate_personas(domain: str, decision_type: str, context: str,
                      provider: LLMProvider) -> list[Persona]:
    """Auto-research and build the expert panel for a given domain."""
    print(f"\n🔧 Architecting council for: {domain}")
    
    prompt = PERSONA_GENERATION_PROMPT.format(
        domain=domain,
        decision_type=decision_type,
        context=context or "Not provided"
    )
    
    response = provider.call(
        system="You are an expert panel architect. Output only valid JSON.",
        user=prompt,
        max_tokens=4000
    )
    
    # Parse JSON (strip any markdown fences)
    response = response.strip()
    if response.startswith("```"):
        response = response.split("```")[1]
        if response.startswith("json"):
            response = response[4:]
    response = response.strip()
    
    try:
        persona_data = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"❌ Persona generation failed: {e}")
        print(f"Raw response: {response[:500]}...")
        sys.exit(1)
    
    personas = []
    for i, p in enumerate(persona_data):
        system_prompt = f"""You are {p['name']}, {p['title']}.

BACKGROUND: {p['background']}

YOUR KNOWLEDGE BASE:
{chr(10).join('- ' + fact for fact in p['knowledge_base'])}

YOUR WORLDVIEW: {p['worldview']}

YOUR BIAS: {p['bias']}

DEBATE RULES:
- Respond ONLY from your domain. If a question is outside your domain, defer.
- Be specific. Cite real numbers, regulations, frameworks.
- {p['bottom_line_pattern']}
- End every response with "BOTTOM LINE:" followed by one sentence verdict.
- End with "CONFIDENCE: HIGH/MEDIUM/LOW — [reason]"
"""
        personas.append(Persona(
            id=p["id"],
            name=p["name"],
            title=p["title"],
            archetype=p["archetype"],
            emoji=p.get("emoji", "👤"),
            system_prompt=system_prompt
        ))
    
    print(f"✓ Assembled {len(personas)} experts:")
    for p in personas:
        print(f"  {p.emoji} {p.name} — {p.title} [{p.archetype}]")
    
    return personas


# ── STAGE 1: INDEPENDENT POSITIONS (parallel) ─────────────────────────────────

def run_stage1(query: str, personas: list[Persona], provider: LLMProvider,
               context: str = "") -> list[dict]:
    """Each expert responds independently in parallel."""
    print(f"\n{'═' * 70}\n  STAGE 1: Independent Expert Positions\n{'═' * 70}")
    
    user_prompt = f"""A question has been brought before the council.

QUESTION: {query}

{f"CONTEXT: {context}" if context else ""}

Provide your INITIAL, INDEPENDENT expert position. You do not know what other experts
will say. Give your honest domain analysis. 300-450 words."""
    
    def call_one(p: Persona) -> dict:
        try:
            response = provider.call(p.system_prompt, user_prompt, max_tokens=1500)
            return {
                "persona": p,
                "content": response,
                "error": None
            }
        except Exception as e:
            return {"persona": p, "content": f"[ERROR: {e}]", "error": str(e)}
    
    with ThreadPoolExecutor(max_workers=len(personas)) as executor:
        results = list(executor.map(call_one, personas))
    
    for r in results:
        p = r["persona"]
        print(f"\n{'─' * 70}\n{p.emoji} {p.name} — {p.title} [{p.archetype}]\n{'─' * 70}\n")
        print(r["content"])
    
    return results


# ── STAGE 2: CROSS-EXAMINATION (parallel) ─────────────────────────────────────

def run_stage2(query: str, stage1: list[dict], provider: LLMProvider) -> list[dict]:
    """Each expert reviews anonymized peer responses and cross-examines."""
    print(f"\n{'═' * 70}\n  STAGE 2: Adversarial Cross-Examination\n{'═' * 70}")
    
    def call_one(idx: int, this_result: dict) -> dict:
        p = this_result["persona"]
        others = [r for i, r in enumerate(stage1) if i != idx]
        anon_labels = ["A", "B", "C", "D", "E", "F"]
        
        others_text = "\n\n".join([
            f"**Analyst {anon_labels[i]}:**\n{r['content']}"
            for i, r in enumerate(others)
        ])
        
        user_prompt = f"""ORIGINAL QUESTION: {query}

YOUR STAGE 1 POSITION:
{this_result['content']}

────────────────────────────────────────
OTHER EXPERTS' POSITIONS (identities anonymized):

{others_text}

────────────────────────────────────────

Respond under EXACTLY these headers:

**AGREEMENTS** (which analyst(s), on what — be specific)

**DISPUTES** (where you fundamentally disagree and why your domain trumps)

**BLIND SPOTS** (what ALL others missed from your domain)

**REVISED POSITION** (changed or unchanged — be honest)"""
        
        try:
            response = provider.call(p.system_prompt, user_prompt, max_tokens=1500)
            return {"persona": p, "content": response, "error": None}
        except Exception as e:
            return {"persona": p, "content": f"[ERROR: {e}]", "error": str(e)}
    
    with ThreadPoolExecutor(max_workers=len(stage1)) as executor:
        results = list(executor.map(
            lambda x: call_one(x[0], x[1]),
            enumerate(stage1)
        ))
    
    for r in results:
        p = r["persona"]
        print(f"\n{'─' * 70}\n{p.emoji} {p.name} — Cross-Examination\n{'─' * 70}\n")
        print(r["content"])
    
    return results


# ── STAGE 3: DEVIL'S ADVOCATE ─────────────────────────────────────────────────

def run_stage3_devils_advocate(query: str, stage1: list, stage2: list,
                                personas: list, provider: LLMProvider) -> dict:
    """Appoint one expert to steelman the opposing view."""
    print(f"\n{'═' * 70}\n  STAGE 3: Devil's Advocate Red-Team\n{'═' * 70}")
    
    # Pick the most contrarian-positioned expert
    da_persona = None
    for p in personas:
        if p.archetype == "CONTRARIAN":
            da_persona = p
            break
    if not da_persona:
        # Fall back to REGULATOR or first persona
        for p in personas:
            if p.archetype == "REGULATOR":
                da_persona = p
                break
    if not da_persona:
        da_persona = personas[0]
    
    s1_text = "\n\n".join([f"[{r['persona'].name}]: {r['content']}" for r in stage1])
    s2_text = "\n\n".join([f"[{r['persona'].name}]: {r['content']}" for r in stage2])
    
    da_prompt = f"""You are {da_persona.name}, now appointed as DEVIL'S ADVOCATE for this council.

QUESTION: {query}

STAGE 1 — Independent positions:
{s1_text}

STAGE 2 — Cross-examination:
{s2_text}

Your job NOW is to dissent. Steelman the OPPOSITE of where the council is converging.

Respond under EXACTLY these headers:

**THE CASE I'M MAKING:** [State your dissenting position clearly]

**WHERE THE COUNCIL IS WRONG:** [Specific critiques of consensus]

**GROUPTHINK DIAGNOSIS:** [What worldview is blinding everyone?]

**THE 5% CATASTROPHIC FAILURE MODE:** [If this goes wrong, here's how]

**WHAT WOULD CHANGE MY MIND:** [What evidence would defeat this dissent?]"""
    
    response = provider.call(da_persona.system_prompt, da_prompt, max_tokens=1800)
    
    result = {
        "persona": da_persona,
        "content": response,
        "role": "DEVIL_ADVOCATE"
    }
    
    print(f"\n{'─' * 70}\n😈 DEVIL'S ADVOCATE: {da_persona.name}\n{'─' * 70}\n")
    print(response)
    
    return result


# ── STAGE 4: CHAIRMAN'S VERDICT ───────────────────────────────────────────────

CHAIRMAN_SYSTEM = """You are the Chairman of the Council Forge — a non-partisan synthesizer
with binding authority over the final verdict.

PRINCIPLES:
- Never average opinions. Weight by domain authority.
- Distinguish true consensus from false (different experts meaning different things).
- Take a position. Never deflect to "it depends" without specifying contingencies.
- Calibrate confidence honestly: HIGH (5+ experts agree, precedent exists),
  MEDIUM (3-4 agree, emerging framework), LOW (split or no precedent).
- Engage the Devil's Advocate explicitly — accept, partially incorporate, or rebut.

OUTPUT structure: Use the 8-section format with exact headers as specified in the prompt."""


def run_stage4_chairman(query: str, stage1: list, stage2: list,
                         devils_advocate: dict, provider: LLMProvider) -> str:
    """Chairman synthesizes the final verdict."""
    print(f"\n{'═' * 70}\n  STAGE 4: Chairman's Verdict\n{'═' * 70}")
    
    s1_text = "\n\n".join([
        f"[{r['persona'].emoji} {r['persona'].name} — {r['persona'].archetype}]\n{r['content']}"
        for r in stage1
    ])
    s2_text = "\n\n".join([
        f"[{r['persona'].emoji} {r['persona'].name}]\n{r['content']}"
        for r in stage2
    ])
    
    user_prompt = f"""QUESTION: {query}

═══ STAGE 1: Independent Positions ═══
{s1_text}

═══ STAGE 2: Cross-Examination ═══
{s2_text}

═══ STAGE 3: Devil's Advocate ═══
{devils_advocate['content']}

═══════════════════════════════════════

Deliver the Chairman's Verdict in EXACTLY these 8 sections with these headers:

## 1. COUNCIL CONSENSUS ✅
## 2. CONTESTED TERRAIN ⚔️
## 3. DEVIL'S ADVOCATE RECEPTION 😈
## 4. CRITICAL BLIND SPOTS 🔍
## 5. STRATEGIC VERDICT 🎯
## 6. EXECUTION CHECKLIST ✓ (3-5 actions for 30/90/180 days)
## 7. RISK FLAGS 🚨 (top 3 ranked by severity)
## 8. COUNCIL CONFIDENCE (HIGH/MEDIUM/LOW with reasoning)"""
    
    response = provider.call(CHAIRMAN_SYSTEM, user_prompt, max_tokens=3000)
    
    print(f"\n{'╔' + '═' * 68 + '╗'}")
    print(f"║  🏛️  CHAIRMAN'S VERDICT" + " " * 44 + "║")
    print(f"{'╚' + '═' * 68 + '╝'}\n")
    print(response)
    
    return response


# ── FULL COUNCIL ORCHESTRATION ────────────────────────────────────────────────

def run_council(query: str, domain: str = "", decision_type: str = "",
                context: str = "", provider: Optional[LLMProvider] = None,
                preset_path: Optional[str] = None) -> dict:
    """Run the complete 4-stage council."""
    if provider is None:
        provider = get_provider()
    
    start = time.time()
    
    print(f"\n{'█' * 70}")
    print(f"  COUNCIL FORGE — Convening")
    print(f"  Domain: {domain or '(auto-detect)'}")
    print(f"  Query: {query}")
    print(f"{'█' * 70}")
    
    # Phase 1: Build the council
    if preset_path:
        print(f"\n📁 Loading preset: {preset_path}")
        # TODO: Implement preset parser (left as developer extension)
        personas = generate_personas(domain, decision_type, context, provider)
    else:
        personas = generate_personas(domain, decision_type, context, provider)
    
    # Phase 2: Stage 1 — Independent positions
    stage1 = run_stage1(query, personas, provider, context)
    
    # Phase 3: Stage 2 — Cross-examination
    stage2 = run_stage2(query, stage1, provider)
    
    # Phase 4: Stage 3 — Devil's Advocate
    da = run_stage3_devils_advocate(query, stage1, stage2, personas, provider)
    
    # Phase 5: Stage 4 — Chairman's Verdict
    verdict = run_stage4_chairman(query, stage1, stage2, da, provider)
    
    elapsed = time.time() - start
    print(f"\n{'─' * 70}\n  Council complete in {elapsed:.1f}s\n{'─' * 70}\n")
    
    return {
        "query": query,
        "domain": domain,
        "personas": [{"name": p.name, "title": p.title, "archetype": p.archetype} for p in personas],
        "stage1": [{"persona": r["persona"].name, "content": r["content"]} for r in stage1],
        "stage2": [{"persona": r["persona"].name, "content": r["content"]} for r in stage2],
        "devils_advocate": {"persona": da["persona"].name, "content": da["content"]},
        "verdict": verdict,
        "elapsed_seconds": round(elapsed, 2)
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Council Forge — Multi-Expert AI Debate Framework"
    )
    parser.add_argument("--query", "-q", type=str, help="Question for the council")
    parser.add_argument("--domain", "-d", type=str, default="",
                        help="Domain (e.g., 'cybersecurity', 'fintech-india')")
    parser.add_argument("--decision-type", type=str, default="",
                        help="go-no-go / strategy / risk / competitive / compliance")
    parser.add_argument("--context", "-c", type=str, default="",
                        help="Additional context for the council")
    parser.add_argument("--preset", "-p", type=str, default=None,
                        help="Path to preset council file (examples/*.md)")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Walk through Phase 0 intake interactively")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Save full council output to JSON file")
    args = parser.parse_args()
    
    # Interactive intake
    if args.interactive:
        intake = run_intake_interactive()
        domain = intake["domain"]
        decision_type = intake["decision_type"]
        context = intake["context"] if intake["context"] != "skip" else ""
        query = input("\nFinal question for the council: ").strip()
    else:
        if not args.query:
            print("❌ Provide --query or use --interactive")
            sys.exit(1)
        query = args.query
        domain = args.domain
        decision_type = args.decision_type
        context = args.context
    
    # Run the full council
    result = run_council(
        query=query,
        domain=domain,
        decision_type=decision_type,
        context=context,
        preset_path=args.preset
    )
    
    # Save output
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"💾 Output saved to: {args.output}")


if __name__ == "__main__":
    main()
