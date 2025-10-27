from fastapi import Depends
from sqlalchemy.orm import Session
from configs.database import get_db
from services.auth_service import AuthService
from utils import responder
from app.middlewares.validations import RegisterLoginSchema

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)

async def register(user_data: RegisterLoginSchema, service: AuthService = Depends(get_auth_service)):
    try:
        check_user = service.get_user_by_email(user_data.email)

        if check_user:
            return responder.response("USER_EXISTS", status_code=400)

        created_user = service.create_user(
            user_data.name,
            user_data.email,
            user_data.password
        )

        if not created_user:
            return responder.response("USER_NOT_REGISTERED", status_code=400)

        return responder.response("USER_REGISTERED")
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)

async def login(user_data: RegisterLoginSchema, service: AuthService = Depends(get_auth_service)):
    try:
        user = service.get_user_by_email(user_data.email)

        if not user:
            return responder.response("USER_NOT_EXISTS", status_code=404)

        is_match = service.verify_password(user_data.password, user.password)

        if not is_match:
            return responder.response("INVALID_CREDS", status_code=401)

        token = service.create_access_token(user)

        return responder.response("LOGIN_SUCCESS", data={"token": token})
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)