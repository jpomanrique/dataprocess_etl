import os
from typing import List

from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from pymongo import MongoClient, UpdateOne

# -----------------------------------------------------------------------------
# Configuração básica
# -----------------------------------------------------------------------------

app = FastAPI(
    title="Pipeline ETL API",
    version="1.0.0",
    description="API intermediária segura para ETL com MongoDB Atlas"
)

ATLAS_URI = os.getenv("ATLAS_URI")
API_KEY = os.getenv("API_KEY")

if not ATLAS_URI:
    raise RuntimeError("ATLAS_URI não configurada")

if not API_KEY:
    raise RuntimeError("API_KEY não configurada")

# -----------------------------------------------------------------------------
# MongoDB
# -----------------------------------------------------------------------------

client = MongoClient(ATLAS_URI)
db = client["test"]
collection = db["users"]

collection.create_index("id", unique=True)

# -----------------------------------------------------------------------------
# Segurança
# -----------------------------------------------------------------------------

def check_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

# -----------------------------------------------------------------------------
# Modelos (Swagger / validação)
# -----------------------------------------------------------------------------

class Account(BaseModel):
    id: int
    balance: float
    limit: float

class User(BaseModel):
    id: int
    name: str
    account: Account
    features: list = []
    news: list = []

# -----------------------------------------------------------------------------
# Rotas
# -----------------------------------------------------------------------------

@app.get("/")
def root():
    return {
        "service": "Pipeline ETL API",
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/users/bulk", dependencies=[Depends(check_api_key)])
def bulk_users(users: List[User]):
    """
    Insere usuários em bulk.
    Se o ID já existir, ignora (upsert).
    """

    operations = [
        UpdateOne(
            {"id": user.id},
            {"$setOnInsert": user.dict()},
            upsert=True
        )
        for user in users
    ]

    if not operations:
        return {"inserted": 0, "total": 0}

    result = collection.bulk_write(operations, ordered=False)

    return {
        "inserted": len(result.upserted_ids),
