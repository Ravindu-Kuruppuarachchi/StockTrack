from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from passlib.context import CryptContext
from datetime import date 

# Make sure these are in your database.py file
from database import get_db, User, Supplier, Product, Order

app = FastAPI(title="Inventory Management System")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_submit(
    request: Request, 
    email: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    
    if not user or password != user.password:
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Invalid email or password"
        })
    
    response = RedirectResponse(url="/dashboard", status_code=303)
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("user_session")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# --- SUPPLIERS ROUTES ---

@app.get("/suppliers", response_class=HTMLResponse)
async def read_suppliers(request: Request, db: Session = Depends(get_db)):
    suppliers_db = db.query(Supplier).all()
    
    suppliers_list = []
    for s in suppliers_db:
        # Handle product string splitting safely
        product_list = [{"name": p.strip(), "unit_price": 0} for p in s.products.split(",")] if s.products else []
        
        suppliers_list.append({
            "id": s.id,
            "name": s.name,
            "contact": s.contact,
            "products": product_list,
            "payment_status": s.payment_status,
            "total_due": s.total_due,
            "last_order_qty": s.last_order_qty,
            "last_order_received": s.last_order_received,
            "last_order_date": s.last_order_date
        })

    return templates.TemplateResponse("suppliers.html", {"request": request, "suppliers": suppliers_list})

# --- PRODUCTS ROUTES ---

@app.get("/products", response_class=HTMLResponse)
async def product_list(request: Request, db: Session = Depends(get_db)):
    products_db = db.query(Product).all()
    
    products_formatted = []
    for p in products_db:
        products_formatted.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "category": p.category,
            "supplier": p.supplier.name if p.supplier else "Unknown",
            "variants": [
                {
                    "sku": v.sku, 
                    "attributes": v.attributes, 
                    "price": v.price, 
                    "stock": v.stock_quantity
                } 
                for v in p.variants
            ]
        })

    return templates.TemplateResponse("products_list.html", {"request": request, "products": products_formatted})

@app.get("/products/create", response_class=HTMLResponse)
async def product_create(request: Request):
    return templates.TemplateResponse("product_create.html", {"request": request})

# --- ORDER ROUTES ---

# --- 1. VIEW ALL ORDERS ROUTE ---
@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request, db: Session = Depends(get_db)):
    # Fetch orders, newest first
    orders_data = db.query(Order).order_by(Order.id.desc()).all()
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders_data})

# --- 2. PLACE ORDER FORM PAGE ---
@app.get("/orders/place", response_class=HTMLResponse)
async def place_order_form(request: Request, supplier_id: int = None, db: Session = Depends(get_db)):
    suppliers_db = db.query(Supplier).all()
    return templates.TemplateResponse("place_order.html", {
        "request": request, 
        "suppliers": suppliers_db,
        "selected_id": supplier_id
    })

# --- 3. PLACE ORDER SUBMISSION ---
@app.post("/orders/place")
async def place_order_submit(
    supplier_id: int = Form(...),
    product_name: str = Form(...),
    quantity: int = Form(...),
    total_cost: float = Form(0.0),
    db: Session = Depends(get_db)
):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    
    if supplier:
        # Update Supplier Stats
        supplier.last_order_qty = quantity
        supplier.last_order_received = False
        supplier.last_order_date = date.today()
        supplier.total_due = (getattr(supplier, "total_due", 0.0) or 0.0) + total_cost
        supplier.payment_status = False

        # Create History Record
        new_order = Order(
            supplier_id=supplier.id,
            product_names=product_name, 
            quantity=quantity,
            total_cost=total_cost,
            order_date=date.today(),
            status="Pending"
        )
        db.add(new_order)
        
        # Update Supplier Product List String
        current_products = getattr(supplier, "products", "")
        if current_products and isinstance(current_products, str):
            # Check if product already exists in the comma-separated list
            product_list = [p.strip() for p in current_products.split(",")]
            if product_name not in product_list:
                supplier.products = current_products + f", {product_name}"
        else:
            supplier.products = product_name

        db.commit()
    
    return RedirectResponse(url="/orders", status_code=303)