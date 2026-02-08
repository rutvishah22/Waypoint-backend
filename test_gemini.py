"""
Direct test of Gemini API to see what's happening.
"""

from app.services.gemini_service import gemini_service


def test_gemini():
    print("\n=== Testing Gemini API ===\n")
    
    # Test 1: Simple generation
    print("Test 1: Simple text generation...")
    try:
        response = gemini_service.generate_text("Say hello in 5 words")
        print(f"✅ Response: {response}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return
    
    # Test 2: Structured generation
    print("Test 2: Structured JSON generation...")
    
    prompt = "Analyze this: 'AI task manager for ADHD'"
    schema = {
        "category": "string",
        "confidence": "float"
    }
    
    try:
        response = gemini_service.generate_structured(prompt, schema)
        print(f"✅ Response: {response}\n")
        
        if response is None:
            print("⚠️ WARNING: Response is None!")
            print("This means JSON parsing failed.")
        
    except Exception as e:
        print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    test_gemini()