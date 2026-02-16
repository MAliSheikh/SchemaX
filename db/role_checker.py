from fastapi import Depends, HTTPException, status
from auth import get_current_user
from models.users import User


# Factory → require specific role
def require_role(role: str):
    async def role_checker(
        user: User = Depends(get_current_user)
    ):
        if user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        return user

    return role_checker