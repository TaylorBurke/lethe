#!/usr/bin/env python3
"""Download and rename all 78 Rider-Waite tarot cards from Wikimedia Commons."""

import urllib.request
import urllib.parse
import json
import os
import time

# Classic tarot order: 0=Fool ... 21=World, then suits: Wands, Cups, Swords, Pentacles
# Each suit: Ace(1) through 10, Page(11), Knight(12), Queen(13), King(14)
CARD_FILES = [
    # Major Arcana (0-21)
    (0,  "RWS Tarot 00 Fool.jpg"),
    (1,  "RWS Tarot 01 Magician.jpg"),
    (2,  "RWS Tarot 02 High Priestess.jpg"),
    (3,  "RWS Tarot 03 Empress.jpg"),
    (4,  "RWS Tarot 04 Emperor.jpg"),
    (5,  "RWS Tarot 05 Hierophant.jpg"),
    (6,  "RWS Tarot 06 Lovers.jpg"),
    (7,  "RWS Tarot 07 Chariot.jpg"),
    (8,  "RWS Tarot 08 Strength.jpg"),
    (9,  "RWS Tarot 09 Hermit.jpg"),
    (10, "RWS Tarot 10 Wheel of Fortune.jpg"),
    (11, "RWS Tarot 11 Justice.jpg"),
    (12, "RWS Tarot 12 Hanged Man.jpg"),
    (13, "RWS Tarot 13 Death.jpg"),
    (14, "RWS Tarot 14 Temperance.jpg"),
    (15, "RWS Tarot 15 Devil.jpg"),
    (16, "RWS Tarot 16 Tower.jpg"),
    (17, "RWS Tarot 17 Star.jpg"),
    (18, "RWS Tarot 18 Moon.jpg"),
    (19, "RWS Tarot 19 Sun.jpg"),
    (20, "RWS Tarot 20 Judgement.jpg"),
    (21, "RWS Tarot 21 World.jpg"),
    # Wands (22-35)
    (22, "Wands01.jpg"),
    (23, "Wands02.jpg"),
    (24, "Wands03.jpg"),
    (25, "Wands04.jpg"),
    (26, "Wands05.jpg"),
    (27, "Wands06.jpg"),
    (28, "Wands07.jpg"),
    (29, "Wands08.jpg"),
    (30, "Tarot Nine of Wands.jpg"),
    (31, "Wands10.jpg"),
    (32, "Wands11.jpg"),
    (33, "Wands12.jpg"),
    (34, "Wands13.jpg"),
    (35, "Wands14.jpg"),
    # Cups (36-49)
    (36, "Cups01.jpg"),
    (37, "Cups02.jpg"),
    (38, "Cups03.jpg"),
    (39, "Cups04.jpg"),
    (40, "Cups05.jpg"),
    (41, "Cups06.jpg"),
    (42, "Cups07.jpg"),
    (43, "Cups08.jpg"),
    (44, "Cups09.jpg"),
    (45, "Cups10.jpg"),
    (46, "Cups11.jpg"),
    (47, "Cups12.jpg"),
    (48, "Cups13.jpg"),
    (49, "Cups14.jpg"),
    # Swords (50-63)
    (50, "Swords01.jpg"),
    (51, "Swords02.jpg"),
    (52, "Swords03.jpg"),
    (53, "Swords04.jpg"),
    (54, "Swords05.jpg"),
    (55, "Swords06.jpg"),
    (56, "Swords07.jpg"),
    (57, "Swords08.jpg"),
    (58, "Swords09.jpg"),
    (59, "Swords10.jpg"),
    (60, "Swords11.jpg"),
    (61, "Swords12.jpg"),
    (62, "Swords13.jpg"),
    (63, "Swords14.jpg"),
    # Pentacles (64-77)
    (64, "Pents01.jpg"),
    (65, "Pents02.jpg"),
    (66, "Pents03.jpg"),
    (67, "Pents04.jpg"),
    (68, "Pents05.jpg"),
    (69, "Pents06.jpg"),
    (70, "Pents07.jpg"),
    (71, "Pents08.jpg"),
    (72, "Pents09.jpg"),
    (73, "Pents10.jpg"),
    (74, "Pents11.jpg"),
    (75, "Pents12.jpg"),
    (76, "Pents13.jpg"),
    (77, "Pents14.jpg"),
]

API_URL = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "tarot-downloader/1.0 (educational use)"}
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_image_url(filename):
    params = urllib.parse.urlencode({
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json",
    })
    url = f"{API_URL}?{params}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    return page["imageinfo"][0]["url"]


def download_file(url, dest):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        with open(dest, "wb") as f:
            f.write(resp.read())


errors = []
for idx, filename in CARD_FILES:
    out_path = os.path.join(OUT_DIR, f"{idx:02d}.jpg")
    if os.path.exists(out_path):
        print(f"  skip {idx:02d}.jpg (exists)")
        continue
    try:
        print(f"  [{idx:02d}] fetching URL for: {filename}")
        img_url = get_image_url(filename)
        print(f"       downloading: {img_url}")
        download_file(img_url, out_path)
        print(f"       saved -> {idx:02d}.jpg")
        time.sleep(0.3)
    except Exception as e:
        print(f"  ERROR on {idx}: {e}")
        errors.append((idx, filename, str(e)))

print(f"\nDone. {len(CARD_FILES) - len(errors)}/78 downloaded.")
if errors:
    print("Errors:")
    for idx, fn, err in errors:
        print(f"  {idx:02d} {fn}: {err}")
