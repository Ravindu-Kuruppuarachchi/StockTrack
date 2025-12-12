from sqlalchemy.orm import Session
from datetime import date 
from models import User, Supplier, Product, Order, Sale
from typing import Optional
from crud_files import login_cruds,supplier_cruds, product_cruds,sale_cruds,order_cruds

def get_all_orders(db: Session):    
    return db.query(Order).order_by(Order.id.desc()).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()



def create_order(db: Session, supplier_id: int, product_name: str, quantity: int, total_cost: float):
    supplier = supplier_cruds.get_supplier_by_id(db, supplier_id)
    
    if supplier:
        # 1. Update Supplier Stats
        supplier.last_order_qty = quantity # type: ignore
        supplier.last_order_received = False #type: ignore
        supplier.last_order_date = date.today() # type: ignore
        current_due = supplier.total_due if supplier.total_due is not None else 0.0 # type: ignore
        supplier.total_due = current_due + total_cost # type: ignore
        supplier.payment_status = False # type: ignore

        # 2. Create Order History Record
        new_order = Order(
            supplier_id=supplier.id,
            product_names=product_name, 
            quantity=quantity,
            total_cost=total_cost,
            order_date=date.today(),
            status=False,
            payment_status=False
        )
        db.add(new_order)
        
        # 3. Update Supplier Product List String
        current_products = str(supplier.products)
        
        if current_products:
            # Check if product already exists to avoid duplicates
            product_list = [p.strip() for p in current_products.split(",")]
            if product_name not in product_list:
                new_products = current_products + f", {product_name}"
                setattr(supplier, "products", new_products)
        else:
            setattr(supplier, "products", product_name)

        db.commit()
        return new_order
    return None

def update_order_state(db: Session, order_id: int, action: str):
    order = get_order_by_id(db, order_id)
    if not order:
        return None
    # Logic to handle Status (Received)
    if action == "receive":
        order.status = True# type: ignore
        if order.supplier:
             order.supplier.last_order_received = True

        unit_price = order.total_cost / order.quantity
        existing_product = product_cruds.get_product_by_name(db, order.product_names) # type: ignore
        if existing_product:
            existing_product.stocks += order.quantity  # type: ignore
            existing_product.buying_price = unit_price  # type: ignore
        else:
            new_product = Product(
                name=order.product_names,
                description="",
                category="Uncategorized",
                stocks=order.quantity,
                selling_price=unit_price * 1.2,  # Assuming a 20% markup
                buying_price=unit_price,
                supplier_id=order.supplier_id
            )
            db.add(new_product)

    # Logic to handle Payment (Paid)
    elif action == "pay":
        order.payment_status = True# type: ignore
        if order.payment_status:# type: ignore
            order.supplier.total_due -= order.total_cost
            if order.supplier.total_due <= 0:
                order.supplier.payment_status = True

    db.commit()
    return order