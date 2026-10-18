from fastapi import APIRouter, status, Depends, HTTPException
from app.exceptions import EntityNotFoundError, InventoryExhaustedError
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.database import get_db_connection
from app.repositories.reservation_repository import ReservationRepository
import asyncpg

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def add_reservation(payload: ReservationCreate, conn: asyncpg.Connection=Depends(get_db_connection)):
    repo = ReservationRepository(conn)

    try:
        return await repo.create_reservation(user_public_id=payload.user_public_id, ticket_type_public_id=payload.ticket_type_public_id)
    except EntityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or Ticket Type not found"
        )
    except InventoryExhaustedError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ticket Capacity Exhausted"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )