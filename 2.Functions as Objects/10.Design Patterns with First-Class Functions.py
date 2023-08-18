"""
Context:
Order: total(), due()

Strategy:
Promotion: discount()

Concrete strategies:
FidelityPromo: discount()
BulkPromo: discount()
LargeOrderPromo: discount()
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from decimal import Decimal
from typing import NamedTuple, Optional

class Customer(NamedTuple):
    name: str
    fidelity: int

class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.price * self.quantity

class Order(NamedTuple):
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional["Promotion"] = None

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'
class Promotion(ABC): # the Strategy: an abstract base class
    @abstractmethod
    def discount(self, order: Order) -> Decimal:
        """Return discount as a positive dollar amount"""

class FidelityPromo(Promotion): # first Concrete Strategy
    """5% discount for customers with 1000 or more fidelity points"""
    def discount(self, order: Order) -> Decimal:
        rate = Decimal("0.05")
        if order.customer.fidelity >= 1000:
            return order.total() * rate
        return Decimal(0)

class BulkItemPromo(Promotion): # second Concrete Strategy
    """10% discount for each LineItem with 20 or more units"""
    def discount(self, order: Order) -> Decimal:
        discount = Decimal(0)
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * Decimal('0.1')
        return discount

class LargeOrderPromo(Promotion): # third Concrete Strategy
    """7% discount for orders with 10 or more distinct items"""
    def discount(self, order: Order) -> Decimal:
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * Decimal('0.07')
        return Decimal(0)

# Sample usage of Order class with different promotions applied
joe = Customer("John Doe", 0)
ann = Customer("Ann Smith", 1100)
cart = (LineItem("banana", 4, Decimal('.5')),
        LineItem("apple", 10, Decimal("1.5")),
        LineItem("watermelon", 5, Decimal(5)))
print(Order(joe, cart, FidelityPromo()))
print(Order(ann, cart, FidelityPromo()))
banana_cart = (LineItem("banana", 30, Decimal('.5')),
               LineItem("apple", 10, Decimal('1.5')))
print(Order(joe, banana_cart, BulkItemPromo()))
long_cart = tuple(LineItem(str(sku), 1, Decimal(1)) for sku in range(10))
print(Order(joe, long_cart, LargeOrderPromo()))
print(Order(joe, cart, LargeOrderPromo()))
print("==============================================")

# Function-Oriented Strategy
# Order class with discount strategies implemented as functions
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Callable, NamedTuple

class Customer(NamedTuple):
    name: str
    fidelity: int

class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self):
        return self.price * self.quantity

@dataclass(frozen=True)
class Order:  # the context
    customer: Customer
    cart: Sequence[LineItem]
    # Callable type; Callable[[int], str] is a function of (int) -> str
    promotion: Optional[ Callable[["Order"], Decimal] ] = None

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'

def fidelity_promo(order: Order) -> Decimal:
    """5% discount for customers with 1000 or more fidelity points"""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)

def bulk_item_promo(order: Order) -> Decimal:
    """10% discount for each LineItem with 20 or more units"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount

def large_order_promo(order: Order) -> Decimal:
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)

joe = Customer("John Doe", 0)
ann = Customer("Ann Smith", 1100)
cart = [
    LineItem("banana", 4, Decimal('.5')),
    LineItem("apple", 10, Decimal('1.5')),
    LineItem("watermelon", 5, Decimal(5))
]
print(Order(joe, cart, fidelity_promo))
print(Order(ann, cart, fidelity_promo))

banana_cart = [
    LineItem("banana", 30, Decimal('.5')),
    LineItem("apple", 10, Decimal('1.5')),
]
print(Order(joe, banana_cart, bulk_item_promo))

long_cart = [LineItem(str(item_code), 1, Decimal(1))
             for item_code in range(10)]
print(Order(joe, long_cart, large_order_promo))
print(Order(joe, cart, large_order_promo))
print("============================================="
      )
# Choosing the Best Strategy: Simple Approach
promos = [fidelity_promo, bulk_item_promo, large_order_promo]
def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)

print(Order(joe, long_cart, best_promo))
print(Order(joe, banana_cart, best_promo))
print(Order(ann, cart, best_promo))
print("=============================================")

# Finding Strategies in a Module
promos = [promo for name, promo in globals().items()
          if name.endswith("_promo") and name != "best_promo"]
print(promos)
print("=============================================")

# Decorator-Enhanced Strategy Pattern
Promotion = Callable[[Order], Decimal]
promos: list[Promotion] = []

def promotion(promo: Promotion) -> Promotion:
    promos.append(promo)
    return promo

def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)

@promotion
def fidelity(order: Order) -> Decimal:
    """5% discount for customers with 1000 or more fidelity points"""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)

@promotion
def bulk_item(order: Order) -> Decimal:
    """10% discount for each LineItem with 20 or more units"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount

@promotion
def large_order(order: Order) -> Decimal:
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal("0.07")
    return Decimal(0)

print(promos)

"""
Command Pattern
Command is another design pattern that can be simplified by the use of functions
passed as arguments.
"""
class MacroCommand:
    """A command thatexecutes a list of commands"""