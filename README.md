# StockTrack - Inventory Management System

A comprehensive inventory management system built with FastAPI, designed to help businesses efficiently track products, manage suppliers, monitor sales, and handle purchase orders.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure login system for system access
- **Product Management**: Add, update, view, and delete products with stock tracking
- **Supplier Management**: Manage supplier information, payment status, and order history
- **Sales Tracking**: Record and monitor product sales with automatic total calculations
- **Order Management**: Create and track purchase orders from suppliers
- **Dashboard Analytics**: Overview cards showing key metrics (total suppliers, payment dues, monthly orders)

### Technical Features
- **Real-time Calculations**: Automatic total amount calculation for sales
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **Data Validation**: Database constraints and form validation
- **Pagination**: Efficient data display for large datasets
- **Search & Filter**: Easy navigation through inventory data

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Templating**: Jinja2
- **Web Server**: Uvicorn (ASGI server)

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- Virtual environment (recommended)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ravindu-Kuruppuarachchi/StockTrack.git
   cd StockTrack
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-multipart jinja2
   ```

4. **Set up PostgreSQL database**
   - Create a database named `inventory_db`
   - Update database credentials in `database.py` if needed

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the application**
   - Open your browser and navigate to `http://localhost:8000`
   - Default login credentials: Check your database setup

## 📁 Project Structure

```
StockTrack/
├── main.py                 # FastAPI application entry point
├── database.py             # Database configuration and connection
├── models.py               # SQLAlchemy database models
├── crud_files/             # CRUD operations for different entities
│   ├── login_cruds.py      # User authentication operations
│   ├── product_cruds.py    # Product management operations
│   ├── supplier_cruds.py   # Supplier management operations
│   ├── sale_cruds.py       # Sales tracking operations
│   └── order_cruds.py      # Order management operations
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Base template with navigation
│   ├── login.html          # Login page
│   ├── products_list.html  # Product listing and management
│   ├── suppliers.html      # Supplier directory
│   ├── sales.html          # Sales records
│   ├── add_sale.html       # Add new sale form
│   └── ...                 # Other templates
├── static/                 # Static files (CSS, JS, images)
│   └── css/
│       └── styles.css      # Custom styles
└── README.md              # Project documentation
```

## 🗄️ Database Schema

### Tables
- **users**: User authentication data
- **suppliers**: Supplier information and payment status
- **products**: Product catalog with pricing and stock levels
- **sales**: Sales transaction records
- **orders**: Purchase order records

### Key Relationships
- Products belong to suppliers (many-to-one)
- Sales are linked to products (many-to-one)
- Orders are linked to suppliers (many-to-one)

## 🎯 Usage

### Adding Products
1. Navigate to Products section
2. Click "Add New Product"
3. Fill in product details (name, description, category, prices, stock)
4. Select supplier from dropdown
5. Save the product

### Recording Sales
1. Go to Sales section
2. Click "Add New Sale"
3. Select product from dropdown
4. Enter quantity
5. Total amount is automatically calculated
6. Complete the sale

### Managing Suppliers
1. Access Suppliers section
2. View supplier directory with payment status
3. Add new suppliers or update existing ones
4. Place orders directly from supplier cards

## 🔒 Security Features

- Password-based authentication
- Session management
- Input validation and sanitization
- Database constraints for data integrity
- CSRF protection through FastAPI

## 📱 Responsive Design

The application is fully responsive and works seamlessly across:
- Desktop computers
- Tablets
- Mobile devices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Ravindu Kuruppuarachchi** - *Initial work* - [GitHub Profile](https://github.com/Ravindu-Kuruppuarachchi)
