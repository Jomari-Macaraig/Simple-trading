from enum import Enum

class BaseEnum(Enum):

    @classmethod
    def raw_list(cls):
        return list(map(lambda c: c, cls))

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list_name(cls):
        return list(map(lambda c: c.name, cls))

    @classmethod
    def dict(cls):
        return dict(map(lambda c: (c.name, c.value), cls))