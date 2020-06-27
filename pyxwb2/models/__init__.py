class LoadDataMixin:
    @classmethod
    def load_data(cls, data):
        obj = cls()
        for k, v in data.items():
            obj.__setattr__(k, v)
        return obj


class BaseItemListMixin:
    def __init__(self, _singular=None):
        self._items = list()

        if _singular:
            self._singular = _singular

    def __len__(self):
        return len(self._items)

    def __getitem__(self, item):
        return self._items[item]

    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        return f"{self.__class__.__name__}({[f for f in self._items]})"

    def append(self, item, _singular=None):
        if isinstance(item, self._singular):
            self._items.append(item)

    @classmethod
    def load_data(cls, data):
        obj = cls()
        for action in data:
            obj._items.append(obj._singular.load_data(action))
        return obj


class ReperMixin:
    def __repr__(self):
        def encap_quotes(value):
            if type(value) == str:
                return f"'{value}'"
            return value

        all_attrs = ", ".join([f"{k}={encap_quotes(v)}" for k, v in self.__dict__.items() if not k.startswith('_')])
        return f"{self.__class__.__name__}({all_attrs})"