from sqlalchemy.orm import Session
from models.comment import Comment
from app.schemas import CommentCreate

def get_comments_for_post(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()

def create_comment(db: Session, comment_data: CommentCreate, post_id: int, user_id: int):
    try:
        comment = Comment(**comment_data.model_dump(), post_id=post_id, user_id=user_id)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment
    except Exception as e:
        db.rollback()
        return None

def delete_comment(db: Session, comment_id: int, user_id: int, is_admin: bool = False):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment and (comment.user_id == user_id or is_admin):
        db.delete(comment)
        db.commit()
    return comment


