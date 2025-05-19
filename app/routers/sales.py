# routers/sales.py
from fastapi import APIRouter, Query, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, func
from typing import Optional, List
from datetime import datetime
from app.database.database import get_session
from app.models.models import Products, Sales
from app.schemas.schemas import SaleCreate, SaleRead
from app.utils.helpers import Period, map_for_analyzing_data, generate_filters

router = APIRouter(prefix="/sales", tags=["sales"])

@router.get("/all", response_model=List[SaleRead])
def read_sales(session: Session = Depends(get_session)):
    sales = session.exec(select(Sales)).all()
    return sales


@router.post("/", response_model=SaleRead)
def create_sale(sale: SaleCreate, session: Session = Depends(get_session)):
    # Check if product exists and has enough stock
    product = session.get(Products, sale.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock < sale.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")
    
    # Create sale
    db_sale = Sales(**sale.model_dump())
    session.add(db_sale)
    
    # Update product stock
    product.stock -= sale.quantity
    session.add(product)
    
    session.commit()
    session.refresh(db_sale)
    return db_sale

@router.get("/", response_model=None)
def get_sales(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    session: Session = Depends(get_session)
) -> JSONResponse:
    filters = generate_filters(
        created_at=Sales.createdAt,
        start_date=start_date,
        end_date=end_date,
    )

    statement = select(Sales).where(*filters)
    sales_data = [
        {
            **sale.dict(),
            "createdAt": sale.createdAt.isoformat() if sale.createdAt else None
        }
        for sale in session.exec(statement).all()
    ]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "message": f"{len(sales_data)} sale(s) found.",
            "data": sales_data
        }
    )

@router.get("/revenue")
def get_revenue(
    group_by: Period = Query(default=Period.Daily),
    session: Session = Depends(get_session)
):
    date_filter = map_for_analyzing_data(Sales.createdAt)[group_by]
    statement = (
        select(
            date_filter.label("period"),
            func.sum(Sales.total_price).label("revenue")
        ).group_by("period")
    )
    data = [
        {
            "period": row.period.isoformat() if hasattr(row.period, "isoformat") else row.period,
            "revenue": float(row.revenue) if row.revenue is not None else 0.0
        }
        for row in session.exec(statement).all()
    ]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "message": "Total Revenue",
            "data": data
        }
    )

@router.get("/compare/revenue")
def compare_revenue(
    medium: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    group_by: Period = Query(default=Period.Daily),
    session: Session = Depends(get_session)
):
    period_label = map_for_analyzing_data(Sales.createdAt)[group_by.value].label("period")
    filters = generate_filters(
        Sales,
        created_at=Sales.createdAt,
        start_date=start_date,
        end_date=end_date,
        medium_of_sales=medium
    )

    statement = (
        select(
            period_label,
            Sales.medium_of_sales,
            func.sum(Sales.total_price).label("revenue")
        )
        .where(*filters)
        .group_by(period_label, Sales.medium_of_sales)
        .order_by(period_label)
    )

    data = session.exec(statement).all()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "message": "Product found.",
            "data": [
                {
                    "period": str(row[0]),
                    "medium_of_sales": row[1],
                    "revenue": row[2]
                }
                for row in data
            ]
        }
    )

@router.get("/summary")
def get_sales_by_filters(
    medium: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    product_id: Optional[int] = None,
    session: Session = Depends(get_session)
) -> JSONResponse:
    filters = generate_filters(
        Sales,
        created_at=Sales.createdAt,
        start_date=start_date,
        end_date=end_date,
        medium=(Sales.medium_of_sales, medium),
        product_id=product_id,
    )

    statement = select(
        Sales.product_id,
        Sales.medium_of_sales,
        func.sum(Sales.total_price).label("total_revenue"),
        func.count(Sales.id).label("total_sales")
    ).where(*filters).group_by(Sales.product_id, Sales.medium_of_sales)

    data = session.exec(statement).all()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "message": "Product found.",
            "data": [
                {
                    "product_id": row[0],
                    "category": row[1],
                    "total_revenue": row[2],
                    "total_sales": row[3]
                }
                for row in data
            ]

        }
    )

@router.get("/{sale_id}", response_model=SaleRead)
def read_sale(sale_id: int, session: Session = Depends(get_session)):
    sale = session.get(Sales, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale