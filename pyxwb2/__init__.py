import json

from pathlib import Path, PurePath

__version__ = "0.0.1a"

manifest_file = PurePath(Path(__file__).parents[0], "data/manifest.json").as_posix()
with open(manifest_file, "r") as f:
    manifest = json.load(f)
