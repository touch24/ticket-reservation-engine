from fastapi import FastAPI, HTTPException, status
import asyncpg
from app.routers.ticket_types import router as ticket_types_router
from app.routers.users import router as users_router
from app.database import lifespan

app = FastAPI(title="Ticket Reservation System", lifespan=lifespan)

app.include_router(users_router)
app.include_router(ticket_types_router)

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
	
