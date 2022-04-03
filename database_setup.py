# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from os import getenv

Base = declarative_base()
metadata = Base.metadata


class Temp_tokens(Base):
    __tablename__ = "temp_tokens"

    id = Column(Integer, primary_key=True)
    code = Column(String(64), nullable=False)
    email = Column(String(250), nullable=False)
    generated_at = Column(DateTime, nullable=False)


class TokenType(Base):
    __tablename__ = "token_type"

    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR(250), nullable=False)
    token = Column(String(64), nullable=False)
    token_type = Column(
        ForeignKey("token_type.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    newsletters = Column(TINYINT(1), nullable=False)
    last_use = Column(DateTime, nullable=False)

    token_type1 = relationship("TokenType")


user: str = getenv("DB_USER")
password: str = getenv("DB_PASSWORD")
db_name: str = getenv("DB_NAME")

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@db/{db_name}?charset=utf8mb4"
)
Base.metadata.bind = engine

# Create tables (if they don't exist)
Base.metadata.create_all(engine)
