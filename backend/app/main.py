from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from typing import List, Annotated
from app.api.routes.auth import router as auth_router
app = FastAPI(
    title = "Mahalaxmi Agency",
    version ="1.0.0"
)

app.include_router(auth_router, prefix ="/api/v1")

@app.get("/")
def root():
    return{
        "message":"Plasto linked MahaLaxmi Agency API is running"
    }

@app.get("/health")
def health():
    return {"Status" : "Healthy"}

