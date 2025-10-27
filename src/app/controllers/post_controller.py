from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from configs.database import get_db
from services.post_service import PostService
from utils import responder
from app.middlewares.is_authenticated import is_authenticated
from app.schemas import PostCreate, PostUpdate, Post
import traceback

def get_post_service(db: Session = Depends(get_db)) -> PostService:
    return PostService(db)

async def get_all_posts(
    service: PostService = Depends(get_post_service),
    skip: int = 0,
    limit: int = 10,
    sort: str = "id"
):
    try:
        posts = service.get_all_posts(skip, limit, sort)
        return posts
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)

async def get_post(
    post_id: int,
    service: PostService = Depends(get_post_service)
):
    try:
        post = service.get_post_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)

async def create_post(
    post_data: PostCreate,
    current_user: dict = Depends(is_authenticated),
    service: PostService = Depends(get_post_service)
):
    try:
        post = service.create_post(post_data, current_user["id"])
        return responder.response(
            "POST_CREATED",
            data=Post.model_validate(post).model_dump()
        )
    except Exception as error:
        print(traceback.format_exc())
        raise error

async def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user: dict = Depends(is_authenticated),
    service: PostService = Depends(get_post_service)
):
    try:
        post = service.update_post(post_id, post_data, current_user["id"])
        if not post:
            raise HTTPException(status_code=404, detail="Post not found or not authorized")
        return responder.response("POST_UPDATED", data=post)
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)

async def delete_post(
    post_id: int,
    current_user: dict = Depends(is_authenticated),
    service: PostService = Depends(get_post_service)
):
    try:
        is_admin = current_user.get("role") == "admin"
        post = service.delete_post(post_id, current_user["id"], is_admin)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found or not authorized")
        return responder.response("POST_DELETED")
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)