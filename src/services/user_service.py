from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas import UserUpdate

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def get_user_by_id(self, user_id: int):
        return self.repo.get_by_id(user_id)

    def update_user(self, user_id: int, user_data: UserUpdate):
        return self.repo.update(user_id, user_data)

    def delete_user(self, user_id: int):
        return self.repo.delete(user_id)