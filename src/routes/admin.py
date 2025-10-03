from fastapi import APIRouter
from app.controllers import auth_controller, home_controller, user_controller

router = APIRouter()

# Pre-Auth Routes
router.add_api_route("/", home_controller.home, methods=["GET"])
router.add_api_route("/register", auth_controller.register, methods=["POST"])
router.add_api_route("/login", auth_controller.login, methods=["POST"])

# Auth Routes
router.add_api_route("/me", user_controller.get_user_profile, methods=["GET"])
