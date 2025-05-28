import strawberry
from typing import Optional, List
from datetime import datetime


@strawberry.type
class SaleType:
    id: int
    product_id: Optional[int]
    quantity: int
    medium_of_sales: str
    total_price: Optional[float]
    createdAt: datetime

@strawberry.type
class InventoryLogType:
    id: int
    product_id: int
    previous_stock: int
    new_stock: int
    createdAt: datetime

@strawberry.type
class ProductType:
    id: int
    name: str
    stock: int
    category: Optional[str]
    price: Optional[float]
    createdAt: datetime
    updatedAt: datetime
    sales: Optional[List[SaleType]] = None
    inventory_logs: Optional[List[InventoryLogType]] = None

@strawberry.input
class CreateProductInput:
    name: str
    stock: int
    category: Optional[str] = None
    price: Optional[float] = None

