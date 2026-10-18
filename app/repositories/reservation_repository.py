import asyncpg
from uuid import UUID
from datetime import datetime, timezone, timedelta
from app.exceptions import EntityNotFoundError, InventoryExhaustedError


class ReservationRepository():
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def create_reservation(self, user_public_id: UUID, ticket_type_public_id: UUID, hold_minutes: int = 10) -> asyncpg.Record:
        async with self.conn.transaction():
            user_id: int | None = await self.conn.fetchval("SELECT id FROM users WHERE public_id = $1;", user_public_id)
            if user_id is None:
                raise EntityNotFoundError("User does not exist")

            ticket_type = await self.conn.fetchrow("SELECT id, total_capacity FROM ticket_types WHERE public_id = $1 FOR UPDATE;", ticket_type_public_id)
            if ticket_type is None:
                raise EntityNotFoundError("Ticket Type not found")

            consumed_seats: int = await self.conn.fetchval("SELECT COUNT(*) FROM reservations WHERE ticket_type_id = $1 AND (status = 'CONFIRMED' OR (status = 'PENDING' AND expires_at > CURRENT_TIMESTAMP));", ticket_type["id"])
            if consumed_seats >= ticket_type["total_capacity"]:
                raise InventoryExhaustedError("Sold Out")

            expires_at: datetime = datetime.now(timezone.utc) + timedelta(minutes=hold_minutes)

            return dict(await self.conn.fetchrow("INSERT INTO reservations (user_id, ticket_type_id, status, expires_at) VALUES ($1, $2, 'PENDING', $3) RETURNING id, public_id, status, expires_at, created_at;", user_id, ticket_type["id"], expires_at))



            

