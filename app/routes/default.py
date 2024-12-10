from typing import List, Optional
from fastapi import APIRouter, Query, Depends
from ..models import Ads
from ..db import AdsDB, Session
from ..logging.middleware import request_logging_dependency


default_router = APIRouter(dependencies=[Depends(request_logging_dependency)],)


@default_router.get("/ads", response_model=List[Ads], status_code=200)
async def get_ads(
    db: Session = Depends(),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    skip: int = 0,
    limit: int = 10,
):
    query = db.query(AdsDB)
    filter = []
    if category:
        filter.append(AdsDB.category == category)
    if min_price:
        filter.append(AdsDB.price <= min_price)
    if max_price:
        filter.append(AdsDB.price >= max_price)
