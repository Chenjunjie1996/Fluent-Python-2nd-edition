"""
• Basic sequence protocol: __len__ and __getitem__
• Safe representation of instances with many items
• Proper slicing support, producing new Vector instances
• Aggregate hashing, taking into account every contained element value
• Custom formatting language extension
"""
from itertools import zip_longest
from array import array
import itertools
import reprlib
import math
import collections
import functools
import operator

# Vector Take #1: Vector2d Compatible
class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return f'Vector({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(*self)

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

print(Vector([3.1, 4.2]))
print(Vector([3, 4, 5]))
print(Vector(range(10)))

# Protocols and Duck typing
Card = collections.namedtuple("Card", ["rank", "suit"])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11) ]+ list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

# Vector Take #2: A Sliceable Sequence
class Vector1(Vector):
    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        return self._components[index]

v1 = Vector1([3, 4, 5])
print(len(v1))
print(v1[0], v1[-1])
v7 = Vector1(range(7))
print(v7[1:4])

# How Slicing Works
class MySeq:
    def __getitem__(self, index):
        return index

s = MySeq()
print(s[1])
print(s[1:4])
print(s[1:4:2])
print(s[1:4:2, 9])
print(s[1:4:2, 7:9])

print(dir(slice))
print(slice(None, 10, 2).indices(5))
print(slice(-3, None, None).indices(5))

# A Slice-Aware __getitem__
class Vector2(Vector):
    def __len__(self):
        return len(self._components)

    def __getitem__(self, key):
        if isinstance(key, slice):
            cls = type(self)
            return cls(self._components[key])
        index = operator.index(key)
        return self._components[index]

v7 = Vector2(range(7))
print(v7[-1])
print(v7[1:4])

# Vector Take #3: Dynamic Attribute Access
class Vector3(Vector2):
    __match_args__ = ('x', 'y', 'z', 't')
    def __getattr__(self, name):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
        if 0 <= pos < len(self._components):
            return self._components[pos]
        msg = f'{cls.__name__!r} object has no attribute {name!r}'
        raise AttributeError(msg)

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.__match_args__:
                error = "readonly attribute {attr_name!r}"
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)

v = Vector3(range(5))
print(v)
print(v.x)
# v.x = 10
print(v.x)
print(v)

# Vector Take #4: Hashing and a Faster ==
print(functools.reduce(lambda x, y: x*y, range(1, 6)))
print(functools.reduce(lambda x, y: x^y, range(1, 6)))
print(functools.reduce(operator.xor, range(6)))

class Vector4(Vector3):
    typecode = 'd'

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

for a, b in zip([1,2,3], [4,5,6]):
    print(a,b)

# The Awesome zip
print(zip(range(3), "ABC"))
print(list(zip(range(3), "ABC")))
print(list(zip(range(3), "ABC", [0.0, 1.1, 2.2, 3.3])))
# zip_longest can generate tuples until the last iterable is exhausted.
print(list(zip_longest(range(3), "ABC", [0.0, 1.1, 2.2, 3.3], fillvalue=-1)))
# zip function can also be used to transpose a matrix represented as nested itera‐bles
a = [(1, 2, 3),
     (4, 5, 6)]
print(list(zip(*a)))
b = [(1, 2),
     (3, 4),
     (5, 6),]
print(list(zip(*b)))

# Vector Take #5: Formatting
class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['): -1]
        return f"Vector({components})"

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))

    def __eq__(self, other):
        return (len(self) == len(other) and
                all(a == b for a, b in zip(self, other)))

    def __hash__(self):
        hashes = (hash(x) for x in self)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return bool(abs(self))

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, key):
        if isinstance(key, slice):
            cls = type(self)
            return cls(self._components[key])
        index = operator.index(key)
        return self._components[index]

    __match_args__ = ('x', 'y', 'z', 't')

    def __getattr__(self, name):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
        if 0 <= pos < len(self._components):
            return self._components[pos]
        msg = f"{cls.__name__!r} object has no attribute {name!r}"
        raise AttributeError(msg)

    def angle(self, n):
        r = math.hypot(*self[n:])
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, format_spec=''):
        if format_spec.endswith('h'):
            format_spec = format_spec[:-1]
            coords = itertools.chain([abs(self)],
                                     self.angle())
            out_fmt = "<{}>"

        else:
            coords = self
            out_fmt = "({})"
        components = (format(c, format_spec) for c in coords)
        return out_fmt.format(','.join(components))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)



