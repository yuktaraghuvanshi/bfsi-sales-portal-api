from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT

from app.routers import users, products, customers, leads
from app.config import settings

app = FastAPI(
    title="BFSI Sales Portal API",
    debug=True
)

# ✅ CORS setup
origins = [
    "http://localhost:3000",   # React dev server
    "http://127.0.0.1:3000",   # React dev server alternative
    # Later add production URL, e.g. "https://yourdomain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],        # important: allows OPTIONS, POST, GET, etc.
    allow_headers=["*"],
)

# ✅ JWT config
@AuthJWT.load_config
def get_config():
    return settings

# ✅ Routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(leads.router)
