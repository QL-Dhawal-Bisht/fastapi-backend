from sqlalchemy.orm import Session
from models.user import User
from app.schemas import UserUpdate

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = get_user_by_id(db, user_id)
    if user:
        if user_data.name:
            user.name = user_data.name
        if user_data.email:
            user.email = user_data.email
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user
