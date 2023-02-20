import uuid
from pydantic import BaseModel, Field
from practical_ddd.building_blocks.entities import Person, Order
from practical_ddd.building_blocks.value_objects import Address


class Customer(BaseModel):
    """Customer aggregate.

    Manages personal information as well as orders.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    person: Person
    orders: list[Order] = Field(default_factory=list)

    def change_address(self, new_address: Address) -> None:
        self.person.address = new_address

    def add_order(self, order: Order) -> None:
        if self.total_value + order.value > 10000:
            raise ValueError("Order cannot have value higher than 10000")
        self.orders.append(order)

    def remove_order(self, order_id: uuid.UUID) -> None:
        order = next((order for order in self.orders if order.id == order_id), None)
        if order is None:
            raise IndexError("Order not found")
        self.orders.remove(order)

    @property
    def total_value(self) -> float:
        return sum(order.value for order in self.orders)
