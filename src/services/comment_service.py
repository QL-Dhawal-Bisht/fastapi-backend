from sqlalchemy.orm import Session
from app.repositories.comment_repository import CommentRepository
from app.schemas import CommentCreate

class CommentService:
    def __init__(self, db: Session):
        self.repo = CommentRepository(db)

    def get_comments_for_post(self, post_id: int):
        return self.repo.get_for_post(post_id)

    def create_comment(self, comment_data: CommentCreate, post_id: int, user_id: int):
        return self.repo.create(comment_data, post_id, user_id)

    def delete_comment(self, comment_id: int, user_id: int, is_admin: bool = False):
        return self.repo.delete(comment_id, user_id, is_admin)
