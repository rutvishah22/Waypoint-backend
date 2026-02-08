#gemini-3-flash-preview

# app/services/gemini_service.py

import google.generativeai as genai
from app.core.config import settings
import json
from typing import Optional, Dict, Any


class GeminiService:
    """
    Gemini AI service.
    Handles all LLM-based reasoning and synthesis.
    """

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-3-flash-preview")
        print("✅ Gemini service initialized")

    def generate_structured(
        self,
        prompt: str,
        response_schema: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Generate STRICT JSON output from Gemini.
        """

        full_prompt = f"""
{prompt}

You MUST respond with ONLY valid JSON.
The JSON MUST strictly match this schema:
{json.dumps(response_schema, indent=2)}

Rules:
- No markdown
- No explanations
- No comments
- No text outside JSON
"""

        try:
            response = self.model.generate_content(full_prompt)
            raw = response.text.strip()

            # Safety cleanup (Gemini sometimes slips)
            raw = raw.replace("```json", "").replace("```", "").strip()

            return json.loads(raw)

        except json.JSONDecodeError:
            print("❌ Gemini JSON parse failed")
            print("Raw output:", raw[:500])
            return None

        except Exception as e:
            print(f"❌ Gemini error: {e}")
            raise

    def expand_dashboard_analysis(
        self,
        collected_data: dict,
        base_analysis: dict
    ) -> Optional[Dict[str, Any]]:
        """
        Expand base analysis into detailed dashboard sections.
        
        CRITICAL: Category Diagnosis is the #1 priority - this is our main USP!
        """

        # Extract category diagnosis from base analysis
        category_data = base_analysis.get("category_diagnosis", {})
        
        prompt = f"""
You are an expert market analyst helping founders validate their product strategy.

CRITICAL FOCUS: Category Diagnosis is THE MOST IMPORTANT insight you provide.
This is what founders come here for - helping them figure out if they're competing in the right category.

You are given:
1. Raw market data (competitors, pain points, communities)
2. A base analysis with initial category diagnosis

Your task:
Expand this into a comprehensive, actionable dashboard analysis.

Raw Market Data:
{json.dumps(collected_data, indent=2)[:4000]}

Base Analysis Summary:
{json.dumps(base_analysis, indent=2)[:2000]}

Category Diagnosis from Base Analysis:
- Current/Assumed Category: {category_data.get('assumed_category', 'Not specified')}
- Recommended Category: {category_data.get('recommended_category', 'Not specified')}
- Should Reframe: {category_data.get('should_reframe', False)}
- Reasoning: {category_data.get('reasoning', 'No reasoning provided')}

DASHBOARD SECTIONS TO CREATE:

1. CATEGORY DIAGNOSIS (TOP PRIORITY!)
   - Start with a clear verdict: "You ARE competing in the right category" OR "You should REFRAME to X category"
   - Explain WHAT category they assumed vs what you recommend
   - Explain WHY (with market evidence)
   - Show the IMPACT of reframing (or not)
   - Be concrete: "Instead of positioning as [X], position as [Y]"
   - Include confidence level and reasoning
   - Make this 2-3 paragraphs, detailed and actionable

2. OVERVIEW
   - Executive summary of the entire analysis
   - Key takeaways and action items
   - 1-2 paragraphs max

3. MARKET REALITY
   - Market size, growth trends, saturation level
   - Current dynamics and forces
   - What's working vs dying
   - Evidence from the collected data

4. COMPETITIVE LANDSCAPE
   - Who the REAL competitors are (not just feature comparisons)
   - Their positioning, pricing, strengths/weaknesses
   - Market gaps and opportunities
   - Specific company examples from the data

5. USER PAIN & DESIRES
   - What users complain about (from pain_points data)
   - What they're really asking for
   - Unmet needs and desires
   - Quote actual pain points if available

6. STRATEGY & POSITIONING
   - How to position uniquely in the market
   - What angle to take
   - Key differentiators to emphasize
   - Messaging direction

7. MVP BLUEPRINT
   - Must-have features for launch
   - Features to skip initially
   - Build sequence and priorities
   - Concrete feature list

8. PRICING & MONETIZATION
   - Recommended pricing model (free/freemium/paid)
   - Price point suggestion with justification
   - Based on competitor pricing from data
   - Monetization strategy

9. GO-TO-MARKET
   - Where to find early users
   - Distribution channels to focus on
   - Communities to target (from communities data)
   - Launch strategy

10. RISKS & UNKNOWNS
    - What could go wrong
    - Market uncertainties
    - Assumptions to validate
    - Red flags

IMPORTANT RULES:
- Be specific, not generic
- Use evidence from the market data
- Write for founders (actionable, not academic)
- If data is missing, state assumptions clearly
- Make category diagnosis detailed and compelling
- Don't invent competitors or data that isn't there
"""

        response_schema = {
            "category_diagnosis": {
                "type": "string",
                "description": "MOST IMPORTANT: Detailed category positioning analysis with clear verdict"
            },
            "overview": {
                "type": "string",
                "description": "Executive summary and key takeaways"
            },
            "market_reality": {
                "type": "string",
                "description": "Market size, trends, and dynamics"
            },
            "competitive_landscape": {
                "type": "string",
                "description": "Competitor analysis with specific examples"
            },
            "user_pain_and_desires": {
                "type": "string",
                "description": "User complaints, needs, and desires"
            },
            "strategy_and_positioning": {
                "type": "string",
                "description": "Unique positioning and differentiation strategy"
            },
            "mvp_blueprint": {
                "type": "string",
                "description": "What to build first and what to skip"
            },
            "pricing_and_monetization": {
                "type": "string",
                "description": "Pricing model and justification"
            },
            "go_to_market": {
                "type": "string",
                "description": "Distribution channels and launch strategy"
            },
            "risks_and_unknowns": {
                "type": "string",
                "description": "Risks, uncertainties, and assumptions to validate"
            }
        }

        result = self.generate_structured(prompt, response_schema)
        
        # Fallback: If category_diagnosis is missing or empty, create one from base_analysis
        if result and (not result.get("category_diagnosis") or result.get("category_diagnosis").strip() == ""):
            
            assumed = category_data.get('assumed_category', 'your current category')
            recommended = category_data.get('recommended_category', assumed)
            should_reframe = category_data.get('should_reframe', False)
            reasoning = category_data.get('reasoning', 'Based on the market analysis, your category positioning needs evaluation.')
            confidence = category_data.get('confidence', 0.7)
            
            if should_reframe and assumed != recommended:
                verdict = f"**You should REFRAME from '{assumed}' to '{recommended}'**"
            else:
                verdict = f"**You ARE competing in the right category: '{assumed}'**"
            
            result["category_diagnosis"] = f"""
{verdict}

**Current Category:** {assumed}

**Recommended Category:** {recommended}

**Reasoning:**
{reasoning}

**Confidence Level:** {int(confidence * 100)}%

**What This Means:**
{"This category shift could significantly impact your positioning, messaging, and go-to-market strategy. Consider how this reframe changes your competitive set and target audience." if should_reframe else "Your current category positioning aligns well with market realities. Focus on differentiation within this category rather than reframing."}
"""
        
        return result


# Singleton instance
gemini_service = GeminiService()