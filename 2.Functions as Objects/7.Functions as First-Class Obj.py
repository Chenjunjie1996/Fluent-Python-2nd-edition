"""
Functions in Python are first-class objects. Programming language researchers define
a “first-class object” as a program entity that can be:
• Created at runtime
• Assigned to a variable or element in a data structure
• Passed as an argument to a function
• Returned as the result of a function
"""
import random
import unicodedata
from operator import itemgetter, attrgetter, methodcaller, mul
from collections import namedtuple
from functools import partial

# Treating a Function Like an Object
def factorial(n):
    """return n!"""
    return 1 if n < 2 else n * factorial(n - 1)

print(factorial.__doc__)

# Higher-Order Functions
sorted(['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana'], key=len)

def reverse(word):
    return word[::-1]
sorted(['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana'], key=reverse)

# Modern Replacements for map, filter, and reduce
[factorial(n) for n in range(6)]
[factorial(n) for n in range(6) if n % 2]

# Anonymous Functions
sorted(['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana'], key=lambda word: word[::-1])

# User-Defined Callable Types
class BingoCage:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError("pick from empty BingoCage")

    def __call__(self):
        return self.pick()

bingo = BingoCage(range(3))
bingo.pick()
bingo()
callable(bingo)

# From Positional to Keyword-Only Parameters
def tag(name, *content, class_=None, **attrs):
    """Generate one or more HTML tags"""
    if class_ is not None:
        attrs["class"] = class_
    attr_pairs = (f' {attr}={value}' for attr, value
                  in sorted(attrs.items()))
    attr_str = ''.join(attr_pairs)
    if content:
        elements = (f'<{name}{attr_str}>{c}</{name}>'
                    for c in content)
        return '\n'.join(elements)
    else:
        return f'<{name}{attr_str} />'

print(tag("br"))
print(tag('p', "hello"))
print(tag('p', "hello", "world"))
print(tag('p', "hello", id=33))
print(tag('p', "hello", "world", class_="sidebar"))
print(tag(content="testing", name="img"))
my_tag = {"name": "img", "title": "Sunset Boulevard",
          "src": "sunset.jpg", "class": "framed"}
print(tag(my_tag))

# Positional-Only Parameters
def divmod(a, b, /):
    return (a // b, a % b)

# All arguments to the left of the / are positional-only. After the /, you may specify
# other arguments, which work as usual.
def tag(name, /, *content, class_=None, **attrs):
    pass

# The operator Module
metro_data = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]
for city in sorted(metro_data, key=itemgetter(1)):
    print(city)

cc_name = itemgetter(1, 0)
for city in metro_data:
    print(cc_name(city))

LatLon = namedtuple("LatLon", "lat lon")
Metropolis = namedtuple("Metropolis", "name cc pop coord")
metro_areas = [Metropolis(name, cc, pop, LatLon(lat, lon))
               for name, cc, pop, (lat, lon) in metro_data]
print(metro_areas[0])
print(metro_areas[0].coord.lat)

name_lat = attrgetter("name", "coord.lat")
for city in sorted(metro_areas, key=attrgetter("coord.lat")):
    print(name_lat(city))

s = "The time has come"
upcase = methodcaller("upper")
print(upcase(s))

hyphenate = methodcaller("replace", ' ', '-')
print(hyphenate(s))

# Freezing Arguments with functools.partial
triple = partial(mul, 3)
print(triple(7))
print([triple(i) for i in range(1,10)])

nfc = partial(unicodedata.normalize, "NFC")
s1 = 'café'
s2 = 'cafe\u0301'
print(s1 == s2)
print(nfc(s1) == nfc(s2))

