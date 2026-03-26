SYNONYMS = {
    "tshirt": "t-shirt",
    "tee": "t-shirt",
    "t shirt": "t-shirt",

    "jeans": "jeans",
    "denim": "jeans",

    "joggers": "joggers",
}

COLOR_MAP = {
    "navy": "blue",
    "sky blue": "blue",
    "light blue": "blue",

    "maroon": "red",
    "wine": "red",

    "beige": "cream",
}

NOISE_WORDS = [
    "cool", "nice", "trendy", "best", "good", "awesome"
]


def normalize_query(parsed: dict):
    normalized = {}

    for key, value in parsed.items():
        if not value:
            continue

        value = value.lower().strip()

        # remove noise
        if value in NOISE_WORDS:
            continue

        # synonym mapping
        if value in SYNONYMS:
            value = SYNONYMS[value]

        # color normalization
        if key == "color" and value in COLOR_MAP:
            value = COLOR_MAP[value]

        normalized[key] = value

    return normalized


def clean_query(query: str):
    words = query.lower().split()
    return " ".join([w for w in words if w not in NOISE_WORDS])