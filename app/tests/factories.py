from datetime import datetime
import factory
from factory.alchemy import SQLAlchemyModelFactory
from factory import LazyFunction, Faker, SubFactory
from app.db.models.user import User
from app.db.models.organization import Organization
from app.db.models.organization_user import OrganizationUser
from app.core.security import get_password_hash

# Create a session factory that will be used by all factories
session = None

def set_session(db_session):
    global session
    session = db_session

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        global session
        if not session:
            raise ValueError("Session not set. Call set_session() before using factories.")
        cls._meta.sqlalchemy_session = session
        obj = super()._create(model_class, *args, **kwargs)
        session.flush()
        return obj

    email = Faker('email')
    full_name = Faker('name')
    hashed_password = LazyFunction(lambda: get_password_hash("testpassword123"))
    created_at = LazyFunction(datetime.utcnow)

class OrganizationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Organization
        sqlalchemy_session = None  # Will be set during creation
        sqlalchemy_session_persistence = "commit"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        global session
        if not session:
            raise ValueError("Session not set. Call set_session() before using factories.")
        cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)

    name = Faker('company')
    db_connection_string = Faker('sentence')
    created_at = LazyFunction(datetime.utcnow)

class OrganizationUserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = OrganizationUser
        sqlalchemy_session = None  # Will be set during creation
        sqlalchemy_session_persistence = "commit"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        global session
        if not session:
            raise ValueError("Session not set. Call set_session() before using factories.")
        cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)

    user = SubFactory(UserFactory)
    organization = SubFactory(OrganizationFactory)
    user_type = "user"  # default type
    created_at = LazyFunction(datetime.utcnow) 