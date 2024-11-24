from sqlalchemy import create_engine
from app.db.base_class import Base
from app.core.config import settings
from app.db.models.organization import Organization
from app.db.models.user import User
from app.db.models.organization_user import OrganizationUser

def init_db():
    engine = create_engine(settings.MASTER_DATABASE_URL)
    
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine) 