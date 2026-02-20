from dataclasses import asdict, dataclass


@dataclass(slots=True)
class Listing:
    region: str
    complex_name: str
    deal_type: str
    price_text: str
    area_m2: float | None
    floor: str
    direction: str
    spec_text: str
    source_url: str

    def to_dict(self) -> dict:
        return asdict(self)
