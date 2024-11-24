from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.repositories.base import BaseRepository
from app.db.models.organization import Organization
from app.db.models.organization_user import OrganizationUser
from app.db.models.user import User
from app.core.constants import UserType

class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, db: Session):
        super().__init__(Organization, db)

    def get_by_name(self, name: str) -> Optional[Organization]:
        return self.db.query(Organization).filter(Organization.name == name).first()

    def get_with_users(self, org_id: int) -> Optional[Organization]:
        return self.db.query(Organization)\
            .filter(Organization.id == org_id)\
            .first()

    def create_with_admin(self, org_data: dict, admin_data: dict) -> Organization:
        # Create organization
        org = Organization(**org_data)
        self.db.add(org)
        self.db.flush()

        # Create admin user
        admin = User(**admin_data)
        self.db.add(admin)
        self.db.flush()

        # Create organization-user relationship
        org_user = OrganizationUser(
            organization_id=org.id,
            user_id=admin.id,
            user_type=UserType.ADMIN
        )
        self.db.add(org_user)
        self.db.commit()
        self.db.refresh(org)
        return org 