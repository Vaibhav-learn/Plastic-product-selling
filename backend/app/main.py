from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from typing import List, Annotated

app = FastAPI(
    title = "Mahalaxmi Agency",
    version ="1.0.0"
)

@app.get("/")
def root():
    return{
        "message":"Plasto linked MahaLaxmi Agency API is running"
    }

@app.get("/health")
def health():
    return {"Status" : "Healthy"}