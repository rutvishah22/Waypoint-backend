"""
Search Trend service using SerpAPI.

Infers market momentum using search intent signals.
"""
from dotenv import load_dotenv
load_dotenv()

from serpapi import GoogleSearch
from typing import Dict, List
from app.services.query_transformer import generate_queries
from app.core.config import settings

import time
import os
import requests


class SerpTrendsService:
    """
    Service for analyzing search demand trends
    using Google SERP signals.
    """

    def __init__(self):
        self.api_key = settings.SERPAPI_KEY
        self.base_url = "https://serpapi.com/search.json"
        if not self.api_key:
            print("⚠️ SERPAPI_KEY not found in environment")
        
        print("✅ SerpAPI Trends service initialized")

    def _run_serp_query(self, query: str) -> dict:
        """
        Run a single SerpAPI Google search query
        and extract useful market signals.
        """

        #print("🔑 SERPAPI_API_KEY loaded:", bool(self.api_key))
        if not self.api_key:
            print("❌ No SerpAPI key configured")
            return {}
        
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "num": 10,
        }

        try:
            response = requests.get(
                self.base_url, 
                params=params, 
                timeout=20
            )

            if response.status_code != 200:
                print(f"⚠️ SerpAPI returned status {response.status_code}")
                return {}

            data = response.json()
            
            # Check for API errors
            if "error" in data:
                print(f"⚠️ SerpAPI error: {data['error']}")
                return {}

            # Extract signals
            result_count = int(
                data.get("search_information", {})
                .get("total_results", "0").replace(",", "")
            )

            people_also_ask = [
                item.get("question")
                for item in data.get("related_questions", [])  # Changed from people_also_ask
                if "question" in item
            ]

            related_searches = [
                item.get("query")
                for item in data.get("related_searches", [])
                if "query" in item
            ]

            return {
                "query": query,
                "result_count": result_count,
                "people_also_ask": people_also_ask,
                "related_searches": related_searches,
            }
            
        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
            return {}
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return {}

    def analyze_keyword(self, user_input: str) -> dict:
        """
        Analyze search trends for a user's product idea.
        
        Args:
            user_input: Product idea in plain English
            
        Returns:
            Dictionary with trend analysis and market signals
        """
        
        print(f"\n{'='*50}")
        print(f"📈 Analyzing search signals for: {user_input}")
        print(f"{'='*50}\n")

        try:
            # Generate smart search queries
            queries = generate_queries(user_input)

            print("🔁 Generated search queries:")
            for q in queries:
                print(f"   - {q}")
            print()

            all_results = []

            for i, query in enumerate(queries):
                print(f"🔍 Querying: {query}")
                
                data = self._run_serp_query(query)

                if not data:
                    print(f"   ⚠️ No data returned\n")
                    continue
                
                print(f"   ✅ Got {data['result_count']:,} results\n")
                all_results.append(data)
                
                # Rate limiting (avoid hitting API limits)
                if i < len(queries) - 1:  # Don't wait after last query
                    time.sleep(2)

            if not all_results:
                return {
                    "data_available": False,
                    "error": "No usable data returned from SerpAPI"
                }

            # Aggregate results
            total_results = sum(r["result_count"] for r in all_results)
            related = set()
            questions = set()

            for r in all_results:
                related.update(r["related_searches"])
                questions.update(r["people_also_ask"])

            # Infer trend from result count
            if total_results > 1_000_000:
                trend = "mainstream"
                trend_emoji = "🔥"
            elif total_results > 100_000:
                trend = "growing"
                trend_emoji = "📈"
            else:
                trend = "niche"
                trend_emoji = "🌱"

            print(f"{trend_emoji} Trend: {trend.upper()}")
            print(f"   Total results: {total_results:,}")
            print(f"   Related searches: {len(related)}")
            print(f"   Questions asked: {len(questions)}\n")

            return {
                "data_available": True,
                "keyword": user_input,
                "trend": trend,
                "estimated_result_count": total_results,
                "related_searches": list(related)[:10],
                "people_also_ask": list(questions)[:10],
                "source": "serpapi"
            }

        except Exception as e:
            print(f"❌ Analysis error: {e}\n")
            return {
                "data_available": False,
                "error": str(e)
            }


# Global instance
serp_trends_service = SerpTrendsService()