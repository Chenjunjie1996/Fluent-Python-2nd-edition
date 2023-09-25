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
from random import shuffle
from collections import namedtuple, abc

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

from collections import Iterable
from typing import Union
# Defensive Programming and “Fail Fast”
def namedtuple(typename: str, field_names:Union[str, Iterable[str]]):
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

class FrenchDeck2(abc.MutableSequence):
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