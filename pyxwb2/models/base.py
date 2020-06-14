from pathlib import Path, PurePath
from jsonpath2.path import Path as JPath
import json

from . import BaseMixin, LoadDataMixin
from pyxwb2 import manifest

from .exceptions import FactionMissingException


class Faction(BaseMixin):
    def __init__(self):
        self.name = None
        self.xws = None
        self.ffg = None

    @classmethod
    def load_data(cls, faction_name):
        """
        Create a Faction object by passing in the faction name. This can be either the XWS spec name or,
        the actual name of the faction
        e.g. faction_name = 'rebelalliance'
             faction_name = 'Rebel Alliance'

        :param faction_name: String value of the faction
        :return:
        """
        obj = cls()
        for file in manifest["factions"]:
            filepath = PurePath(Path(__file__).parents[1], file).as_posix()
            with open(filepath, "r") as f:
                factions = json.load(f)

            jpath = JPath.parse_str(f"$..[?(@.xws=\"{faction_name}\"or@.name=\"{faction_name}\")]")
            faction = [m.current_value for m in jpath.match(factions)]

            if not len(faction):
                raise FactionMissingException("Found no valid faction, be sure you have a valid faction "
                                              "or the xws spec is at least version 2.0.0")

            for k, v in faction[0].items():
                obj.__setattr__(k, v)

        return obj

    # def __repr__(self):
    #     return f"Faction(name='{self.name}', xws='{self.xws}', ffg={self.ffg})"


class Ship:
    def __init__(self):
        self._skip_attr = ["pilots", "actions"]

    @classmethod
    def load_data(cls, ship_data):
        obj = cls()
        for k, v in ship_data.items():
            if k in obj._skip_attr:
                continue
            obj.__setattr__(k, v)

        return obj


class Upgrade:
    pass


class ShipDial:
    pass


class ShipArc:
    pass


class ShipStat:
    pass

class Action:
    pass


class Conditions:
    pass


class Damage:
    pass
