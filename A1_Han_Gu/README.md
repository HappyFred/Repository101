# Nursery Greenhouse Ordering System

## Overview

This project models the nursery ordering process described by Brent. It keeps
plants, customers, and single-plant orders in memory. The driver demonstrates
the normal workflow and the validation needed to protect stock and order data.

The program uses object-oriented design with classes, private attributes,
properties, validation, object relationships, and customised `__str__`
methods.

add notes

## Class responsibilities

### `Plant`

`Plant` owns plant details and stock rules. Its price property rejects zero or
negative values. Its stock methods accept only positive quantities and never
allow stock to fall below zero.
`stock_level` has a validated setter for assigning a stock value, while
`increase_stock()` and `reduce_stock()` are used for operations that change
stock by a quantity.

### `Customer`

`Customer` owns customer identity and contact details. It requires an email or
phone number but does not attempt to validate either format because Brent did
not define formatting rules. `update_contact()` validates both values together
so the contact details remain valid when switching between email-only and
phone-only contact.

### `Order`

`Order` records one customer ordering one plant type. It validates quantity and
date, starts as pending, calculates any bulk discount, and controls its own
status transitions. It deliberately does not change plant stock.
Payment settlement is intentionally outside the system scope because Brent
said that it does not need to be tracked in this version.

### `NurserySystem`

`NurserySystem` coordinates the collections and business workflow. It adds and
finds objects, performs stock enquiries, places orders, restores stock after a
valid cancellation, records collection, returns reports, and exposes focused
update operations. Its update methods use the validation already provided by
the relevant class instead of repeating the same checks.

## Identity and collections

Plant and customer names are not unique. IDs distinguish different plants or
people that happen to share a name, so the system stores them in dictionaries
keyed by ID. Dictionary keys also make duplicate detection and lookup direct.

Brent did not specify an order identifier, but orders need a stable identity for
lookup, cancellation, and collection. The system therefore generates unique
IDs in the sequence `ORD001`, `ORD002`, and so on. Only successful orders use
the next number.

Absence is a valid search result, so `find_plant()`, `find_customer()`, and
`find_order()` return `None` when an ID is not found. Other operations
require the referenced record to exist, so methods such as `check_stock()`,
`place_order()`, and `update_plant_price()` raise `ValueError` for an
unknown ID.

Identifiers are read-only after construction. The customer, plant, quantity,
date, and total of an existing order are also read-only because changing them
would rewrite the meaning of a transaction. Properties with setters are
provided only for values that need to change, while getter-only properties
protect identity and historical facts.

## Stock and order integrity

An order is constructed successfully before stock is reduced and before the
order is stored. Invalid dates, quantities, missing records, and insufficient stock are rejected before an order is stored or stock is reduced.

Stock is deducted immediately when an order is placed. Cancellation is allowed
only while an order is pending. The order validates that transition before the
system restores stock, which prevents repeated cancellation from restoring the
same quantity twice. Cancelled orders cannot later be collected, and collected
orders cannot be cancelled.

Orders of 10 or more units receive a 10% discount. The total is rounded to two
decimal places and captured when the order is created. Later plant price changes
affect future orders only; they do not change historical totals.

## Material assumptions and design decisions

- Order IDs are required even though Brent did not specify them, and the system
  generates them automatically.
- All identifiers are read-only after object construction.
- A plant price must be greater than zero.
- A plant category must exactly match one of Brent's four supplied categories:
  trees and shrubs, perennials, pot plants, or vegetable seedlings.
- A cancelled order cannot later be collected.
- An order total is captured at creation and is unaffected by later prices.
- An available plant is one with `stock_level > 0`.
- Email or phone presence is checked, but their formats are not validated.
- Cancelled orders remain recorded and appear in customer order history.
- Dates must be real calendar dates in exact `DD-MM-YYYY` form. Future dates are
  allowed because the brief does not prohibit them.

## Driver demonstration

`main.py` demonstrates:

- valid plant and customer creation;
- duplicate ID rejection and duplicate-name acceptance;
- invalid price, category, contact, quantity, stock, and date handling;
- stock enquiry, immediate deduction, exact-stock ordering, and failed-order
  stock integrity;
- ordinary and discounted totals;
- cancellation, one-time stock restoration, collection, and invalid status
  transitions;
- plant price, restock, and atomic customer-contact updates through
  `NurserySystem`;
- immutable historical totals;
- customer history and all required collection listings.

Expected validation failures are caught and printed so the driver continues to
demonstrate the remaining behaviour.

## Running the program

Python 3.10 or later is required because the code uses modern union and built-in
collection type-hint syntax. From the directory containing the files, run:

```text
python main.py
```
