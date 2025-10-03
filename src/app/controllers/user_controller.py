from fastapi import Depends
from sqlalchemy.orm import Session
from configs.database import get_db
from services import user_service
from utils import responder
from app.middlewares.is_authenticated import is_authenticated

async def get_user_profile(
    current_user: dict = Depends(is_authenticated),
    db: Session = Depends(get_db)
):
    try:
        user = user_service.get_user_by_id(db, current_user["id"])
        return responder.response_ok(
            "YOUR_PROFILE",
            {"id": user.id, "name": user.name, "email": user.email}
        )
    except Exception as error:
        return responder.response_server_error()
