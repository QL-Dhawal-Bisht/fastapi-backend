from fastapi import Depends
from sqlalchemy.orm import Session
from configs.database import get_db
from services import auth_service

async def home(db: Session = Depends(get_db)):
    users = auth_service.get_all_users(db)
    return [{"id": user.id, "name": user.name, "email": user.email} for user in users]

