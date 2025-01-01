from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.TransactionResponse)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_transaction(
        db=db, transaction=transaction, user_id=current_user.id
    )


@router.get("/", response_model=list[schemas.TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    transactions = crud.get_transactions_by_user(db=db, user_id=current_user.id)
    return transactions


@router.get("/{transaction_id}", response_model=schemas.TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    transaction = crud.get_transaction(db=db, transaction_id=transaction_id)
    if transaction.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view this transaction",
        )
    return transaction


@router.delete("/{transaction_id}", response_model=schemas.TransactionResponse)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    transaction = crud.get_transaction(db=db, transaction_id=transaction_id)
    if transaction.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this transaction",
        )
    return crud.delete_transaction(db=db, transaction_id=transaction_id)


@router.put("/{transaction_id}", response_model=schemas.TransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    existing_transaction = crud.get_transaction(db=db, transaction_id=transaction_id)
    if existing_transaction.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update this transaction",
        )

    updated_transaction = crud.update_transaction(
        db=db, transaction_id=transaction_id, transaction_update=transaction
    )
    return updated_transaction
