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
