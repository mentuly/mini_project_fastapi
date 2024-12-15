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
from ..logging import request_logging_dependency
from ..models import Ads

crud_router = APIRouter(
    prefix="/item",
    tags=["Item"],
    dependencies=[Depends(request_logging_dependency)],
)


@crud_router.get("/")
def read_root():
    return {"hello": "world"}


@crud_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create():
    pass


@crud_router.get("/read")
async def read():
    pass


@crud_router.put("/update/{item_id}")
async def update():
    pass


@crud_router.delete("/delete")
async def delete_item():
    pass


@crud_router.get("/items/all", response_model=List[Ads])
async def get_all_items():
    pass
