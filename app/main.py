from fastapi import FastAPI, Depends, HTTPException, status
import asyncpg
from contextlib import asynccontextmanager 
import os

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

app = FastAPI(title="Ticket Reservation System", lifespan=lifespan)

async def get_db_connection():
	pool = app.state.db_pool
	async with pool.acquire() as connection:
		yield connection
	

@app.get("/")
async def root():
	return {
		"status": "Running",
		"service": "Ticket Reservation System"
	}

@app.get("/health")
async def health_check():
	try:
		pool: asyncpg.Pool = app.state.db_pool

		async with pool.acquire(timeout=2.0) as connection:
			conn: asyncpg.Connection = connection
			result = await conn.fetchval("SELECT 1;")
			if (result != 1):
				raise Exception("Invalid ping response from the database")
			
		return {
			# "status_code": status.HTTP_200_OK,
			"status": "healthy",
			"service": "Ticket Reservation System",
			"database": "Reachable"
		} 
	except Exception as err:
		err_msg = str(err) or type(err).__name__
		raise HTTPException(
			status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
			detail=f"Database Unreachable: {err_msg}"
		)
	
