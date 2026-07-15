import re
from pathlib import Path
from typing import List, Optional, Tuple

from lib.common.regions import (
    LANGUAGE_CODE_MAP,
    COUNTRY_REGION_LANGUAGE_MAP,
    REGION_CODE_MAP,
)


CONTINENT_REGIONS = {"Europe", "USA", "Asia", "World", "Australia", "Korea", "Japan"}


def sanitize_title(title: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "", title).strip()


def map_languages(languages: List[str]) -> List[str]:
    return [LANGUAGE_CODE_MAP.get(l, l) for l in languages]


def resolve_region_language(region: str, languages: List[str]) -> Tuple[str, List[str]]:
    if region in COUNTRY_REGION_LANGUAGE_MAP:
        mapped_region, mapped_lang = COUNTRY_REGION_LANGUAGE_MAP[region]
        return mapped_region, [mapped_lang]
    region_code = REGION_CODE_MAP.get(region, "XX")
    lang_codes = map_languages(languages) if languages else []
    return region_code, lang_codes


def build_filename(title: str, region: str, languages: List[str], serial: str, disc: Optional[str] = None, extra_tags: Optional[List[str]] = None, extension: str = ".chd") -> str:
    clean_title = sanitize_title(title)
    region_code, lang_codes = resolve_region_language(region, languages)
    lang_part = f"[{','.join(lang_codes)}]" if lang_codes else ""

    extra_part = ""
    if extra_tags:
        extra_part = " " + " ".join(f"({sanitize_title(tag)})" for tag in extra_tags)

    disc_part = f" (Disc {disc})" if disc else ""
    ext = extension if extension.startswith(".") else f".{extension}"
    return f"[PS1] {clean_title}{extra_part}{disc_part} [{region_code}]{lang_part} [{serial}]{ext}"


def rename_chd(chd_path: Path, title: str, region: str, languages: List[str], serial: str, disc: Optional[str] = None, extra_tags: Optional[List[str]] = None, dry_run: bool = True) -> Path:
    new_name = build_filename(
        title, region, languages, serial,
        disc=disc, extra_tags=extra_tags, extension=chd_path.suffix
    )
    new_path = chd_path.with_name(new_name)

    if new_path.exists() and new_path != chd_path:
        raise FileExistsError(f"Target already exists: {new_path.name}")

    if dry_run:
        print(f"[DRY RUN] {chd_path.name} -> {new_path.name}")
    else:
        chd_path.rename(new_path)
        print(f"Renamed: {chd_path.name} -> {new_path.name}")

    return new_path
