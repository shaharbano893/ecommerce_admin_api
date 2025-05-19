from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column, func, DateTime

class Products(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    stock: int
    category: Optional[str] = Field(default=None, index=True)
    price: Optional[float] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
    updatedAt: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            default=func.now(),
            onupdate=func.now(),
            nullable=False,
            index=True
        )
    )
    sales: List["Sales"] = Relationship(back_populates="product")
    inventory_logs: List["InventoryLog"] = Relationship(back_populates="product")

class Sales(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: Optional[int] = Field(default=None, foreign_key="products.id", index=True)
    quantity: int
    medium_of_sales: str
    total_price: Optional[float] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)

    product: Optional[Products] = Relationship(back_populates="sales")

class InventoryLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(
        foreign_key="products.id",
        index=True
    )
    previous_stock: int
    new_stock: int
    createdAt: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        index=True
    )
    product: Optional[Products] = Relationship(back_populates="inventory_logs") 