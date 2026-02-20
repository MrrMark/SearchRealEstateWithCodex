import csv
from pathlib import Path

from .models import Listing


FIELDNAMES = [
    "region",
    "complex_name",
    "deal_type",
    "price_text",
    "area_m2",
    "floor",
    "direction",
    "spec_text",
    "source_url",
]


def save_listings_to_csv(listings: list[Listing], output_path: str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for item in listings:
            writer.writerow(item.to_dict())
    return path
