from fastapi import Depends
from sqlalchemy.orm import Session
from configs.database import get_db
from services import auth_service
from utils import responder
from app.middlewares.validations import RegisterLoginSchema

async def register(user_data: RegisterLoginSchema, db: Session = Depends(get_db)):
    try:
        check_user = auth_service.get_user_by_email(db, user_data.email)

        if check_user:
            return responder.response("USER_EXISTS", status_code=400)

        created_user = auth_service.create_user(
            db,
            user_data.name,
            user_data.email,
            user_data.password
        )

        if not created_user:
            return responder.response("USER_NOT_REGISTERED", status_code=400)

        return responder.response("USER_REGISTERED")
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)

async def login(user_data: RegisterLoginSchema, db: Session = Depends(get_db)):
    try:
        user = auth_service.get_user_by_email(db, user_data.email)

        if not user:
            return responder.response("USER_NOT_EXISTS", status_code=404)

        is_match = auth_service.verify_password(user_data.password, user.password)

        if not is_match:
            return responder.response("INVALID_CREDS", status_code=401)

        token = auth_service.create_access_token(user)

        return responder.response("LOGIN_SUCCESS", data={"token": token})
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)
