class LoadDataMixin:
    @classmethod
    def load_data(cls, data):
        obj = cls()
        for k, v in data.items():
            obj.__setattr__(k, v)
        return obj


class BaseItemListMixin:
    def __init__(self):
        self._items = list()

    def __len__(self):
        return len(self._items)

    def __getitem__(self, item):
        return self._items[item]

    def __iter__(self):
        return iter(self.__dict__.keys())


class ReperMixin:
    def __repr__(self):
        def encap_quotes(value):
            if type(value) == str:
                return f"'{value}'"
            return value

        all_attrs = ", ".join([f"{k}={encap_quotes(v)}" for k, v in self.__dict__.items() if not k.startswith('_')])
        return f"{self.__class__.__name__}({all_attrs})"