from lib.rename import build_filename


def test_build_filename_basic():
    fname = build_filename("Test Game", "USA", ["En"], "SLES-12345", disc="1", extra_tags=["Rev A"], extension=".chd")
    assert "Test Game" in fname
    assert "[US]" in fname
    assert "[SLES-12345]" in fname
