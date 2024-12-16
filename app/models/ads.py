from typing import Optional, Annotated
from datetime import datetime
from pydantic import BaseModel, field_validator
from fastapi import UploadFile, File


class Ads(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price: float
    published_at: datetime
    photo: Annotated[UploadFile, File(...)] = None

    @field_validator("created_at")
    @classmethod
    def validate_published_at(cls, value):
        if value > datetime.utcnow():
            raise ValueError("The publication date cannot be in the future.")
        return value

    @field_validator("price")
    @classmethod
    def check_price(cls, value):
        if value < 0:
            raise ValueError("The price cannot be lower then 0")
        return value


class AdsFilter(BaseModel):
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None



class AdsOut(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price: float
    published_at: datetime
    