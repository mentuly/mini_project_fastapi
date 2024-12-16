from typing import List, Annotated
from fastapi import (
    middleware,
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status,
)
from ..db import AdsDB, User, Session
from ..logging import request_logging_dependency
from sqlalchemy import select
from ..models import Ads, AdsOut

crud_router = APIRouter(
    prefix="/item",
    tags=["Item"],
    dependencies=[Depends(request_logging_dependency)],
)


@crud_router.get("/")
def read_root():
    return {"hello": "world"}


@crud_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create(user: Annotated[User, Depends()]):
    pass


@crud_router.get("/read/{item_id}")
async def read():
    pass


@crud_router.put("/update/{item_id}")
async def update():
    pass


@crud_router.delete("/delete/{item_id}")
async def delete_item():
    pass


@crud_router.get("/items/all", response_model=List[Ads])
async def get_all_items():
    item = select(AdsDB)
    
    
