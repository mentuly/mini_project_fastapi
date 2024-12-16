from typing import Optional
from pydantic import BaseModel


class Ads(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price: float


class AdsFilter(BaseModel):
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None

