from sqlalchemy.orm import Session
from models.post import Post
from app.schemas import PostCreate, PostUpdate
from app.repositories.base_repository import BaseRepository

class PostRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_all(self, skip: int = 0, limit: int = 10, sort: str = "id"):
        return self.db.query(Post).order_by(sort).offset(skip).limit(limit).all()

    def get_by_id(self, post_id: int):
        return self.db.query(Post).filter(Post.id == post_id).first()

    def create(self, post_data: PostCreate, user_id: int):
        try:
            post = Post(**post_data.model_dump(), user_id=user_id)
            self.db.add(post)
            self.db.commit()
            self.db.refresh(post)
            return post
        except Exception as e:
            self.db.rollback()
            return None

    def update(self, post_id: int, post_data: PostUpdate, user_id: int):
        post = self.get_by_id(post_id)
        if post and post.user_id == user_id:
            if post_data.title:
                post.title = post_data.title
            if post_data.description:
                post.description = post_data.description
            self.db.commit()
            self.db.refresh(post)
        return post

    def delete(self, post_id: int, user_id: int, is_admin: bool = False):
        post = self.get_by_id(post_id)
        if post and (post.user_id == user_id or is_admin):
            self.db.delete(post)
            self.db.commit()
        return post