from typing import Optional
import uuid
from loguru import logger
from app.schemas import organization as org_schemas
from app.schemas import user as user_schemas
from app.core.security import get_password_hash
from app.db.repositories.organization import OrganizationRepository
from app.db.repositories.database import DatabaseRepository
from app.core.config import settings

class OrganizationService:
    def __init__(self, org_repository: OrganizationRepository):
        self.org_repository = org_repository
        self.db_repository = DatabaseRepository()

    def create_db_connection_string(self, org_name: str) -> str:
        """Create a unique database name and connection string"""
        db_name = f"org_{org_name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}"
        connection_string = f"postgresql://eish:postgres@localhost:5432/{db_name}"
        logger.debug(f"Created connection string: {connection_string}")
        return connection_string

    def create_organization_with_admin(
        self,
        org_data: org_schemas.OrganizationCreate,
        admin_data: user_schemas.UserCreate
    ):
        logger.info(f"Creating organization: {org_data.name} with admin: {admin_data.email}")
        
        # Create connection string for new database
        connection_string = self.create_db_connection_string(org_data.name)

        # Create the organization entry in master database
        org_dict = org_data.dict()
        org_dict["db_connection_string"] = connection_string

        try:
            # Create the new database and its schema
            logger.debug("Creating new database")
            self.db_repository.create_database(connection_string)

            # Create organization in master database
            logger.debug("Creating organization and admin user")
            org = self.org_repository.create_with_admin(org_dict, {
                "email": admin_data.email,
                "hashed_password": get_password_hash(admin_data.password),
                "full_name": admin_data.full_name if hasattr(admin_data, 'full_name') else None
            })

            logger.info(f"Successfully created organization {org.name} with ID {org.id}")
            return org

        except Exception as e:
            logger.error(f"Failed to create organization: {str(e)}")
            # If anything fails, clean up
            try:
                logger.debug("Attempting cleanup of failed database creation")
                self.db_repository.cleanup_failed_database(connection_string)
            except Exception as cleanup_error:
                logger.error(f"Cleanup error: {cleanup_error}")
            raise Exception(f"Organization creation failed: {str(e)}")

    def get_organization_by_name(self, name: str):
        logger.info(f"Getting organization by name: {name}")
        return self.org_repository.get_by_name(name=name)

    def get_organization(self, org_id: int):
        logger.info(f"Getting organization by ID: {org_id}")
        return self.org_repository.get(id=org_id) 