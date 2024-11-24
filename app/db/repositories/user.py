from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.repositories.base import BaseRepository
from app.db.models.user import User
from app.core.constants import UserType

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def is_admin_of_any_org(self, user_id: int) -> bool:
        """Check if user is admin in any organization"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
            
        for org_user in user.organizations:
            if org_user.user_type == UserType.ADMIN:
                return True
        return False

    def get_admin_organizations(self, user_id: int) -> List[int]:
        """Get list of organization IDs where user is admin"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return []
            
        return [
            org_user.organization_id 
            for org_user in user.organizations 
            if org_user.user_type == UserType.ADMIN
        ]

    def get_organizations(self, user_id: int):
        return self.db.query(User)\
            .filter(User.id == user_id)\
            .first() 