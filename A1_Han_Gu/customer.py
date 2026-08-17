"""Customer class for the nursery ordering system."""


class Customer:
    """Represent a nursery customer with at least one contact method."""

    def __init__(
        self,
        customer_id: str,
        name: str,
        email: str | None,
        phone: str | None,
    ) -> None:
        """Initialise a customer and validate their identity and contact."""
        if not customer_id.strip():
            raise ValueError("Customer ID must not be empty.")
        if not name.strip():
            raise ValueError("Customer name must not be empty.")

        self.__customer_id = customer_id.strip()
        self.__name = name.strip()
        self.__email: str | None = None
        self.__phone: str | None = None
        self.update_contact(email, phone)

    @property
    def customer_id(self) -> str:
        """Return the customer's read-only identifier."""
        return self.__customer_id

    @property
    def name(self) -> str:
        """Return the customer's name."""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """Set the customer name after checking it is not empty."""
        if not value.strip():
            raise ValueError("Customer name must not be empty.")
        self.__name = value.strip()

    @property
    def email(self) -> str | None:
        """Return the customer's email address, if supplied."""
        return self.__email

    @email.setter
    def email(self, value: str | None) -> None:
        """Set email without leaving the customer with no contact method."""
        email = value.strip() if value and value.strip() else None
        if email is None and self.__phone is None:
            raise ValueError("An email address or phone number is required.")
        self.__email = email

    @property
    def phone(self) -> str | None:
        """Return the customer's phone number, if supplied."""
        return self.__phone

    @phone.setter
    def phone(self, value: str | None) -> None:
        """Set phone without leaving the customer with no contact method."""
        phone = value.strip() if value and value.strip() else None
        if phone is None and self.__email is None:
            raise ValueError("An email address or phone number is required.")
        self.__phone = phone

    def update_contact(
        self,
        email: str | None,
        phone: str | None,
    ) -> None:
        """Replace both contact values together after joint validation."""
        new_email = email.strip() if email and email.strip() else None
        new_phone = phone.strip() if phone and phone.strip() else None
        if new_email is None and new_phone is None:
            raise ValueError("An email address or phone number is required.")

        # Validate the pair before assignment so email-only and phone-only
        # contacts can be exchanged without a temporarily invalid state.
        self.__email = new_email
        self.__phone = new_phone

    def __str__(self) -> str:
        """Return a readable summary of the customer."""
        contact_parts = []
        if self.__email is not None:
            contact_parts.append(f"email={self.__email}")
        if self.__phone is not None:
            contact_parts.append(f"phone={self.__phone}")
        return (
            f"Customer {self.__customer_id}: {self.__name}, "
            + ", ".join(contact_parts)
        )
