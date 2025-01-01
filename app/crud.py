from typing import List

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_transaction(
    db: Session, transaction: schemas.TransactionCreate, user_id: int
):
    db_transaction = models.Transaction(**transaction.dict(), owner_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions_by_user(db: Session, user_id: int) -> List[models.Transaction]:
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.owner_id == user_id)
        .all()
    )


def get_transaction(db: Session, transaction_id: int):
    transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


def update_transaction(
    db: Session, transaction_id: int, transaction_update: schemas.TransactionCreate
):
    transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in transaction_update.dict(exclude_unset=True).items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)
    return transaction


def delete_transaction(db: Session, transaction_id: int):
    transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return transaction


def create_platform(
    db: Session, platform: schemas.PlatformCreate, user_id: int
) -> models.Platform:
    db_platform = models.Platform(**platform.dict(), owner_id=user_id)
    db.add(db_platform)
    db.commit()
    db.refresh(db_platform)
    return db_platform


def get_platform(db: Session, platform_id: int) -> models.Platform:
    platform = (
        db.query(models.Platform).filter(models.Platform.id == platform_id).first()
    )
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    return platform


def get_platforms_by_user(db: Session, user_id: int) -> List[models.Platform]:
    return db.query(models.Platform).filter(models.Platform.owner_id == user_id).all()


def update_platform(
    db: Session, platform_id: int, platform_update: schemas.PlatformCreate
):
    platform = (
        db.query(models.Platform).filter(models.Platform.id == platform_id).first()
    )
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")

    for key, value in platform_update.dict(exclude_unset=True).items():
        setattr(platform, key, value)

    db.commit()
    db.refresh(platform)
    return platform


def delete_platform(db: Session, platform_id: int):
    platform = (
        db.query(models.Platform).filter(models.Platform.id == platform_id).first()
    )
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    db.delete(platform)
    db.commit()
    return platform


def get_assets_by_user(db: Session, user_id: int) -> List[dict]:
    results = (
        db.query(
            models.Transaction.asset_name,
            func.coalesce(models.Transaction.cost_asset, "").label("cost_asset"),
            models.Transaction.transaction_type,
            models.Platform.name.label("platform_name"),
            func.coalesce(func.sum(models.Transaction.amount), 0).label("total_amount"),
            func.coalesce(func.sum(models.Transaction.cost), 0).label("total_cost"),
        )
        .join(models.Platform, models.Platform.id == models.Transaction.platform_id)
        .filter(models.Transaction.owner_id == user_id)
        .group_by(
            models.Transaction.asset_name,
            models.Transaction.cost_asset,
            models.Transaction.transaction_type,
            models.Platform.name,
        )
        .all()
    )
    assets = [
        {
            "asset_name": row.asset_name,
            "cost_asset": row.cost_asset,
            "transaction_type": row.transaction_type,
            "platform_name": row.platform_name,
            "total_amount": row.total_amount,
            "total_cost": row.total_cost,
        }
        for row in results
    ]

    return assets
