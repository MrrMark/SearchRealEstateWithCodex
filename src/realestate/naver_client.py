from __future__ import annotations

import re
from dataclasses import dataclass
from html import unescape
from typing import Iterable

from .models import Listing


@dataclass(slots=True)
class CollectorConfig:
    max_items: int = 100


class NaverRealEstateClient:
    BASE_URL = "https://new.land.naver.com/complexes"

    def __init__(self, region_label: str, cortar_no: str, config: CollectorConfig | None = None):
        self.region_label = region_label
        self.cortar_no = cortar_no
        self.config = config or CollectorConfig()

    def build_search_url(self) -> str:
        return f"{self.BASE_URL}?ms=37.5665,126.9780,11&a=APT:ABYG:JGC&e=RETAIL&articleNo=&cortarNo={self.cortar_no}"

    def parse_listings_from_html(self, html: str, source_url: str) -> list[Listing]:
        card_pattern = re.compile(r"<div\s+class=\"item_inner\"[^>]*>(.*?)</div>", re.DOTALL)
        listings: list[Listing] = []

        for raw_card in card_pattern.findall(html):
            complex_name = self._extract_by_class(raw_card, "text")
            spec_text = self._extract_by_class(raw_card, "type")
            price_text = self._extract_by_class(raw_card, "price")
            deal_type = self._extract_by_class(raw_card, "type2")

            area_m2, floor, direction = self._parse_spec(spec_text)
            listings.append(
                Listing(
                    region=self.region_label,
                    complex_name=complex_name,
                    deal_type=deal_type,
                    price_text=price_text,
                    area_m2=area_m2,
                    floor=floor,
                    direction=direction,
                    spec_text=spec_text,
                    source_url=source_url,
                )
            )
            if len(listings) >= self.config.max_items:
                break

        return listings

    def collect_with_playwright(self, headless: bool = True) -> list[Listing]:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError(
                "playwright가 설치되어 있지 않습니다. `pip install playwright` 후 다시 실행하세요."
            ) from exc

        url = self.build_search_url()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2500)
            html = page.content()
            browser.close()

        return self.parse_listings_from_html(html, source_url=url)

    @staticmethod
    def _extract_by_class(fragment: str, class_name: str) -> str:
        pattern = re.compile(
            rf"<[^>]*class=\"{re.escape(class_name)}\"[^>]*>(.*?)</[^>]+>",
            re.DOTALL,
        )
        match = pattern.search(fragment)
        if not match:
            return ""
        text = re.sub(r"<[^>]+>", "", match.group(1))
        return " ".join(unescape(text).split())

    @staticmethod
    def _parse_spec(spec_text: str) -> tuple[float | None, str, str]:
        area_m2: float | None = None
        floor = ""
        direction = ""

        if not spec_text:
            return area_m2, floor, direction

        parts = [part.strip() for part in spec_text.split(",")]
        for part in parts:
            if "㎡" in part:
                number = part.replace("㎡", "").strip()
                try:
                    area_m2 = float(number)
                except ValueError:
                    area_m2 = None
            elif "층" in part:
                floor = part
            elif "향" in part:
                direction = part

        return area_m2, floor, direction


def flatten(items: Iterable[list[Listing]]) -> list[Listing]:
    out: list[Listing] = []
    for chunk in items:
        out.extend(chunk)
    return out
