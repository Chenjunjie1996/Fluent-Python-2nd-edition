"""
The major topics in this chapter are:
• A hands-on introduction to gradual typing with Mypy
• The complementary perspectives of duck typing and nominal typing
• Overview of the main categories of types that can appear in annotations—this is
about 60% of the chapter
• Type hinting variadic parameters (*args, **kwargs)
• Limitations and downsides of type hints and static typing
"""
import typing
import sys
import re
import unicodedata
from typing import Optional, Union, NamedTuple, TypeVar, Any, Protocol, NoReturn
from collections.abc import Sequence, Iterator, Iterable, Mapping, Hashable, Callable
from random import shuffle
from collections import Counter
from decimal import Decimal
from fractions import Fraction


# Making Mypy More Strict
def show_count(count: int, singular: str, plural: str = '') -> str:
    if count == 1:
        return f"1 {singular}"
    count_str = str(count) if count else "no"
    if not plural:
        plural = singular + 's'
    return f"{count_str} {plural}"

# Using None as a Default
# • Optional[str] means plural may be a str or None.
# • You must explicitly provide the default value = None.
def show_count(count: int, singular: str, plural: Optional[str] = None) -> str:
    pass

# Types Are Defined by Supported Operations
class Bird:
    pass

class Duck(Bird):
    def quack(self):
        print("Quack!")

def alert(birdie):
    birdie.quack()

def alert_duck(birdie: Duck) -> None:
    birdie.quack()

def alert_bird(birdie: Bird) -> None:
    birdie.quack()


""" Types Usable in Annotations
• typing.Any
• Simple types and classes
• typing.Optional and typing.Union
• Generic collections, including tuples and mappings
• Abstract base classes
• Generic iterables
• Parameterized generics and TypeVar
• typing.Protocols—the key to static duck typing
• typing.Callable
• typing.NoReturn—a good way to end this list
"""
# typing.Any
def double(x: typing.Any) -> typing.Any:
    pass

def double(x: object) -> object:
    pass

# Simple types and classes
def show_count(plural: Optional[str] = None) -> str:
    pass

def parse_token(token: str) -> Union[str, float]:
    try:
        return float(token)
    except ValueError:
        return token

# Generic Collections
def tokenize(text: str) -> list[str]:
    return text.upper().split()

# Tuple Types
# • Tuples as records
("Shanghai", 24.28, "China")

# • Tuples as records with named fields
# Coordinate is consistent-with tuple[float, float]
class Coordinate(NamedTuple):
    lat: float
    lon: float

def display(lat_lon: tuple[float, float]) -> str:
    lat, lon = lat_lon
    ns = 'N' if lat >= 0 else 'S'
    ew = 'E' if lon >= 0 else 'W'
    return f'{abs(lat):0.1f}°{ns}, {abs(lon):0.1f}°{ew}'

# • Tuples as immutable sequences
animals = 'drake fawn heron ibex koala lynx tahr xerus yak zapus'.split()
def columnize(sequence: Sequence[str], num_columns: int=0) -> list[tuple[str, ...]]:
    if num_columns == 0:
        num_columns = round(len(sequence) ** 0.5)
    num_rows, reminder = divmod(len(sequence), num_columns)
    num_rows += bool(reminder)
    return [tuple(sequence[i::num_rows]) for i in range(num_rows)]
table = columnize(animals)
print(table)


# Generic Mappings
RE_WORD = re.compile(r'\w+')
STOP_CODE = sys.maxunicode + 1
def tokenize(text: str) -> Iterator[str]:
    """return iterable of upper"""
    for match in RE_WORD.finditer(text):
        yield match.group().upper()

def name_index(start: int=32, end: int=STOP_CODE) -> dict[str,set[str]]:
    index: dict[str, set[str]] = {}
    for char in (chr(i) for i in range(start, end)):
        if name:= unicodedata.name(char, ''):
            for word in tokenize(name):
                index.setdefault(word, set()).add(char)
    return index

# Abstract Base Classes
def name2hex(name: str, color_map: Mapping[str, int]) -> str:
    pass

# Iterable
FromTo = tuple[str, str]
def zip_replace(text: str, changes: Iterable[FromTo]) -> str:
    for from_, to in changes:
        text = text.replace(from_, to)
    return text

l33t = [('a', '4'), ('e', '3'), ('i', '1'), ('o', '0')]
text = "mad skilled noob powned leet"
result = zip_replace(text, l33t)
print(result)

"""
iterable:具体应该叫做可迭代对象。他的特点其实就是我的序列的大小长度已经确定了
(list,tuple,dict,string等)。他遵循可迭代的协议。

iterator:具体应该叫做迭代器的对象。他的特点就是他不知道要执行多少次，
所以可以理解不知道有多少个元素，每调用一次__next__()方法，就会往下走一步，
当然是用__next__()方法只能往下走，不会回退。是惰性的。
这样我可以存很大很大的数据，即使是整个自然数，也可以很轻松的用迭代器来表示出来。
他满足的是迭代器协议。
"""

# Parameterized Generics and TypeVar
T = TypeVar('T')
def sample(population: Sequence[T], size: int) -> list[T]:
    if size < 1:
        raise ValueError("size must be >= 1")
    result = list(population)
    shuffle(result)
    return result[:size]

def mode(data: Iterable[float]) -> float:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError("no mode for empty data")
    return pairs[0][0]

def mode(data: Iterable[T]) -> T:
    pass

## Restricted TypeVar
NumberT = TypeVar("NumberT", float, Decimal, Fraction)
def mode(data:Iterable[NumberT]) -> NumberT:
    pass

## Bounded TypeVar type parameter may be Hashable or any subtype of it
def mode(data: Iterable[Hashable]) -> Hashable:
    pass

HashableT = TypeVar("HashableT", bound=Hashable)
def mode(data:Iterable[HashableT]) -> HashableT:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError("no mode for empty data")
    return pairs[0][0]

# Static Protocols
def top(series: Iterable[T], length: int) -> list[T]:
    ordered = sorted(series, reverse=True)
    return ordered[:length]
top([4, 1, 5, 2, 6, 7, 3], 3)

# constrain T
class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool: pass

LT = TypeVar("LT", bound=SupportsLessThan)

def top(series: Iterable[LT], length: int) -> list[LT]:
    ordered = sorted(series, reverse=True)
    return ordered[:length]

# Callable
## variance in Callable types
def update(probe: Callable[[], float], display: Callable[[float], None]) -> None:
    """Callable[[int], str] is a function of (int) -> str"""
    temperature = probe()
    display(temperature)

# NoReturn
"""
This is a special type used only to annotate the return type of functions 
that never return. Usually, they exist to raise exceptions.
For example, sys.exit() raises SystemExit to terminate the Python process.
"""
def exit(__status: object = ...) -> NoReturn:
    pass

# Annotating Positional Only and Variadic Parameters
def tag(__name: str, *content: str, class_:Optional[str]=None, **attrs: str) -> str:
    pass
