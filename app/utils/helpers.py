from datetime import datetime, timezone
from enum import Enum
from sqlmodel import SQLModel, func
from typing import Optional, List, Tuple

class Period(str, Enum):
    Daily = "daily"
    Weekly = "weekly"
    Monthly = "monthly"
    Yearly = "yearly"

def convert_to_datetime(date_str: str) -> datetime:
    """Convert string to datetime object."""
    return datetime.fromisoformat(date_str.replace('Z', '+00:00'))

def convert_to_iso_format(dt: datetime) -> str:
    """Convert datetime to ISO format string."""
    return dt.isoformat()

def generate_filters(
    model: SQLModel,
    created_at: Optional[datetime] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    medium: Optional[Tuple[str, str]] = None,
    product_id: Optional[int] = None
) -> List:
    """Generate SQL filters based on provided parameters."""
    filters = []
    
    if start_date:
        filters.append(created_at >= start_date)
    if end_date:
        filters.append(created_at <= end_date)
    if medium and medium[1]:
        filters.append(medium[0] == medium[1])
    if product_id:
        filters.append(model.product_id == product_id)
    
    return filters

def map_for_analyzing_data(column: datetime) -> dict:
    """Map period types to SQL functions for data analysis."""
    return {
        Period.Daily: func.date(column),
        Period.Weekly: func.strftime('%Y-%W', column),
        Period.Monthly: func.strftime('%Y-%m', column),
        Period.Yearly: func.strftime('%Y', column)
    }
