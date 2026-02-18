"""All 78 tarot card definitions."""

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Card:
    name: str
    numeral: str
    arcana_type: str  # "major" or "minor"
    suit: str | None  # None for major arcana
    description: str  # Scene/imagery description
    key_symbols: list[str]
    composition: str = ""  # Framing/composition hint (e.g., "centered full-body figure")

    @property
    def slug(self) -> str:
        return self.name.lower().replace(" ", "_").replace("'", "")

    @property
    def filename(self) -> str:
        return f"{self.numeral}_{self.slug}.png"


# fmt: off
MAJOR_ARCANA: list[Card] = [
    Card("The Fool", "00", "major", None,
         "A young traveler at cliff's edge with a small dog, about to step into the unknown",
         ["cliff", "knapsack", "white rose", "small dog"]),
    Card("The Magician", "01", "major", None,
         "A figure at a table with arms raised, one pointing up and one down, tools of magic before them",
         ["infinity symbol", "wand", "cup", "sword", "pentacle", "table"]),
    Card("The High Priestess", "02", "major", None,
         "A serene woman seated between two pillars, a crescent moon at her feet, holding a scroll",
         ["two pillars", "crescent moon", "scroll", "veil", "pomegranates"]),
    Card("The Empress", "03", "major", None,
         "A regal woman on a throne amid lush nature, crowned with stars, holding a scepter",
         ["crown of stars", "wheat field", "scepter", "cushioned throne", "flowing water"]),
    Card("The Emperor", "04", "major", None,
         "An authoritative figure on a stone throne with ram heads, holding an ankh scepter",
         ["stone throne", "ram heads", "ankh scepter", "armor", "mountains"]),
    Card("The Hierophant", "05", "major", None,
         "A robed religious figure seated between pillars, blessing two acolytes, holding a triple cross",
         ["triple cross", "two acolytes", "pillars", "raised hand", "crown"]),
    Card("The Lovers", "06", "major", None,
         "Two figures beneath an angel in the sky, a tree of knowledge and tree of life behind them",
         ["angel", "two figures", "tree of knowledge", "tree of life", "sun"]),
    Card("The Chariot", "07", "major", None,
         "A warrior in a chariot pulled by two sphinxes, one black and one white, under a starry canopy",
         ["chariot", "two sphinxes", "starry canopy", "armor", "city behind"]),
    Card("Strength", "08", "major", None,
         "A gentle figure calmly closing a lion's mouth, infinity symbol above their head",
         ["lion", "infinity symbol", "garland of flowers", "white robe"]),
    Card("The Hermit", "09", "major", None,
         "A cloaked elder atop a mountain holding a lantern with a six-pointed star inside",
         ["lantern", "six-pointed star", "staff", "mountain peak", "cloak"]),
    Card("Wheel of Fortune", "10", "major", None,
         "A great wheel with mystical symbols, figures rising and falling, sphinx atop",
         ["wheel", "sphinx", "serpent", "anubis", "mystical symbols", "clouds"]),
    Card("Justice", "11", "major", None,
         "A seated figure holding a sword upright in one hand and balanced scales in the other",
         ["sword", "scales", "throne", "crown", "purple veil"]),
    Card("The Hanged Man", "12", "major", None,
         "A figure suspended upside-down from a living tree by one foot, serene expression, halo of light",
         ["living tree", "suspended figure", "halo", "crossed leg"]),
    Card("Death", "13", "major", None,
         "A skeleton in armor riding a white horse, carrying a black flag with a white rose",
         ["skeleton", "white horse", "black flag", "white rose", "rising sun"]),
    Card("Temperance", "14", "major", None,
         "A winged angel pouring water between two cups, one foot on land and one in water",
         ["angel wings", "two cups", "flowing water", "path to mountains", "triangle"]),
    Card("The Devil", "15", "major", None,
         "A horned figure on a pedestal with two chained figures below, inverted pentagram above",
         ["horned figure", "chains", "two figures", "inverted pentagram", "pedestal"]),
    Card("The Tower", "16", "major", None,
         "A tall tower struck by lightning, crown blown off the top, figures falling from windows",
         ["tower", "lightning bolt", "falling figures", "crown", "flames"]),
    Card("The Star", "17", "major", None,
         "A nude figure kneeling by a pool pouring water onto land and into the pool, stars above",
         ["large star", "seven smaller stars", "two vessels", "pool", "bird in tree"]),
    Card("The Moon", "18", "major", None,
         "A moon with a face between two towers, a dog and wolf howling, a crayfish emerging from water",
         ["moon face", "two towers", "dog", "wolf", "crayfish", "winding path"]),
    Card("The Sun", "19", "major", None,
         "A joyful child on a white horse beneath a radiant sun, sunflowers behind a wall",
         ["radiant sun", "child", "white horse", "sunflowers", "red banner"]),
    Card("Judgement", "20", "major", None,
         "An angel blowing a trumpet from the clouds, figures rising from coffins below",
         ["angel", "trumpet", "rising figures", "coffins", "mountains", "clouds"]),
    Card("The World", "21", "major", None,
         "A dancing figure inside a laurel wreath, four creatures in each corner",
         ["laurel wreath", "dancing figure", "angel", "eagle", "bull", "lion"]),
]

def _minor_cards(suit: str, suit_symbol: str, court_descriptions: dict[str, tuple[str, list[str]]],
                 pip_descriptions: dict[str, tuple[str, list[str]]], start_index: int = 0) -> list[Card]:
    """Build 14 cards for one suit with sequential numbering from start_index."""
    cards = []
    i = 0
    for num in range(1, 11):
        name_prefix = "Ace" if num == 1 else str(num)
        name = f"{name_prefix} of {suit}"
        numeral = f"{start_index + i:02d}"
        desc, symbols = pip_descriptions[str(num)]
        cards.append(Card(name, numeral, "minor", suit, desc, symbols))
        i += 1
    for rank, (desc, symbols) in court_descriptions.items():
        name = f"{rank} of {suit}"
        numeral = f"{start_index + i:02d}"
        cards.append(Card(name, numeral, "minor", suit, desc, symbols))
        i += 1
    return cards

_WANDS_PIPS: dict[str, tuple[str, list[str]]] = {
    "1": ("A hand emerging from a cloud holding a single budding wand", ["hand", "cloud", "budding wand", "leaves"]),
    "2": ("A figure holding a globe looks out from a castle battlement, two wands mounted on the wall", ["globe", "castle", "two wands", "sea"]),
    "3": ("A figure on a cliff gazing at ships on the sea, three wands planted behind them", ["cliff", "ships", "three wands", "horizon"]),
    "4": ("A celebration scene with four wands forming a canopy decorated with garlands", ["four wands", "garland", "castle", "celebrating figures"]),
    "5": ("Five figures wielding wands in chaotic conflict on rough terrain", ["five wands", "five figures", "struggle", "rough ground"]),
    "6": ("A rider on horseback wearing a laurel wreath, attendants carrying six wands", ["horseback rider", "laurel wreath", "six wands", "attendants"]),
    "7": ("A figure on a hill defending their position against six wands rising from below", ["hilltop", "defending figure", "seven wands", "uneven ground"]),
    "8": ("Eight wands flying through the air over an open landscape at speed", ["eight wands", "open sky", "landscape", "river"]),
    "9": ("A wounded but vigilant figure leaning on a wand, eight wands arrayed behind them", ["bandaged figure", "nine wands", "defensive stance"]),
    "10": ("A figure struggling under the weight of ten wands, walking toward a distant town", ["ten wands", "burdened figure", "distant town", "path"]),
}
_WANDS_COURT: dict[str, tuple[str, list[str]]] = {
    "Page": ("A youthful figure in a desert landscape holding a wand and gazing at it with wonder", ["wand", "desert", "tunic", "salamanders"]),
    "Knight": ("An armored rider on a rearing horse charging forward, brandishing a wand", ["rearing horse", "wand", "armor", "pyramids"]),
    "Queen": ("A queen on a throne holding a wand and sunflower, a black cat at her feet", ["throne", "wand", "sunflower", "black cat", "lions"]),
    "King": ("A king on a throne adorned with salamanders, holding a flowering wand", ["throne", "salamanders", "flowering wand", "crown", "cape"]),
}

