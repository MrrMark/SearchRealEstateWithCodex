"""Minimal region map used for Naver Real Estate URL parameters.

You can expand this map as you validate exact area codes in your target regions.
"""

REGIONS = {
    "gangnam": {"label": "서울 강남구", "cortarNo": "1168000000"},
    "songpa": {"label": "서울 송파구", "cortarNo": "1171000000"},
    "bundang": {"label": "성남시 분당구", "cortarNo": "4113500000"},
}


def resolve_region(user_input: str) -> dict:
    key = user_input.strip().lower()
    if key in REGIONS:
        return REGIONS[key]

    for item in REGIONS.values():
        if user_input.strip() in item["label"]:
            return item

    options = ", ".join(REGIONS.keys())
    raise ValueError(f"지원하지 않는 지역입니다: {user_input}. 사용 가능한 키: {options}")
