from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from configs.database import get_db
from services import comment_service
from utils import responder
from app.middlewares.is_authenticated import is_authenticated
from app.schemas import CommentCreate, Comment

async def get_comments_for_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    try:
        comments = comment_service.get_comments_for_post(db, post_id)
        # Convert SQLAlchemy models to Pydantic models for proper serialization
        comments_data = [Comment.model_validate(comment).model_dump() for comment in comments]
        return responder.response("COMMENTS_FETCHED", data=comments_data)
    except Exception as error:
        print(f"Error fetching comments: {error}")
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
        # Convert SQLAlchemy model to Pydantic model for proper serialization
        comment_data = Comment.model_validate(comment).model_dump()
        return responder.response("COMMENT_ADDED", data=comment_data)
    except Exception as error:
        print(f"Error creating comment: {error}")
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
        print(f"Error deleting comment: {error}")
        return responder.response("SERVER_ERROR", status_code=500)
