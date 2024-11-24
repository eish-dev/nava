import pytest
from sqlalchemy import text
from app.db.base_class import Base
from app.tests.factories import set_session

class BaseTest:
    @pytest.fixture(autouse=True)
    def setup_base(self, db_session):
        """Base setup that runs for all test classes that inherit from BaseTest"""
        self.db = db_session
        set_session(db_session)  # Set the session for factories
        
        yield
        
        # Cleanup
        self.db.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            self.db.execute(text(f'TRUNCATE TABLE "{table.name}" CASCADE'))
        self.db.commit()
        set_session(None)  # Clear the session after the test
        
    def teardown(self):
        self.db.rollback() 