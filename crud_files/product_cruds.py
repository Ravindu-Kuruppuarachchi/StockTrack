from sqlalchemy.orm import Session
from datetime import date 
from models import User, Supplier, Product, Order, Sale
from typing import Optional
from crud_files import login_cruds,supplier_cruds, product_cruds,sale_cruds,order_cruds


def get_all_products(db: Session):
    return db.query(Product).all() 

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()   


def get_product_by_name(db: Session, product_name: str):
    return db.query(Product).filter(Product.name == product_name).first()


def get_products_filtered(db: Session, search: Optional[str] = None, category: Optional[str] = None):
    # Start the query
    query = db.query(Product)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    
    if category and category != "All Categories":
        query = query.filter(Product.category == category)
        
    return query.all()

def update_product_details(db: Session, product_id: int, name: str, category: str, description: str, stocks: int, selling_price: float, buying_price: float):
    product = get_product_by_id(db, product_id)
    if product:
        product.name = name  # type: ignore
        product.description = description  # type: ignore
        product.category = category  # type: ignore
        product.stocks = stocks  # type: ignore
        product.selling_price = selling_price  # type: ignore
        product.buying_price = buying_price  # type: ignore
        db.commit()
    return product

def delete_product(db: Session, product: Product):
    db.delete(product)
    db.commit()


def create_product(db: Session, name: str, description: str, category: str, supplier_id: int):
    new_product = Product(
        name=name,
        description=description,
        category=category,
        stocks=0,
        selling_price=0.0,
        buying_price=0.0,
        supplier_id=supplier_id
    )
    db.add(new_product)
    db.commit()

    supplier = supplier_cruds.get_supplier_by_id(db, supplier_id)
    if supplier:
        current_products = str(supplier.products)
        
        if current_products:
            # Check if product already exists to avoid duplicates
            product_list = [p.strip() for p in current_products.split(",")]
            if name not in product_list:
                new_products = current_products + f", {name}"
                setattr(supplier, "products", new_products)
        else:
            setattr(supplier, "products", name)
        db.commit()


    return new_product