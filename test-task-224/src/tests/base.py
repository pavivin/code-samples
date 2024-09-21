from src.auth.manager import get_jwt_strategy
from src.app.auth.models import User


async def get_user_headers(user: User) -> dict:  # TODO: fixture on base user
    token = await get_jwt_strategy().write_token(user)
    return {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {token}",
    }
