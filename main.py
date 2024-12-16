import uvicorn
from app import (
    app,
    filter_router,
    crud_router,
    migrate,
    # es,
)


if __name__ == "__main__":
    migrate()
    app.include_router(filter_router)
    app.include_router(crud_router)
    uvicorn.run(app, port=8080)
    # es.info().body
    
