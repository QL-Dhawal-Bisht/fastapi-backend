from fastapi import APIRouter, Depends
from typing import List
from app.controllers import auth_controller, home_controller, user_controller, post_controller, comment_controller
from app.schemas import UserUpdate, PostCreate, PostUpdate, CommentCreate, Post
from app.middlewares.is_authenticated import is_authenticated
from app.middlewares.validations import RegisterLoginSchema

router = APIRouter()

# Pre-Auth Routes
@router.get("/")
async def home_route(service: home_controller.AuthService = Depends(home_controller.get_auth_service)):
    return await home_controller.home(service)

@router.post("/register")
async def register_route(user_data: RegisterLoginSchema, service: auth_controller.AuthService = Depends(auth_controller.get_auth_service)):
    return await auth_controller.register(user_data, service)

@router.post("/login")
async def login_route(user_data: RegisterLoginSchema, service: auth_controller.AuthService = Depends(auth_controller.get_auth_service)):
    return await auth_controller.login(user_data, service)

# Auth Routes
@router.get("/me")
async def get_user_profile_route(current_user: dict = Depends(is_authenticated), service: user_controller.UserService = Depends(user_controller.get_user_service)):
    return await user_controller.get_user_profile(current_user, service)

@router.put("/me")
async def update_user_profile_route(user_data: UserUpdate, current_user: dict = Depends(is_authenticated), service: user_controller.UserService = Depends(user_controller.get_user_service)):
    return await user_controller.update_user_profile(user_data, current_user, service)

@router.delete("/me")
async def delete_user_profile_route(current_user: dict = Depends(is_authenticated), service: user_controller.UserService = Depends(user_controller.get_user_service)):
    return await user_controller.delete_user_profile(current_user, service)

# Post Routes
@router.get("/posts/", response_model=List[Post])
async def get_all_posts_route(service: post_controller.PostService = Depends(post_controller.get_post_service), skip: int = 0, limit: int = 10, sort: str = "id"):
    return await post_controller.get_all_posts(service, skip, limit, sort)

@router.get("/posts/{post_id}", response_model=Post)
async def get_post_route(post_id: int, service: post_controller.PostService = Depends(post_controller.get_post_service)):
    return await post_controller.get_post(post_id, service)

@router.post("/posts/create")
async def create_post_route(post_data: PostCreate, current_user: dict = Depends(is_authenticated), service: post_controller.PostService = Depends(post_controller.get_post_service)):
    return await post_controller.create_post(post_data, current_user, service)

@router.put("/posts/{post_id}")
async def update_post_route(post_id: int, post_data: PostUpdate, current_user: dict = Depends(is_authenticated), service: post_controller.PostService = Depends(post_controller.get_post_service)):
    return await post_controller.update_post(post_id, post_data, current_user, service)

@router.delete("/posts/{post_id}")
async def delete_post_route(post_id: int, current_user: dict = Depends(is_authenticated), service: post_controller.PostService = Depends(post_controller.get_post_service)):
    return await post_controller.delete_post(post_id, current_user, service)

# Comment Routes
@router.get("/posts/{post_id}/comments")
async def get_comments_for_post_route(post_id: int, service: comment_controller.CommentService = Depends(comment_controller.get_comment_service)):
    return await comment_controller.get_comments_for_post(post_id, service)

@router.post("/posts/{post_id}/comments/create")
async def add_comment_to_post_route(post_id: int, comment_data: CommentCreate, current_user: dict = Depends(is_authenticated), service: comment_controller.CommentService = Depends(comment_controller.get_comment_service)):
    return await comment_controller.add_comment_to_post(post_id, comment_data, current_user, service)

@router.delete("/comments/{comment_id}")
async def delete_comment_route(comment_id: int, current_user: dict = Depends(is_authenticated), service: comment_controller.CommentService = Depends(comment_controller.get_comment_service)):
    return await comment_controller.delete_comment(comment_id, current_user, service)