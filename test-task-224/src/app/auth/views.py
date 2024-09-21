from fastapi import APIRouter
from src.app.auth.schemas import UserCreate, UserRead, UserUpdate
from src.auth.manager import fastapi_auth, auth_backend


router = APIRouter()

router.include_router(fastapi_auth.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])

router.include_router(
    fastapi_auth.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_auth.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_auth.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_auth.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
