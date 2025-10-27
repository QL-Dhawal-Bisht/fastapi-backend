from fastapi import Depends
from sqlalchemy.orm import Session
from configs.database import get_db
from services.auth_service import AuthService

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)

async def home(service: AuthService = Depends(get_auth_service)):
    users = service.get_all_users()
    return [{"id": user.id, "name": user.name, "email": user.email} for user in users]