import pytest
from app.tests.base_test import BaseTest
from app.tests.factories import UserFactory, OrganizationUserFactory
import uuid
import logging
from app.core.security import get_password_hash
from app.tests.factories import set_session
from app.db.models.user import User

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestAdminEndpoints(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.db = db_session
        # Set the session for factories
        set_session(db_session)  # Import this from factories
        yield
        # Clean up
        set_session(None)  # Reset the session after test

    def test_admin_login_success(self, client):
        logger.debug("Starting test_admin_login_success")
        
        # Create admin user with unique email
        email = f"admin_{uuid.uuid4()}@test.com"
        password = "testpassword123"
        logger.debug(f"Creating user with email: {email}")
        
        # Create user with known password
        hashed_password = get_password_hash(password)
        user = UserFactory(
            email=email,
            hashed_password=hashed_password
        )
        
        logger.debug("Creating organization user")
        org_user = OrganizationUserFactory(user=user, user_type="admin")
        self.db.commit()
        self.db.refresh(user)
        
        # Verify user exists and has correct data
        saved_user = self.db.query(User).filter(User.email == email).first()
        logger.debug(f"Saved user found: {saved_user is not None}")
        if saved_user:
            logger.debug(f"User email: {saved_user.email}")
            logger.debug(f"User has organizations: {len(saved_user.organizations)}")
            for org in saved_user.organizations:
                logger.debug(f"Organization user type: {org.user_type}")
        
        # Login data matching UserLogin schema
        login_data = {
            "email": email,
            "password": password
        }
        
        logger.debug("Making login request")
        response = client.post("/api/v1/admin/login", json=login_data)
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response body: {response.text}")
        
        assert response.status_code == 200
        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"
    
    def test_admin_login_invalid_credentials(self, client):
        login_data = {
            "email": "wrong@example.com",
            "password": "wrongpass"
        }
        response = client.post("/api/v1/admin/login", json=login_data)
        
        assert response.status_code == 401 