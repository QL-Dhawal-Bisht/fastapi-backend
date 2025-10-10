from sqlalchemy.orm import Session
from models.post import Post
from app.schemas import PostCreate, PostUpdate

def get_all_posts(db: Session, skip: int = 0, limit: int = 10, sort: str = "id"):
    return db.query(Post).order_by(sort).offset(skip).limit(limit).all()

def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def create_post(db: Session, post_data: PostCreate, user_id: int):
    try:
        post = Post(**post_data.model_dump(), user_id=user_id)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    except Exception as e:
        db.rollback()
        return None

def update_post(db: Session, post_id: int, post_data: PostUpdate, user_id: int):
    post = get_post_by_id(db, post_id)
    if post and post.user_id == user_id:
        if post_data.title:
            post.title = post_data.title
        if post_data.description:
            post.description = post_data.description
        db.commit()
        db.refresh(post)
    return post

def delete_post(db: Session, post_id: int, user_id: int, is_admin: bool = False):
    post = get_post_by_id(db, post_id)
    if post and (post.user_id == user_id or is_admin):
        db.delete(post)
        db.commit()
    return post


