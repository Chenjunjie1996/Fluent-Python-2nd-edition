"""
• Modern syntax to build and handle dicts and mappings, including enhanced
unpacking and pattern matching
• Common methods of mapping types
• Special handling for missing keys
• Variations of dict in the standard library
• The set and frozenset types
• Implications of hash tables in the behavior of sets and dictionaries
"""

# Unpacking Mappings
import collections

import pandas as pd

print({'a': 0, **{'x': 1}, 'y': 2})

# Merging Mappings with |
d1, d2 = {'a': 1, 'b': 2}, {'b': 4, 'c': 5}
print(d1 | d2)


# Pattern Matching with Mappings
def get_creators(record: dict) -> list:
    match record:
        case {'type': 'book', 'api': 2, 'authors': [*names]}:
            return names
        case {'type': 'book', 'api': 1, 'author': name}:
            return [name]
        case {'type': 'book'}:
            raise ValueError(f"Invalid 'book' record: {record!r}")
        case {'type': 'movie', 'director': name}:
            return [name]
        case _:
            raise ValueError(f'Invalid record: {record!r}')


from collections import OrderedDict

b1 = dict(api=1, author='Douglas Hofstadter', type='book', title='Gödel, Escher, Bach')
print(get_creators(b1))
b2 = OrderedDict(api=2, type='book', title='Python in a Nutshell', authors='Martelli Ravenscroft Holden'.split())
print(get_creators(b2))

food = dict(category='ice cream', flavor='vanilla', cost=199)
match food:
    case {'category': 'ice cream', **details}:
        print(f"Ice cream details: {details}")

# Standard API of Mapping Types
from collections import abc

my_dict = {}
print(isinstance(my_dict, abc.Mapping))
print(isinstance(my_dict, abc.MutableMapping))

# Variations of dict
from collections import OrderedDict

c = OrderedDict(a=1, b=2)
c.move_to_end('a')
c.popitem()
print(c)

from collections import ChainMap

d1 = dict(a=1, b=3)
d2 = dict(a=2, b=4, c=6)
d3 = dict(a=3, b=5, c=5)
chain = ChainMap(d1, d2, d3)
print(chain['a'], chain['b'], chain['c'])
chain['c'] = -1
print(d1)

from collections import Counter

ct = Counter('abracadabra')
ct.update('aaaaazzz')
print(ct.most_common(3))

# subclass UserDict
"""
It’s better to create a new mapping type by extending 
collections.UserDict rather than dict
"""
from collections import UserDict


class StrKeyDict(UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, value):
        self.data[str(key)] = value


# Set
"""
{1, 2, 3} is both faster and more readable than calling the
constructor (e.g., set([1, 2, 3]))
"""

