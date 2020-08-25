class LoadDataMixin:
    @classmethod
    def load_data(cls, data):
        obj = cls()
        for k, v in data.items():
            obj.__setattr__(k, v)
        return obj


class BaseItemListMixin:
    def __init__(self, singular=None):
        self._items = list()

        if singular:
            self.__singular__ = singular

    def __len__(self):
        return len(self._items)

    def __getitem__(self, item):
        return self._items[item]

    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        return f"{self.__class__.__name__}({[f for f in self._items]})"

    def append(self, item):
        if isinstance(item, self.__singular__):
            self._items.append(item)

    @classmethod
    def load_data(cls, data):
        obj = cls()
        for action in data:
            obj._items.append(obj.__singular__.load_data(action))
        return obj


class ReperMixin:
    def __repr__(self):
        def encap_quotes(value):
            if type(value) == str:
                return f"'{value}'"
            return value

        all_attrs = ", ".join([f"{k}={encap_quotes(v)}" for k, v in self.__dict__.items() if not k.startswith('_')])
        return f"{self.__class__.__name__}({all_attrs})"


class SearchableItemMixin:
    _items = list()

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._items[item]
        elif isinstance(item, str):
            _tmp = self.__class__()
            for maneuver in self._items:
                for c in maneuver:
                    if item.lower() in str(getattr(maneuver, c)).lower():
                        _tmp._items.append(maneuver)
            return _tmp
