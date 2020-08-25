from . import LoadDataMixin, ReperMixin, BaseItemListMixin, SearchableItemMixin
from pyxwb2.utils import manifest


class ShipAbility(LoadDataMixin, ReperMixin):
    pass


class Upgrade(LoadDataMixin, ReperMixin):
    pass


class Upgrades(BaseItemListMixin):
    __singular__ = Upgrade


class DamageCard(LoadDataMixin, ReperMixin):
    pass


class DamageDeck(BaseItemListMixin):
    __singular__ = DamageCard


class Condition(LoadDataMixin, ReperMixin):
    pass


class Conditions(BaseItemListMixin):
    __singular__ = Condition


class ShipStat(LoadDataMixin, ReperMixin):
    pass


class ShipStats(BaseItemListMixin):
    __singular__ = ShipStat


class Action(LoadDataMixin, ReperMixin):
    pass


class Actions(BaseItemListMixin):
    __singular__ = Action


class Maneuver(ReperMixin):
    def __iter__(self):
        return iter(self.__dict__.keys())

    @classmethod
    def load_data(cls, maneuver):
        """
        A single maneuver on a ship's dial

        :param maneuver: 3 character maneuver following xwing-data2 data set which is encoded to match
                        the vassal league nomenclature
        :return: Initialized Maneuver class
        """
        obj = cls()
        speed, direction, difficulty = list(maneuver)
        obj.__setattr__("name", manifest["maneuvers"]["maneuvers"][direction]["name"])
        obj.__setattr__("speed", int(speed))
        obj.__setattr__("difficulty", manifest["maneuvers"]["difficulty"][difficulty]["name"])
        obj.__setattr__("direction", manifest["maneuvers"]["maneuvers"][direction]["direction"])
        obj.__setattr__("vassal", maneuver)

        return obj


class ShipDial(SearchableItemMixin):
    """
    The ship's dial containing all of the possible maneuvers the ship can perform. The returned object
    is a ShipDial with as a list of Maneuver objects.

    This object allows searching a keyword to return a smaller subset of items with that keyword
    e.g. ShipDial['red'] would return a ShipDial object of all maneuvers that have a difficulty of red
         ShipDial['left'] would return a ShipDial object of all maneuvers that have a direction of turn left
         ShipDial['2'] would return a ShipDial object of all maneuvers that speed of 2

    You can also do multi-searches
    e.g. ShipDial['1']['blue'] would return a ShipDial object of all blue difficulty maneuvers with a speed of 1

    However, the object still allows for getting a maneuver at a specific index.
    e.g. ShipDial[1] returns a single maneuver object at the index
    """
    def __init__(self):
        self._items = list()

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"ShipDial({[m for m in self._items][:5]}{' ...' if len(self._items) > 5 else ''})"

    @classmethod
    def load_data(cls, dial):
        obj = cls()
        for maneuver in dial:
            obj._items.append(Maneuver.load_data(maneuver))

        return obj
