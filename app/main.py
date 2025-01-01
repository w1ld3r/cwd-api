from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.database import engine
from app.routers import assets, platforms, token, transactions, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cwd.danjon.xyz"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(token.router, prefix="/token", tags=["Token"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(platforms.router, prefix="/platforms", tags=["Platforms"])
app.include_router(assets.router, prefix="/assets", tags=["Assets"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Crypto Wallet API"}
