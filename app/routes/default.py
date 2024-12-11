from typing import List, Optional
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy import select
from ..models import Ads
from ..db import AdsDB, Session
from ..logging.middleware import request_logging_dependency


default_router = APIRouter(
    dependencies=[Depends(request_logging_dependency)],
)


@default_router.get("/ads", response_model=List[Ads], status_code=200)
async def get_ads(
    category: Optional[str] = Query(None, description="Category to filter ads"),
    min_price: Optional[float] = Query(
        None, description="Minimum price for filtering ads"
    ),
    max_price: Optional[float] = Query(
        None, description="Maximum price for filtering ads"
    ),
):
    stmt = select(AdsDB)
    with Session() as session:
        if category:
            stmt = stmt.where(AdsDB.category == category)
        if min_price is not None:
            stmt = stmt.where(AdsDB.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(AdsDB.price <= max_price)

        ads = session.execute(stmt).scalars().all()

        if not ads:
            raise HTTPException(
                status_code=404, detail="No ads found matching the criteria."
            )

        session.commit()

        return [Ads.from_orm(ad) for ad in ads]
