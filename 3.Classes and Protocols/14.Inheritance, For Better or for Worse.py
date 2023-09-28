"""
• The super() function
• The pitfalls of subclassing from built-in types
• Multiple inheritance and method resolution order
• Mixin classes
"""
import collections
from collections import OrderedDict


# The super function
class LastUpdatedOrderedDict(OrderedDict):
    """Store items in the order they were last updated
    Overrides __setitem__ to:
    1. Use super().__setitem__ to let it insert or update the key/value pair
    2. Call self.move_to_end to ensure the updated key is in the last position.
    """

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end()


# Subclassing Built-In Types Is Tricky
class DoppelDict(dict):
    """
    __setitem__ override is ignored by the __init__ and __update__
    methods of the built-in dict
    """

    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


dd = DoppelDict(one=1)  # __init__ method
dd["two"] = 2  # __setitem__ method
dd.update(three=3)  # update method
print(dd)


class AnswerDict(dict):
    """
     The __getitem__ of AnswerDict is bypassed by dict.update
    """

    def __getitem__(self, item):
        return 42


ad = AnswerDict(a="foo")  # ad is an AnswerDict loaded with the key-value pair ('a', 'foo').
print(ad)
print(ad['a'])  # ad['a'] returns 42, as expected.

d = {}
d.update(ad)  # d is an instance of plain dict, which we update with ad.
print(d['a'])  # The dict.update method ignored our AnswerDict.__getitem__.
print(d)


class DoppelDict2(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


class AnswerDict2(collections.UserDict):
    def __getitem__(self, item):
        return 42


dd = DoppelDict2(one=1)
dd['two'] = 2
dd.update(three=3)
print(dd)

ad = AnswerDict2(a="foo")
d = {}
d.update(ad)
print(ad['a'])
print(d['a'])
print(d)

# Multiple Inheritance and Method Resolution Order
