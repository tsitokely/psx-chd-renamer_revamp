import argparse
import sys
from typing import Optional

from lib.main import main as run_main

CHDMAN_PATH: str = ""
BASE_DIR: str = r""


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Rename PSX CHD/ISO files using metadata lookup")
    parser.add_argument("--chdman", dest="chdman_path", default=None, help="Path to chdman executable")
    parser.add_argument("--base-dir", dest="base_dir", default=None, help="Directory containing CHD/ISO files")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", help="Preview changes without renaming")
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false", help="Apply renames without preview")
    parser.set_defaults(dry_run=True)

    args = parser.parse_args(argv or sys.argv[1:])
    run_main(
        chdman_path=args.chdman_path if args.chdman_path is not None else CHDMAN_PATH,
        base_dir=args.base_dir if args.base_dir is not None else BASE_DIR,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()