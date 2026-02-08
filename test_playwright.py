"""
Test Playwright scraping service (FINAL).
"""

import asyncio
from app.services.playwright_service import playwright_service


async def test_single_scrape():
    print("\n" + "=" * 60)
    print("TEST: Single Competitor Scrape")
    print("=" * 60)

    result = await playwright_service.scrape_competitor(
        "https://example.com"
    )

    if result["success"]:
        print("\n✅ SUCCESS!\n")
        print(f"URL: {result['url']}")
        print(f"Headline: {result['headline']}")
        print(f"Pricing: {result['pricing']}")
        print(f"CTAs: {result['ctas']}")
        print(f"Features found: {len(result['features'])}")
        print(f"Confidence score: {result['confidence_score']}")
    else:
        print("\n❌ FAILED")
        print(f"Error: {result.get('error')}")


async def test_real_competitor():
    print("\n" + "=" * 60)
    print("TEST: Real Competitor (Motion)")
    print("=" * 60)

    result = await playwright_service.scrape_competitor(
        "https://usemotion.com"
    )

    if result["success"]:
        print("\n✅ SUCCESS!\n")
        print(f"Headline: {result['headline']}")
        print(f"Pricing: {result['pricing']}")
        print("\nTop Features:")
        for i, feature in enumerate(result["features"][:5], 1):
            print(f"  {i}. {feature}")
    else:
        print("\n❌ FAILED")
        print(f"Error: {result.get('error')}")


if __name__ == "__main__":
    asyncio.run(test_single_scrape())
    asyncio.run(test_real_competitor())
