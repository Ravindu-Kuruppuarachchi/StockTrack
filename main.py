from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse # Added RedirectResponse

app = FastAPI(title="Inventory Management System")

# 1. Tell FastAPI where to find HTML files
templates = Jinja2Templates(directory="templates")

# (Optional) Static files mount (CSS/JS)
# app.mount("/static", StaticFiles(directory="static"), name="static")

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

# --- Route 2: Product Create Form ---
@app.get("/products/create", response_class=HTMLResponse)
async def product_create(request: Request):
    return templates.TemplateResponse("product_create.html", {"request": request})