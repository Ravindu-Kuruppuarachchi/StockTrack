from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Inventory Management System")

# 1. Tell FastAPI where to find HTML files
templates = Jinja2Templates(directory="templates")

# (Optional) If you have CSS/Images later, you'd mount static files here
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_dashboard(request: Request):
    # 2. Render the 'dashboard.html' template
    # We must pass the 'request' object to the template
    return templates.TemplateResponse("dashboard.html", {"request": request})

# We will add the other routes (products, orders) here later