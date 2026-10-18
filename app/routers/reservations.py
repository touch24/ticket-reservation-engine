from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.database import get_db_connection
from app.repositories.reservation_repository import ReservationRepository
import asyncpg

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def add_reservation(payload: ReservationCreate, conn: asyncpg.Connection=Depends(get_db_connection)):
    repo = ReservationRepository(conn)

    try:
        reservation_data = dict(await repo.create_reservation(user_public_id=payload.user_public_id, ticket_type_public_id=payload.ticket_type_public_id))
    except LookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or Ticket Type not found"
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ticket Capacity Exhausted"
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {err}"
        )

    reservation_data["ticket_type_public_id"] = payload.ticket_type_public_id
    reservation_data["user_public_id"] = payload.user_public_id

    return reservation_data