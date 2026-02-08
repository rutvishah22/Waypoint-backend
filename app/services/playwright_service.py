# app/services/playwright_service.py

from playwright.async_api import async_playwright
from typing import Dict, List
import re
from app.utils.fingerprint import url_fingerprint


class PlaywrightService:

    async def scrape_competitor(self, url: str) -> Dict:
        fingerprint = url_fingerprint(url)

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                page.set_default_timeout(15000)
                await page.set_extra_http_headers({
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    )
                })

                await page.goto(url, wait_until="domcontentloaded")
                await page.wait_for_timeout(2000)

                body_text = await page.inner_text("body")

                data = {
                    "url": url,
                    "fingerprint": fingerprint,
                    "success": True,
                    "headline": await self._extract_headline(page),
                    "pricing": self._extract_pricing(body_text),
                    "features": await self._extract_features(page),
                    "ctas": await self._extract_ctas(page),
                }

                await browser.close()
                return data

        except Exception as e:
            return {
                "url": url,
                "fingerprint": fingerprint,
                "success": False,
                "error": str(e)
            }

    async def _extract_headline(self, page) -> str:
        selectors = ["h1", "[class*='hero'] h1", "[class*='headline']"]
        for sel in selectors:
            try:
                el = page.locator(sel).first
                text = await el.inner_text()
                if text and len(text) > 8:
                    return text.strip()
            except:
                continue
        return "Not found"

    def _extract_pricing(self, text: str) -> Dict:
        prices = re.findall(r'[$₹€£]\s*\d+', text)
        return {
            "found": bool(prices),
            "prices": list(set(prices)),
            "has_free": "free" in text.lower()
        }

    async def _extract_features(self, page) -> List[str]:
        features = []
        items = await page.locator("ul li").all()
        for el in items[:12]:
            try:
                txt = await el.inner_text()
                if 10 < len(txt) < 120:
                    features.append(txt.strip())
            except:
                continue
        return features

    async def _extract_ctas(self, page) -> List[str]:
        ctas = []
        buttons = await page.locator("button, a").all()
        for b in buttons[:8]:
            try:
                txt = await b.inner_text()
                if txt and len(txt) < 40:
                    ctas.append(txt.strip())
            except:
                continue
        return list(dict.fromkeys(ctas))


playwright_service = PlaywrightService()
