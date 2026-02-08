from urllib.parse import urlparse

def match_ph_metadata(domain: str, ph_items: list) -> dict | None:
    """
    Attach Product Hunt metadata if domains match.
    """
    for item in ph_items:
        url = item.get("website", "")
        if not url:
            continue

        ph_domain = urlparse(url).netloc.replace("www.", "")
        if ph_domain == domain:
            return {
                "producthunt": {
                    "name": item.get("name"),
                    "votes": item.get("votes"),
                    "tagline": item.get("tagline")
                }
            }
    return None
