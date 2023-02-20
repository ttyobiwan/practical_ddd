import uuid
from practical_ddd.building_blocks import aggregates, entities, value_objects
from practical_ddd.database.repository import CustomerJSONRepository
from practical_ddd.service import CustomerService

# Initialize domain service with json repository
srv = CustomerService(repository=CustomerJSONRepository("test.json"))

# Create a new customer
customer = aggregates.Customer(
    person=entities.Person(
        first_name="Peter",
        last_name="Tobias",
        address=value_objects.Address(
            country="Germany",
            city="Berlin",
            street="Postdamer Platz",
            house_number="2/3",
        ),
    ),
)
srv.save_customer(customer)

# Add orders to existing customer
customer = srv.get_customer(uuid.UUID("a32dd73a-6c1b-4581-b1d3-2a1247320938"))
assert customer is not None
customer.add_order(entities.Order(description="Order 1", value=10))
customer.add_order(entities.Order(description="Order 2", value=210))
customer.add_order(entities.Order(description="Order 3", value=3210))
srv.save_customer(customer)

# Remove orders from existing customer
# If there are only 3 orders, it's gonna fail
customer = srv.get_customer(uuid.UUID("a32dd73a-6c1b-4581-b1d3-2a1247320938"))
assert customer is not None
customer.remove_order(uuid.UUID("0f3c0a7f-67fd-4309-8ca2-d007ac003b69"))
customer.remove_order(uuid.UUID("a4fd7648-4ea3-414a-a344-56082e00d2f9"))
srv.save_customer(customer)
