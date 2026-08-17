"""Plant class for the nursery ordering system."""


class Plant:
    """Represent a plant type sold by the nursery."""

    ALLOWED_CATEGORIES: tuple[str, ...] = (
        "trees and shrubs",
        "perennials",
        "pot plants",
        "vegetable seedlings",
    )

    def __init__(
        self,
        plant_id: str,
        name: str,
        category: str,
        price: float,
        stock_level: int,
    ) -> None:
        """Initialise a plant with identifying, pricing, and stock data."""
        if not plant_id.strip():
            raise ValueError("Plant ID must not be empty.")

        self.__plant_id = plant_id.strip()
        self.__name = ""
        self.__category = ""
        self.__price = 0.0
        self.__stock_level = 0
        # Use the property setters so creation follows the same validation
        # rules as later updates.
        self.name = name
        self.category = category
        self.price = price
        self.stock_level = stock_level

    @property
    def plant_id(self) -> str:
        """Return the plant's read-only identifier."""
        return self.__plant_id

    @property
    def name(self) -> str:
        """Return the plant name."""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """Set the plant name after checking it is not empty."""
        if not value.strip():
            raise ValueError("Plant name must not be empty.")
        self.__name = value.strip()

    @property
    def category(self) -> str:
        """Return the plant category."""
        return self.__category

    @category.setter
    def category(self, value: str) -> None:
        """Set the category when it is one of the permitted categories."""
        category = value.strip()
        if category not in self.ALLOWED_CATEGORIES:
            raise ValueError("Plant category is not valid.")
        self.__category = category

    @property
    def price(self) -> float:
        """Return the unit price."""
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        """Set the unit price after checking that it is positive."""
        if value <= 0:
            raise ValueError("Plant price must be greater than zero.")
        self.__price = float(value)

    @property
    def stock_level(self) -> int:
        """Return the number of plants currently in stock."""
        return self.__stock_level

    @stock_level.setter
    def stock_level(self, value: int) -> None:
        """Set the stock level after checking that it is not negative."""
        if value < 0:
            raise ValueError("Plant stock must not be negative.")
        self.__stock_level = value

    def is_stock_available(self, quantity: int) -> bool:
        """Return whether a positive requested quantity is in stock."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        return self.__stock_level >= quantity

    def reduce_stock(self, quantity: int) -> None:
        """Reduce stock by a positive available quantity."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if not self.is_stock_available(quantity):
            raise ValueError("Insufficient plant stock.")
        self.__stock_level -= quantity

    def increase_stock(self, quantity: int) -> None:
        """Increase stock by a positive quantity."""
        if quantity <= 0:
            raise ValueError("Restock quantity must be greater than zero.")
        self.__stock_level += quantity

    def __str__(self) -> str:
        """Return a readable summary of the plant."""
        return (
            f"Plant {self.__plant_id}: {self.__name}, "
            f"{self.__category}, ${self.__price:.2f}, "
            f"stock={self.__stock_level}"
        )
