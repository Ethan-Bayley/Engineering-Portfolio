import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "general" / "tools"))
import onshape_images as oi  # noqa: E402

URL = ("https://cad.onshape.com/documents/0123456789abcdef01234567/w/89abcdef0123456789abcdef"
       "/e/fedcba9876543210fedcba98")


def test_parse_element_url():
    ids = oi.parse_url(URL)
    assert ids == {"host": "cad.onshape.com", "did": "0123456789abcdef01234567", "wvm": "w", "wvmid": "89abcdef0123456789abcdef",
                   "eid": "fedcba9876543210fedcba98"}


def test_parse_rejects_non_element_urls():
    for bad in ("https://cad.onshape.com/documents/0123456789abcdef01234567", "https://example.com/x", ""):
        with pytest.raises(ValueError):
            oi.parse_url(bad)


def test_isometric_is_sent_as_a_matrix_and_named_views_pass_through():
    iso = oi.shaded_view_params("isometric", 2000, 1500, edges=True)
    assert iso["viewMatrix"].count(",") == 11 and iso["pixelSize"] == 0
    assert oi.shaded_view_params("front", 800, 600, edges=False)["viewMatrix"] == "front"
    with pytest.raises(ValueError):
        oi.shaded_view_params("sideways", 800, 600, edges=True)


def test_missing_keys_stop_without_a_network_call(monkeypatch, tmp_path):
    monkeypatch.delenv("ONSHAPE_ACCESS_KEY", raising=False)
    monkeypatch.delenv("ONSHAPE_SECRET_KEY", raising=False)
    monkeypatch.setattr(oi, "KEY_FILE", tmp_path / "none.json")
    with pytest.raises(SystemExit):
        oi.load_keys()


def test_school_onshape_address_is_kept():
    assert oi.parse_url(URL.replace("cad.onshape.com", "barker.onshape.com"))["host"] == "barker.onshape.com"
