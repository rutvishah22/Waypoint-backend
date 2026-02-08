# app/utils/fingerprint.py

from urllib.parse import urlparse

def url_fingerprint(url: str) -> str:
    """
    Normalize URL to avoid duplicate scraping.
    """
    parsed = urlparse(url.lower())
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")
