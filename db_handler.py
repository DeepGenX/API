from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Temp_tokens, Base
from os import getenv
import secrets
import datetime

# Geting the database credentials from the environment variables in docker-compose
user: str = getenv("DB_USER")
password: str = getenv("DB_PASSWORD")
db_name: str = getenv("DB_NAME")

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@db/{db_name}?charset=utf8mb4"
)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def email_exists(email: str) -> bool:
    """Check if the email exists in the database"""
    user: User = session.query(User).filter_by(email=email).first()
    return user is not None


def temp_token_exists(token: str) -> bool:
    """Check if the temp token exists in the database"""
    temp_token: Temp_tokens = session.query(Temp_tokens).filter_by(code=token).first()
    return temp_token is not None


def user_token_exists(token: str) -> bool:
    """Check if the user token exists in the database"""
    user_token: User = session.query(User).filter_by(token=token).first()
    return user_token is not None


def generate_temp_token() -> str:
    """Create a random token of 64 len for the registration"""
    # token_urlsafe is taking a number of bytes as an argument 48 bytes = 64 characters
    token: str = secrets.token_urlsafe(48)
    if temp_token_exists(token):
        return generate_temp_token()
    return token


def generate_user_token() -> str:
    """Create a random token of 64 len for the user"""
    # token_urlsafe is taking a number of bytes as an argument 48 bytes = 64 characters
    token: str = secrets.token_urlsafe(48)
    if user_token_exists(token):
        return generate_user_token()
    return token


def create_temp_token(email: str) -> str:
    """Create a temp token for the registration"""
    token: str = generate_temp_token()
    temp_token: Temp_tokens = Temp_tokens(
        code=token,
        email=email,
        generated_at=datetime.datetime.now(),
    )
    session.add(temp_token)
    session.commit()
    return token


def get_temp_token(token: str) -> Temp_tokens:
    """Get the temp token from the database"""
    temp_token: Temp_tokens = session.query(Temp_tokens).filter_by(code=token).first()
    return temp_token


def create_user(email: str) -> None:
    """Create a user in the database"""
    user: User = User(
        email=email,
        token=generate_user_token(),
        token_type=1,
        newsletters=1,
        last_use=datetime.datetime.now(),
    )
    session.add(user)
    session.commit()
