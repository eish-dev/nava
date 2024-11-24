from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
from app.core.constants import UserType

class OrganizationUser(Base):
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organization.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    user_type: Column[UserType] = Column(
        Enum(UserType),
        nullable=False,
        default=UserType.MEMBER
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="users")
    user = relationship("User", back_populates="organizations") 