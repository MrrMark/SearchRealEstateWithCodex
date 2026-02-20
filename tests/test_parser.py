from realestate.naver_client import NaverRealEstateClient


SAMPLE_HTML = """
<div class="item_inner">
  <span class="text">은마아파트</span>
  <span class="type">84.96㎡, 12/25층, 남향</span>
  <span class="price">25억</span>
  <span class="type2">매매</span>
</div>
<div class="item_inner">
  <span class="text">대치아이파크</span>
  <span class="type">59.98㎡, 7/20층, 동향</span>
  <span class="price">16억</span>
  <span class="type2">전세</span>
</div>
"""


def test_parse_listings_from_html_extracts_core_fields() -> None:
    client = NaverRealEstateClient(region_label="서울 강남구", cortar_no="1168000000")

    listings = client.parse_listings_from_html(SAMPLE_HTML, source_url="https://example.com")

    assert len(listings) == 2
    assert listings[0].complex_name == "은마아파트"
    assert listings[0].area_m2 == 84.96
    assert listings[0].floor == "12/25층"
    assert listings[0].direction == "남향"
    assert listings[1].deal_type == "전세"
