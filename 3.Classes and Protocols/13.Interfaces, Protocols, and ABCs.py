"""
• “Two Kinds of Protocols” on page 434 compares the two forms of structural
typing with protocols—i.e., the lefthand side of the Typing Map.
• “Programming Ducks” on page 435 dives deeper into Python’s usual duck typing,
including how to make it safer while preserving its major strength: flexibility.
• “Goose Typing” on page 442 explains the use of ABCs for stricter runtime type
checking. This is the longest section, not because it’s more important, but
because there are more sections about duck typing, static duck typing, and static
typing elsewhere in the book.
• “Static Protocols” on page 466 covers usage, implementation, and design of typ
ing.Protocol subclasses—useful for static and runtime type checking.
"""

import collections
import random
import abc
import typing
import numbers
import sys
import math
import numpy as np
import decimal
from random import shuffle
from fractions import Fraction
from typing import TypeVar, Protocol
from array import array
from typing import Any, Iterable, TYPE_CHECKING, runtime_checkable


# Two kinds of Protocols: Dynamic, Static
class Vowels:
    def __getitem__(self, i):
        return "AEIOU"[i]


v = Vowels()
print(v[0])
print(v[-1])
for c in v: print(c)
print('E' in v)

# Programming Ducks
# dynamic protocols with two of the most important in Python: the sequence and iterable protocols.
Card = collections.namedtuple("Card", ["rank", "suit"])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


# Monkey Patching: Implementing a Protocol at Runtime
l = list(range(10))
shuffle(l)
deck = FrenchDeck()


# shuffle(deck)
# # Monkey patching FrenchDeck to make it mutable and compatible with random.shuffle
def set_card(deck, position, card):
    """mutable sequence protocol"""
    deck._cards[position] = card


FrenchDeck.__setitem__ = set_card
shuffle(deck)

from collections.abc import Iterable
from typing import Union


# Defensive Programming and “Fail Fast”
def namedtuple(typename: str, field_names: Union[str, Iterable[str]]):
    """Dynamic protocols Duck typing"""
    try:
        field_names = field_names.replace(',', ' ').split()
    except AttributeError:
        pass
    field_names = tuple(field_names)
    if not all(s.isidentifier() for s in field_names):
        raise ValueError("field_names must all be valid identifiers")


# Goose Typing
# Python doesn’t have an interface keyword. We use abstract base classes (ABCs) to define interfaces

# Goose typing in practice
## Suclassing an ABC
Card = namedtuple("Card", ["rank", "suit"])


class FrenchDeck2(collections.abc.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):
        self._cards[position] = value

    def __delitem__(self, position):
        del self._cards[position]

    def insert(self, position, value):
        self._cards.insert(position, value)


## ABCs in the Standard Library
"""
Iterable, Container, Sized
Collection
Sequence, Mapping, Set
MappingView
Iterator
Callable, Hashable
"""


## Defining and Using an ABC
class Tombola(abc.ABC):
    """
    the definition of the Tombola ABC.
    """

    @abc.abstractmethod
    def load(self, iterable):
        """Add items from an iterable."""
        pass

    @abc.abstractmethod
    def pick(self):
        """Remove item at random, returning it.
        This method should raise LookupError when the instance is empty.
        """
        pass

    def loaded(self):
        """Return True if there is at least 1 item, otherwise False."""
        return bool(self.inspect())

    def inspect(self):
        """Return a ssorted tuple with the items currently inside."""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(items)


