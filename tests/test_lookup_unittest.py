from pathlib import Path

from lib.lookup import DAT_PATH, PDC_CACHE_PATH
from lib.lookup.utils import smart_title_case
from lib.lookup.redump import parse_redump_name


def test_smart_title_case_basic():
    text = "the legend of zelda: a link to the past"
    got = smart_title_case(text)
    assert "Legend" in got


def test_parse_redump_name():
    name = "Final Fantasy VII (Japan) (En, Ja) (Disc 2)"
    parsed = parse_redump_name(name, {"Japan": "JP"}, lambda t: True)
    assert parsed["disc"] == "2"
    assert parsed["region"] == "Japan"


def test_default_lookup_data_files_live_in_assets_directory():
    repo_root = Path(__file__).resolve().parents[1]
    assert Path(DAT_PATH) == repo_root / "assets" / "redump-psx.dat"
    assert PDC_CACHE_PATH == repo_root / "assets" / "psxdatacenter_cache.json"
