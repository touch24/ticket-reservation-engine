from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class ReservationCreate(BaseModel):
    user_public_id: UUID
    ticket_type_public_id: UUID

class ReservationResponse(BaseModel):
    public_id: UUID
    user_public_id: UUID
    ticket_type_public_id: UUID
    status: str
    created_at: datetime
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)