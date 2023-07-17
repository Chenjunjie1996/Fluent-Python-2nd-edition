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