# ABC Syntax Details
## the preferred way to declare an abstract class
class MyABC(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def an_abstract_classmethod(cls, ):
        pass


## Subclassing an ABC
class BingoCage(Tombola):
    def __init__(self, items):
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(items)

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError("pick from empty BingoCage")

    def __call__(self):
        self.pick()


class LottoBlower(Tombola):
    def __init__(self, iterable):
        self_balls = list(iterable)

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError("pick from empty LottoBlower")
        return self._balls.pop(position)

    def loaded(self):
        return bool(self._balls)

    def inspect(self):
        return tuple(self._balls)


# A Virtual Subclass of an ABC
@Tombola.register
class TomboList(list):

    def pick(self):
        if self:
            position = random.randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError("pop from empty TomboList")

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(self)


# Usage of register in Practice
collections.abc.Sequence.register(tuple)
collections.abc.Sequence.register(str)
collections.abc.Sequence.register(range)
collections.abc.Sequence.register(memoryview)


# Structural Typing with ABCs
class Struggle:
    def __len__(self):
        return 23


print(isinstance(Struggle(), collections.abc.Sized))
print(issubclass(Struggle, collections.abc.Sized))


class Sized(metaclass=abc.ABCMeta):
    __slots__ = ()

    @abc.abstractmethod
    def __len__(self):
        return 0

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Sized:
            if any("__len__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


# Static Protocols
# The Typed double Function
def double(x):
    return x * 2


print(double(1.5))
print(double('A'))
print(double([10, 20, 30]))
print(double(Fraction(2, 5)))

# definition of double using a Protocol
T = TypeVar('T')


class Repeatable(Protocol):
    def __mul__(self: T, repeat_count: int) -> T:
        pass


RT = TypeVar("RT", bound=Repeatable)


def double(x: RT) -> RT:
    return x * 2


# Runtime Checkable Static Protocols
@typing.runtime_checkable
class SupportsComplex(Protocol):
    """An ABC with one abstract method __complex__."""
    __slots__ = ()

    @abc.abstractmethod
    def __complex__(self) -> complex:
        pass


c64 = np.complex64(3 + 4j)
print(isinstance(c64, complex))
print(isinstance(c64, typing.SupportsComplex))

c = complex(c64)
print(c)
print(isinstance(c, typing.SupportsComplex))
print(complex(c))

print(isinstance(c, numbers.Complex))
print(isinstance(c64, numbers.Complex))


# Supporting a Static Protocol
class Vector2d:
    __match_args__ = ('x', 'y')
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    property

    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, self)))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __hash__(self):
        return hash((self.x, self.y))

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def angle(self):
        return math.atan2(self.y, self.x)

    def __format__(self, format_spec=''):
        if format_spec.endswith('p'):
            format_spec = format_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = "<{}, {}>"
        else:
            coords = self
            outer_fmt = "({}, {})"
        components = (format(c, format_spec) for c in coords)
        return outer_fmt.format(*components)

    @classmethod
    def from_bytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)

    def __complex__(self):
        return complex(self.x, self.y)

    @classmethod
    def fromcomplex(cls, datum):
        return cls(datum.real, datum.imag)


v = Vector2d(3, 4)
print(isinstance(v, typing.SupportsComplex))
print(isinstance(v, typing.SupportsAbs))


# Designing a Static Protocol
@runtime_checkable
class RandomPicker(Protocol):
    def pick(self) -> Any:
        pass


class SimplePicker:
    def __init__(self, items: Iterable) -> None:
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self) -> Any:
        return self._items.pop()

    def test_isinstance(self) -> None:
        popper: RandomPicker = SimplePicker([1])
        assert isinstance(popper, RandomPicker)

    def test_item_type(self) -> None:
        items = [1, 2]
        popper = SimplePicker(items)
        item = popper.pick()
        assert item in items
        if TYPE_CHECKING:
            typing.reveal_type(item)
        assert isinstance(item, int)


# Best Practices for Protocol Design
"""
• Use plain names for protocols that represent a clear concept (e.g., Iterator,
Container).
• Use SupportsX for protocols that provide callable methods (e.g., SupportsInt,
SupportsRead, SupportsReadSeek).21
• Use HasX for protocols that have readable and/or writable attributes or getter/
setter methods (e.g., HasItems, HasFileno).
"""

# Extending a Protocol
@runtime_checkable
class LoadableRandomPicker(RandomPicker, Protocol):
    def load(self, Iterable) -> None:
        pass

# The numbers ABCs and Numeric Protocols
_Number = Union[float, Fraction, decimal.Decimal]
_NumberT = TypeVar("_NumberT", float, decimal.Decimal, Fraction)

sample = [1+0j, np.complex64(1+0j), 1.0, np.float16(1.0), 1, np.int8(1)]
print([isinstance(x, typing.SupportsComplex) for x in sample])
print([complex(x) for x in sample])

def to_complex(n: typing.SupportsComplex) -> complex:
    return complex(n)