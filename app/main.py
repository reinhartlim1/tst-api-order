from fastapi import FastAPI
from . import models
from .database import engine
from .routers import order, product, auth, user
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(order.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(product.router)

@app.get("/")
def root():
    return {"message": "Hello World"}