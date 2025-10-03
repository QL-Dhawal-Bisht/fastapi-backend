import os
import jwt
from fastapi import Header
from utils.responder import response_unauthenticated, response_validation_issues

async def is_authenticated(authentication_token: str = Header(None, alias="AuthenticationToken")):
    if not authentication_token:
        return response_validation_issues("TOKEN_NOT_FOUND", {}, {})

    try:
        decoded_token = jwt.decode(
            authentication_token,
            os.getenv("JWT_SECRET_KEY"),
            algorithms=["HS256"]
        )
        return {
            "id": decoded_token.get("id"),
            "name": decoded_token.get("name")
        }
    except jwt.InvalidTokenError:
        return response_unauthenticated()
