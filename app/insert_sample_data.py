from datetime import datetime, timezone, timedelta
from sqlmodel import Session
from app.database.database import engine, create_db_and_tables
from app.models.models import Products, Sales, InventoryLog

def insert_sample_data():
    # Create database tables
    create_db_and_tables()
    
    # Sample products
    products = [
        Products(
            name="Amazon Echo Dot",
            stock=100,
            category="Electronics",
            price=49.99
        ),
        Products(
            name="Walmart Smart TV",
            stock=50,
            category="Electronics",
            price=299.99
        ),
        Products(
            name="Amazon Basics Microwave",
            stock=75,
            category="Home Appliances",
            price=89.99
        ),
        Products(
            name="Walmart Office Chair",
            stock=30,
            category="Furniture",
            price=129.99
        )
    ]
    
    with Session(engine) as session:
        # Add products
        for product in products:
            session.add(product)
        session.commit()
        
        # Add sales
        sales = []
        for product in products:
            # Create some sales for each product
            for i in range(3):
                sale = Sales(
                    product_id=product.id,
                    quantity=2,
                    medium_of_sales="Online",
                    total_price=product.price * 2,
                    createdAt=datetime.now(timezone.utc) - timedelta(days=i)
                )
                sales.append(sale)
        
        for sale in sales:
            session.add(sale)
        session.commit()
        
        # Add inventory logs
        for product in products:
            log = InventoryLog(
                product_id=product.id,
                previous_stock=0,
                new_stock=product.stock,
                createdAt=datetime.now(timezone.utc) - timedelta(days=7)
            )
            session.add(log)
        session.commit()

if __name__ == "__main__":
    print("Inserting sample data...")
    insert_sample_data()
    print("Sample data inserted successfully.")
