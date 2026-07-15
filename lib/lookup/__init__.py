from pathlib import Path

from lib.common.assets import REDUMP_DAT_PATH, PDC_CACHE_PATH
from .utils import (
    smart_title_case,
    is_language_tag,
    is_cache_stale,
    DISC_PATTERN,
    PAREN_PATTERN,
    REGION_CODE_MAP,
)
from .redump import load_redump_dat, parse_redump_name

# avoid importing `.pdc` (which requires `requests`) at module import time;
# expose the cache path constant and a lazy loader for the lookup builder


def build_psxdatacenter_lookup(*args, **kwargs):
    from .pdc import build_psxdatacenter_lookup as _build
    return _build(*args, **kwargs)

# defaults used by root-level wrapper
DAT_PATH = str(REDUMP_DAT_PATH)

CACHE_MAX_AGE_SECONDS = 7 * 24 * 60 * 60

def get_metadata(serial: str, original_name: str = "", redump_lookup: dict = None, pdc_lookup: dict = None) -> dict | None:
    if redump_lookup is None:
        redump_lookup = load_redump_dat(DAT_PATH)
    if pdc_lookup is None:
        pdc_lookup = build_psxdatacenter_lookup()

    names = redump_lookup.get(serial)
    if names:
        if len(names) > 1 and original_name:
            best = max(names, key=lambda n: len(set(n.lower().split()) & set(original_name.lower().split())))
            return parse_redump_name(best, REGION_CODE_MAP, is_language_tag)
        return parse_redump_name(names[0], REGION_CODE_MAP, is_language_tag)

    if serial in pdc_lookup:
        return pdc_lookup[serial]

    return None
