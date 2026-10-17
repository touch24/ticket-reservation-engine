import asyncpg

class TicketTypeRepository():
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def create(self, name: str, total_capacity: int, price_in_cents: int) -> asyncpg.Record:
        return await self.conn.fetchrow("INSERT INTO ticket_types (name, total_capacity, price_in_cents) VALUES ($1, $2, $3) RETURNING public_id, name, total_capacity, price_in_cents, created_at", name, total_capacity, price_in_cents)

    async def list_all(self) -> list[asyncpg.Record]:
        return await self.conn.fetch("SELECT * FROM ticket_types ORDER BY created_at DESC")

    async def get_by_name(self, name: str) -> asyncpg.Record | None:
        return await self.conn.fetchrow("SELECT * from ticket_types WHERE name = $1", name)