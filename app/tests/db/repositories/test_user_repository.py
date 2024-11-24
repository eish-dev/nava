import pytest
from app.tests.base_test import BaseTest
from app.tests.factories import UserFactory
from app.db.repositories.user import UserRepository

class TestUserRepository(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.db = db_session
        self.repository = UserRepository(self.db)
    
    def test_get_by_email(self):
        user = UserFactory(email="test@example.com")
        
        result = self.repository.get_by_email("test@example.com")
        assert result is not None
        assert result.email == user.email
    
    def test_get_by_email_not_found(self):
        retrieved_user = self.repository.get_by_email("nonexistent@example.com")
        assert retrieved_user is None 