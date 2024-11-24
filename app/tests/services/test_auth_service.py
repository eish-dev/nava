import pytest
from unittest.mock import Mock
from app.tests.base_test import BaseTest
from app.services.auth import AuthService
from app.tests.factories import UserFactory, OrganizationUserFactory
from fastapi import HTTPException
import uuid
from app.core.security import get_password_hash

class TestAuthService(BaseTest):
    def setup_method(self):
        self.user_repository = Mock()
        self.service = AuthService(self.user_repository)
    
    def test_authenticate_admin_success(self):
        password = "password123"
        hashed_password = get_password_hash(password)
        
        # Create mock admin with proper hashed password
        admin = UserFactory(
            email=f"admin_{uuid.uuid4()}@test.com",
            hashed_password=hashed_password
        )
        OrganizationUserFactory(user=admin, user_type="admin")
        
        # Set up mock to return our admin
        self.user_repository.get_by_email.return_value = admin
        
        # Use the same password we hashed
        result = self.service.authenticate_admin(admin.email, password)
        assert result is not None  # Add appropriate assertions based on expected return value
    
    def test_authenticate_admin_invalid_credentials(self):
        self.user_repository.get_by_email.return_value = None
        
        with pytest.raises(HTTPException) as exc:
            self.service.authenticate_admin("wrong@example.com", "wrongpass")
        
        assert exc.value.status_code == 401 