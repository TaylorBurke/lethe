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


class TestSlidingCrop:
    """Seed-based crop offset behavior."""

    def test_no_seed_matches_center_crop(self):
        """card_seed=None should produce identical output to default."""
        path = _make_test_image(2000, 3000)
        center = resize_image_to_aspect(path, 768, 1152)
        no_seed = resize_image_to_aspect(path, 768, 1152, card_seed=None)
        assert center == no_seed

    def test_different_seeds_produce_different_crops(self):
        """Two different seeds on a large image should produce different bytes."""
        # Use a gradient image so different crops are visually distinct
        img = Image.new("RGB", (3000, 4000))
        for x in range(3000):
            for y in range(4000):
                img.putpixel((x, y), (x % 256, y % 256, (x + y) % 256))
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img.save(tmp, format="PNG")
        tmp.close()
        path = Path(tmp.name)

        crop_a = resize_image_to_aspect(path, 768, 1152, card_seed=42, diversity="high")
        crop_b = resize_image_to_aspect(path, 768, 1152, card_seed=99, diversity="high")
        assert crop_a != crop_b

    def test_same_seed_is_deterministic(self):
        """Same seed should always produce the same crop."""
        path = _make_test_image(2000, 3000)
        crop_1 = resize_image_to_aspect(path, 768, 1152, card_seed=42, diversity="medium")
        crop_2 = resize_image_to_aspect(path, 768, 1152, card_seed=42, diversity="medium")
        assert crop_1 == crop_2

    def test_small_image_falls_back_to_center(self):
        """An image at or below target size should center crop regardless of seed."""
        path = _make_test_image(768, 1152)
        center = resize_image_to_aspect(path, 768, 1152)
        seeded = resize_image_to_aspect(path, 768, 1152, card_seed=42, diversity="high")
        assert center == seeded

    def test_diversity_low_less_variation_than_high(self):
        """Low diversity should constrain offsets more than high."""
        # Create gradient image
        img = Image.new("RGB", (3000, 4000))
        for x in range(3000):
            for y in range(4000):
                img.putpixel((x, y), (x % 256, y % 256, (x + y) % 256))
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img.save(tmp, format="PNG")
        tmp.close()
        path = Path(tmp.name)

        # Generate crops for seeds 0-9 at low and high diversity
        low_crops = set()
        high_crops = set()
        for s in range(10):
            low_crops.add(resize_image_to_aspect(path, 768, 1152, card_seed=s, diversity="low"))
            high_crops.add(resize_image_to_aspect(path, 768, 1152, card_seed=s, diversity="high"))
        # High diversity should produce at least as many unique crops as low
        assert len(high_crops) >= len(low_crops)
