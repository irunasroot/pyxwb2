import json
from pathlib import Path, PurePath

manifest_file = PurePath(Path(__file__).parents[0], "data/manifest.json").as_posix()
with open(manifest_file, "r") as f:
    manifest = json.load(f)

bearing_conversion_file = PurePath(Path(__file__).parents[0], "data/dial-maneuvers-conversion.json").as_posix()
with open(bearing_conversion_file) as f:
    manifest["maneuvers"] = json.load(f)
