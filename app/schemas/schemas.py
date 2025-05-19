from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    stock: int
    category: Optional[str] = None
    price: Optional[float] = None

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    medium_of_sales: str
    total_price: Optional[float] = None

class SaleCreate(SaleBase):
    pass

class SaleRead(SaleBase):
    id: int
    createdAt: datetime

    class Config:
        from_attributes = True

class InventoryLogBase(BaseModel):
    product_id: int
    previous_stock: int
    new_stock: int

class InventoryLogCreate(InventoryLogBase):
    pass

class InventoryLogRead(InventoryLogBase):
    id: int
    createdAt: datetime

    class Config:
        from_attributes = True 