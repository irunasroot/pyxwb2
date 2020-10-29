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

    def test_points_cost(self):
        squad = XwingSquadron(trust_source=True)
        with open(local_dir.joinpath("files/sample_xws.json"), "r") as f:
            squad.import_squad(json.load(f))
        self.assertEqual(squad.pilots[0].points, 46)
        self.assertEqual(squad.points, 80)

    def test_export(self):
        squad = XwingSquadron(trust_source=True)
        with open(local_dir.joinpath("files/sample_xws.json"), "r") as f:
            sample_xws = json.load(f)
            squad.import_squad(sample_xws)
            exported_xws = squad.export_squad(as_dict=True)

        self.assertEqual(sample_xws["faction"], exported_xws["faction"])
        self.assertEqual(sample_xws["points"], exported_xws["points"])
        self.assertEqual(sample_xws["version"], exported_xws["version"])
        self.assertEqual(len(sample_xws["pilots"]), len(exported_xws["pilots"]))

        # print(exported_xws)

        for sp, ep in zip(sample_xws["pilots"], exported_xws["pilots"]):
            self.assertEqual(sp["id"], ep["id"])
            self.assertEqual(sp["points"], ep["points"])
            self.assertEqual(sp["upgrades"], ep["upgrades"])


if __name__ == "__main__":
    unittest.main()
