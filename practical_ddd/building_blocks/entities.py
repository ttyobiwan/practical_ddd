import uuid

from pydantic import BaseModel, Field
from practical_ddd.building_blocks.value_objects import Address


class Person(BaseModel):
    """Personal data."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    first_name: str
    last_name: str
    address: Address


class Order(BaseModel):
    """Customer order."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    description: str
    value: float
