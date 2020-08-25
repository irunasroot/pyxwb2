import unittest

from pyxwb2.models.pilot import Pilots
from pyxwb2.models.base import Faction
from pyxwb2.models.misc import ShipDial, Maneuver
from pyxwb2.models.exceptions import PilotsMissingException


class TestPilotLoad(unittest.TestCase):

    def setUp(self):
        self.pilots_known = [
            {
                "id": "bladesquadronveteran",
                "upgrades": {
                    "title": ["awingtestpilot"],
                    "missile": ["chardaanrefit"],
                    "ept": ["pushthelimit", "experthandling"],
                    "mod": ["experimentalinterface"]
                },
                "vendor": {
                    "voidstate": {
                        "pilot_id": 30
                    }
                }
            }
        ]
        self.pilots_known1 = [
            {
                "id": "zeborrelios",
            }
        ]
        self.pilots_unknown = [
            {
                "id": "unknownpilot-unknownship",
                "upgrades": {
                    "missile": ["chardaanrefit"],
                    "ept": ["elusiveness", "experthandling"],
                    "somewrongupgradeslot": ["stealthdevice"]
                },
                "vendor": {
                    "voidstate": {
                        "pilot_id": 33
                    }
                }
            }
        ]

        self.faction = Faction.load_data("rebelalliance")
        self.pilots1_known = Pilots.load_data(self.pilots_known, self.faction)
        self.pilots2_known = Pilots.load_data(self.pilots_known, self.faction)
        self.pilots3_known = Pilots.load_data(self.pilots_known1, self.faction)

    def test_known_pilot(self):
        self.assertGreater(len(self.pilots1_known), 0)

    def test_conains_methods(self):
        """
        The Pilots object allows searching the list of pilots by name, xws, or even another Pilot object.
        We need to be sure all three of these types of checks can work
        """

        self.assertIn("bladesquadronveteran", self.pilots1_known)
        self.assertIn("Blade Squadron Veteran", self.pilots2_known)

    def test_subscriptable_known_pilot(self):
        _ = self.pilots1_known[0]

    def test_unknown_pilot(self):
        """
        The XWS spec calls for pilots to be required, so if none loaded we need to error out.
        """

        with self.assertRaises(PilotsMissingException):
            self.pilots1_unknown = Pilots.load_data(self.pilots_unknown, self.faction)

    def test_ship_ability(self):
        self.assertIn("ship_ability", self.pilots3_known[0])

    def test_search_ship_dial(self):
        self.assertIsInstance(self.pilots1_known[0].ship.dial["1"], ShipDial)
        self.assertIsInstance(self.pilots1_known[0].ship.dial[1], Maneuver)


if __name__ == "__main__":
    unittest.main()
