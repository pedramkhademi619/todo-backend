from fastapi import FastAPI,Depends, Path,HTTPException
from contextlib import asynccontextmanager
from app.core.database import Base, engine
from app.tasks.routes import router as tasks_routes
from app.tasks.models import TaskModel
tags_metadata = [
    {
        "name": "tasks",
        "description": "عملیات مربوط به تسک‌ها",
    },
    {
        "name":"general",
        "description":"api های عمومی"
    }

]

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield

# اضافه کردن متاداده‌ها به FastAPI
app = FastAPI(
    title="TODO App",
    version="1.0.0",

    openapi_tags=tags_metadata,
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.include_router(tasks_routes)

@app.get("/", tags=["general"])
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}", tags=["general"])
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
