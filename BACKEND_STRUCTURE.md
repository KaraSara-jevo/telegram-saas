# Myanmar SME - Clean Backend Structure

## 🏗️ **Backend Architecture Overview**

Based on your requirements, here's the clean backend structure:

### **📋 Requirements Analysis:**
1. **Admin Panel** - Admin login and management
2. **Public View** - Landing page and information
3. **User Login** - Email + Subscription code authentication
4. **Telegram Mini App** - User dashboard for sales/items management

### **🔧 Current Backend Services:**

## 1️⃣ **User Service** - Authentication & User Management
```
user-service/
├── 📄 composer.json           # Laravel dependencies
├── 📄 .env                    # Environment variables
├── 📁 app/
│   ├── 📁 Http/Controllers/
│   │   ├── 📄 AuthController.php      # Email + Code login
│   │   ├── 📄 UserController.php      # User management
│   │   └── 📄 SubscriptionController.php # Subscription handling
│   ├── 📁 Models/
│   │   ├── 📄 User.php               # User model
│   │   └── 📄 Subscription.php       # Subscription model
│   └── 📁 Middleware/
├── 📁 database/
│   └── 📁 migrations/
│       ├── 📄 2024_01_01_000001_create_users_table.php
│       └── 📄 2024_01_01_000002_create_activation_codes_table.php
└── 📁 routes/
    └── 📄 api.php               # API routes
```

### **📊 Database Schema:**

**Users Table:**
```sql
- id (bigint, primary)
- username (string, unique)
- email (string, unique) - NEW
- password (string) - NEW
- shop_name (string)
- telegram_user_id (bigint, nullable) - NEW
- is_active (boolean)
- subscription_end_date (date)
- created_at/updated_at
```

**Activation Codes Table:**
```sql
- id (bigint, primary)
- user_id (bigint, foreign)
- code (string, unique)
- is_used (boolean)
- expires_at (timestamp)
- created_at/updated_at
```

## 2️⃣ **Inventory Service** - Product Management
```
inventory-service/
├── 📄 composer.json
├── 📄 .env
├── 📁 app/
│   ├── 📁 Http/Controllers/
│   │   └── 📄 ProductController.php
│   └── 📁 Models/
│       └── 📄 Product.php
├── 📁 database/
│   └── 📁 migrations/
│       └── 📄 2024_01_01_000003_create_products_table.php
└── 📁 routes/
    └── 📄 api.php
```

### **📦 Products Table:**
```sql
- id (bigint, primary)
- user_id (bigint, foreign) - NEW
- name (string)
- description (text)
- cost_price (decimal)
- selling_price (decimal)
- stock_quantity (integer)
- min_stock_level (integer)
- sku (string, unique)
- category (string)
- is_active (boolean)
- created_at/updated_at
```

## 3️⃣ **Sales Service** - Sales & Revenue Management
```
sales-service/
├── 📄 composer.json
├── 📄 .env
├── 📁 app/
│   ├── 📁 Http/Controllers/
│   │   ├── 📄 SaleController.php
│   │   └── 📄 ReportController.php
│   └── 📁 Models/
│       ├── 📄 Sale.php
│       └── 📄 Expense.php
├── 📁 database/
│   └── 📁 migrations/
│       ├── 📄 2024_01_01_000004_create_sales_table.php
│       ├── 📄 2024_01_01_000005_create_expenses_table.php
│       └── 📄 2026_04_06_000006_create_digit_records_table.php
└── 📁 routes/
    └── 📄 api.php
```

### **💰 Sales Table:**
```sql
- id (bigint, primary)
- user_id (bigint, foreign)
- product_id (bigint, foreign)
- quantity (integer)
- unit_price (decimal)
- total_amount (decimal)
- payment_method (string)
- customer_name (string)
- customer_phone (string)
- notes (text)
- sale_date (timestamp)
- created_at/updated_at
```

## 🔗 **API Endpoints Structure:**

### **User Service APIs:**
```
POST /api/auth/login          # Email + Password login
POST /api/auth/verify-code    # Subscription code verification
POST /api/auth/telegram       # Telegram authentication
GET  /api/users/profile       # User profile
PUT  /api/users/profile       # Update profile
GET  /api/users/subscription  # Subscription status
POST /api/subscriptions/activate # Activate subscription
```

### **Inventory Service APIs:**
```
GET    /api/products           # List user products
POST   /api/products           # Create product
GET    /api/products/{id}      # Get product
PUT    /api/products/{id}      # Update product
DELETE /api/products/{id}      # Delete product
PATCH  /api/products/{id}/stock # Update stock
GET    /api/products/low-stock # Low stock alerts
```

### **Sales Service APIs:**
```
GET    /api/sales              # List sales
POST   /api/sales              # Create sale
GET    /api/sales/{id}         # Get sale
PUT    /api/sales/{id}         # Update sale
DELETE /api/sales/{id}         # Delete sale
GET    /api/sales/summary      # Sales summary
GET    /api/sales/reports      # Sales reports
POST   /api/sales/digit-entry  # Quick digit entry
```

## 🎯 **Required Updates:**

### **1. User Service Updates:**
- ✅ Add email field to users table
- ✅ Add password field for authentication
- ✅ Add telegram_user_id for Telegram integration
- ✅ Create AuthController for email + code login
- ✅ Update User model with new fields

### **2. Inventory Service Updates:**
- ✅ Add user_id foreign key to products table
- ✅ Update Product model with user relationship
- ✅ Add user-specific product filtering

### **3. Sales Service Updates:**
- ✅ Ensure user_id foreign key exists
- ✅ Add user-specific sales filtering
- ✅ Create Telegram-specific endpoints

### **4. Admin Service (NEW):**
- ❌ Create admin-service directory
- ❌ Add admin authentication
- ❌ Add user management APIs
- ❌ Add system monitoring APIs

## 🔧 **Clean Implementation:**

### **Authentication Flow:**
1. **Admin Login** - Traditional username/password
2. **User Login** - Email + Subscription code
3. **Telegram Auth** - Telegram user ID + code

### **User Management:**
1. **Admin** - Can create/manage users
2. **Users** - Can manage their own data
3. **Telegram** - Mini app access

### **Data Flow:**
1. **Admin** → Creates users → Generates codes
2. **Users** → Login with email + code → Access dashboard
3. **Telegram** → Auth with telegram_id → Mini app access

## 🚀 **Next Steps:**

1. **Update User Service** - Add email/password auth
2. **Update Inventory Service** - Add user relationships
3. **Update Sales Service** - Add user filtering
4. **Create Admin Service** - Admin panel APIs
5. **Test Integration** - All services working together

---

## 📋 **Summary:**

**✅ Current Services:** 3 (User, Inventory, Sales)
**🔧 Required Updates:** Email auth, user relationships
**❌ Missing Service:** Admin Service (needs creation)
**🎯 Target:** Clean backend for Admin Panel + Public View + Telegram Mini App

**This structure supports your exact requirements:**
- Admin panel with admin login
- Public view (landing page)
- User login with email + subscription code
- Telegram mini app for user dashboard
