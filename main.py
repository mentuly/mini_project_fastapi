import uvicorn
from app import (
    app,
    default_router,
    migrate
)


if __name__ == "__main__":
    migrate()
    app.include_router(default_router)
    uvicorn.run(app, port=8080)
