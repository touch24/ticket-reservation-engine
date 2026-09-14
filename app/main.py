from fastapi import FastAPI

app = FastAPI(title="Ticket Reservation System")

@app.get("/")
async def root():
	return {
		"status": "Running",
		"service": "Ticket Reservation System"
	}

@app.get("/health")
async def health_check():
	return {
		"status": "healthy",
		"service": "Ticket Reservation System"
	}
