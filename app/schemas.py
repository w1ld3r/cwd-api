import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class TransactionType(str, enum.Enum):
    DEPOSIT = "DEPOSIT"
    BUY = "BUY"
    SELL = "SELL"
    WITHDRAW = "WITHDRAW"
    AIRDROP = "AIRDROP"


class PlatformType(str, enum.Enum):
    EXCHANGE = "EXCHANGE"
    BLOCKCHAIN = "BLOCKCHAIN"


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

    @validator("email", pre=True, always=True)
    def set_lowercase(cls, v):
        if v:
            return v.lower()
        return v


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    asset_name: str
    contract_type: Optional[str]
    amount: float
    cost: Optional[float]
    cost_asset: Optional[str]
    date: Optional[datetime]
    transaction_type: TransactionType
    platform_id: int


class TransactionCreate(TransactionBase):
    asset_name: str = Field(..., min_length=3)
    contract_type: Optional[str] = Field(None, max_length=50)
    amount: float = Field(..., gt=0)
    cost: Optional[float] = Field(None, ge=0)
    cost_asset: Optional[str] = Field(None, max_length=50)
    date: Optional[datetime] = Field(None)
    transaction_type: str = Field(...)
    platform_id: int = Field(...)

    @validator("asset_name", "cost_asset", pre=True, always=True)
    def set_lowercase(cls, v):
        if v:
            return v.lower()
        return v


class TransactionResponse(TransactionBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class PlatformBase(BaseModel):
    name: str
    platform_type: PlatformType
    wallet_address: Optional[str]


class PlatformCreate(PlatformBase):
    name: str = Field(..., min_length=3)
    platform_type: str = Field(...)
    wallet_address: Optional[str] = Field(None, max_length=100)


class PlatformResponse(PlatformBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class AssetResponse(BaseModel):
    asset_name: str
    cost_asset: Optional[str]
    platform_name: str
    total_amount: float
    total_cost: float

    class Config:
        from_attributes = True
