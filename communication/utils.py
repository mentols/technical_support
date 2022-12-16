from enum import Enum


class Status(Enum):
    R = 'Resolved'
    U = 'Unresolved'
    F = 'Frozen'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    def __str__(self):
        return f'{self.value}'
