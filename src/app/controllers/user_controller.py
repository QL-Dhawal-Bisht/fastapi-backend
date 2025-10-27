from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from configs.database import get_db
from services.user_service import UserService
from utils import responder
from app.middlewares.is_authenticated import is_authenticated
from app.schemas import UserUpdate

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

async def get_user_profile(
    current_user: dict = Depends(is_authenticated),
    service: UserService = Depends(get_user_service)
):
    try:
        user = service.get_user_by_id(current_user["id"])
        return responder.response(
            "YOUR_PROFILE",
            data={"id": user.id, "name": user.name, "email": user.email}
        )
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)

async def update_user_profile(
    user_data: UserUpdate,
    current_user: dict = Depends(is_authenticated),
    service: UserService = Depends(get_user_service)
):
    try:
        user = service.update_user(current_user["id"], user_data)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return responder.response(
            "PROFILE_UPDATED",
            data={"id": user.id, "name": user.name, "email": user.email}
        )
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)

async def delete_user_profile(
    current_user: dict = Depends(is_authenticated),
    service: UserService = Depends(get_user_service)
):
    try:
        user = service.delete_user(current_user["id"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return responder.response("PROFILE_DELETED")
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)