from sqlalchemy.orm import Session
from datetime import date 
from models import User, Supplier, Product, Order, Sale
from typing import Optional


def get_supplier_by_id(db: Session, supplier_id: int):
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()

def get_all_suppliers(db: Session):
    return db.query(Supplier).all() 

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


def get_supplier_by_name(db: Session, supplier_name: str):
    supplier = db.query(Supplier).filter(Supplier.name == supplier_name).first()
    if supplier:
        return supplier.id
    return None


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

def delete_supplier(db: Session, supplier: Supplier):
    db.delete(supplier)
    db.commit() 
    return None