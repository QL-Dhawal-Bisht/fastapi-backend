from fastapi import APIRouter
from app.controllers import auth_controller, home_controller, user_controller

router = APIRouter()

# Pre-Auth Routes
@router.get("/")
async def home_route(db: auth_controller.Session = auth_controller.Depends(auth_controller.get_db)):
    return await home_controller.home(db)

@router.post("/register")
async def register_route(user_data: auth_controller.RegisterLoginSchema, db: auth_controller.Session = auth_controller.Depends(auth_controller.get_db)):
    return await auth_controller.register(user_data, db)

@router.post("/login")
async def login_route(user_data: auth_controller.RegisterLoginSchema, db: auth_controller.Session = auth_controller.Depends(auth_controller.get_db)):
    return await auth_controller.login(user_data, db)

# Auth Routes
@router.get("/me")
async def get_user_profile_route(current_user: dict = auth_controller.Depends(user_controller.is_authenticated), db: auth_controller.Session = auth_controller.Depends(user_controller.get_db)):
    return await user_controller.get_user_profile(current_user, db)
