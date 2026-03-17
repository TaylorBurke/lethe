#!/bin/bash
# Download 78 Rider-Waite cards from Wikimedia Commons (URLs from API lookup)
# Skips files already downloaded

DIR="$(cd "$(dirname "$0")" && pwd)"
UA="Mozilla/5.0 (compatible; tarot-downloader/1.0)"

download() {
  local idx="$1"
  local url="$2"
  local out="$DIR/$(printf '%02d' $idx).jpg"
  if [ -f "$out" ]; then
    echo "  skip $idx (exists)"
    return
  fi
  echo "  [$idx] $url"
  curl -s -A "$UA" --retry 3 --retry-delay 5 -o "$out" "$url"
  local status=$?
  if [ $status -ne 0 ] || [ ! -s "$out" ]; then
    echo "  ERROR: failed to download $idx"
    rm -f "$out"
  else
    echo "       -> $(printf '%02d' $idx).jpg"
    sleep 1.5
  fi
}

# Major Arcana
download  0  "https://upload.wikimedia.org/wikipedia/commons/9/90/RWS_Tarot_00_Fool.jpg"
download  1  "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg"
download  2  "https://upload.wikimedia.org/wikipedia/commons/8/88/RWS_Tarot_02_High_Priestess.jpg"
download  3  "https://upload.wikimedia.org/wikipedia/commons/d/d2/RWS_Tarot_03_Empress.jpg"
download  4  "https://upload.wikimedia.org/wikipedia/commons/c/c3/RWS_Tarot_04_Emperor.jpg"
download  5  "https://upload.wikimedia.org/wikipedia/commons/8/8d/RWS_Tarot_05_Hierophant.jpg"
download  6  "https://upload.wikimedia.org/wikipedia/commons/d/db/RWS_Tarot_06_Lovers.jpg"
download  7  "https://upload.wikimedia.org/wikipedia/commons/9/9b/RWS_Tarot_07_Chariot.jpg"
download  8  "https://upload.wikimedia.org/wikipedia/commons/f/f5/RWS_Tarot_08_Strength.jpg"
download  9  "https://upload.wikimedia.org/wikipedia/commons/4/4d/RWS_Tarot_09_Hermit.jpg"
download 10  "https://upload.wikimedia.org/wikipedia/commons/3/3c/RWS_Tarot_10_Wheel_of_Fortune.jpg"
download 11  "https://upload.wikimedia.org/wikipedia/commons/e/e0/RWS_Tarot_11_Justice.jpg"
download 12  "https://upload.wikimedia.org/wikipedia/commons/2/2b/RWS_Tarot_12_Hanged_Man.jpg"
download 13  "https://upload.wikimedia.org/wikipedia/commons/d/d7/RWS_Tarot_13_Death.jpg"
download 14  "https://upload.wikimedia.org/wikipedia/commons/f/f8/RWS_Tarot_14_Temperance.jpg"
download 15  "https://upload.wikimedia.org/wikipedia/commons/5/55/RWS_Tarot_15_Devil.jpg"
download 16  "https://upload.wikimedia.org/wikipedia/commons/5/53/RWS_Tarot_16_Tower.jpg"
download 17  "https://upload.wikimedia.org/wikipedia/commons/d/db/RWS_Tarot_17_Star.jpg"
download 18  "https://upload.wikimedia.org/wikipedia/commons/7/7f/RWS_Tarot_18_Moon.jpg"
download 19  "https://upload.wikimedia.org/wikipedia/commons/1/17/RWS_Tarot_19_Sun.jpg"
download 20  "https://upload.wikimedia.org/wikipedia/commons/d/dd/RWS_Tarot_20_Judgement.jpg"
download 21  "https://upload.wikimedia.org/wikipedia/commons/f/ff/RWS_Tarot_21_World.jpg"
# Wands
download 22  "https://upload.wikimedia.org/wikipedia/commons/1/11/Wands01.jpg"
download 23  "https://upload.wikimedia.org/wikipedia/commons/0/0f/Wands02.jpg"
download 24  "https://upload.wikimedia.org/wikipedia/commons/f/ff/Wands03.jpg"
download 25  "https://upload.wikimedia.org/wikipedia/commons/a/a4/Wands04.jpg"
download 26  "https://upload.wikimedia.org/wikipedia/commons/9/9d/Wands05.jpg"
download 27  "https://upload.wikimedia.org/wikipedia/commons/3/3b/Wands06.jpg"
download 28  "https://upload.wikimedia.org/wikipedia/commons/e/e4/Wands07.jpg"
download 29  "https://upload.wikimedia.org/wikipedia/commons/6/6b/Wands08.jpg"
download 30  "https://upload.wikimedia.org/wikipedia/commons/4/4d/Tarot_Nine_of_Wands.jpg"
download 31  "https://upload.wikimedia.org/wikipedia/commons/0/0b/Wands10.jpg"
download 32  "https://upload.wikimedia.org/wikipedia/commons/6/6a/Wands11.jpg"
download 33  "https://upload.wikimedia.org/wikipedia/commons/1/16/Wands12.jpg"
download 34  "https://upload.wikimedia.org/wikipedia/commons/0/0d/Wands13.jpg"
download 35  "https://upload.wikimedia.org/wikipedia/commons/c/ce/Wands14.jpg"
# Cups
download 36  "https://upload.wikimedia.org/wikipedia/commons/3/36/Cups01.jpg"
download 37  "https://upload.wikimedia.org/wikipedia/commons/f/f8/Cups02.jpg"
download 38  "https://upload.wikimedia.org/wikipedia/commons/7/7a/Cups03.jpg"
download 39  "https://upload.wikimedia.org/wikipedia/commons/3/35/Cups04.jpg"
download 40  "https://upload.wikimedia.org/wikipedia/commons/d/d7/Cups05.jpg"
download 41  "https://upload.wikimedia.org/wikipedia/commons/1/17/Cups06.jpg"
download 42  "https://upload.wikimedia.org/wikipedia/commons/a/ae/Cups07.jpg"
download 43  "https://upload.wikimedia.org/wikipedia/commons/6/60/Cups08.jpg"
download 44  "https://upload.wikimedia.org/wikipedia/commons/2/24/Cups09.jpg"
download 45  "https://upload.wikimedia.org/wikipedia/commons/8/84/Cups10.jpg"
download 46  "https://upload.wikimedia.org/wikipedia/commons/a/ad/Cups11.jpg"
download 47  "https://upload.wikimedia.org/wikipedia/commons/f/fa/Cups12.jpg"
download 48  "https://upload.wikimedia.org/wikipedia/commons/6/62/Cups13.jpg"
download 49  "https://upload.wikimedia.org/wikipedia/commons/0/04/Cups14.jpg"
# Swords
download 50  "https://upload.wikimedia.org/wikipedia/commons/1/1a/Swords01.jpg"
download 51  "https://upload.wikimedia.org/wikipedia/commons/9/9e/Swords02.jpg"
download 52  "https://upload.wikimedia.org/wikipedia/commons/0/02/Swords03.jpg"
download 53  "https://upload.wikimedia.org/wikipedia/commons/b/bf/Swords04.jpg"
download 54  "https://upload.wikimedia.org/wikipedia/commons/2/23/Swords05.jpg"
download 55  "https://upload.wikimedia.org/wikipedia/commons/2/29/Swords06.jpg"
download 56  "https://upload.wikimedia.org/wikipedia/commons/3/34/Swords07.jpg"
download 57  "https://upload.wikimedia.org/wikipedia/commons/a/a7/Swords08.jpg"
download 58  "https://upload.wikimedia.org/wikipedia/commons/2/2f/Swords09.jpg"
download 59  "https://upload.wikimedia.org/wikipedia/commons/d/d4/Swords10.jpg"
download 60  "https://upload.wikimedia.org/wikipedia/commons/4/4c/Swords11.jpg"
download 61  "https://upload.wikimedia.org/wikipedia/commons/b/b0/Swords12.jpg"
download 62  "https://upload.wikimedia.org/wikipedia/commons/d/d4/Swords13.jpg"
download 63  "https://upload.wikimedia.org/wikipedia/commons/3/33/Swords14.jpg"
# Pentacles
download 64  "https://upload.wikimedia.org/wikipedia/commons/f/fd/Pents01.jpg"
download 65  "https://upload.wikimedia.org/wikipedia/commons/9/9f/Pents02.jpg"
download 66  "https://upload.wikimedia.org/wikipedia/commons/4/42/Pents03.jpg"
download 67  "https://upload.wikimedia.org/wikipedia/commons/3/35/Pents04.jpg"
download 68  "https://upload.wikimedia.org/wikipedia/commons/9/96/Pents05.jpg"
download 69  "https://upload.wikimedia.org/wikipedia/commons/a/a6/Pents06.jpg"
download 70  "https://upload.wikimedia.org/wikipedia/commons/6/6a/Pents07.jpg"
download 71  "https://upload.wikimedia.org/wikipedia/commons/4/49/Pents08.jpg"
download 72  "https://upload.wikimedia.org/wikipedia/commons/f/f0/Pents09.jpg"
download 73  "https://upload.wikimedia.org/wikipedia/commons/4/42/Pents10.jpg"
download 74  "https://upload.wikimedia.org/wikipedia/commons/e/ec/Pents11.jpg"
download 75  "https://upload.wikimedia.org/wikipedia/commons/d/d5/Pents12.jpg"
download 76  "https://upload.wikimedia.org/wikipedia/commons/8/88/Pents13.jpg"
download 77  "https://upload.wikimedia.org/wikipedia/commons/1/1c/Pents14.jpg"

echo ""
echo "Files in dir: $(ls "$DIR"/*.jpg 2>/dev/null | wc -l)/78"
