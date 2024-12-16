import json
from datetime import datetime
from fastapi import Request
from .logg import logger


async def log_request(request: Request):
    request_time = datetime.now()

    headers = dict(request.headers)

    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.json()
        except json.JSONDecodeError:
            body_bytes = await request.body()
            body = body_bytes.decode("utf-8") if body_bytes else None

    logger.info(
        f"Request Time: {request_time}, Handler: {request.url.path}, Method: {request.method}, "
        f"Headers: {headers}, Body: {body}, User-Agent: {headers.get('user-agent')}"
    )


async def request_logging_dependency(request: Request):
    await log_request(request)