"""
• Overloaded function signatures
• typing.TypedDict for type hinting dicts used as records
• Type casting
• Runtime access to type hints
• Generic types
— Declaring a generic class
— Variance: invariant, covariant, and contravariant types
— Generic static protocols
"""

# Overloaded Signatures
import functools
import json
import operator
import typing
from collections.abc import Iterable, Callable
from typing import overload, Union, TypeVar, Any, Protocol, TypedDict, TYPE_CHECKING, cast

T = TypeVar('T')
S = TypeVar('S')


@overload
def sum(it: Iterable[T]) -> Union[T, int]:
    pass


@overload
def sum(it: Iterable[T], /, start: S) -> Union[T, S]:
    pass


def sum(it, /, start=0):
    return functools.reduce(operator.add, it, start)


# Max Overload
MISSING = object()
EMPTY_MSG = "max() arg is an empty sequence"


def max(first, *args, key=None, default=MISSING):
    if args:
        series = args
        candidate = first
    else:
        series = iter(first)
        try:
            candidate = next(series)
        except StopIteration:
            if default is not MISSING:
                return default
            raise ValueError(EMPTY_MSG) from None
    if key is None:
        for current in series:
            if candidate < current:
                candidate = current
    else:
        candidate_key = key(candidate)
        for current in series:
            current_key = key(current)
            if candidate_key < current_key:
                candidate = current
                candidate_key = current_key
    return candidate


class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool:
        pass


T = TypeVar('T')
LT = TypeVar('LT', bound=SupportsLessThan)
DT = TypeVar('DT')

MISSING = object()
EMPTY_MSG = "max() arg is an empty sequence"


@overload
def max(__arg1: LT, __arg2: LT, *args: LT, key: None = ...) -> LT:
    pass


@overload
def max(__arg1: T, __arg2: T, *args: T, key: Callable[[T], LT]) -> T:
    pass


@overload
def max(__iterable: Iterable[LT], *, key: None = ...) -> LT:
    pass


@overload
def max(__iterable: Iterable[T], *, key: Callable[[T], LT]) -> T:
    pass


@overload
def max(__iterable: Iterable[LT], *, key: None = ..., default: DT) -> Union[LT, DT]:
    pass


@overload
def max(__iterable: Iterable[T], *, key: Callable[[T], LT], default: DT) -> Union[T, DT]:
    pass


## Arguments implementing SupportsLessThan, but key and default not provided
@overload
def max(__arg1: LT, __arg2: LT, *_args: LT, key: None = ...) -> LT:
    pass


@overload
def max(__iterable: Iterable[LT], *, key: None = ...) -> LT:
    pass


# max(1, 2, -3)
# max(["Go", "Python", "Rust"])

## Argument key provided, but no default
@overload
def max(__arg1: T, __arg2: T, *_args: T, key: Callable[[T], LT]) -> T:
    pass


@overload
def max(__iterable: Iterable[T], *, key: Callable[[T], LT]) -> T:
    pass


# max(1, 2, -3, key=abs)
# max(["Go", "Python", "Rust"], key=len)

## Argument default provided, but no key
@overload
def max(__iterable: Iterable[LT], *, key: None = ..., default: DT) -> Union[LT, DT]:
    pass


# max([1, 2, -3], default=0)
# max([], default=None)

## Arguments key and default provided
@overload
def max(__iterable: Iterable[T], *, key: Callable[[T], LT], default: DT) -> Union[T, DT]:
    pass


# max([1, 2, -3], key=abs, default=None) # returns -3
# max([], key=abs, default=None) # returns None

# TypedDict
class BookDict(TypedDict):
    isbn: str
    title: str
    authors: list[str]
    pagecount: int


pp = BookDict(title="Programming Pearls",
              authors="Jon Bentley",
              isbn="0201657880",
              pagecount=256)
print(pp)
print(type(pp))
# print(pp.title) AttributeError
print(pp["title"])
print(BookDict.__annotations__)


def demo() -> None:
    """legal and illegal operations on a BookDict"""
    book = BookDict(
        isbn="0134757599",
        title="Refactoring, 2e",
        authors=["Martin Fowler", "Kent Beck"],
        pagecount=478
    )
    authors = book["authors"]
    if TYPE_CHECKING:
        typing.reveal_type(authors)
    authors = "Bob"
    book["weight"] = 4.2
    del book["title"]


def from_json(data: str) -> BookDict:
    whatever = json.loads(data)
    return whatever


def from_json(data: str) -> BookDict:
    whatever: BookDict = json.loads(data)
    return whatever


# Type Casting
def find_first_str(a: list[object]) -> str:
    index = next(i for i, x in enumerate(a) if isinstance(x, str))
    # We only get here if there is at least one string
    return cast(str, a[index])