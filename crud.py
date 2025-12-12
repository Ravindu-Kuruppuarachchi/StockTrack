from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from passlib.context import CryptContext
from datetime import date 

from models import User, Supplier, Product, Order, Sale
from database import get_db


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()

def update_user_password(db: Session, user: User, new_password: str):
    user.password = new_password  # type: ignore
    db.commit()

def create_user(db: Session, email: str, password: str):    
    new_user = User(email=email, password=password)
    db.add(new_user)
    db.commit()

def get_supplier_by_id(db: Session, supplier_id: int):
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()

def get_all_suppliers(db: Session):
    return db.query(Supplier).all() 

def get_all_products(db: Session):
    return db.query(Product).all() 

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()   

def get_all_orders(db: Session):    
    return db.query(Order).order_by(Order.id.desc()).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def create_supplier(db: Session, supplier_name: str, contact_number: str):
    new_supplier = Supplier(
        name=supplier_name,
        contact=contact_number,
        products="",
        payment_status=True,
        total_due=0.0,
        last_order_received=True,
        last_order_date=None
    )
    db.add(new_supplier)
    db.commit()

def get_product_by_name(db: Session, product_name: str):
    return db.query(Product).filter(Product.name == product_name).first()


def update_supplier_details(db: Session, supplier_id: int, supplier_name: str, contact_number: str, items: str, total_due: float):
    supplier = get_supplier_by_id(db, supplier_id)
    if supplier:
        supplier.name = supplier_name  # type: ignore
        supplier.contact = contact_number  # type: ignore
        supplier.products = items  # type: ignore
        supplier.total_due = total_due  # type: ignore

        if total_due <= 0:
            supplier.payment_status = True  # type: ignore
        else:
            supplier.payment_status = False  # type: ignore
        

        db.commit()


def create_order(db: Session, supplier_id: int, product_name: str, quantity: int, total_cost: float):
    supplier = get_supplier_by_id(db, supplier_id)
    
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
        existing_product = get_product_by_name(db, order.product_names) # type: ignore
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


def delete_supplier(db: Session, supplier: Supplier):
    db.delete(supplier)
    db.commit() 
    return None

def get_all_sales(db: Session):
    return db.query(Sale).order_by(Sale.id.desc()).all()

def create_sale(db: Session, product_name: str, quantity: int, total_amount: float):
    new_sale = Sale(
        product_name=product_name,
        quantity=quantity,
        total_amount=total_amount,
        sale_date=date.today()
    )
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    product = get_product_by_name(db, product_name)
    product.stocks -= quantity  # type: ignore
    db.commit() 

    
    return new_sale