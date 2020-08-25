import json
from pathlib import Path, PurePath
from jsonpath2.path import Path as JPath

from pyxwb2.utils import manifest

from . import ReperMixin, BaseItemListMixin
from .base import Ship
from .misc import ShipAbility
from .exceptions import PilotsMissingException


class Pilot(ReperMixin):
    def __init__(self):
        self._skip_attr = ["vendor", "alt", "shipAbility"]

    def __contains__(self, item):
        return item in self.__dict__

    @classmethod
    def load_data(cls, pilot_data):
        obj = cls()
        try:
            for k, v in pilot_data.items():
                if k in obj._skip_attr:
                    continue
                obj.__setattr__(k, v)

                if "shipAbility" in pilot_data:
                    obj.__setattr__("ship_ability", ShipAbility.load_data(pilot_data["shipAbility"]))
        except IndexError:
            pass

        return obj


class Pilots(BaseItemListMixin, ReperMixin):
    __singular__ = Pilot

    def __getitem__(self, item):
        return self._items[item]

    def __contains__(self, item):
        all_names = [p.xws for p in self._items] + [p.name for p in self._items]

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

        :param pilots: Pass in a list of pilots to process. The list should be the direct list of pilots in
                       accordance with the xws spec
        :param faction: Pass in the processed Faction object.
        :return: Processed Pilots object with all incoming pilots attached
        """
        obj = cls()
        jpath_ship = JPath.parse_str(f"$.pilots..[?(@.faction=\"{faction.xws}\")].ships.*")
        manifest_ship_files = [m.current_value for m in jpath_ship.match(manifest)]

        for pilot in pilots:
            pilot_xws = pilot.get("id")
            for file in manifest_ship_files:
                manifest_ship_fn = PurePath(Path(__file__).parents[1], file).as_posix()
                with open(manifest_ship_fn, "r") as f:
                    ship_file_data = json.load(f)
                jpath_pilot = JPath.parse_str(f"$.pilots..[?(@.xws=\"{pilot_xws}\")]")
                pilot_file_data = [m.current_value for m in jpath_pilot.match(ship_file_data)]
                if not pilot_file_data:
                    continue

                _ship = Ship.load_data(ship_file_data)
                _ship.faction = faction
                _pilot = Pilot.load_data(pilot_file_data[0])
                _pilot.__setattr__("ship", _ship)
                _pilot.__setattr__("faction", faction)
                obj._items.append(_pilot)

        if not len(obj):
            raise PilotsMissingException("Found no valid pilots, be sure you have valid pilots "
                                         "or the xws spec is at least version 2.0.0")
        return obj
