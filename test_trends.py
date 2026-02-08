"""
Simple SerpAPI Trends test - just one request.
"""

from app.services.serp_trends_service import serp_trends_service
import time


print("\nWaiting 10 seconds before request...")
time.sleep(10)

print("\nTesting search trend analysis with SerpAPI...")

result = serp_trends_service.analyze_keyword("AI apps for productivity")

if result.get("data_available"):
    print("\n✅ IT WORKS!\n")
    print(f"Keyword: {result['keyword']}")
    print(f"Trend: {result['trend']}")
    print(f"Estimated result count: {result['estimated_result_count']}")

    print("\nRelated searches:")
    for q in result.get("related_searches", [])[:5]:
        print(f"  - {q}")

    print("\nPeople also ask:")
    for q in result.get("people_also_ask", [])[:5]:
        print(f"  - {q}")

else:
    print("\n❌ Failed")
    print(f"Error: {result.get('error', 'Unknown')}")
