from typing import Optional
from app.schemas.base import BaseSchema
from datetime import datetime

class OrganizationBase(BaseSchema):
    name: str

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime
    db_connection_string: str

    class Config:
        from_attributes = True

# For the request body that includes both org and admin data
class OrganizationWithAdminCreate(BaseSchema):
    org_in: OrganizationCreate
    admin_in: "UserCreate"  # Forward reference to avoid circular import

from app.schemas.user import UserCreate  # Add at the end to resolve forward reference