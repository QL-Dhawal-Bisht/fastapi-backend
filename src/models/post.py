from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from configs.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User")
