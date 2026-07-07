# Kos-App-Store

App Store catalog for [PiOS / Kos](https://github.com/kd1211/Kos).

## `apps.json`

Each entry describes one installable app.

### Single-file app

```json
{
  "name": "Dice Roller",
  "class_name": "DiceApp",
  "icon": "\u2680",
  "description": "Roll a virtual 6-sided dice.",
  "file": "dice_app.py"
}
```

### Folder package (images + extra modules)

```json
{
  "name": "Slots",
  "class_name": "SlotsApp",
  "icon": "\U0001F3B0",
  "description": "Spin the reels and win coins.",
  "folder": "slots",
  "file": "slots_app.py"
}
```

- `folder` — directory in this repo; the whole tree is installed to `apps/installed/<folder>/` on the Pi.
- `file` — main Python module inside that folder (must define an `App` subclass).
- `files` (optional) — explicit list of repo paths to download instead of using the GitHub API to list the folder.

Helper modules and assets live beside the main file, e.g.:

```
slots/
  slots_app.py
  symbols.py
  assets/
    cherry.png
    lemon.png
    ...
```

Load assets relative to the app folder:

```python
APP_DIR = os.path.dirname(os.path.abspath(__file__))
img = Image.open(os.path.join(APP_DIR, "assets", "cherry.png"))
```

## Publishing

1. Add or update the app under this repo.
2. Add an entry to `apps.json`.
3. Push to `main` — PiOS pulls from raw GitHub on install.
