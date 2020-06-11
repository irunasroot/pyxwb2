import json
from pathlib import Path, PurePath
from jsonpath2.path import Path as JPath

from . import BaseMixin
from .base import Ship, ShipAbility
from pyxwb2 import manifest

from .exceptions import PilotsMissingException


class Pilot(BaseMixin):
    def __init__(self):
        self._skip_attr = ["vendor"]

    @classmethod
    def load_data(cls, data):
        obj = cls()
        try:
            for k, v in data["pilot"][0].items():
                if k in obj._skip_attr:
                    continue
                obj.__setattr__(k, v)
        except IndexError:
            pass

        if "shipAbility" in data["pilot"]:
            obj.__setattr__("ship_ability", ShipAbility.load_data(data["pilot"]["shipAbility"]))

        obj.__setattr__("ship", Ship.load_data({"ship": data["ship"],
                                                "faction": data["faction"]}))

        return obj


class Pilots(BaseMixin):
    def __init__(self):
        # self.__setattr__("pilots", list())
        self.pilots = list()

    def __repr__(self):
        return f"Pilots({[p for p in self.pilots]})"

    def __len__(self):
        return len(self.pilots)

    def __iter__(self):
        return iter(self.pilots)

    def __getitem__(self, item):
        return self.pilots[item]

    def __contains__(self, item):
        all_names = [p.xws for p in self.pilots] + [p.name for p in self.pilots]

        if isinstance(item, Pilot):
            for pilot in self.pilots:
                if pilot.xws in all_names or pilot.name in all_names:
                    return True
            return False

        return item in all_names

    @classmethod
    def load_data(cls, pilots, faction):
        """
        Create a list of pilot objects loaded from xwing-data.

        This object allows quick searching for pilots that were loaded in. It will also allow you to search
        using a pilot object. This particular search doesn't compare any kind of equality of the Pilot object
        but instead will use the Pilot object and search if the same pilot is contained in Pilots
        e.g. 'bladesquadronveteran' in Pilots
        or   'Blade Squadron Veteran' in Pilots
        or   my_pilot in Pilots

        :param pilots: Pass in a list of pilots to load in following the xws spec
        :param faction: Pass in the loaded Faction object, doing this allows for referencing the same faction object
                        in other attached objects. e.g. Ship.faction would reference the same faction object
        :return: Loaded Pilots object
        """
        obj = cls()
        jpath_ship = JPath.parse_str(f"$.pilots..[?(@.faction=\"{faction.xws}\")].ships.*")
        manifest_ship_files = [m.current_value for m in jpath_ship.match(manifest)]

        for pilot in pilots:
            pilot_xws, ship_xws, *_ = pilot["id"].split("-")
            for file in manifest_ship_files:
                ship_name_of_file = "".join(PurePath(file).stem.split("-"))
                if ship_xws == ship_name_of_file:
                    ship_file = PurePath(Path(__file__).parents[1], file).as_posix()
                    with open(ship_file, "r") as f:
                        manifest_ship = json.load(f)
                        jpath_pilot = JPath.parse_str(f"$.pilots..[?(@.xws=\"{pilot_xws}\")]")
                        manifest_pilots = [m.current_value for m in jpath_pilot.match(manifest_ship)]
                        pilot = Pilot.load_data({"pilot": manifest_pilots,
                                                 "ship": manifest_ship,
                                                 "faction": faction})
                        obj.pilots.append(pilot)

        if not len(obj):
            raise PilotsMissingException("Found no valid pilots, be sure you have valid pilots "
                                         "or the xws spec is at least version 2.0.0")
        return obj
