"""Tests for tarot_gen.consistency module."""

from io import BytesIO
from pathlib import Path
import tempfile

from PIL import Image
import pytest

from tarot_gen.consistency import resize_image_to_aspect


def _make_test_image(width: int, height: int, color: tuple = (128, 64, 32)) -> Path:
    """Create a temporary solid-color PNG and return its path."""
    img = Image.new("RGB", (width, height), color)
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img.save(tmp, format="PNG")
    tmp.close()
    return Path(tmp.name)


class TestResizeImageToAspect:
    """Existing center-crop behavior (no card_seed)."""

    def test_center_crop_wider_image(self):
        """A wide image cropped to 2:3 should produce 768x1152 output."""
        path = _make_test_image(2000, 1000)
        result = resize_image_to_aspect(path, 768, 1152)
        img = Image.open(BytesIO(result))
        assert img.size == (768, 1152)

    def test_center_crop_taller_image(self):
        """A tall image cropped to 3:2 should produce 1152x768 output."""
        path = _make_test_image(1000, 2000)
        result = resize_image_to_aspect(path, 1152, 768)
        img = Image.open(BytesIO(result))
        assert img.size == (1152, 768)

    def test_exact_ratio_no_crop(self):
        """An image already at target ratio should resize without cropping."""
        path = _make_test_image(1536, 2304)  # exactly 2:3
        result = resize_image_to_aspect(path, 768, 1152)
        img = Image.open(BytesIO(result))
        assert img.size == (768, 1152)
