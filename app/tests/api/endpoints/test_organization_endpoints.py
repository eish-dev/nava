import pytest
from app.tests.base_test import BaseTest
from app.tests.factories import UserFactory, OrganizationFactory, OrganizationUserFactory
from app.core.security import create_access_token
import uuid

class TestOrganizationEndpoints(BaseTest):
    @pytest.fixture(autouse=True)
    def setup_method(self, db_session):
        super().setup_base(db_session)  # Call the base setup first
        # Create admin user and get token
        self.admin_user = UserFactory(email=f"admin_{uuid.uuid4()}@test.com")
        self.org_user = OrganizationUserFactory(user=self.admin_user, user_type="admin")
        self.db.commit()  # Commit to get the ID
        self.db.refresh(self.admin_user)  # Refresh to get relationships
        # Create token with the user object
        self.admin_token = create_access_token(user=self.admin_user)

    def test_create_organization_success(self, client):
        """Test successful organization creation"""
        payload = {
            "org_in": {
                "name": "My Organization 2",
                "db_connection_string": "postgresql://test:test@localhost:5432/test_org_2"
            },
            "admin_in": {
                "email": "admin1@example.com",
                "password": "strongpassword123",
                "full_name": "Admin User"
            }
        }

        response = client.post(
            "/api/v1/organization/",
            json=payload,
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == payload["org_in"]["name"]
        assert "id" in data
        assert "db_connection_string" in data
  