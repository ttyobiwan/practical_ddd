import uuid
from typing import Protocol
from practical_ddd.building_blocks.aggregates import Customer


class CustomerRepository(Protocol):
    """Customer repository interface."""

    def get(self, customer_id: uuid.UUID) -> Customer:
        ...

    def save(self, customer: Customer) -> None:
        ...


class CustomerService:
    """Customer service."""

    def __init__(self, repository: CustomerRepository) -> None:
        self.repository = repository

    def get_customer(self, customer_id: uuid.UUID) -> Customer | None:
        try:
            return self.repository.get(customer_id)
        except IndexError:
            return None

    def save_customer(self, customer: Customer) -> None:
        existing_customer = self.get_customer(customer.id)
        # If customer is already in the database and has more than 2 orders,
        # he cannot end up with half of them after a single save.
        if (
            existing_customer is not None
            and len(existing_customer.orders) > 2
            and len(customer.orders) < (len(existing_customer.orders) / 2)
        ):
            raise ValueError(
                "Customer cannot lose more than half of his orders upon single save!"
            )

        self.repository.save(customer)