_CUPS_PIPS: dict[str, tuple[str, list[str]]] = {
    "1": ("A hand from a cloud holds an overflowing chalice, a dove descends toward it", ["hand", "cloud", "overflowing cup", "dove", "lotus"]),
    "2": ("Two figures exchange cups beneath a winged lion head, a caduceus between them", ["two figures", "two cups", "caduceus", "winged lion"]),
    "3": ("Three maidens raise their cups in celebration in a garden of flowers and fruit", ["three maidens", "three cups", "garden", "fruit"]),
    "4": ("A figure sits under a tree looking discontent, three cups on the ground, a hand offers a fourth", ["tree", "seated figure", "four cups", "hand from cloud"]),
    "5": ("A cloaked figure in grief before three spilled cups, two cups still standing behind", ["cloaked figure", "three spilled cups", "two standing cups", "bridge", "river"]),
    "6": ("Children in a garden with six cups filled with flowers, a nostalgic village scene", ["children", "six cups", "flowers", "village", "garden"]),
    "7": ("A silhouetted figure gazes at seven cups in the clouds, each holding a different vision", ["silhouette", "seven cups", "clouds", "visions", "castle", "jewels", "snake"]),
    "8": ("A figure walks away from eight stacked cups toward mountains under a moon", ["departing figure", "eight cups", "mountains", "moon", "river"]),
    "9": ("A content figure sits with arms crossed before nine golden cups arranged on a curved table", ["seated figure", "nine cups", "curved table", "satisfaction"]),
    "10": ("A joyful family beneath a rainbow of ten cups, a cottage and garden in background", ["family", "ten cups", "rainbow", "cottage", "garden"]),
}
_CUPS_COURT: dict[str, tuple[str, list[str]]] = {
    "Page": ("A young figure in flowing robes gazes at a cup with a fish emerging from it", ["cup", "fish", "flowing robes", "sea"]),
    "Knight": ("A knight on a calm horse holds a cup forward, a river flowing beneath them", ["horse", "cup", "river", "wings on helmet"]),
    "Queen": ("A queen on an ornate throne at the water's edge, holding a elaborate chalice", ["ornate throne", "chalice", "water", "cherubs", "pebbles"]),
    "King": ("A king on a throne amid turbulent seas, holding a cup and scepter", ["throne", "cup", "scepter", "turbulent sea", "ship"]),
}

_SWORDS_PIPS: dict[str, tuple[str, list[str]]] = {
    "1": ("A hand from a cloud grips a gleaming sword, a crown and wreath at its tip", ["hand", "cloud", "sword", "crown", "wreath", "mountains"]),
    "2": ("A blindfolded figure sits balancing two crossed swords, a crescent moon over calm water", ["blindfold", "two swords", "crescent moon", "calm water"]),
    "3": ("A heart pierced by three swords under dark storm clouds, rain falling", ["heart", "three swords", "storm clouds", "rain"]),
    "4": ("A figure lies in repose on a tomb, three swords on the wall and one beneath them", ["tomb", "resting figure", "four swords", "stained glass window"]),
    "5": ("A smirking figure picks up three swords while two defeated figures walk away, stormy sky", ["victor", "five swords", "defeated figures", "stormy sky", "water"]),
    "6": ("A ferryman guides a boat with a woman and child across water, six swords in the bow", ["boat", "ferryman", "woman and child", "six swords", "calm water"]),
    "7": ("A figure sneaks away from a camp carrying five swords, two swords left planted", ["sneaking figure", "seven swords", "camp", "tents"]),
    "8": ("A bound and blindfolded figure surrounded by eight swords stuck in muddy ground", ["bound figure", "blindfold", "eight swords", "muddy ground", "castle"]),
    "9": ("A figure sits up in bed, head in hands in anguish, nine swords on the dark wall behind", ["bed", "anguished figure", "nine swords", "dark wall", "quilt"]),
    "10": ("A figure lies face down with ten swords in their back, a dark sky with a hint of dawn", ["fallen figure", "ten swords", "dark sky", "dawn on horizon"]),
}
_SWORDS_COURT: dict[str, tuple[str, list[str]]] = {
    "Page": ("A youthful figure strides over rough ground holding a sword aloft, windswept clouds", ["sword", "windswept clouds", "rough ground", "birds"]),
    "Knight": ("A knight charges on a galloping horse brandishing a sword, butterflies in the wind", ["galloping horse", "sword", "wind", "butterflies", "storm clouds"]),
    "Queen": ("A queen on a stone throne holds a sword upright, her free hand raised, cloudy sky", ["stone throne", "sword", "raised hand", "clouds", "bird"]),
    "King": ("A stern king on a throne holds a sword, trees bend in a strong wind behind him", ["throne", "sword", "wind-bent trees", "butterflies", "storm clouds"]),
}

