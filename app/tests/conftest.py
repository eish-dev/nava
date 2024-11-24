import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from fastapi.testclient import TestClient
from app.db.base_class import Base
from app.db.session import get_db
from app.main import app
from app.tests.factories import set_session

# Test database URL
TEST_DATABASE_URL = "postgresql://eish:postgres@localhost:5432/test_db"
TEST_DATABASE_NAME = "test_db"


def create_test_database():
    """Create test database if it doesn't exist"""
    default_engine = create_engine("postgresql://eish:postgres@localhost:5432/postgres")
    
    with default_engine.connect() as default_conn:
        default_conn.execution_options(isolation_level="AUTOCOMMIT")
        
        try:
            # Drop existing connections
            default_conn.execute(text(
                f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{TEST_DATABASE_NAME}'
                AND pid <> pg_backend_pid();
                """
            ))
            # Drop database if exists
            default_conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DATABASE_NAME}"))
            # Create fresh database
            default_conn.execute(text(f"CREATE DATABASE {TEST_DATABASE_NAME}"))
        except Exception as e:
            print(f"Error setting up test database: {e}")
            raise

@pytest.fixture(scope="session")
def engine():
    create_test_database()
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(text(f'TRUNCATE TABLE "{table.name}" CASCADE'))
        session.commit()
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def client():
    return TestClient(app)