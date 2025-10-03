import os
import jwt
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
            return responder.response_ok_issues("USER_EXISTS", {})

        created_user = auth_service.create_user(
            db,
            user_data.name,
            user_data.email,
            user_data.password
        )

        if not created_user:
            return responder.response_ok_issues("USER_NOT_REGISTERED", {})

        return responder.response_ok("USER_REGISTERED", {})
    except Exception as error:
        return responder.response_server_error()

async def login(user_data: RegisterLoginSchema, db: Session = Depends(get_db)):
    try:
        user = auth_service.get_user_by_email(db, user_data.email)

        if not user:
            return responder.response_ok_issues("USER_NOT_EXISTS", {})

        is_match = auth_service.verify_password(user_data.password, user.password)

        if not is_match:
            return responder.response_ok_issues("INVALID_CREDS", {})

        token = jwt.encode(
            {"id": user.id, "name": user.name},
            os.getenv("JWT_SECRET_KEY"),
            algorithm="HS256"
        )

        return responder.response_ok("LOGIN_SUCCESS", {"token": token})
    except Exception as error:
        return responder.response_server_error()
