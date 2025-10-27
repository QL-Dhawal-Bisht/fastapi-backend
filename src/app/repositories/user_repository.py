from sqlalchemy.orm import Session
from models.user import User
from app.schemas import UserUpdate
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def update(self, user_id: int, user_data: UserUpdate):
        user = self.get_by_id(user_id)
        if user:
            if user_data.name:
                user.name = user_data.name
            if user_data.email:
                user.email = user_data.email
            self.db.commit()
            self.db.refresh(user)
        return user

    def delete(self, user_id: int):
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
        return user
