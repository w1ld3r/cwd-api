from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.auth import Token, create_access_token, logged_out_tokens, verify_token
from app.config import settings
from app.database import get_db
from app.dependencies import oauth2_scheme

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def verify(token: str = Depends(oauth2_scheme)):
    if token in logged_out_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )
    verify_token(token)
    return {"message": "Token is valid"}


@router.post("/", response_model=Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": db_user.email}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.delete("/", status_code=status.HTTP_200_OK)
def logout(token: str = Depends(oauth2_scheme)):
    if token:
        logged_out_tokens.add(token)
    return {"message": "Successfully logged out"}
