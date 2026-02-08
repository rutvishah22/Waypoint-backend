"""
Test Product Hunt API integration.
"""

from app.services.producthunt_service import producthunt_service


def test_search():
    """Test searching for products."""
    
    print("\n" + "="*50)
    print("Testing Product Hunt API")
    print("="*50)
    
    # Search for productivity tools
    products = producthunt_service.search_products("productivity", limit=10)
    
    if products:
        print(f"\n✅ SUCCESS! Found {len(products)} products\n")
        
        print("Top 5 products:")
        for i, product in enumerate(products[:5], 1):
            print(f"\n{i}. {product['name']}")
            print(f"   Tagline: {product['tagline']}")
            print(f"   Votes: {product['votes']}")
            print(f"   Website: {product['website']}")
    else:
        print("\n❌ FAILED - No products found")
        print("Check your API token in .env file")


if __name__ == "__main__":
    test_search()