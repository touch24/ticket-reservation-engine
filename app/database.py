from contextlib import asynccontextmanager
import os
from fastapi import Request
import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/ticket_db")


@asynccontextmanager
async def lifespan(app):
	app.state.db_pool = await asyncpg.create_pool(
		dsn=DATABASE_URL,
		min_size=5,
		max_size=20,
		timeout=10.0,
		command_timeout=5.0
	)

	yield

	await app.state.db_pool.close()


async def get_db_connection(request: Request):
	pool = request.app.state.db_pool
	async with pool.acquire() as connection:
		yield connection