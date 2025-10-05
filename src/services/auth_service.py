import os
import jwt
from sqlalchemy.orm import Session
from models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, name: str, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = User(name=name, email=email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user: User):
    try:
        token = jwt.encode(
            {"id": user.id, "name": user.name},
            os.getenv("JWT_SECRET_KEY"),
            algorithm="HS256"
        )
        return token
    except Exception as e:
        return None
