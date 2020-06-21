from pathlib import Path, PurePath
from jsonpath2.path import Path as JPath
import json

from . import BaseItemListMixin, ReperMixin
from .misc import ShipDial
from pyxwb2.utils import manifest

from .exceptions import FactionMissingException


class Factions(BaseItemListMixin):
    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        return f"Factions({[f for f in self._items]})"

    def __contains__(self, item):
        all_names = [p.xws for p in self._items] + [p.name for p in self._items]
        return item in all_names

    def append(self, faction):
        if isinstance(faction, Faction):
            self._items.append(faction)

    @classmethod
    def load_data(cls, factions):
        obj = cls()

        for faction in factions:
            obj._items.add(Faction.load_data(faction))

        return obj


class Faction:
    def __init__(self):
        self.name = None
        self.xws = None
        self.ffg = None

    def __repr__(self):
        return f"Faction(name='{self.name}', xws='{self.xws}'"

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


class Ships(BaseItemListMixin, ReperMixin):
    def append(self, ship):
        if isinstance(ship, Ship):
            self._items.append(ship)


class Ship:
    def __init__(self):
        self._skip_attr = ["pilots", "actions, dial"]
        self.name = None
        self.xws = None
        self.size = None
        self.faction = None

    def __repr__(self):
        return f"Ship(name='{self.name}', xws='{self.xws}', size='{self.size}', faction={self.faction})"

    @classmethod
    def load_data(cls, ship_data):
        obj = cls()
        for k, v in ship_data.items():
            if k in obj._skip_attr:
                continue
            obj.__setattr__(k, v)
        obj.__setattr__("dial", ShipDial.load_data(ship_data["dial"]))

        return obj


class Upgrade:
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
