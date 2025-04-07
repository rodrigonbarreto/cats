from fastapi import APIRouter

from api.v1.endpoints import cat
from api.v1.endpoints import dog


api_router = APIRouter()

api_router.include_router(cat.router, prefix="/cats", tags=["cats"])
api_router.include_router(dog.router, prefix="/dogs", tags=["dogs"])
