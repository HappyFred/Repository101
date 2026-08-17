"""Central management class for the nursery ordering system."""

from customer import Customer
from order import Order
from plant import Plant


class NurserySystem:
    """Manage the nursery's plants, customers, orders, and stock workflow."""

    def __init__(self) -> None:
        """Initialise empty collections and the first order number."""
        # Key collections by ID because names may repeat and IDs are used
        # for duplicate checks and direct lookups.
        self.__plants: dict[str, Plant] = {}
        self.__customers: dict[str, Customer] = {}
        self.__orders: dict[str, Order] = {}
        self.__next_order_number = 1

    def add_plant(self, plant: Plant) -> None:
        """Add a plant unless its identifier is already registered."""
        if plant.plant_id in self.__plants:
            raise ValueError(f"Plant ID {plant.plant_id} already exists.")
        self.__plants[plant.plant_id] = plant

    def add_customer(self, customer: Customer) -> None:
        """Add a customer unless their identifier is already registered."""
        if customer.customer_id in self.__customers:
            raise ValueError(
                f"Customer ID {customer.customer_id} already exists."
            )
        self.__customers[customer.customer_id] = customer

    def find_plant(self, plant_id: str) -> Plant | None:
        """Return the plant with the supplied identifier, if it exists."""
        return self.__plants.get(plant_id)

    def find_customer(self, customer_id: str) -> Customer | None:
        """Return the customer with the supplied identifier, if they exist."""
        return self.__customers.get(customer_id)

    def find_order(self, order_id: str) -> Order | None:
        """Return the order with the supplied identifier, if it exists."""
        return self.__orders.get(order_id)

    def check_stock(self, plant_id: str, quantity: int) -> bool:
        """Return whether a managed plant can supply a positive quantity."""
        plant = self.find_plant(plant_id)
        if plant is None:
            raise ValueError(f"Plant ID {plant_id} was not found.")
        return plant.is_stock_available(quantity)

    def update_plant_price(self, plant_id: str, new_price: float) -> None:
        """Update a managed plant's price through its validated property."""
        plant = self.find_plant(plant_id)
        if plant is None:
            raise ValueError(f"Plant ID {plant_id} was not found.")
        plant.price = new_price

    def restock_plant(self, plant_id: str, quantity: int) -> None:
        """Restock a managed plant through its validated stock method."""
        plant = self.find_plant(plant_id)
        if plant is None:
            raise ValueError(f"Plant ID {plant_id} was not found.")
        plant.increase_stock(quantity)

    def update_customer_contact(
        self,
        customer_id: str,
        email: str | None,
        phone: str | None,
    ) -> None:
        """Update both contact values through the customer's public method."""
        customer = self.find_customer(customer_id)
        if customer is None:
            raise ValueError(f"Customer ID {customer_id} was not found.")
        customer.update_contact(email, phone)

    def place_order(
        self,
        customer_id: str,
        plant_id: str,
        quantity: int,
        order_date: str,
    ) -> Order:
        """Create and store an order, reducing stock only after validation."""
        customer = self.find_customer(customer_id)
        if customer is None:
            raise ValueError(f"Customer ID {customer_id} was not found.")

        plant = self.find_plant(plant_id)
        if plant is None:
            raise ValueError(f"Plant ID {plant_id} was not found.")
        if not plant.is_stock_available(quantity):
            raise ValueError("Insufficient plant stock.")

        order_id = f"ORD{self.__next_order_number:03d}"
        order = Order(order_id, customer, plant, quantity, order_date)

        # The order is fully valid before stock or collections are changed.
        plant.reduce_stock(quantity)
        self.__orders[order_id] = order
        # Advance the number only after a successful order so failed
        # attempts do not consume an order ID.
        self.__next_order_number += 1
        return order

    def cancel_order(self, order_id: str) -> None:
        """Cancel a pending order and restore its stock exactly once."""
        order = self.find_order(order_id)
        if order is None:
            raise ValueError(f"Order ID {order_id} was not found.")

        # Order.cancel validates state before stock is restored, preventing a
        # repeated cancellation from adding the same stock twice.
        order.cancel()
        order.plant.increase_stock(order.quantity)

    def collect_order(self, order_id: str) -> None:
        """Mark a managed pending order as collected."""
        order = self.find_order(order_id)
        if order is None:
            raise ValueError(f"Order ID {order_id} was not found.")
        order.mark_collected()

    def get_customer_order_history(self, customer_id: str) -> list[Order]:
        """Return all recorded orders for an existing customer."""
        customer = self.find_customer(customer_id)
        if customer is None:
            raise ValueError(f"Customer ID {customer_id} was not found.")
        return [
            order
            for order in self.__orders.values()
            if order.customer.customer_id == customer.customer_id
        ]

    def get_all_plants(self) -> list[Plant]:
        """Return all registered plants in insertion order."""
        return list(self.__plants.values())

    def get_available_plants(self) -> list[Plant]:
        """Return registered plants whose stock level is greater than zero."""
        return [
            plant
            for plant in self.__plants.values()
            if plant.stock_level > 0
        ]

    def get_all_customers(self) -> list[Customer]:
        """Return all registered customers in insertion order."""
        return list(self.__customers.values())

    def get_all_orders(self) -> list[Order]:
        """Return all recorded orders in creation order."""
        return list(self.__orders.values())

    def __str__(self) -> str:
        """Return a readable summary of the managed collections."""
        return (
            "NurserySystem: "
            f"{len(self.__plants)} plants, "
            f"{len(self.__customers)} customers, "
            f"{len(self.__orders)} orders"
        )
