from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.models.user import User
from app.core.security import hash_password

# CREATE USER
async def create_user(db: AsyncSession, email: str, password: str):
    try:
        user = User(
            email=email,
            password=hash_password(password)
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError:
        await db.rollback()
        raise ValueError("Email already exists")
    except SQLAlchemyError as e:
        await db.rollback()
        raise RuntimeError(f"DB error: {str(e)}")


# GET USER BY ID
async def get_user(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise RuntimeError(f"DB error: {str(e)}")


# GET USER BY EMAIL
async def get_user_by_email(db: AsyncSession, email: str):
    try:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise RuntimeError(f"DB error: {str(e)}")


# GET ALL USERS
async def get_users(db: AsyncSession):
    try:
        result = await db.execute(select(User))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise RuntimeError(f"DB error: {str(e)}")


# UPDATE USER
async def update_user(db: AsyncSession, user_id: int, data: dict):
    user = await get_user(db, user_id)
    if not user:
        raise ValueError("User not found")

    try:
        for key, value in data.items():
            if key == "password":
                value = hash_password(value)
            setattr(user, key, value)
        await db.commit()
        await db.refresh(user)
        return user
    except SQLAlchemyError as e:
        await db.rollback()
        raise RuntimeError(f"DB error: {str(e)}")


# DELETE USER
async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    if not user:
        raise ValueError("User not found")

    try:
        await db.execute(delete(User).where(User.id == user_id))
        await db.commit()
        return {"message": "User deleted"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise RuntimeError(f"DB error: {str(e)}")