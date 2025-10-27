from sqlalchemy.orm import Session
from models.comment import Comment
from app.schemas import CommentCreate
from app.repositories.base_repository import BaseRepository

class CommentRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_for_post(self, post_id: int):
        return self.db.query(Comment).filter(Comment.post_id == post_id).all()

    def create(self, comment_data: CommentCreate, post_id: int, user_id: int):
        try:
            comment = Comment(**comment_data.model_dump(), post_id=post_id, user_id=user_id)
            self.db.add(comment)
            self.db.commit()
            self.db.refresh(comment)
            return comment
        except Exception as e:
            self.db.rollback()
            return None

    def delete(self, comment_id: int, user_id: int, is_admin: bool = False):
        comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
        if comment and (comment.user_id == user_id or is_admin):
            self.db.delete(comment)
            self.db.commit()
        return comment