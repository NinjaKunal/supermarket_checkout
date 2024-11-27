from fastapi import FastAPI
from app.supermarket import supermarket_router
from app.cart import cart_router

app = FastAPI(title="Supermarket Checkout System")

# Include routers
app.include_router(supermarket_router, prefix="/api/supermarket", tags=["Supermarket"])
app.include_router(cart_router, prefix="/api/cart", tags=["Cart"])
