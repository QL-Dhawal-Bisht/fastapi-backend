import os
import jwt
from sqlalchemy.orm import Session
from models.user import User
from app.repositories.auth_repository import AuthRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session):
        self.repo = AuthRepository(db)

    def get_user_by_email(self, email: str):
        return self.repo.get_user_by_email(email)

    def create_user(self, name: str, email: str, password: str):
        return self.repo.create_user(name, email, password)

    def get_all_users(self):
        return self.repo.get_all()

    def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, user: User):
        try:
            token = jwt.encode(
                {"id": user.id, "name": user.name},
                os.getenv("JWT_SECRET_KEY"),
                algorithm="HS256"
            )
            return token
        except Exception as e:
            return None