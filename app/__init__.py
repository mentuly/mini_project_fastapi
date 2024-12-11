from fastapi import FastAPI


app = FastAPI()

from .routes import default_router
from .db import migrate
