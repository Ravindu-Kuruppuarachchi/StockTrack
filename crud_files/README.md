# CRUD Operations Module

This folder contains the database CRUD (Create, Read, Update, Delete) operations for the Inventory Management System. Each file handles a specific entity and provides functions that are called by the FastAPI routes in `main.py`.

## Overview

The CRUD layer provides a clean separation between the API routes and database operations. All functions use SQLAlchemy ORM for database interactions and accept a database session (`db: Session`) as the first parameter.

## Directory Structure

```
crud_files/
├── login_cruds.py      # User authentication operations
├── product_cruds.py    # Product management operations
├── supplier_cruds.py   # Supplier management operations
├── sale_cruds.py       # Sales tracking operations
├── order_cruds.py      # Order management operations
└── README.md           # This file
```

## File Descriptions

### login_cruds.py
Handles user authentication and management.

**Functions:**
| Function | Description | Parameters |
|----------|-------------|------------|
| `get_user_by_username()` | Find user by username | `db`, `username` |
| `verify_password()` | Verify password hash | `plain_password`, `hashed_password` |
| `authenticate_user()` | Complete login flow | `db`, `username`, `password` |
| `create_user()` | Register new user | `db`, `username`, `password`, `email` |

**Usage Example:**
```python
from crud_files.login_cruds import authenticate_user

user = authenticate_user(db, "admin", "password123")
if user:
    # Login successful
```

---

### product_cruds.py
Manages product inventory operations.

**Functions:**
| Function | Description | Parameters |
|----------|-------------|------------|
| `get_all_products()` | List all products | `db` |
| `get_product_by_id()` | Find product by ID | `db`, `product_id` |
| `get_product_by_name()` | Find product by name | `db`, `product_name` |
| `get_products_filtered()` | Search/filter products | `db`, `search`, `category` |
| `create_product()` | Add new product | `db`, `name`, `description`, `category`, `supplier_id` |
| `update_product_details()` | Update product info | `db`, `product_id`, `name`, `category`, etc. |
| `delete_product()` | Remove product | `db`, `product` |

**Usage Example:**
```python
from crud_files.product_cruds import get_products_filtered

# Search for products containing "laptop" in "Electronics" category
products = get_products_filtered(db, search="laptop", category="Electronics")
```

---

### supplier_cruds.py
Handles supplier information and relationships.

**Functions:**
| Function | Description | Parameters |
|----------|-------------|------------|
| `get_all_suppliers()` | List all suppliers | `db` |
| `get_supplier_by_id()` | Find supplier by ID | `db`, `supplier_id` |
| `get_supplier_by_name()` | Find supplier by name | `db`, `supplier_name` |
| `create_supplier()` | Add new supplier | `db`, `name`, `email`, `phone`, `address` |
| `update_supplier()` | Update supplier info | `db`, `supplier_id`, ... |
| `delete_supplier()` | Remove supplier | `db`, `supplier` |
| `get_suppliers_with_dues()` | Suppliers with pending payments | `db` |

**Usage Example:**
```python
from crud_files.supplier_cruds import get_suppliers_with_dues

# Get suppliers who have outstanding payments
suppliers_with_dues = get_suppliers_with_dues(db)
```

---

### sale_cruds.py
Manages sales transactions and reporting.

**Functions:**
| Function | Description | Parameters |
|----------|-------------|------------|
| `get_all_sales()` | List all sales | `db` |
| `get_sale_by_id()` | Find sale by ID | `db`, `sale_id` |
| `get_sales_by_product()` | Sales for a product | `db`, `product_id` |
| `get_sales_by_date_range()` | Sales within dates | `db`, `start_date`, `end_date` |
| `create_sale()` | Record new sale | `db`, `product_id`, `quantity`, `total_amount` |
| `get_monthly_sales_total()` | Monthly revenue | `db`, `month`, `year` |
| `delete_sale()` | Remove sale record | `db`, `sale` |

**Usage Example:**
```python
from crud_files.sale_cruds import create_sale

# Record a new sale
new_sale = create_sale(
    db,
    product_id=1,
    quantity=5,
    total_amount=499.95
)
```

---

### order_cruds.py
Handles purchase orders to suppliers.

**Functions:**
| Function | Description | Parameters |
|----------|-------------|------------|
| `get_all_orders()` | List all orders | `db` |
| `get_order_by_id()` | Find order by ID | `db`, `order_id` |
| `get_orders_by_supplier()` | Orders from supplier | `db`, `supplier_id` |
| `get_pending_orders()` | Unfulfilled orders | `db` |
| `create_order()` | Place new order | `db`, `supplier_id`, `product_id`, `quantity` |
| `update_order_status()` | Mark order complete | `db`, `order_id`, `status` |
| `get_monthly_orders_count()` | Orders this month | `db` |

**Usage Example:**
```python
from crud_files.order_cruds import create_order

# Place order with supplier
new_order = create_order(
    db,
    supplier_id=1,
    product_id=5,
    quantity=100
)
```

## Architecture Pattern

```
┌─────────────────────┐
│     main.py         │  ← FastAPI Routes
│   (API Endpoints)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    crud_files/      │  ← Business Logic
│  (CRUD Operations)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     models.py       │  ← SQLAlchemy Models
│  (Database Schema)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    database.py      │  ← Database Connection
│   (Session/Engine)  │
└─────────────────────┘
```

## Database Models Used

Each CRUD file interacts with models defined in `models.py`:

| CRUD File | Primary Model | Related Models |
|-----------|---------------|----------------|
| `login_cruds.py` | `User` | - |
| `product_cruds.py` | `Product` | `Supplier` |
| `supplier_cruds.py` | `Supplier` | `Product`, `Order` |
| `sale_cruds.py` | `Sale` | `Product` |
| `order_cruds.py` | `Order` | `Supplier`, `Product` |

## Best Practices Used

1. **Session Management**: All functions receive `db: Session` - the caller manages the session lifecycle.

2. **Type Hints**: Functions use type hints for better code clarity:
   ```python
   def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
   ```

3. **Query Building**: Complex queries use SQLAlchemy's query builder:
   ```python
   query = db.query(Product)
   if search:
       query = query.filter(Product.name.ilike(f"%{search}%"))
   return query.all()
   ```

4. **Commit Control**: Functions that modify data call `db.commit()`:
   ```python
   db.add(new_product)
   db.commit()
   db.refresh(new_product)
   return new_product
   ```

## Usage in FastAPI Routes

```python
# In main.py
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from crud_files import product_cruds

@app.get("/products")
def list_products(db: Session = Depends(get_db)):
    return product_cruds.get_all_products(db)

@app.post("/products")
def create_product(name: str, db: Session = Depends(get_db)):
    return product_cruds.create_product(db, name=name, ...)
```

## Testing

To test CRUD operations:

```python
from database import SessionLocal
from crud_files import product_cruds

# Create a test session
db = SessionLocal()

try:
    # Test get all products
    products = product_cruds.get_all_products(db)
    print(f"Found {len(products)} products")
    
    # Test filtered search
    filtered = product_cruds.get_products_filtered(db, search="test")
    print(f"Filtered: {len(filtered)} products")
finally:
    db.close()
```

## Related Documentation

- [Main README](../README.md) - Project overview
- [models.py](../models.py) - Database models
- [database.py](../database.py) - Database connection setup
- [Helm Chart](../helm/inventory-app/README.md) - Kubernetes deployment
