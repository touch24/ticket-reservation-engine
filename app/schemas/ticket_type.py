from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime

class TicketTypeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    total_capacity: int = Field(gt=0)
    price_in_cents: int = Field(ge=0)

class TicketTypeResponse(BaseModel):
    public_id: UUID
    name: str
    total_capacity: int
    price_in_cents: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

