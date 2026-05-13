import uvicorn
from fastapi import FastAPI

from app.api.routers import import_router
from app.dal.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab App")
app.include_router(import_router.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
