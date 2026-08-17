"""Order class for the nursery ordering system."""

from datetime import datetime

from customer import Customer
from plant import Plant


class Order:
    """Represent one customer's order for one type of plant."""

    def __init__(
        self,
        order_id: str,
        customer: Customer,
        plant: Plant,
        quantity: int,
        order_date: str,
    ) -> None:
        """Initialise a pending order and capture its historical total."""
        if not order_id.strip():
            raise ValueError("Order ID must not be empty.")
        if quantity <= 0:
            raise ValueError("Order quantity must be greater than zero.")

        try:
            parsed_date = datetime.strptime(order_date, "%d-%m-%Y")
        except ValueError as error:
            raise ValueError(
                "Order date must be a valid date in DD-MM-YYYY format."
            ) from error
        # The round-trip check enforces the exact zero-padded DD-MM-YYYY
        # format after the date itself has been validated.
        if parsed_date.strftime("%d-%m-%Y") != order_date:
            raise ValueError(
                "Order date must be a valid date in DD-MM-YYYY format."
            )

        self.__order_id = order_id.strip()
        self.__customer = customer
        self.__plant = plant
        self.__quantity = quantity
        self.__order_date = order_date
        self.__status = "pending"

        discount_rate = 0.10 if quantity >= 10 else 0.0
        # Capture the total now so later plant price changes do not rewrite
        # the financial history of an existing order.
        self.__order_total = round(
            plant.price * quantity * (1 - discount_rate),
            2,
        )

    @property
    def order_id(self) -> str:
        """Return the order's read-only identifier."""
        return self.__order_id

    @property
    def customer(self) -> Customer:
        """Return the customer attached to the order."""
        return self.__customer

    @property
    def plant(self) -> Plant:
        """Return the plant attached to the order."""
        return self.__plant

    @property
    def quantity(self) -> int:
        """Return the ordered quantity."""
        return self.__quantity

    @property
    def order_date(self) -> str:
        """Return the order date in DD-MM-YYYY format."""
        return self.__order_date

    @property
    def status(self) -> str:
        """Return the current order status."""
        return self.__status

    @property
    def order_total(self) -> float:
        """Return the immutable total captured when the order was created."""
        return self.__order_total

    def mark_collected(self) -> None:
        """Change a pending order to collected."""
        if self.__status != "pending":
            raise ValueError("Only a pending order can be collected.")
        self.__status = "collected"

    def cancel(self) -> None:
        """Change a pending order to cancelled."""
        if self.__status != "pending":
            raise ValueError("Only a pending order can be cancelled.")
        self.__status = "cancelled"

    def __str__(self) -> str:
        """Return a readable summary of the order."""
        return (
            f"Order {self.__order_id}: "
            f"customer={self.__customer.customer_id}, "
            f"plant={self.__plant.plant_id}, quantity={self.__quantity}, "
            f"date={self.__order_date}, status={self.__status}, "
            f"total=${self.__order_total:.2f}"
        )
