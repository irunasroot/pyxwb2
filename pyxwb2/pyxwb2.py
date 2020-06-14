import json

from .models.base import Faction
from .models.pilot import Pilots


class XwingSquadron:

    def __init__(self, trust_source=False):
        self.trust_source = trust_source

        # Optional attributes
        self.name = None
        self.description = None
        self.obstacles = None
        self.points = None
        self.vendor = None

    def import_squad(self, xws):
        """
        Import the xws data to validate the squad

        :param xws: Importing data from either an already imported json file, or pass
                    in a string of the json file to process. This will populate the already
                    initialized Xwb object.
        :return: None
        """

        if isinstance(xws, str):
            with open(xws, "r") as xws_file:
                _xws_data = json.load(xws_file)
        elif isinstance(xws, dict):
            _xws_data = xws
        else:
            raise ValueError("Unable to load data set. Be sure to pass in a string of the filename or"
                             "an already loaded dict from the xws json file.")

        self.version = _xws_data.get("version")
        self.name = _xws_data.get("name")
        self.description = _xws_data.get("description")

        self.faction = Faction.load_data(_xws_data.get("faction"))
        self.pilots = Pilots.load_data(_xws_data.get("pilots"), self.faction)
