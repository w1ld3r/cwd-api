import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    transactions = relationship("Transaction", back_populates="owner")
    platforms = relationship("Platform", back_populates="owner")


class TransactionType(enum.Enum):
    DEPOSIT = "DEPOSIT"
    BUY = "BUY"
    SELL = "SELL"
    WITHDRAW = "WITHDRAW"
    AIRDROP = "AIRDROP"


class PlatformType(enum.Enum):
    EXCHANGE = "EXCHANGE"
    BLOCKCHAIN = "BLOCKCHAIN"


class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    platform_type = Column(Enum(PlatformType), nullable=False)
    wallet_address = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="platforms")
    transactions = relationship("Transaction", back_populates="platform")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String, nullable=False)
    contract_type = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    cost = Column(Float, nullable=True)
    cost_asset = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="transactions")
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    platform = relationship("Platform", back_populates="transactions")
