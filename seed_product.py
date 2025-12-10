from database import SessionLocal, Product, ProductVariant, Supplier, engine, Base

# Ensure tables exist
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# 1. Get an existing supplier (from our previous steps)
supplier = db.query(Supplier).first()

if not supplier:
    print("❌ No suppliers found! Please run seed_supply.py first.")
else:
    # 2. Check if products already exist to avoid duplicates
    if not db.query(Product).first():
        # --- Create Parent Product: T-Shirt ---
        tshirt = Product(
            name="Nike T-Shirt",
            description="Cotton round neck t-shirt",
            category="Clothing",
            supplier_id=supplier.id
        )
        db.add(tshirt)
        db.commit() # Commit to get the ID

        # --- Create Variants for T-Shirt ---
        v1 = ProductVariant(product_id=tshirt.id, sku="TSH-RED-L", attributes="Red, Large", price=25.00, stock_quantity=50)
        v2 = ProductVariant(product_id=tshirt.id, sku="TSH-RED-M", attributes="Red, Medium", price=25.00, stock_quantity=12)
        
        db.add_all([v1, v2])

        # --- Create Parent Product: Monitor ---
        monitor = Product(
            name="Gaming Monitor",
            description="27-inch 144Hz IPS Display",
            category="Electronics",
            supplier_id=supplier.id
        )
        db.add(monitor)
        db.commit()

        # --- Create Variant for Monitor ---
        v3 = ProductVariant(product_id=monitor.id, sku="MON-27-144", attributes="Standard", price=299.99, stock_quantity=8)
        db.add(v3)

        db.commit()
        print("✅ Products and Variants added successfully!")
    else:
        print("⚠️ Products already exist.")

db.close()