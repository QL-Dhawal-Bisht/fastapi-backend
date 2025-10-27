from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from configs.database import get_db
from services.comment_service import CommentService
from utils import responder
from app.middlewares.is_authenticated import is_authenticated
from app.schemas import CommentCreate, Comment

def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    return CommentService(db)

async def get_comments_for_post(
    post_id: int,
    service: CommentService = Depends(get_comment_service)
):
    try:
        comments = service.get_comments_for_post(post_id)
        comments_data = [Comment.model_validate(comment).model_dump() for comment in comments]
        return responder.response("COMMENTS_FETCHED", data=comments_data)
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)

async def add_comment_to_post(
    post_id: int,
    comment_data: CommentCreate,
    current_user: dict = Depends(is_authenticated),
    service: CommentService = Depends(get_comment_service)
):
    try:
        comment = service.create_comment(comment_data, post_id, current_user["id"])
        if not comment:
            return responder.response("COMMENT_NOT_ADDED", status_code=400)
        comment_data = Comment.model_validate(comment).model_dump()
        return responder.response("COMMENT_ADDED", data=comment_data)
    except Exception as error:
        return responder.response("SERVER_ERROR", status_code=500)

async def delete_comment(
    comment_id: int,
    current_user: dict = Depends(is_authenticated),
    service: CommentService = Depends(get_comment_service)
):
    try:
        is_admin = current_user.get("role") == "admin"
        comment = service.delete_comment(comment_id, current_user["id"], is_admin)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found or not authorized")
        return responder.response("COMMENT_DELETED")
    except Exception as error:
        print(f"Error deleting comment: {error}")
        return responder.response("SERVER_ERROR", status_code=500)