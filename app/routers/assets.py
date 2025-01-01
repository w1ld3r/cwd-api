from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter()


def calculate_real_assets(assets: list) -> list:
    grouped_assets = defaultdict(lambda: {"total_amount": 0, "total_cost": 0})

    for asset in assets:
        key = (
            asset["asset_name"],
            asset["cost_asset"],
            asset["platform_name"],
        )
        transaction_type = asset["transaction_type"].value
        total_amount = asset["total_amount"]
        total_cost = asset["total_cost"]

        if transaction_type == schemas.TransactionType.DEPOSIT.value:
            grouped_assets[key]["total_amount"] += total_amount
        elif transaction_type == schemas.TransactionType.BUY.value:
            asset_key = (asset["asset_name"], asset["cost_asset"], asset["platform_name"])
            grouped_assets[asset_key]["total_amount"] += total_amount
            grouped_assets[asset_key]["total_cost"] += total_cost
            if asset["cost_asset"]:
                cost_key = (asset["cost_asset"], "", asset["platform_name"])
                grouped_assets[cost_key]["total_amount"] -= total_cost
        elif transaction_type == schemas.TransactionType.SELL.value:
            asset_key = (asset["asset_name"], asset["cost_asset"], asset["platform_name"])
            grouped_assets[asset_key]["total_amount"] -= total_amount
            grouped_assets[asset_key]["total_cost"] -= total_cost
            cost_key = (asset["cost_asset"], "", asset["platform_name"])
            grouped_assets[cost_key]["total_amount"] += total_cost
        elif transaction_type == schemas.TransactionType.AIRDROP.value:
            grouped_assets[key]["total_amount"] += total_amount
        elif transaction_type == schemas.TransactionType.WITHDRAW.value:
            grouped_assets[key]["total_amount"] -= total_amount

    real_assets_result = [
        {
            "asset_name": key[0],
            "cost_asset": key[1],
            "platform_name": key[2],
            "total_amount": values["total_amount"],
            "total_cost": values["total_cost"],
        }
        for key, values in grouped_assets.items()
        if values["total_amount"] > 0
    ]

    return real_assets_result


@router.get("/", response_model=list[dict])
def get_assets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    assets = crud.get_assets_by_user(db=db, user_id=current_user.id)
    real_assets = calculate_real_assets(assets)

    return real_assets
