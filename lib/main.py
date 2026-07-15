from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union

from lib.identify import extract_serial, resolve_chdman
from lib.lookup import DAT_PATH, load_redump_dat, get_metadata, build_psxdatacenter_lookup
from lib.rename import rename_chd

def _iter_chd_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        yield path
        return
    for p in path.rglob("*.chd"):
        yield p
    for p in path.rglob("*.iso"):
        yield p


def main(chdman_path: Optional[str] = None, base_dir: Optional[Union[str, Path]] = None, dry_run: bool = True) -> None:
    chdman: Optional[str] = None
    if chdman_path:
        # resolve_chdman expects a non-empty string
        chdman = resolve_chdman(chdman_path)

    redump_lookup: Dict[str, List[str]] = load_redump_dat(DAT_PATH)

    chd_path = Path(base_dir) if base_dir is not None else Path(BASE_DIR)
    chd_files: List[Path] = list(_iter_chd_files(chd_path))

    print(f"Processing {len(chd_files)} file(s)")
    failures: List[tuple[str, str]] = []

    for chd_file in chd_files:
        serial = extract_serial(chd_file, chdman)
        if serial is None:
            failures.append((chd_file.name, "no serial found"))
            continue

        # Build pdc lookup lazily (may read cache or attempt fetch); some
        # serials exist only on psxdatacenter, so pass None to allow lookup.
        metadata: Optional[Dict[str, Any]] = get_metadata(serial, chd_file.stem, redump_lookup, None)
        if metadata is None:
            failures.append((chd_file.name, f"serial {serial} not found in any source"))
            continue

        try:
            rename_chd(
                chd_file,
                metadata["title"],
                metadata["region"],
                metadata.get("languages", []),
                serial,
                disc=metadata.get("disc"),
                extra_tags=metadata.get("extra_tags"),
                dry_run=dry_run,
            )
        except FileExistsError as e:
            failures.append((chd_file.name, str(e)))

    if failures:
        print("\nFailed items:")
        for name, reason in failures:
            print(f"  {name}: {reason}")


if __name__ == "__main__":
    main()
