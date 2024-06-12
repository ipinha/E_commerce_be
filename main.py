from fastapi import FastAPI
from routers import user, category, product, cart, authentication
import models
from database import engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


app.include_router(user.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(authentication.router)