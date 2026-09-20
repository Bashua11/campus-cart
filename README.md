# CampusCart

## Project Overview

CampusCart is a command-line interface (CLI) solution designed to help campus vendors manage stock, calculate cart totals, and generate receipts.

## Problem Statement

## Problem Statement

Campus vendors often struggle to keep accurate records of their inventory and sales, which can lead to poor stock management and financial losses. CampusCart addresses this problem by providing a simple platform where vendors can track inventory and sales efficiently.

## Target Audience

CampusCart is designed for:
- Student business owners
- Campus-based vendors
- Pop-up vendors who need a simple way to manage their inventory and sales

## Key Value Propositions

- Easy sales tracking
- Simple inventory management
- Quick and accurate receipt generation
CampusCart Pricing: ₦1,000 monthly subscription.

## CLI Mockup

```text id="bzmd84"
1. View Inventory

================================
          CAMPUSCART
================================

1. View Inventory
2. Add Item to Cart
3. View Cart
4. Checkout
5. Exit

Select an option: _
```### Inventory Screen

```text
================================
        CURRENT INVENTORY
================================

Item                    Quantity
--------------------------------
Red Gowns                  4
Black Shoes               20
Milk Jugs                   2

--------------------------------
Total Items:              26
```

## User Personas

### Ada - Student Fashion Vendor

Ada is a university student who sells clothes and shoes to other students on campus. She needs a simple way to track available inventory, monitor sales, and reduce errors when managing customer purchases.

**Needs:**
- Keep track of available stock
- Record sales easily
- Calculate customer purchases accurately
- Generate receipts for customers
## Proposed Feature Milestones

### Milestone 1: Inventory Management
- Add and remove products
- Update product quantities
- View available stock

### Milestone 2: Sales and Cart Management
- Add products to a customer's cart
- Calculate cart totals
- Record completed sales

### Milestone 3: Receipt Generation
- Generate a simple receipt after checkout
- Display purchased items, quantities, and total cost

### Milestone 4: Sales Summary
- View total sales
- Track products sold
- Review remaining inventory


## Stage 2: Procedural Python CLI

In Stage 2, I developed CampusCart into an interactive command-line
shopping application using procedural Python.

### Features Implemented

- View the available product catalog with prices and stock levels
- Add products to the cart using product IDs
- Select product quantities
- View cart items and total cost
- Validate product IDs and quantity inputs
- Prevent purchases that exceed available stock
- Apply a 10% discount to orders above $20
- Generate an itemized checkout receipt
- Update inventory after checkout
- Exit the application through the main menu

### Python Concepts Applied

- Dictionaries and nested dictionaries
- Lists
- `while` and `for` loops
- `if`, `elif`, and `else`
- User input and type conversion
- `try` and `except` for input validation
- Calculations and string formatting
- Git and GitHub version control

## CLI Demo

The screenshot below shows CampusCart running from the command line.

![CampusCart CLI Demo](campuscart-cli.png)