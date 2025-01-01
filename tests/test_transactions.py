from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.database import SessionLocal, engine
from app.main import app

client = TestClient(app)


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_create_transaction():
    response = client.post(
        "/transactions/",
        json={
            "name": "Bitcoin Deposit",
            "symbol": "BTC",
            "platform": "Binance",
            "platform_type": "exchange",
            "blockchain": "Bitcoin",
            "holding": 0.5,
            "cost": 10000,
            "cost_asset": "USD",
            "transaction_type": "deposit",
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Bitcoin Deposit"
