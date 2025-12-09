"""
Simple seed script to populate the CRM database.

Usage:
    python seed_db.py
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphql_crm.settings")
django.setup()

from crm.models import Customer, Product, Order  # noqa
from decimal import Decimal


def run():
    Customer.objects.all().delete()
    Product.objects.all().delete()
    Order.objects.all().delete()

    alice = Customer.objects.create(
        name="Alice",
        email="alice@example.com",
        phone="+1234567890",
    )
    bob = Customer.objects.create(
        name="Bob",
        email="bob@example.com",
        phone="123-456-7890",
    )

    laptop = Product.objects.create(name="Laptop", price=Decimal("999.99"), stock=10)
    mouse = Product.objects.create(name="Mouse", price=Decimal("19.99"), stock=100)

    order = Order.objects.create(
        customer=alice,
        total_amount=laptop.price + mouse.price,
    )
    order.products.set([laptop, mouse])

    print("Seeded customers, products, and one order.")


if __name__ == "__main__":
    run()
