import unittest
import json

from pathlib import Path

from pyxwb2 import XwingSquadron
from jsonschema.exceptions import ValidationError


local_dir = Path(__file__).parent


class TestFullXwsImport(unittest.TestCase):
    def test_schema_validation_trusted(self):
        squad = XwingSquadron(trust_source=True)
        with open(local_dir.joinpath("files/sample_xws.json"), "r") as f:
            squad.import_squad(json.load(f))

    def test_schema_validation_invalid(self):
        squad = XwingSquadron()
        with self.assertRaises(ValidationError):
            with open(local_dir.joinpath("files/sample_invalid_xws_schema.json"), "r") as f:
                squad.import_squad(json.load(f))


if __name__ == "__main__":
    unittest.main()
