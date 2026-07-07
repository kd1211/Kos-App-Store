import os
from PIL import Image

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(APP_DIR, "assets")

SYMBOL_NAMES = ["cherry", "lemon", "bell", "bar", "seven", "diamond"]

_cache = {}


def load_symbol(name, size=56):
    key = (name, size)
    if key in _cache:
        return _cache[key]
    path = os.path.join(ASSETS_DIR, name + ".png")
    img = Image.open(path).convert("RGBA")
    if img.size != (size, size):
        img = img.resize((size, size), Image.LANCZOS)
    _cache[key] = img
    return img


def pick_symbols(count=3):
    import random
    return [random.choice(SYMBOL_NAMES) for _ in range(count)]
