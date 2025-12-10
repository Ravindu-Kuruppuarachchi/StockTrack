from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="Inventory Management System")

# 1. Setup Templates
templates = Jinja2Templates(directory="templates")

# Auto-redirect to Login)
@app.get("/")
async def root():
    return RedirectResponse(url="/login")

# --- LOGIN ROUTES ---
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_submit(request: Request, email: str = Form(...), password: str = Form(...)):
    # YOUR UPDATED CREDENTIALS
    if email == "admin@isa.com" and password == "airarabia":
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="user_session", value="logged_in")
        return response
    else:
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Invalid email or password"
        })

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("user_session")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # You can pass any summary data here (e.g., total_orders=50)
    return templates.TemplateResponse("dashboard.html", {"request": request})

# SUPPLIERS ROUTE
@app.get("/suppliers", response_class=HTMLResponse)
async def read_suppliers(request: Request):
    # Mock Data
    suppliers_data = [
        {
            "name": "Acme Corp",
            "contact": "+1 (555) 010-9988",
            "products": [
                {"name": "Steel Rods", "unit_price": 15.50}, 
                {"name": "Bolts", "unit_price": 0.50}
            ],
            "payment_status": "Due",
            "total_due": 1250.00,
            "last_order_qty": 500,
            "last_order_received": True 
        },
        {
            "name": "Global Tech",
            "contact": "+1 (555) 012-3456",
            "products": [{"name": "Monitors", "unit_price": 120.00}],
            "payment_status": "Settled",
            "total_due": 0,
            "last_order_qty": 10,
            "last_order_received": True
        },
        {
            "name": "Fresh Supplies",
            "contact": "+44 20 7946 0958",
            "products": [{"name": "Packaging", "unit_price": 2.00}],
            "payment_status": "Due",
            "total_due": 300.00,
            "last_order_qty": 150,
            "last_order_received": False 
        }
    ]
    return templates.TemplateResponse("suppliers.html", {"request": request, "suppliers": suppliers_data})

# PRODUCTS ROUTES 
@app.get("/products", response_class=HTMLResponse)
async def product_list(request: Request):
    products_data = [
        {
            "id": 101,
            "name": "Nike T-Shirt",
            "description": "Cotton round neck t-shirt",
            "category": "Clothing",
            "supplier": "Acme Corp",
            "variants": [
                {"sku": "TSH-RED-L", "attributes": "Red, Large", "price": 25.00, "stock": 50},
                {"sku": "TSH-RED-M", "attributes": "Red, Medium", "price": 25.00, "stock": 12},
                {"sku": "TSH-BLK-L", "attributes": "Black, Large", "price": 26.50, "stock": 5}
            ]
        },
        {
            "id": 102,
            "name": "Gaming Monitor",
            "description": "27-inch 144Hz IPS Display",
            "category": "Electronics",
            "supplier": "Global Tech",
            "variants": [
                {"sku": "MON-27-144", "attributes": "27 Inch, Standard", "price": 299.99, "stock": 8}
            ]
        }
    ]
    return templates.TemplateResponse("products_list.html", {"request": request, "products": products_data})

@app.get("/products/create", response_class=HTMLResponse)
async def product_create(request: Request):
    return templates.TemplateResponse("product_create.html", {"request": request})