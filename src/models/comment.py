from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from configs.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User")
    post = relationship("Post")
