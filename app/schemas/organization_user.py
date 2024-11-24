from pydantic import BaseModel
from datetime import datetime
from app.core.constants import UserType

class OrganizationUserCreate(BaseModel):
    organization_id: int
    user_id: int
    user_type: UserType

class OrganizationUserResponse(OrganizationUserCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 