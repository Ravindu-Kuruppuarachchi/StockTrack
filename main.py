from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
import crud

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
    user = crud.get_user_by_email(db, email)

    if not user or password != user.password:
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Invalid email or password"
        })
    
    response = RedirectResponse(url="/products", status_code=303)
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("user_session")
    return response

@app.get("/login/update", response_class=HTMLResponse)
async def update_login(request: Request):
    return templates.TemplateResponse("add_user.html", {"request": request})


@app.post("/login/update")
async def update_login_submit( 
    action: str = Form(...),
    email: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, email)
    
    if action == "delete":
        if user:
            crud.delete_user(db, user)
        return RedirectResponse(url="/login", status_code=303)
    
    if action == "update":
        if user:
            crud.update_user_password(db, user, password)
            return RedirectResponse(url="/products", status_code=303)
        else:
            crud.create_user(db, email, password)
            return RedirectResponse(url="/products", status_code=303)
    
    return RedirectResponse(url="/products", status_code=303)

# SUPPLIERS ROUTES
@app.get("/suppliers", response_class=HTMLResponse)
async def read_suppliers(request: Request, db: Session = Depends(get_db)):
    suppliers_db = crud.get_all_suppliers(db)
    
    suppliers_list = []
    for s in suppliers_db:
        # Handle product string splitting safely
        product_list = [{"name": p.strip(), "unit_price": 0} for p in s.products.split(",")] 
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

# PRODUCTS ROUTES
@app.get("/products", response_class=HTMLResponse)
async def product_list(request: Request, db: Session = Depends(get_db)):
    products_db = crud.get_all_products(db)
    
    products_formatted = []
    for p in products_db:
        products_formatted.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "category": p.category,
            "supplier": p.supplier.name if p.supplier else "Unknown",
            "stock": p.stocks,
            
            "selling_price": p.selling_price, 
            "buying_price": p.buying_price
        })

    return templates.TemplateResponse("products_list.html", {"request": request, "products": products_formatted})



@app.get("/products/create", response_class=HTMLResponse)
async def product_create(request: Request, db: Session = Depends(get_db)):

    suppliers_list = crud.get_all_suppliers(db)

    return templates.TemplateResponse("product_create.html", {
        "request": request, 
        "suppliers": suppliers_list}
    )

@app.post("/products/create") 
async def product_create_submit(
    product_name: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    supplier_id: int = Form(...),
    db: Session = Depends(get_db)

):
    crud.create_product(
        db, 
        name=product_name,
        description=description,
        category=category,
        supplier_id= supplier_id #type: ignore
    )

    return RedirectResponse(url="/products", status_code=303)

# ORDER ROUTES
@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request, db: Session = Depends(get_db)):
    # Fetch orders, newest first
    orders_data = crud.get_all_orders(db)
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders_data})

# 2. PLACE ORDER FORM PAGE
@app.get("/orders/new", response_class=HTMLResponse)
async def place_order_form(request: Request, supplier_id: int, db: Session = Depends(get_db)):
    suppliers_db = crud.get_all_suppliers(db)
    return templates.TemplateResponse("place_order.html", {
        "request": request, 
        "suppliers": suppliers_db,
        "selected_id": supplier_id
    })

# 3. PLACE ORDER SUBMISSION 
@app.post("/orders/place")
async def place_order_submit(
    supplier_id: int = Form(...),
    product_name: str = Form(...),
    quantity: int = Form(...),
    total_cost: float = Form(0.0),
    db: Session = Depends(get_db)
):
    supplier = crud.get_supplier_by_id(db, supplier_id)

    if supplier:
        crud.create_order(db, supplier_id, product_name, quantity, total_cost)
    
    return RedirectResponse(url="/orders", status_code=303)


