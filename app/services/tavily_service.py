# app/services/tavily_service.py

from tavily import TavilyClient
from app.core.config import settings


class TavilyService:
    def __init__(self):
        self.client = TavilyClient(
            api_key=settings.TAVILY_API_KEY.strip()
        )

    async def search_competitors(self, product_idea: str, max_results: int = 15):
        """
        Search for direct competitors using Tavily.
        Returns companies/products that compete in the same space.
        """
        try:
            # Create competitor-focused search query
            competitor_query = f"{product_idea} competitors alternatives similar products tools"
            
            print(f"🔍 Searching for competitors with Tavily...")
            
            response = self.client.search(
                query=competitor_query,
                search_depth="advanced",
                max_results=max_results,
                include_raw_content=True
            )

            competitors = []
            for item in response.get("results", []):
                competitors.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "content": item.get("content", "")[:2000],
                    "score": item.get("score", 0)
                })

            print(f"✅ Found {len(competitors)} potential competitors from Tavily")
            return competitors

        except Exception as e:
            print("❌ Tavily competitor search failed:", e)
            return []

    async def search_market_signals(self, query: str, max_results: int = 10):
        """
        Fetch broad market intelligence from the web.
        This includes blogs, tools, communities, discussions, etc.
        """
        try:
            print(f"🔍 Searching for market signals with Tavily...")
            
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_raw_content=True
            )

            results = []
            for item in response.get("results", []):
                results.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "content": item.get("content", "")[:2000],
                    "score": item.get("score", 0)
                })

            print(f"✅ Found {len(results)} market signals from Tavily")
            return results

        except Exception as e:
            print("❌ Tavily search failed:", e)
            return []


tavily_service = TavilyService()