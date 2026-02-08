"""
Product Hunt API service.

Discovers competitors by searching Product Hunt for products
in specific categories.
"""

import requests
from typing import List, Dict, Optional
from app.core.config import settings


class ProductHuntService:
    """
    Service for interacting with Product Hunt API.
    
    Used to discover competitors and market activity.
    """
    
    def __init__(self):
        """
        Initialize Product Hunt service.
        """
        self.api_token = settings.PRODUCTHUNT_API_TOKEN.strip()
        self.base_url = "https://api.producthunt.com/v2/api/graphql"
        
        # Set up headers for API requests
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}",
            "User-Agent": "Waypoint/1.0"
        }
        
        print("✅ Product Hunt service initialized")

    
    def search_products(self, topic: str, limit: int = 20) -> List[Dict]:
        """
        Search for products in a specific topic/category.
        
        Args:
            topic: Category to search (e.g., "productivity", "AI")
            limit: Max number of products to return
            
        Returns:
            List of product dictionaries
        """
        
        print(f"\n{'='*50}")
        print(f"🔍 Searching Product Hunt for: {topic}")
        print(f"{'='*50}\n")
        
        # GraphQL query for Product Hunt
        # GraphQL = Query language for APIs (like SQL for databases)
        query = """
        query ($topic: String!, $limit: Int!) {
          posts(topic: $topic, order: RANKING, first: $limit) {
            edges {
              node {
                id
                name
                tagline
                description
                votesCount
                website
                url
                createdAt
                topics {
                  edges {
                    node {
                      name
                    }
                  }
                }
              }
            }
          }
        }
        """
        
        # Variables for the query
        variables = {
            "topic": topic,
            "limit": limit
        }
        
        try:
            # Make API request
            response = requests.post(
                self.base_url,
                json={"query": query, "variables": variables},
                headers=self.headers,
                timeout=10
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            #FOR DEBUGGING
            print(data)
            
            # Extract products from GraphQL response
            products = []
            
            if "data" in data and "posts" in data["data"]:
                edges = data["data"]["posts"]["edges"]
                
                for edge in edges:
                    node = edge["node"]
                    
                    # Extract topic names
                    topics = []
                    if "topics" in node:
                        topics = [
                            t["node"]["name"] 
                            for t in node["topics"]["edges"]
                        ]
                    
                    # Create clean product dictionary
                    product = {
                        "name": node.get("name", "Unknown"),
                        "tagline": node.get("tagline", ""),
                        "description": node.get("description", ""),
                        "website": node.get("website", ""),
                        "producthunt_url": node.get("url", ""),
                        "votes": node.get("votesCount", 0),
                        "created_at": node.get("createdAt", ""),
                        "topics": topics,
                        "data_source": "producthunt"
                    }
                    
                    products.append(product)
                
                print(f"✅ Found {len(products)} products on Product Hunt\n")
                
                # Show first 3 for debugging
                for i, p in enumerate(products[:3], 1):
                    print(f"  {i}. {p['name']} - {p['votes']} upvotes")
                
                if len(products) > 3:
                    print(f"  ... and {len(products) - 3} more\n")
            
            return products
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Product Hunt API error: {e}\n")
            return []
        
        except Exception as e:
            print(f"❌ Unexpected error: {e}\n")
            return []


# Create global instance
producthunt_service = ProductHuntService()