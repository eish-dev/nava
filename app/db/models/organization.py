from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Organization(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    db_connection_string = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # One Organization can have many OrganizationUsers
    users = relationship("OrganizationUser", back_populates="organization", uselist=True) 