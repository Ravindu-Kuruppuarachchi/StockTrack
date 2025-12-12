from sqlalchemy.orm import Session
from datetime import date 
from models import User, Supplier, Product, Order, Sale
from typing import Optional
from crud_files import login_cruds,supplier_cruds, product_cruds,sale_cruds,order_cruds

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

    product = product_cruds.get_product_by_name(db, product_name)
    product.stocks -= quantity  # type: ignore
    db.commit() 
    return new_sale




