# app/services/data_collector.py

from app.services.producthunt_service import producthunt_service
from app.services.tavily_service import tavily_service
from app.utils.market_classifier import classify_market_signal


class DataCollector:

    def __init__(self):
        pass

    async def collect_market_data(self, product_idea: str):
        print(f"\n🚀 Collecting market data for: {product_idea}\n")

        result = {
            "product_idea": product_idea,
            "category": "Unknown",
            "competitors": [],
            "market_intelligence": {
                "pain_points": [],
                "existing_alternatives": [],
                "communities": [],
                "demand_signals": [],
                "general_insight": []
            }
        }

        # --------------------------------------------------
        # 1️⃣ Tavily → COMPETITORS (Primary Source)
        # --------------------------------------------------
        print("=" * 50)
        print("🔍 Phase 1: Searching for competitors...")
        print("=" * 50)
        
        tavily_competitors = await tavily_service.search_competitors(product_idea, max_results=15)

        for item in tavily_competitors:
            # Extract competitor info from Tavily results
            result["competitors"].append({
                "name": self._extract_company_name(item.get("title", "")),
                "url": item.get("url"),
                "headline": item.get("title", ""),
                "description": item.get("content", "")[:500],
                "source": "tavily",
                "confidence_score": round(item.get("score", 0.7), 2)
            })

        print(f"✅ Added {len(result['competitors'])} competitors from Tavily\n")

        # --------------------------------------------------
        # 2️⃣ Product Hunt → Additional competitors (if any)
        # --------------------------------------------------
        print("=" * 50)
        print("🔍 Phase 2: Checking Product Hunt...")
        print("=" * 50)
        
        ph_products = producthunt_service.search_products(product_idea)

        for product in ph_products:
            url = product.get("url")
            if not url:
                continue

            # Check if already added from Tavily
            if any(comp.get("url") == url for comp in result["competitors"]):
                continue

            result["competitors"].append({
                "name": product.get("name"),
                "url": url,
                "headline": product.get("tagline", ""),
                "description": product.get("description", "")[:500],
                "source": "producthunt",
                "confidence_score": 0.9
            })

        print(f"✅ Added {len([c for c in result['competitors'] if c['source'] == 'producthunt'])} competitors from Product Hunt\n")

        # --------------------------------------------------
        # 3️⃣ Tavily → Market Intelligence
        # --------------------------------------------------
        print("=" * 50)
        print("🔍 Phase 3: Gathering market intelligence...")
        print("=" * 50)
        
        # Search for pain points and user needs
        pain_query = f"{product_idea} problems pain points complaints issues challenges"
        pain_results = await tavily_service.search_market_signals(pain_query, max_results=8)
        
        for item in pain_results:
            result["market_intelligence"]["pain_points"].append({
                "title": item.get("title"),
                "url": item.get("url"),
                "summary": item.get("content", "")[:300],
                "confidence_score": round(item.get("score", 0.5), 2)
            })

        # Search for communities and discussions
        community_query = f"{product_idea} community forum reddit discord slack groups"
        community_results = await tavily_service.search_market_signals(community_query, max_results=5)
        
        for item in community_results:
            classification = classify_market_signal(
                url=item.get("url", ""),
                content=item.get("content", "")
            )
            
            result["market_intelligence"][classification].append({
                "title": item.get("title"),
                "url": item.get("url"),
                "summary": item.get("content", "")[:300],
                "confidence_score": round(item.get("score", 0.5), 2)
            })

        # Search for alternatives and solutions
        alternatives_query = f"{product_idea} alternatives solutions tools software"
        alt_results = await tavily_service.search_market_signals(alternatives_query, max_results=8)
        
        for item in alt_results:
            # Check if it's a competitor (already added)
            url = item.get("url", "")
            if any(comp.get("url") == url for comp in result["competitors"]):
                continue
                
            result["market_intelligence"]["existing_alternatives"].append({
                "title": item.get("title"),
                "url": url,
                "summary": item.get("content", "")[:300],
                "confidence_score": round(item.get("score", 0.5), 2)
            })

        print(f"✅ Market Intelligence Summary:")
        print(f"   - Pain Points: {len(result['market_intelligence']['pain_points'])}")
        print(f"   - Communities: {len(result['market_intelligence']['communities'])}")
        print(f"   - Alternatives: {len(result['market_intelligence']['existing_alternatives'])}")
        print(f"   - Demand Signals: {len(result['market_intelligence']['demand_signals'])}")
        print()

        # --------------------------------------------------
        # 4️⃣ Final Summary
        # --------------------------------------------------
        print("=" * 50)
        print("✅ Data Collection Complete!")
        print("=" * 50)
        print(f"📊 Total Competitors: {len(result['competitors'])}")
        print(f"📊 Total Market Signals: {sum(len(v) for v in result['market_intelligence'].values())}")
        print()

        return result

    def _extract_company_name(self, title: str) -> str:
        """
        Extract company/product name from Tavily result title.
        """
        # Remove common suffixes
        title = title.replace(" - Official Site", "")
        title = title.replace(" | ", " - ")
        
        # Take first part before dash or pipe
        if " - " in title:
            return title.split(" - ")[0].strip()
        elif "|" in title:
            return title.split("|")[0].strip()
        
        # Return first 5 words max
        words = title.split()
        return " ".join(words[:5])


data_collector = DataCollector()