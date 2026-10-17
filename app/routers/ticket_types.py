from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.ticket_type import TicketTypeCreate, TicketTypeResponse
from app.repositories.ticket_repository import TicketTypeRepository
from app.database import get_db_connection
import asyncpg

router = APIRouter(prefix="/ticket_types", tags=["Ticket Types"])

@router.post("/", response_model=TicketTypeResponse, status_code=status.HTTP_201_CREATED)
async def add_ticket_type(payload: TicketTypeCreate, conn: asyncpg.Connection=Depends(get_db_connection)):
    repo = TicketTypeRepository(conn)

    existing_ticket_type = await repo.get_by_name(payload.name)
    print(existing_ticket_type)
    if existing_ticket_type is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{payload.name} already exists."
        )

    return dict(await repo.create(payload.name, payload.total_capacity, payload.price_in_cents))

@router.get("/", response_model=list[TicketTypeResponse])
async def get_ticket_types(conn: asyncpg.Connection=Depends(get_db_connection)) -> list[asyncpg.Record]:
    repo = TicketTypeRepository(conn)
    ticket_types = await repo.list_all()

    return [dict(ticket_type) for ticket_type in ticket_types]