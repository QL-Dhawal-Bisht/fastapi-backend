from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from configs.database import get_db
from services import comment_service
from utils import responder
from app.middlewares.is_authenticated import is_authenticated
from app.schemas import CommentCreate

async def get_comments_for_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    try:
        comments = comment_service.get_comments_for_post(db, post_id)
        return responder.response("COMMENTS_FETCHED", data=comments)
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)

async def add_comment_to_post(
    post_id: int,
    comment_data: CommentCreate,
    current_user: dict = Depends(is_authenticated),
    db: Session = Depends(get_db)
):
    try:
        comment = comment_service.create_comment(db, comment_data, post_id, current_user["id"])
        if not comment:
            return responder.response("COMMENT_NOT_ADDED", status_code=400)
        return responder.response("COMMENT_ADDED", data=CommentCreate.model_validate(comment).dict())
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)

async def delete_comment(
    comment_id: int,
    current_user: dict = Depends(is_authenticated),
    db: Session = Depends(get_db)
):
    try:
        is_admin = current_user.get("role") == "admin"
        comment = comment_service.delete_comment(db, comment_id, current_user["id"], is_admin)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found or not authorized")
        return responder.response("COMMENT_DELETED")
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)
