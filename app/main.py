from fastapi import FastAPI 

from app.routers.car_rent import router
from app.models.car_rent import init_db

init_db()
app = FastAPI(title="Car Rental Service")
app.include_router(router)
