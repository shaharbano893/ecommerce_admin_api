# 🛒 E-commerce Admin API

This is a backend REST API built with **FastAPI** and **SQLModel**, designed to power an **admin dashboard** for managing an e-commerce platform. It provides endpoints to analyze sales, monitor inventory, and manage products.

---

## 🚀 Features

### 📊 Sales Insights

- Retrieve and filter sales data by date range, product, and category.
- Analyze revenue on a **daily**, **weekly**, **monthly**, and **annual** basis.
- Compare revenue across **different sales channels** (e.g., Amazon, Walmart).
- Group and aggregate revenue by periods and mediums.

### 📦 Inventory Management

- View current inventory levels.
- Low stock alerts.
- Update product stock and track stock changes over time via `InventoryLog`.

### ➕ Product Management

- Register new products with category, price, and stock levels.

---

## 🧱 Tech Stack

| Component      | Tech               |
|----------------|--------------------|
| Framework      | FastAPI            |
| ORM            | SQLModel           |
| DBMS           | MySQL (via PyMySQL)|
| Python Version | 3.9+               |
| Dev Server     | fastapi dev        |

---

### 🧱 Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/shaharbano893/ecommerce-admin-api.git
cd ecommerce-admin-api
```

#### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Add Environment Variables

Create a `.env` file in the project root and add your MySQL connection credentials:

```dotenv
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecommerce_admin_api_db
```

#### 5. Verify the `database.py` Connection

The connection string is dynamically built using these environment variables:

```python
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
```

#### 6. Run Setup Script

This will create the database tables and populate them with demo data:

```bash
python initial_setup.py
```
### 7. Start Development Server

Run using the built-in FastAPI development server:

```bash
fastapi dev
```

---

## 📘 API Endpoints

### 🔸 Sales Endpoints

| Method | Endpoint                 | Description                                                                |
| ------ | ------------------------ |----------------------------------------------------------------------------|
| GET    | `/sales/`                | Retrieve sales with optional filters of date range(start_date, end_date)   |
| GET    | `/sales/revenue`         | Get total revenue grouped by time period (daily, weekly, monthly, yearly.) |
| GET    | `/sales/compare/revenue` | Compare revenue by sales channel across time periods                       |
| GET    | `/sales/summary`         | Get sales summary grouped by product and medium                            |
| GET    | `/sales/{sale_id}`       | Get details of a specific sale by ID                                       |
| POST   | `/sales/`                | Create a new sale and update product inventory                             |


### 🔸 Inventory Endpoints

| Method | Endpoint              | Description                                             |
| ------ | --------------------- | ------------------------------------------------------- |
| GET    | `/inventory/status`   | View current inventory levels with low stock flag       |
| PUT    | `/inventory/update`   | Update inventory stock and automatically log the change |
| GET    | `/inventory/logs`     | Retrieve all inventory update logs                      |
| POST   | `/inventory/`         | Manually create a new inventory log entry               |
| GET    | `/inventory/`         | Get all inventory logs (response as model list)         |
| GET    | `/inventory/{log_id}` | Get a specific inventory log by ID                      |
### 🔸 Product Endpoints

| Method | Endpoint                 | Description                     |
| ------ | ------------------------ | ------------------------------- |
| POST   | `/products/`             | Create a new product            |
| GET    | `/products/`             | Get a list of all products      |
| GET    | `/products/{product_id}` | Retrieve a single product by ID |
| PUT    | `/products/{product_id}` | Update a product by ID          |
| DELETE | `/products/{product_id}` | Delete a product by ID          |

---
# 📡 GraphQL API (Strawberry)

The **GraphQL** layer of the E-commerce Admin API is built using **Strawberry** and exposes flexible endpoints for interacting with products, sales, and inventory.

---

## 🔗 Endpoint

```
POST /graphql
```

GraphQL Playground:

```
http://localhost:8000/graphql
```

---

## 🧾 Schema Overview

### 🟩 Types

#### `ProductType`

```graphql
type ProductType {
  id: Int!
  name: String!
  stock: Int!
  category: String
  price: Float
  createdAt: DateTime!
  updatedAt: DateTime!
  sales: [SaleType]
  inventoryLogs: [InventoryLogType]
}
```

#### `SaleType`

```graphql
type SaleType {
  id: Int!
  productId: Int
  quantity: Int!
  mediumOfSales: String!
  totalPrice: Float
  createdAt: DateTime!
}
```

#### `InventoryLogType`

```graphql
type InventoryLogType {
  id: Int!
  productId: Int!
  previousStock: Int!
  newStock: Int!
  createdAt: DateTime!
}
```

---

### 📝 Inputs

#### `CreateProductInput`

```graphql
input CreateProductInput {
  name: String!
  stock: Int!
  category: String
  price: Float
}
```

---

## 📥 Mutations

### `createProduct`

Create a new product.

```graphql
mutation {
  createProduct(createProduct: {
    name: "Wireless Mouse",
    stock: 100,
    category: "Electronics",
    price: 25.99
  }) {
    id
    name
    stock
    category
    price
    createdAt
    updatedAt
  }
}
```

---

## 📤 Queries

### `getProduct`

Retrieve a product by ID.

```graphql
query {
  getProduct(productId: 1) {
    id
    name
    stock
    category
    price
    createdAt
    updatedAt
    sales {
      id
      quantity
      mediumOfSales
      totalPrice
      createdAt
    }
    inventoryLogs {
      id
      previousStock
      newStock
      createdAt
    }
  }
}
```

---

## 🧪 Example Response

```json
{
  "data": {
    "createProduct": {
      "id": 5,
      "name": "Wireless Mouse",
      "stock": 100,
      "category": "Electronics",
      "price": 25.99,
      "createdAt": "2025-05-28T14:22:31.123Z",
      "updatedAt": "2025-05-28T14:22:31.123Z"
    }
  }
}
```

---

## 🗂 Database Schema

### 📦 `Products`

| Column          | Type     | Description                          |
| --------------- | -------- | ------------------------------------ |
| id              | Integer  | Primary Key                          |
| name            | String   | Product name                         |
| stock           | Integer  | Quantity in stock                    |
| category        | String   | Product category (optional)          |
| price           | Float    | Price in USD (optional)              |
| createdAt       | DateTime | Created timestamp (UTC)              |
| updatedAt       | DateTime | Last update timestamp (auto-updated) |
| sales           | Relation | One-to-many with `Sales`             |
| inventory\_logs | Relation | One-to-many with `InventoryLog`      |

### 🧾 `Sales`

| Column            | Type       | Description                           |
| ----------------- | ---------- | ------------------------------------- |
| id                | Integer    | Primary Key                           |
| product\_id       | ForeignKey | Linked to `Products`                  |
| quantity          | Integer    | Units sold                            |
| medium\_of\_sales | String     | Sales channel (e.g., Amazon, Shopify) |
| total\_price      | Float      | Total sale price (optional)           |
| createdAt         | DateTime   | Sale date and time (UTC)              |
| product           | Relation   | Many-to-one with `Products`           |

### 📚 `InventoryLog`

| Column          | Type       | Description                 |
| --------------- | ---------- | --------------------------- |
| id              | Integer    | Primary Key                 |
| product\_id     | ForeignKey | Linked to `Products`        |
| previous\_stock | Integer    | Stock before update         |
| new\_stock      | Integer    | Stock after update          |
| createdAt       | DateTime   | Time of update (UTC)        |
| product         | Relation   | Many-to-one with `Products` |

---
## 🧪 Sample Data

This project includes demo records for:

* Products across categories like **Electronics**, **Home Appliances**, and **Furniture**
* Sales via **Amazon** and **Walmart**
* Inventory logs reflecting stock changes over time

---

## 📂 Project Structure

```bash
.
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── routers/
│   │   ├── sales.py
│   │   ├── products.py
│   │   └── inventory.py
│   │── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py
│   │── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   │── __init__.py
│   │── insert_sample_data.py
│   └── main.py
├── venv
├── .env
├── .env.example
├── .gitignore
├── initial_setup.py
├── README.md
└── requirements.txt
```