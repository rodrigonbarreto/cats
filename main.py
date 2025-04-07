from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session
from fastapi.middleware.cors import CORSMiddleware

from core.database import get_session
from core.configs import settings
from models.pet_model import PetModel
from api.v1.api import api_router


app = FastAPI(
    title="Pets API", description="API para gerenciamento de gatos", version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Live!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8181, log_level="info", reload=True)
