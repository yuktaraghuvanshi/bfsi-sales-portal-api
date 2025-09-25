# app/models/__init__.py
from .user import User
from .product import Product
from .customer import Customer
from .lead import Lead

__all__ = ["User", "Product", "Customer", "Lead"]
