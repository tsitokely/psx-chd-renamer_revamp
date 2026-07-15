import xml.etree.ElementTree as ET
from pathlib import Path
from .utils import DISC_PATTERN, PAREN_PATTERN


def load_redump_dat(dat_path: str) -> dict:
    tree = ET.parse(dat_path)
    root = tree.getroot()
    lookup = {}

    for game in root.findall("game"):
        serial_elem = game.find("serial")
        if serial_elem is None or not serial_elem.text:
            continue
        serial = serial_elem.text.strip().split(",")[0]
        lookup.setdefault(serial, []).append(game.get("name"))

    return lookup


def parse_redump_name(name: str, region_map: dict, is_language_tag_fn) -> dict:
    disc_match = DISC_PATTERN.search(name)
    disc_number = disc_match.group(1) if disc_match else None

    name_no_disc = DISC_PATTERN.sub("", name)
    title = name_no_disc.split("(")[0].strip()

    tags = PAREN_PATTERN.findall(name_no_disc)

    region = None
    languages = []
    extra_tags = []
    for i, tag in enumerate(tags):
        tag = tag.strip()
        if i == 0 and tag in region_map:
            region = tag
            continue
        if is_language_tag_fn(tag):
            languages = [p.strip() for p in tag.split(",")]
            continue
        extra_tags.append(tag)

    region_code = region_map.get(region, region)

    formatted_parts = [title]
    for t in extra_tags:
        formatted_parts.append(f"({t})")
    if disc_number:
        formatted_parts.append(f"(Disc {disc_number})")
    if region_code:
        formatted_parts.append(f"[{region_code}]")

    formatted_title = " ".join(formatted_parts)

    return {
        "title": title,
        "region": region,
        "languages": languages,
        "disc": disc_number,
        "extra_tags": extra_tags,
        "formatted_title": formatted_title,
    }
