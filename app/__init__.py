from fastapi import FastAPI
from elasticsearch import Elasticsearch


app = FastAPI()
es = Elasticsearch("http://localhost:9200")

from .routes import filter_router, crud_router, auth_router
from .db import migrate

