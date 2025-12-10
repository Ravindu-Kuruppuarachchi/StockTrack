from database import SessionLocal, Supplier, engine, Base
from datetime import date

# Ensure table exists
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Check if empty
if not db.query(Supplier).first():
    s1 = Supplier(
        name="Acme Corp",
        contact="+1 555-0199",
        products="Steel Rods, Bolts",
        payment_status=False,
        total_due=1250.00,
        last_order_received=True,
        last_order_date=date.today()
    )
    s2 = Supplier(
        name="Global Tech",
        contact="+1 555-0000",
        products="Monitors",
        payment_status=True,
        total_due=0.00,
        last_order_received=True
    )
    
    db.add_all([s1, s2])
    db.commit()
    print("✅ Suppliers added!")
else:
    print("⚠️ Suppliers already exist.")

db.close()