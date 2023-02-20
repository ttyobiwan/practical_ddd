import json
import uuid
from practical_ddd.building_blocks.aggregates import Customer


class CustomerJSONRepository:
    """Customer repository operating on JSON files."""

    def __init__(self, path: str) -> None:
        self.path = path

    def get(self, customer_id: uuid.UUID) -> Customer:
        with open(self.path, "r") as file:
            database = json.load(file)
            customer = database["customers"].get(str(customer_id))
            if customer is None:
                raise IndexError("Customer not found")

            person = database["persons"][str(customer["person"])]
            orders = [database["orders"][order_id] for order_id in customer["orders"]]

        return Customer(
            id=customer["id"],
            person=person,
            orders=orders,
        )

    def save(self, customer: Customer) -> None:
        with open(self.path, "r+") as file:
            database = json.load(file)
            # Save customer
            database["customers"][str(customer.id)] = {
                "id": customer.id,
                "person": customer.person.id,
                "orders": [o.id for o in customer.orders],
            }
            # Save person
            database["persons"][str(customer.person.id)] = customer.person.dict()
            # Save orders
            for order in customer.orders:
                database["orders"][str(order.id)] = order.dict()

            file.seek(0)
            json.dump(database, file, indent=4, default=str)
