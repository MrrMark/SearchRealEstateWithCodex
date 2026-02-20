from __future__ import annotations

import argparse
import json
import sys

from .exporter import save_listings_to_csv
from .naver_client import CollectorConfig, NaverRealEstateClient
from .region import resolve_region


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="네이버 부동산 아파트 매물/시세 수집기")
    parser.add_argument("--region", required=True, help="지역 키(gangnam) 또는 라벨 일부(강남구)")
    parser.add_argument("--max-items", type=int, default=100, help="최대 수집 건수")
    parser.add_argument("--csv", default="output/listings.csv", help="CSV 저장 경로")
    parser.add_argument("--json", action="store_true", help="수집 결과를 JSON으로 표준출력")
    parser.add_argument("--headed", action="store_true", help="브라우저 UI를 보면서 실행")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        region = resolve_region(args.region)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    client = NaverRealEstateClient(
        region_label=region["label"],
        cortar_no=region["cortarNo"],
        config=CollectorConfig(max_items=args.max_items),
    )

    listings = client.collect_with_playwright(headless=not args.headed)
    output_path = save_listings_to_csv(listings, args.csv)
    print(f"Saved {len(listings)} items to {output_path}")

    if args.json:
        print(json.dumps([item.to_dict() for item in listings], ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
