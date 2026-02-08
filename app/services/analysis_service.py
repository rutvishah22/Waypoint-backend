# app/services/analysis_service.py

from app.services.gemini_service import gemini_service
from app.services.data_collector import data_collector
from app.core.database import get_database
from datetime import datetime
import uuid


class AnalysisService:
    """
    Full market intelligence and strategy synthesis service.
    """

    async def analyze_product(
        self,
        product_idea: str,
        tier: str,        # "prelaunch" | "postlaunch"
        email: str
    ) -> dict:

        db = get_database()
        job_id = str(uuid.uuid4())

        print(f"\n🚀 Starting analysis: {job_id}")
        print(f"📝 Idea: {product_idea}")
        print(f"👤 User type: {tier}\n")

        # --------------------------------------------------
        # 1️⃣ Create DB record
        # --------------------------------------------------
        db["analyses"].insert_one({
            "job_id": job_id,
            "email": email,
            "product_idea": product_idea,
            "tier": tier,
            "status": "processing",
            "progress": 10,
            "created_at": datetime.utcnow()
        })

        try:
            # --------------------------------------------------
            # 2️⃣ Collect market evidence
            # --------------------------------------------------
            print("🔍 Collecting market data...")
            db["analyses"].update_one(
                {"job_id": job_id},
                {"$set": {"progress": 30}}
            )
            market_data = await data_collector.collect_market_data(product_idea)

            # --------------------------------------------------
            # 3️⃣ Compress evidence for Gemini
            # --------------------------------------------------
            print("📊 Summarizing evidence...")
            db["analyses"].update_one(
                {"job_id": job_id},
                {"$set": {"progress": 50}}
            )
            evidence = self._summarize_evidence(market_data)

            # --------------------------------------------------
            # 4️⃣ Base Strategic Analysis (Gemini)
            # --------------------------------------------------
            print("🧠 Running base analysis...")
            db["analyses"].update_one(
                {"job_id": job_id},
                {"$set": {"progress": 70}}
            )
            base_analysis = self._run_gemini_analysis(
                product_idea=product_idea,
                tier=tier,
                evidence=evidence
            )

            if base_analysis is None:
                raise Exception("Gemini returned invalid structured output")

            # --------------------------------------------------
            # 5️⃣ NEW: Expand into dashboard sections
            # --------------------------------------------------
            print("📈 Expanding dashboard analysis...")
            db["analyses"].update_one(
                {"job_id": job_id},
                {"$set": {"progress": 90}}
            )
            
            # No await needed - this is a synchronous method
            dashboard_analysis = gemini_service.expand_dashboard_analysis(
                collected_data=market_data,
                base_analysis=base_analysis
            )

            if dashboard_analysis is None:
                raise Exception("Dashboard expansion returned invalid output")

            # --------------------------------------------------
            # 6️⃣ Persist result
            # --------------------------------------------------
            db["analyses"].update_one(
                {"job_id": job_id},
                {
                    "$set": {
                        "status": "complete",
                        "progress": 100,
                        "raw_market_data": market_data,
                        "base_analysis": base_analysis,
                        "analysis": dashboard_analysis,
                        "completed_at": datetime.utcnow()
                    }
                }
            )

            print("✅ Analysis completed\n")

            return {
                "job_id": job_id,
                "status": "complete",
                "analysis": dashboard_analysis
            }

        except Exception as e:
            print(f"❌ Analysis failed: {str(e)}")
            db["analyses"].update_one(
                {"job_id": job_id},
                {
                    "$set": {
                        "status": "failed",
                        "error": str(e),
                        "completed_at": datetime.utcnow()
                    }
                }
            )
            raise

    # --------------------------------------------------
    # Alternative method name for compatibility
    # --------------------------------------------------
    async def run_analysis(self, job_id: str, idea: str, user_type: str) -> dict:
        """
        Alternative interface for the analysis pipeline.
        Maps to analyze_product but uses pre-existing job_id.
        """
        db = get_database()
        
        # Find existing job record to get email
        job = db["analyses"].find_one({"job_id": job_id})
        email = job.get("email", "unknown@example.com") if job else "unknown@example.com"
        
        # Run the full analysis
        return await self.analyze_product(
            product_idea=idea,
            tier=user_type,
            email=email
        )

    # --------------------------------------------------
    # Evidence summarizer (deterministic, no AI)
    # --------------------------------------------------
    def _summarize_evidence(self, market_data: dict) -> dict:
        """
        Compress raw data into LLM-digestible signals.
        """

        return {
            "competitor_count": len(market_data.get("competitors", [])),
            "competitor_names": [
                c["name"] for c in market_data.get("competitors", [])[:10]
            ],
            "pain_point_count": len(market_data.get("market_intelligence", {}).get("pain_points", [])),
            "top_pain_points": [
                p["title"] for p in market_data.get("market_intelligence", {}).get("pain_points", [])[:5]
            ],
            "existing_alternatives": [
                a["title"] for a in market_data.get("market_intelligence", {}).get("existing_alternatives", [])[:5]
            ],
            "communities": [
                c["url"] for c in market_data.get("market_intelligence", {}).get("communities", [])[:5]
            ],
            "demand_signal_strength": len(
                market_data.get("market_intelligence", {}).get("demand_signals", [])
            )
        }

    # --------------------------------------------------
    # Gemini reasoning
    # --------------------------------------------------
    def _run_gemini_analysis(
        self,
        product_idea: str,
        tier: str,
        evidence: dict
    ) -> dict:

        prompt = f"""
You are a senior startup strategist and market analyst.

USER STAGE:
{tier.upper()}
(prelaunch = idea-stage, no product yet)
(postlaunch = product exists, seeking growth)

PRODUCT IDEA:
"{product_idea}"

MARKET EVIDENCE (REAL DATA):
- Competitors found: {evidence['competitor_count']}
- Known competitors: {evidence['competitor_names']}
- Pain points mentioned: {evidence['pain_point_count']}
- Top pain points: {evidence['top_pain_points']}
- Existing alternatives: {evidence['existing_alternatives']}
- Active communities: {evidence['communities']}
- Demand signals detected: {evidence['demand_signal_strength']}

YOUR TASK:
Analyze ALL this data and provide comprehensive market intelligence:

1. Category Diagnosis - Is the assumed category optimal?
2. Market Conditions - Size, growth, saturation, timing
3. Competitive Analysis - Who they compete with, pricing, gaps
4. User Needs - What users complain about, what they want
5. Strategic Recommendations - What to build, what to skip
6. Distribution Strategy - Where to find users
7. Pricing Recommendation - What to charge and why
8. Risk Assessment - What could go wrong

For each section, cite SPECIFIC evidence from the data above.
Be concrete, not generic.

INSTRUCTIONS:
- Base conclusions strictly on evidence
- Adjust recommendations based on user stage
- Be specific, not generic
- Prefer clarity over hype
"""

        response_schema = {
            "category_diagnosis": {
                "assumed_category": "string",
                "recommended_category": "string",
                "should_reframe": "boolean",
                "confidence": "float",
                "reasoning": "string"
            },
            "market_timing": {
                "stage": "growing | stable | declining",
                "justification": "string"
            },
            "competitive_landscape": {
                "intensity": "low | medium | high",
                "patterns_observed": ["string"],
                "opportunity_gaps": ["string"]
            },
            "strategy": {
                "mvp_feature_priorities": ["string"],
                "distribution_channels": ["string"],
                "pricing_recommendation": {
                    "model": "freemium | subscription | one-time | usage-based",
                    "expected_range": "string",
                    "rationale": "string"
                },
                "messaging_templates": ["string"]
            },
            "overall_confidence": "float"
        }

        return gemini_service.generate_structured(prompt, response_schema)


analysis_service = AnalysisService()