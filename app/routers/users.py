from fastapi import APIRouter, status, HTTPException, Depends
from app.schemas.user import UserResponse, UserCreate
from app.repositories.user_repository import UserRepository
import asyncpg
from app.database import get_db_connection

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def add_user(payload: UserCreate, conn: asyncpg.Connection=Depends(get_db_connection)):
    repo = UserRepository(conn)

    existing_email = await repo.get_by_email(payload.email)
    if (existing_email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{payload.email} already registered"
        );

    return dict(await repo.create(email=payload.email, full_name=payload.full_name))

