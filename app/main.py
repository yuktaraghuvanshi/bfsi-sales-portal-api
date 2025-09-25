# app/main.py
from fastapi import FastAPI
from app.routers import users, products, customers, leads

app = FastAPI(
    title="BFSI Sales Portal API",
    debug=True  # <-- Enable debug mode
)
from fastapi_jwt_auth import AuthJWT
from app.config import settings

@AuthJWT.load_config
def get_config():
    return settings

app.include_router(users.router)
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(leads.router)
