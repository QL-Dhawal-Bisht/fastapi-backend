from sqlalchemy.orm import Session
from models.user import User
from app.repositories.base_repository import BaseRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, name: str, email: str, password: str):
        hashed_password = pwd_context.hash(password)
        user = User(name=name, email=email, password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all(self):
        return self.db.query(User).all()
