from unittest.mock import Mock
from datetime import datetime

def mock_user(
    id: int = 1,
    email: str = "test@example.com",
    full_name: str = "Test User",
    is_admin: bool = False
) -> Mock:
    user = Mock()
    user.id = id
    user.email = email
    user.full_name = full_name
    user.created_at = datetime.utcnow()
    
    # Mock organizations relationship
    org_user = Mock()
    org_user.user_type = "admin" if is_admin else "member"
    org_user.organization_id = 1
    user.organizations = [org_user] if is_admin else []
    
    return user

def mock_organization(
    id: int = 1,
    name: str = "Test Org",
) -> Mock:
    org = Mock()
    org.id = id
    org.name = name
    org.created_at = datetime.utcnow()
    return org 