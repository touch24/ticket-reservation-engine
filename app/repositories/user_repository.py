import asyncpg

class UserRepository():
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def get_by_email(self, email: str) -> asyncpg.Record | None :
        return await self.conn.fetchrow("SELECT * from users WHERE email = $1;", email)

    async def create(self, email: str, full_name: str) -> asyncpg.Record:
        return await self.conn.fetchrow("INSERT INTO users (email, full_name) VALUES ($1, $2) RETURNING public_id, email, full_name, created_at", email, full_name)