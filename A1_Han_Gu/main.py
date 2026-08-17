"""Driver program demonstrating the nursery ordering system."""

from collections.abc import Sequence

from customer import Customer
from nursery_system import NurserySystem
from plant import Plant


def check(description: str, condition: bool) -> None:
    """Print whether a Boolean correctness check passes or fails."""
    if condition:
        print(f"PASS - {description}")
    else:
        print(f"FAIL - {description}")


def print_items(
    heading: str,
    items: Sequence[object],
) -> None:
    """Print a heading followed by readable collection items."""
    print(f"\n{heading}")
    for item in items:
        print(f"  {item}")


def main() -> None:
    """Demonstrate normal operations, validation, and boundary cases."""
    nursery = NurserySystem()
    print(nursery)

    # Identity and object validation
    plants = [
        Plant("P001", "Griselinia", "trees and shrubs", 12.50, 30),
        Plant("P002", "Lavender", "perennials", 7.25, 20),
        Plant("P003", "Fern", "pot plants", 15.00, 5),
        Plant("P004", "Tomato", "vegetable seedlings", 3.40, 0),
        Plant("P005", "Griselinia", "trees and shrubs", 13.00, 6),
    ]
    for plant in plants:
        nursery.add_plant(plant)

    customers = [
        Customer("C001", "Alex Smith", "alex@example.com", None),
        Customer("C002", "Alex Smith", None, "021-555-0102"),
        Customer("C003", "Mia Chen", "mia@example.com", "021-555-0103"),
    ]
    for customer in customers:
        nursery.add_customer(customer)

    print("\nPASS - valid plants and customers added")
    print("PASS - same customer names accepted under different IDs")
    print("PASS - same plant names accepted under different IDs")

    try:
        nursery.add_plant(
            Plant("P001", "Kowhai", "trees and shrubs", 20.00, 2)
        )
    except ValueError as error:
        print(f"PASS - duplicate plant ID rejected: {error}")
    else:
        print(
            "FAIL - duplicate plant ID rejected: "
            "no ValueError was raised"
        )

    try:
        nursery.add_customer(
            Customer("C001", "Different Name", None, "021-000-0000")
        )
    except ValueError as error:
        print(f"PASS - duplicate customer ID rejected: {error}")
    else:
        print(
            "FAIL - duplicate customer ID rejected: "
            "no ValueError was raised"
        )

    try:
        Plant("P010", "Rose", "perennials", -1.00, 4)
    except ValueError as error:
        print(f"PASS - negative price rejected: {error}")
    else:
        print(
            "FAIL - negative price rejected: "
            "no ValueError was raised"
        )

    try:
        Plant("P012", "Rose", "perennials", 8.00, -1)
    except ValueError as error:
        print(f"PASS - negative initial stock rejected: {error}")
    else:
        print(
            "FAIL - negative initial stock rejected: "
            "no ValueError was raised"
        )

    try:
        Plant("P011", "Rose", "flowers", 8.00, 4)
    except ValueError as error:
        print(f"PASS - invalid category rejected: {error}")
    else:
        print(
            "FAIL - invalid category rejected: "
            "no ValueError was raised"
        )

    try:
        Customer("C010", "No Contact", None, None)
    except ValueError as error:
        print(f"PASS - missing customer contact rejected: {error}")
    else:
        print(
            "FAIL - missing customer contact rejected: "
            "no ValueError was raised"
        )

    check(
        "find_plant located P001",
        nursery.find_plant("P001") is plants[0],
    )
    check(
        "find_customer located C001",
        nursery.find_customer("C001") is customers[0],
    )

    # Ordering, stock, and discount rules
    print(
        "\nStock enquiry: P001 has 8 available =",
        nursery.check_stock("P001", 8),
    )

    normal_order = nursery.place_order("C001", "P001", 4, "12-08-2026")
    print("PASS - normal order below 10 units:", normal_order)
    check(
        "stock immediately reduced after normal order",
        plants[0].stock_level == 26,
    )
    check(
        "find_order located the normal order",
        nursery.find_order(normal_order.order_id) is normal_order,
    )

    discount_order = nursery.place_order("C001", "P002", 10, "12-08-2026")
    check(
        "10-unit order receives 10% discount",
        discount_order.order_total == 65.25,
    )

    equal_stock_order = nursery.place_order(
        "C002", "P003", 5, "13-08-2026"
    )
    check(
        "quantity equal to available stock leaves zero stock",
        plants[2].stock_level == 0,
    )

    stock_before_failure = plants[0].stock_level
    try:
        nursery.place_order("C003", "P001", 100, "13-08-2026")
    except ValueError as error:
        print(f"PASS - insufficient-stock order rejected: {error}")
    else:
        print(
            "FAIL - insufficient-stock order rejected: "
            "no ValueError was raised"
        )
    check(
        "stock unchanged after failed order",
        plants[0].stock_level == stock_before_failure,
    )

    try:
        nursery.place_order("C003", "P001", 0, "13-08-2026")
    except ValueError as error:
        print(f"PASS - zero order quantity rejected: {error}")
    else:
        print(
            "FAIL - zero order quantity rejected: "
            "no ValueError was raised"
        )

    try:
        nursery.place_order("C003", "P001", -2, "13-08-2026")
    except ValueError as error:
        print(f"PASS - negative order quantity rejected: {error}")
    else:
        print(
            "FAIL - negative order quantity rejected: "
            "no ValueError was raised"
        )

    try:
        nursery.place_order("C003", "P001", 1, "31-02-2026")
    except ValueError as error:
        print(f"PASS - impossible date rejected: {error}")
    else:
        print(
            "FAIL - impossible date rejected: "
            "no ValueError was raised"
        )

    try:
        nursery.place_order("C003", "P001", 1, "1-8-2026")
    except ValueError as error:
        print(f"PASS - non-zero-padded date format rejected: {error}")
    else:
        print(
            "FAIL - non-zero-padded date format rejected: "
            "no ValueError was raised"
        )

    # Status transitions
    stock_before_cancel = plants[0].stock_level
    nursery.cancel_order(normal_order.order_id)
    check(
        "pending cancellation restored stock",
        plants[0].stock_level == stock_before_cancel + normal_order.quantity,
    )
    stock_after_cancel = plants[0].stock_level
    try:
        nursery.cancel_order(normal_order.order_id)
    except ValueError as error:
        print(f"PASS - repeated cancellation rejected: {error}")
    else:
        print(
            "FAIL - repeated cancellation rejected: "
            "no ValueError was raised"
        )
    check(
        "repeated cancellation did not restore stock twice",
        plants[0].stock_level == stock_after_cancel,
    )

    nursery.collect_order(discount_order.order_id)
    try:
        nursery.cancel_order(discount_order.order_id)
    except ValueError as error:
        print(f"PASS - collected order cannot be cancelled: {error}")
    else:
        print(
            "FAIL - collected order cannot be cancelled: "
            "no ValueError was raised"
        )

    try:
        nursery.collect_order(normal_order.order_id)
    except ValueError as error:
        print(f"PASS - cancelled order cannot be collected: {error}")
    else:
        print(
            "FAIL - cancelled order cannot be collected: "
            "no ValueError was raised"
        )

    # Updates and reporting
    old_total = equal_stock_order.order_total
    nursery.update_plant_price("P003", 18.50)
    check("NurserySystem updated plant price", plants[2].price == 18.50)
    check(
        "historical order total stayed fixed",
        equal_stock_order.order_total == old_total,
    )
    nursery.restock_plant("P003", 7)
    check("NurserySystem restocked plant", plants[2].stock_level == 7)
    nursery.update_customer_contact("C001", None, "021-555-0199")
    check(
        "customer contact changed atomically to phone-only",
        customers[0].email is None
        and customers[0].phone == "021-555-0199",
    )
    try:
        nursery.update_plant_price("P001", 0)
    except ValueError as error:
        print(
            "PASS - invalid managed price update rejected by Plant: "
            f"{error}"
        )
    else:
        print(
            "FAIL - invalid managed price update rejected by Plant: "
            "no ValueError was raised"
        )

    try:
        nursery.restock_plant("P001", 0)
    except ValueError as error:
        print(
            "PASS - invalid managed restock rejected by Plant: "
            f"{error}"
        )
    else:
        print(
            "FAIL - invalid managed restock rejected by Plant: "
            "no ValueError was raised"
        )

    try:
        nursery.update_customer_contact("C001", None, None)
    except ValueError as error:
        print(
            "PASS - missing managed contact rejected by Customer: "
            f"{error}"
        )
    else:
        print(
            "FAIL - missing managed contact rejected by Customer: "
            "no ValueError was raised"
        )

    print_items(
        "Customer C001 order history (cancelled orders retained):",
        nursery.get_customer_order_history("C001"),
    )
    print_items("All plants:", nursery.get_all_plants())
    print_items(
        "Available plants (stock > 0):",
        nursery.get_available_plants(),
    )
    print_items("All customers:", nursery.get_all_customers())
    print_items("All orders:", nursery.get_all_orders())
    print("\nFinal system summary:", nursery)


if __name__ == "__main__":
    main()