@app.post("/orders/{order_id}/update")
async def update_order_status(
    order_id: int, 
    action: str = Form(...), # Takes 'receive' or 'pay'
    db: Session = Depends(get_db)
):
    order = crud.get_order_by_id(db, order_id)
    if not order:
        return RedirectResponse(url="/orders", status_code=303)

    crud.update_order_state(db, order_id, action)
    return RedirectResponse(url="/orders", status_code=303)

@app.get("/supplier/newsupplier", response_class=HTMLResponse)
async def add_suppier(request: Request):
    return templates.TemplateResponse("add_supplier.html", {"request": request})

@app.get("/suppliers/{supplier_id}/update", response_class=HTMLResponse)
async def edit_supplier_form(
    request: Request,
    supplier_id: int, 
    db: Session = Depends(get_db)):

    supplier = crud.get_supplier_by_id(db, supplier_id)
    return templates.TemplateResponse("update_supplier.html", {
        "request": request, 
        "supplier": supplier
    })

@app.post("/suppliers/{supplier_id}/update", response_class=HTMLResponse)
async def edit_supplier_submit(
    supplier_id: int,
    action: str = Form(...),
    supplier_name: str = Form(...),
    contact_number: str = Form(...),
    items: str = Form(""),
    total_due: float = Form(0.0),
    db: Session = Depends(get_db)
):
    if action == "update":
        crud.update_supplier_details(db, supplier_id, supplier_name, contact_number, items, total_due)
        return RedirectResponse(url="/suppliers", status_code=303)
    
    if action == "delete":
        supplier = crud.get_supplier_by_id(db, supplier_id)
        crud.delete_supplier(db, supplier)
        return RedirectResponse(url="/suppliers", status_code=303)


@app.post("/suppliers/place")
async def add_supplier_submit(
    supplier_name: str = Form(...),
    contact_number: str = Form(...),
    db: Session = Depends(get_db)
):
    crud.create_supplier(db,supplier_name=supplier_name, contact_number=contact_number)
    return RedirectResponse(url="/suppliers", status_code=303)


@app.get("/sales", response_class=HTMLResponse)
async def sales_list(request: Request, db: Session = Depends(get_db)):
    sales_data = crud.get_all_sales(db)
    return templates.TemplateResponse("sales.html", {"request": request, "sales": sales_data})

@app.get("/sales/new", response_class=HTMLResponse)
async def new_sale_form(request: Request, db: Session = Depends(get_db)):
    products = crud.get_all_products(db)
    return templates.TemplateResponse("add_sale.html", {"request": request, "products": products})

@app.post("/sales/add")
async def add_sale_submit(
    product_name: str = Form(...),
    quantity: int = Form(...),
    total_amount: float = Form(...),
    db: Session = Depends(get_db)
):
    crud.create_sale(db, product_name, quantity, total_amount)
    return RedirectResponse(url="/sales", status_code=303)

@app.get("/products/{product_id}/update", response_class=HTMLResponse)
async def edit_product_form(
    request: Request,
    product_id: int, 
    db: Session = Depends(get_db)):

    product = crud.get_product_by_id(db, product_id)
    suppliers_list = crud.get_all_suppliers(db)

    return templates.TemplateResponse("update_product.html", {
        "request": request, 
        "product": product,
        "suppliers": suppliers_list
    })



@app.post("/product/{product_id}/update", response_class=HTMLResponse)
async def edit_product_submit(
    product_id: int,
    action: str = Form(...),
    product_name: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    stocks: int = Form(...),
    selling_price: float = Form(...),
    buying_price: float = Form(...),
    db: Session = Depends(get_db)
):
    if action == "update":
        crud.update_product_details(
            db, 
            product_id, 
            product_name, 
            category, 
            description, 
            stocks, 
            selling_price,
            buying_price
        )
        return RedirectResponse(url="/products", status_code=303)
    
    if action == "delete":
        product = crud.get_product_by_id(db, product_id)
        crud.delete_product(db, product)
        return RedirectResponse(url="/products", status_code=303)
    return RedirectResponse(url="/products", status_code=303)
