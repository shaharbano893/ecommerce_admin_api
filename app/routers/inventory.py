# routers/sales.py
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import List
from app.database.database import get_session
from app.models.models import Products, InventoryLog
from app.schemas.schemas import InventoryLogCreate, InventoryLogRead

router = APIRouter(prefix="/inventory", tags=["inventory"])

class InventoryUpdateRequest(BaseModel):
    product_id: int
    new_stock: int

@router.get("/status")
def get_inventory_status(session: Session = Depends(get_session)):
    low_stack_value = 5
    products = session.exec(select(Products)).all()

    result = [
        {
            "product_id": product.id,
            "name": product.name,
            "stock": product.stock,
            "low_stock": product.stock < low_stack_value
        }
        for product in products
    ]

    return JSONResponse(
        status_code=200,
        content={"status": "success", "message": "Low stock products", "data": result}
    )

@router.put("/update")
def update_inventory(
    data: InventoryUpdateRequest,
    session: Session = Depends(get_session)
):
    product = session.get(Products, data.product_id)
    if not product:
        return JSONResponse(status_code=404, content={"status": "error", "message": "Product not found"})

    # Log the change
    log = InventoryLog(
        product_id=product.id,
        previous_stock=product.stock,
        new_stock=data.new_stock
    )
    product.stock = data.new_stock
    product.updatedAt = datetime.now(timezone.utc)

    session.add(product)
    session.add(log)
    session.commit()

    return JSONResponse(status_code=200, content={"status": "success", "message": "Inventory updated and logged"})

@router.get("/logs")
def get_inventory_logs(session: Session = Depends(get_session)):
    logs = session.exec(select(InventoryLog)).all()
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": [
                {
                    "product_id": log.product_id,
                    "previous_stock": log.previous_stock,
                    "new_stock": log.new_stock,
                    "created_at": log.createdAt.isoformat()
                }
                for log in logs
            ]
        }
    )

@router.post("/", response_model=InventoryLogRead)
def create_inventory_log(log: InventoryLogCreate, session: Session = Depends(get_session)):
    # Check if product exists
    product = session.get(Products, log.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Create inventory log
    db_log = InventoryLog(**log.model_dump())
    session.add(db_log)
    
    # Update product stock
    product.stock = log.new_stock
    session.add(product)
    
    session.commit()
    session.refresh(db_log)
    return db_log

@router.get("/", response_model=List[InventoryLogRead])
def read_inventory_logs(session: Session = Depends(get_session)):
    logs = session.exec(select(InventoryLog)).all()
    return logs

@router.get("/{log_id}", response_model=InventoryLogRead)
def read_inventory_log(log_id: int, session: Session = Depends(get_session)):
    log = session.get(InventoryLog, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Inventory log not found")
    return log