_PENTACLES_PIPS: dict[str, tuple[str, list[str]]] = {
    "1": ("A hand from a cloud holds a golden pentacle over a lush garden with an archway", ["hand", "cloud", "golden pentacle", "garden", "archway", "lilies"]),
    "2": ("A juggler dances holding two pentacles in a figure eight, ships on a wavy sea behind", ["juggler", "two pentacles", "infinity loop", "ships", "waves"]),
    "3": ("A stonemason works on a cathedral arch, three pentacles in the design, monks observe", ["stonemason", "three pentacles", "cathedral", "monks", "tools"]),
    "4": ("A figure clutches a pentacle to their chest atop a pile, two under feet, one on crown", ["figure", "four pentacles", "city background", "miserly pose"]),
    "5": ("Two destitute figures trudge through snow past a lit church window with five pentacles", ["two figures", "snow", "five pentacles", "stained glass window", "tattered clothes"]),
    "6": ("A wealthy merchant weighs pentacles on a scale, giving to kneeling figures", ["merchant", "six pentacles", "scale", "kneeling figures", "generosity"]),
    "7": ("A farmer leans on a hoe gazing at a bush bearing seven pentacles, patient waiting", ["farmer", "hoe", "seven pentacles", "bush", "patience"]),
    "8": ("A craftsman carefully carves pentacles at a workbench, a town in the background", ["craftsman", "workbench", "eight pentacles", "tools", "town"]),
    "9": ("A well-dressed figure in a luxurious garden with a falcon, surrounded by nine pentacles", ["garden", "falcon", "nine pentacles", "grapevines", "manor"]),
    "10": ("A multigenerational family under an archway with ten pentacles, dogs at their feet", ["family", "ten pentacles", "archway", "dogs", "estate"]),
}
_PENTACLES_COURT: dict[str, tuple[str, list[str]]] = {
    "Page": ("A studious youth holds up a pentacle, standing in a green field with young trees", ["pentacle", "green field", "young trees", "studious pose"]),
    "Knight": ("A knight on a sturdy, still horse holds a pentacle, a plowed field stretches behind", ["sturdy horse", "pentacle", "plowed field", "patient stance"]),
    "Queen": ("A queen sits on a throne in a flowering garden, cradling a pentacle, a rabbit nearby", ["throne", "pentacle", "flowering garden", "rabbit"]),
    "King": ("A prosperous king on a throne decorated with bull carvings, pentacle on lap, castle grounds", ["throne", "bull carvings", "pentacle", "castle", "grapevines"]),
}

MINOR_ARCANA: list[Card] = (
    _minor_cards("Wands", "wand", _WANDS_COURT, _WANDS_PIPS, start_index=22) +
    _minor_cards("Cups", "cup", _CUPS_COURT, _CUPS_PIPS, start_index=36) +
    _minor_cards("Swords", "sword", _SWORDS_COURT, _SWORDS_PIPS, start_index=50) +
    _minor_cards("Pentacles", "pentacle", _PENTACLES_COURT, _PENTACLES_PIPS, start_index=64)
)

ALL_CARDS: list[Card] = MAJOR_ARCANA + MINOR_ARCANA
# fmt: on


