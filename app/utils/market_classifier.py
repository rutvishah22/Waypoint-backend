# app/utils/market_classifier.py

def classify_market_signal(url: str, content: str) -> str:
    url = url.lower()
    content = content.lower()

    if any(k in url for k in ["reddit", "quora", "forum", "community"]):
        return "communities"

    if any(k in content for k in ["pain", "struggle", "problem", "difficult", "adhd"]):
        return "pain_points"

    if any(k in content for k in ["alternative", "tool", "app", "software"]):
        return "existing_alternatives"

    if any(k in content for k in ["market", "trend", "growth", "demand"]):
        return "demand_signals"

    return "general_insight"
