from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
from app.core.constants import UserType

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    organizations = relationship("OrganizationUser", back_populates="user")

    @property
    def is_superuser(self, organization_id: Optional[int] = None) -> bool:
        """Check if user is a superuser"""
        for org_user in self.organizations:
            if organization_id is None or org_user.organization_id == organization_id:
                if org_user.user_type == UserType.SUPERUSER:
                    return True
        return False

    @property
    def is_admin(self, organization_id: Optional[int] = None) -> bool:
        """Check if user is an admin"""
        for org_user in self.organizations:
            if organization_id is None or org_user.organization_id == organization_id:
                if org_user.user_type in [UserType.SUPERUSER, UserType.ADMIN]:
                    return True
        return False
  