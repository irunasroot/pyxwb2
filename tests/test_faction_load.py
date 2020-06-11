import unittest

from pyxwb2.models.base import Faction
from pyxwb2.models.exceptions import FactionMissingException


class TestFactionLoad(unittest.TestCase):

    def setUp(self):
        self.known_faction = "scumandvillainy"
        self.unknown_faction = "lukeskywalkerisababy"
        self.uncanonical_known = "Rebel Alliance"

    def test_known_faction(self):
        faction = Faction.load_data(self.known_faction)

        self.assertEqual(faction.xws, self.known_faction)

    def test_unknown_faction(self):
        with self.assertRaises(FactionMissingException):
            _ = Faction.load_data(self.unknown_faction)

    def test_faction_class_type(self):
        # Lets make sure we're actually getting a faction class back

        faction = Faction.load_data(self.known_faction)

        self.assertIsInstance(faction, Faction)

    def test_faction_uncanonical_name(self):
        _ = Faction.load_data(self.uncanonical_known)


if __name__ == "__main__":
    unittest.main()
