from typing import List, Optional
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy import select
from ..models import Ads
from ..db import AdsDB, Session
from ..logging import request_logging_dependency

# from ..helpers import search_in_elasticsearch


filter_router = APIRouter(
    prefix="/filter",
    tags=["Filters"],
    dependencies=[Depends(request_logging_dependency)],
)


@filter_router.get("/ads", response_model=List[Ads], status_code=200)
async def get_ads(
    category: Optional[str] = Query(None, description="Category to filter ads"),
    min_price: Optional[float] = Query(
        None, description="Minimum price for filtering ads"
    ),
    max_price: Optional[float] = Query(
        None, description="Maximum price for filtering ads"
    ),
    page: int = Query(1, ge=1, description="Page number, starts from 1"),
    size: int = Query(10, ge=1, le=100, description="Number of ads per page, max 100"),
):

    # if category or min_price or max_price:
    #     search_results = search_in_elasticsearch(category, min_price, max_price)

    #     if not search_results:
    #         raise HTTPException(
    #             status_code=404, detail="No ads found matching the criteria in Elasticsearch."
    #         )

    #     return [Ads.from_orm(hit["_source"]) for hit in search_results]
    # else:

    query = select(AdsDB)
    with Session() as session:
        if category:
            query = query.where(AdsDB.category == category)
        if min_price is not None:
            query = query.where(AdsDB.price >= min_price)
        if max_price is not None:
            query = query.where(AdsDB.price <= max_price)

        offset = (page - 1) * size
        query = query.offset(offset).limit(size)

        ads = session.execute(query).scalars().all()

        if not ads:
            raise HTTPException(
                status_code=404, detail="No ads found matching the criteria."
            )

        session.commit()

        return [Ads.from_orm(ad) for ad in ads]
