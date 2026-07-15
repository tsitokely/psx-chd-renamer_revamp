from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"

REDUMP_DAT_PATH = ASSETS_DIR / "redump-psx.dat"
PDC_CACHE_PATH = ASSETS_DIR / "psxdatacenter_cache.json"

__all__ = ["PROJECT_ROOT", "ASSETS_DIR", "REDUMP_DAT_PATH", "PDC_CACHE_PATH"]
