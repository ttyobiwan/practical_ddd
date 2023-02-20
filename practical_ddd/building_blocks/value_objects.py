from pydantic import BaseModel


class Address(BaseModel):
    """Customer address."""

    country: str
    city: str
    street: str
    house_number: str

    class Config:
        frozen = True
