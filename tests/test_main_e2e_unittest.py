import sys
from pathlib import Path

import main as cli_entry
import lib.main as lib_main
from lib.main import main


def test_main_processes_iso(tmp_path, monkeypatch):
    iso_path = tmp_path / "game.iso"
    iso_path.write_bytes(b"junk SLES_123.45 junk")

    dat_path = tmp_path / "redump-psx.dat"
    dat_path.write_text(
        '<data>\n  <game name="Test Game">\n    <serial> SLES_123.45 </serial>\n  </game>\n</data>',
        encoding="utf-8",
    )

    monkeypatch.setattr(lib_main, "DAT_PATH", str(dat_path))
    monkeypatch.setattr(
        lib_main,
        "get_metadata",
        lambda serial, original_name, redump_lookup, pdc_lookup: {
            "title": "Test Game",
            "region": "USA",
            "languages": ["En"],
            "disc": None,
            "extra_tags": [],
        },
    )

    main(chdman_path=None, base_dir=tmp_path, dry_run=True)

    assert iso_path.exists()


def test_cli_supports_disabling_dry_run(monkeypatch):
    calls = []

    def fake_run_main(**kwargs):
        calls.append(kwargs)

    monkeypatch.setattr(cli_entry, "run_main", fake_run_main)
    monkeypatch.setattr(sys, "argv", ["main.py", "--no-dry-run"])

    cli_entry.main()

    assert calls == [{
        "chdman_path": cli_entry.CHDMAN_PATH,
        "base_dir": cli_entry.BASE_DIR,
        "dry_run": False,
    }]
