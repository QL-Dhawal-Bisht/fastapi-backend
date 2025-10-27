from sqlalchemy.orm import Session
from app.repositories.post_repository import PostRepository
from app.schemas import PostCreate, PostUpdate

class PostService:
    def __init__(self, db: Session):
        self.repo = PostRepository(db)

    def get_all_posts(self, skip: int = 0, limit: int = 10, sort: str = "id"):
        return self.repo.get_all(skip, limit, sort)

    def get_post_by_id(self, post_id: int):
        return self.repo.get_by_id(post_id)

    def create_post(self, post_data: PostCreate, user_id: int):
        return self.repo.create(post_data, user_id)

    def update_post(self, post_id: int, post_data: PostUpdate, user_id: int):
        return self.repo.update(post_id, post_data, user_id)

    def delete_post(self, post_id: int, user_id: int, is_admin: bool = False):
        return self.repo.delete(post_id, user_id, is_admin)
