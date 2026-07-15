import re
import json
import requests
from pathlib import Path
from lib.common.assets import PDC_CACHE_PATH
from .utils import smart_title_case, is_language_tag

REGION_BY_LIST = {"ulist": "USA", "plist": "Europe", "jlist": "Japan"}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://psxdatacenter.com/",
}

ROW_PATTERN = re.compile(
    r'href="games/[^\"]+">INFO</a></td>\s*'
    r'<td class="col2"[^>]*>(.*?)</td>\s*'
    r'<td class="col3"[^>]*>([^<]*)</td>\s*'
    r'<td class="col4"[^>]*>([^<]*)</td>',
    re.IGNORECASE | re.DOTALL
)


def clean_html_text(text: str) -> str:
    return text.replace("&nbsp;", " ").strip()


def fetch_psxdatacenter_list(list_name: str) -> str:
    url = f"https://psxdatacenter.com/{list_name}.html"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse_psxdatacenter_list(html: str, region: str) -> dict:
    lookup = {}
    for serial_raw, title_raw, langs_raw in ROW_PATTERN.findall(html):
        title_raw = clean_html_text(title_raw)
        langs_raw = clean_html_text(langs_raw)

        serials = [
            clean_html_text(s) for s in re.split(r"<br\s*/?>", serial_raw, flags=re.IGNORECASE)
            if clean_html_text(s)
        ]

        disc_match = re.search(r"\[\s*(\d+)\s*DISCS?\s*\]", title_raw, re.IGNORECASE)
        clean_title = re.sub(r"\s*-?\s*\[\s*\d+\s*DISCS?\s*\]", "", title_raw, flags=re.IGNORECASE).strip()
        clean_title = smart_title_case(clean_title)

        languages = re.findall(r"\[([A-Za-z]+)\]", langs_raw)

        for i, s in enumerate(serials):
            lookup[s] = {
                "title": clean_title,
                "region": region,
                "languages": languages,
                "disc": str(i + 1) if disc_match else None,
            }
    return lookup


def build_psxdatacenter_lookup(fetch_fn=fetch_psxdatacenter_list, force_refresh: bool = False, cache_path: Path = PDC_CACHE_PATH) -> dict:
    cache_exists = cache_path.exists()
    # lightweight max age constant (reuse from caller)
    from .utils import is_cache_stale, CACHE_MAX_AGE_SECONDS

    stale = is_cache_stale(cache_path, CACHE_MAX_AGE_SECONDS)

    if cache_exists and not force_refresh and not stale:
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    combined = {}
    for list_name, region in REGION_BY_LIST.items():
        try:
            html = fetch_fn(list_name)
            combined.update(parse_psxdatacenter_list(html, region))
        except Exception as e:
            print(f"Skipping {list_name}: {type(e).__name__}: {e}")

    if combined:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(combined, f, ensure_ascii=False, indent=2)
        return combined

    if cache_exists:
        print("WARNING: refresh failed, falling back to stale cache on disk")
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    print("WARNING: no cache available and fetch failed — returning empty lookup")
    return {}
