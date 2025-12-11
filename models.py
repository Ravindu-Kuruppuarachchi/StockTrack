from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from database import Base

# MODELS

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact = Column(String)
    products = Column(String)  # Comma-separated items
    payment_status = Column(Boolean, default=False)
    last_order_qty = Column(Integer, default=0)
    total_due = Column(Float, default=0.0)
    last_order_received = Column(Boolean, default=False)
    last_order_date = Column(Date, nullable=True)


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    category = Column(String)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    
    # Relationships
    supplier = relationship("Supplier", backref="products_list")
    variants = relationship("ProductVariant", backref="product")


class ProductVariant(Base):
    __tablename__ = "product_variants"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    sku = Column(String, unique=True, index=True)
    attributes = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    product_names = Column(String)
    quantity = Column(Integer)
    total_cost = Column(Float)
    order_date = Column(Date)
    status = Column(Boolean, default=False)
    payment_status = Column(Boolean, default=False)
    
    # Relationship to link Order -> Supplier
    supplier = relationship("Supplier", backref="all_orders")


