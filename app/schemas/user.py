from pydantic import EmailStr, Field, BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(
        min_length=2,
        max_length=100
    )

class UserResponse(BaseModel):
    public_id: UUID 
    email: str
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)