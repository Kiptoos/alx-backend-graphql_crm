import re
from decimal import Decimal

import django_filters
import graphene
from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter


# -----------------------
# GraphQL Types
# -----------------------

class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (relay.Node,)
        filterset_class = CustomerFilter


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (relay.Node,)
        filterset_class = ProductFilter


class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (relay.Node,)
        filterset_class = OrderFilter


# -----------------------
# Input Types
# -----------------------

class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)


class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int(required=False)


class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime(required=False)


# -----------------------
# Validation helpers
# -----------------------

PHONE_REGEX = re.compile(
    r"^(\+\d{7,15}|\d{3}-\d{3}-\d{4})$"
)


def validate_phone(phone: str):
    if phone is None or phone == "":
        return
    if not PHONE_REGEX.match(phone):
        raise GraphQLError(
            "Invalid phone format. Use +1234567890 or 123-456-7890."
        )


def validate_unique_email(email: str):
    if Customer.objects.filter(email=email).exists():
        raise GraphQLError("Email already exists")


def decimal_from_float(value: float) -> Decimal:
    return Decimal(str(value))


# -----------------------
# Mutations
# -----------------------

class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerNode)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, input: CustomerInput):
        # validations
        try:
            validate_email(input.email)
        except DjangoValidationError:
            raise GraphQLError("Invalid email address")

        validate_unique_email(input.email)
        validate_phone(input.phone)

        customer = Customer.objects.create(
            name=input.name,
            email=input.email,
            phone=input.phone or "",
        )

        return CreateCustomer(
            customer=customer, message="Customer created successfully"
        )


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerNode)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, input):
        created_customers = []
        errors = []

        with transaction.atomic():
            for idx, customer_input in enumerate(input, start=1):
                try:
                    # Validate
                    try:
                        validate_email(customer_input.email)
                    except DjangoValidationError:
                        raise GraphQLError(
                            f"Row {idx}: Invalid email '{customer_input.email}'"
                        )

                    validate_unique_email(customer_input.email)
                    validate_phone(customer_input.phone)

                    customer = Customer.objects.create(
                        name=customer_input.name,
                        email=customer_input.email,
                        phone=customer_input.phone or "",
                    )
                    created_customers.append(customer)
                except GraphQLError as e:
                    errors.append(str(e))

        return BulkCreateCustomers(customers=created_customers, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductNode)

    @classmethod
    def mutate(cls, root, info, input: ProductInput):
        if input.price <= 0:
            raise GraphQLError("Price must be a positive value")
        if input.stock is not None and input.stock < 0:
            raise GraphQLError("Stock cannot be negative")

        product = Product.objects.create(
            name=input.name,
            price=decimal_from_float(input.price),
            stock=input.stock if input.stock is not None else 0,
        )

        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderNode)

    @classmethod
    def mutate(cls, root, info, input: OrderInput):
        # Validate customer
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist:
            raise GraphQLError("Invalid customer ID")

        if not input.product_ids:
            raise GraphQLError("At least one product must be selected")

        # Validate products
        products = list(Product.objects.filter(pk__in=input.product_ids))
        if len(products) != len(set(input.product_ids)):
            raise GraphQLError("One or more product IDs are invalid")

        # Compute total amount
        total_amount = sum((p.price for p in products), Decimal("0.00"))

        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
        )
        order.products.set(products)

        # optional: override order_date if provided
        if input.order_date is not None:
            order.order_date = input.order_date
            order.save(update_fields=["order_date"])

        return CreateOrder(order=order)


# -----------------------
# Query with filtering
# -----------------------

class Query(graphene.ObjectType):
    # Relay node fields (optional, useful for direct node lookups)
    customer = relay.Node.Field(CustomerNode)
    all_customers = DjangoFilterConnectionField(CustomerNode)

    product = relay.Node.Field(ProductNode)
    all_products = DjangoFilterConnectionField(ProductNode)

    order = relay.Node.Field(OrderNode)
    all_orders = DjangoFilterConnectionField(OrderNode)


# -----------------------
# Root Mutation object
# -----------------------

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
