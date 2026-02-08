"""
Test complete data collection pipeline.

Sources:
- Product Hunt → competitors
- Tavily → market intelligence
- Playwright → enrichment (fingerprinted)
"""

import asyncio
from app.services.data_collector import data_collector


async def test_complete_collection():
    print("\n" + "=" * 60)
    print("TESTING COMPLETE DATA COLLECTION PIPELINE")
    print("=" * 60 + "\n")

    idea = "AI-powered task manager for people with ADHD"
    data = await data_collector.collect_market_data(idea)

    print("\n" + "=" * 60)
    print("DATA COLLECTION SUMMARY")
    print("=" * 60 + "\n")

    # --- Core info ---
    print(f"Product Idea : {data.get('product_idea', 'N/A')}")
    print(f"Category     : {data.get('category', 'N/A')}\n")

    # --- Competitors ---
    competitors = data.get("competitors", [])
    print(f"Competitors Scraped : {len(competitors)}\n")

    if competitors:
        print("Top Competitors:\n")
        for idx, comp in enumerate(competitors, 1):
            print(f"{idx}. {comp.get('name', 'Unknown')}")
            print(f"   URL      : {comp.get('url', 'N/A')}")
            print(f"   Headline : {(comp.get('headline') or 'N/A')[:80]}")
            print(f"   Pricing  : {comp.get('pricing', {}).get('found', False)}")
            print(f"   Features : {len(comp.get('features', []))}")
            print(f"   Confidence: {comp.get('confidence_score', 0)}")
            print("-" * 40)
    else:
        print("⚠️ No competitors found via Product Hunt.\n")

    # --- Market Intelligence ---
    mi = data.get("market_intelligence", {})
    print("\nMarket Intelligence Breakdown:\n")

    for category, items in mi.items():
        print(f"{category.replace('_', ' ').title()} ({len(items)}):")
        for item in items[:3]:  # preview only
            print(f"  • {item.get('title', 'Untitled')}")
            print(f"    {item.get('url')}")
        print()

    print("✅ Test completed successfully.")


if __name__ == "__main__":
    asyncio.run(test_complete_collection())