def _sample_cards() -> list[Card]:
    """Return a small representative sample: 5 major, 2 pips + king per suit."""
    cards = MAJOR_ARCANA[:5]
    for suit in ("Wands", "Cups", "Swords", "Pentacles"):
        suit_cards = [c for c in MINOR_ARCANA if c.suit == suit]
        # First two pips (Ace + 2) and the King
        pips = [c for c in suit_cards if "King" not in c.name]
        king = [c for c in suit_cards if "King" in c.name]
        cards.extend(pips[:2])
        cards.extend(king)
    return cards


def _load_cards_from_yaml(yaml_path: Path) -> tuple[list[Card], list[Card]]:
    """Load cards from a YAML file, returning (major_arcana, minor_arcana)."""
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    major = []
    for card_data in data.get("major_arcana", []):
        major.append(Card(
            name=card_data["name"],
            numeral=card_data["numeral"],
            arcana_type="major",
            suit=None,
            description=card_data["description"],
            key_symbols=card_data["key_symbols"],
            composition=card_data.get("composition", ""),
        ))

    # Suit order and start indices for sequential numbering
    suit_start = {"wands": 22, "cups": 36, "swords": 50, "coins": 64, "pentacles": 64}
    minor = []
    for suit_name, suit_data in data.get("minor_arcana", {}).items():
        suit_title = suit_name.title()  # "wands" -> "Wands"
        # Map "coins" -> "Pentacles" for the suit field
        if suit_name.lower() == "coins":
            suit_title = "Pentacles"
        start_index = suit_start.get(suit_name.lower(), 0)
        i = 0
        # Load pips (1-10)
        for num_str, pip_data in suit_data.get("pips", {}).items():
            num = int(num_str)
            name_prefix = "Ace" if num == 1 else str(num)
            name = f"{name_prefix} of {suit_title}"
            numeral = f"{start_index + i:02d}"
            minor.append(Card(
                name=name,
                numeral=numeral,
                arcana_type="minor",
                suit=suit_title,
                description=pip_data["description"],
                key_symbols=pip_data["key_symbols"],
                composition=pip_data.get("composition", ""),
            ))
            i += 1
        # Load court cards
        for rank, court_data in suit_data.get("court", {}).items():
            name = f"{rank} of {suit_title}"
            numeral = f"{start_index + i:02d}"
            minor.append(Card(
                name=name,
                numeral=numeral,
                arcana_type="minor",
                suit=suit_title,
                description=court_data["description"],
                key_symbols=court_data["key_symbols"],
                composition=court_data.get("composition", ""),
            ))
            i += 1

    return major, minor


def get_cards(subset: str = "all", cards_file: Path | None = None) -> list[Card]:
    """Return cards based on subset filter: 'all', 'major', 'minor', or 'sample'.

    If cards_file is provided, loads card definitions from that YAML file.
    Otherwise uses the built-in defaults.
    """
    if cards_file is not None:
        major, minor = _load_cards_from_yaml(cards_file)
        all_cards = major + minor
    else:
        major = MAJOR_ARCANA
        minor = MINOR_ARCANA
        all_cards = ALL_CARDS

    match subset:
        case "all":
            return all_cards
        case "major":
            return major
        case "minor":
            return minor
        case "sample":
            # Build sample from loaded cards
            cards = major[:5]
            for suit in ("Wands", "Cups", "Swords", "Pentacles"):
                suit_cards = [c for c in minor if c.suit == suit]
                pips = [c for c in suit_cards if "King" not in c.name]
                king = [c for c in suit_cards if "King" in c.name]
                cards.extend(pips[:2])
                cards.extend(king)
            return cards
        case _:
            raise ValueError(f"Unknown card subset: {subset!r}. Use 'all', 'major', 'minor', or 'sample'.")


def get_card_by_index(index: int, cards_file: Path | None = None) -> Card:
    """Return the card matching the given index (0-77).

    Looks up by the two-digit numeral (e.g. index 0 → numeral "00").
    """
    all_cards = get_cards("all", cards_file=cards_file)
    numeral = f"{index:02d}"
    for card in all_cards:
        if card.numeral == numeral:
            return card
    raise ValueError(f"No card found with index {index}")
