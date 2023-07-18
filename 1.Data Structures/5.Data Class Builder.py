""" three
different class builders that you may use as shortcuts to write data classes:
collections.namedtuple
The simplest way—available since Python 2.6.
typing.NamedTuple
An alternative that requires type hints on the fields—since Python 3.5, with
class syntax added in 3.6.
@dataclasses.dataclass
A class decorator that allows more customization than previous alternatives,
adding lots of options and potential complexity—since Python 3.7.
"""
from collections import namedtuple
import json

Coordinate = namedtuple('Coordinate', 'lat lon')
print(issubclass(Coordinate, tuple))
moscow = Coordinate(55.756, 37.617)
print(moscow)

import typing

Coordinate = typing.NamedTuple('Coordinate',
                               [('lat', float), ('lon', float)])
print(issubclass(Coordinate, tuple))

class Coordinate(typing.NamedTuple):
    lat: float
    lon: float
    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'


from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float
    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'


# Classic Named Tuples
City = namedtuple('City', 'name country population coordinates')
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
print(f"{tokyo}\n{tokyo.population}\t{tokyo.coordinates}")
print(tokyo[1])

# _fields
print(City._fields)

# _make
Coordinate = namedtuple('Coordinate', 'lat lon')
delhi_data = ('Delhi NCR', 'IN', 21.935, Coordinate(28.613889, 77.208889))
delhi = City._make(delhi_data)
print(delhi)

# _asdict()
print(delhi._asdict())

# JSON
json_obj = json.dumps(delhi._asdict())
print(json_obj)

# default
Coordinate = namedtuple('Coordinate', 'lat lon reference', defaults=['WGS84'])
print(Coordinate(0, 0))
print(Coordinate._field_defaults)

# Typed Named Tuples
class Coordinate(typing.NamedTuple):
    lat: float
    lon: float
    reference: str = 'WGS84'

print(Coordinate.__annotations__)

class DemoNTClass(typing.NamedTuple):
    a: int
    b: float = 1.1
    c = "spam"
print(DemoNTClass.__annotations__)
print(DemoNTClass.__doc__)
print(f"{DemoNTClass.a}\t{DemoNTClass.b}\t{DemoNTClass.c}")

nt = DemoNTClass(8)
print(f"{nt.a}\t{nt.b}\t{nt.c}")

# Inspecting a class decorated with dataclass
# DemoDataClass instances are mutable
@dataclass
class DemoDataClass:
    a: int
    b: float = 1.1
    c = "spam"
dc = DemoDataClass(9)
dc.a = 11.1
dc.z = 12

from dataclasses import field
@dataclass
class ClubMember:
    name: str
    guests: list = field(default_factory=list)

# more precise
@dataclass
class ClubMember:
    name: str
    guests: list[str] = field(default_factory=list)
cc = ClubMember('a', ['a'])
print(cc)

@dataclass
class ClubMember:
    name: str
    guests: list = field(default_factory=list)
    athlete: bool = field(default=False, repr=False)
cc = ClubMember('a', ['a'], False)
print(cc)

# Post-init Processing
"""
Common use cases for __post_init__ are validation and computing
field values based on other fields.
"""
@dataclass
class HackerClubMember(ClubMember):
    all_handles = set()
    handle: str = ''
    def __post_init__(self):
        cls = self.__class__
        if self.handle == '':
            self.handle = self.name.split()[0]
        if self.handle in cls.all_handles:
            msg = f"hanle {self.handle!r} already exists."
            raise ValueError(msg)
        cls.all_handles.add(self.handle)

from dataclasses import dataclass, field, fields
from typing import Optional
from enum import Enum, auto
from datetime import date

class ResourceType(Enum):
    BOOK = auto()
    EBOOK = auto()
    VIDEO = auto()

@dataclass
class Resource:
    """Media resource description."""
    identifier: str
    title: str = "<untitled>"
    creators: list[str] = field(default_factory=list)
    date: Optional[date] = None
    type: ResourceType = ResourceType.BOOK
    description: str = ''
    language: str = ''
    subjects: list[str] = field(default_factory=list)

    def __repr__(self):
        cls = self.__class__
        cls_name = cls.__name__
        indent = ' ' * 4
        res = [f"{cls_name}("]
        for f in fields(cls):
            value = getattr(self, f.name)
            res.append(f"{indent}{f.name} = {value!r},")
        res.append(')')
        return '\n'.join(res)

# instance
book = Resource(
    "978-0-13-475759-9", "Refactoring, 2nd Edition",
    ['Martin Fowler', 'Kent Beck'], date(2018, 11, 19),
    ResourceType.BOOK, "Improving the design of existing code",
    "EN", ['computer programming', 'OOP']
)
print(book)
