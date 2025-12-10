from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse # Added RedirectResponse

app = FastAPI(title="Inventory Management System")

# 1. Tell FastAPI where to find HTML files
templates = Jinja2Templates(directory="templates")

# (Optional) Static files mount (CSS/JS)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# --- NEW: Root Route ---
# This fixes the "404 Not Found" error when you first open the app.
@app.get("/suppliers", response_class=HTMLResponse)
async def read_suppliers(request: Request):
    suppliers_data = [
        {
            "name": "Acme Corp",
            "contact": "+1 (555) 010-9988",
            "products": [  # <--- RENAMED FROM "items"
                {"name": "Steel Rods", "unit_price": 15.50}, 
                {"name": "Bolts", "unit_price": 0.50}
            ],
            "payment_status": "Due",
            "total_due": 1250.00,
            "last_order_qty": 500,
            "last_order_received": True,
            "last_order_date": "2024-06-15"  # <--- NEW FIELD
        },
        {
            "name": "Global Tech",
            "contact": "+1 (555) 012-3456",
            "products": [{"name": "Monitors", "unit_price": 120.00}], # <--- RENAMED
            "payment_status": "Settled",
            "total_due": 0,
            "last_order_qty": 10,
            "last_order_received": True,
            "last_order_date": "2024-06-10"  # <--- NEW FIELD
        },
        {
            "name": "Fresh Supplies",
            "contact": "+44 20 7946 0958",
            "products": [{"name": "Packaging", "unit_price": 2.00}], # <--- RENAMED
            "payment_status": "Due",
            "total_due": 300.00,
            "last_order_qty": 150,
            "last_order_received": False,
            "last_order_date": "2024-06-12"  # <--- NEW FIELD
        }
    ]
    
    return templates.TemplateResponse("suppliers.html", {"request": request, "suppliers": suppliers_data})