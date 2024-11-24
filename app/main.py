from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.endpoints import organization, admin
from app.db.init_db import init_db
from app.core.logging import setup_logging, logger
from app.db.session import SessionLocal
from app.db.repositories.user import UserRepository
from app.db.models.user import User
from app.db.models.organization import Organization
from app.db.models.organization_user import OrganizationUser
from app.core.security import get_password_hash
from app.api.endpoints.admin import router as admin_router  # Updated import path

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    logger.info("Starting application...")
    init_db()
    logger.info("Database initialized")
    create_first_admin()
    logger.info("Initial setup completed")
    
    yield  # Server is running
    
    # Shutdown
    logger.info("Shutting down application...")

app = FastAPI(lifespan=lifespan)

def create_first_admin():
    """Create first admin user if it doesn't exist"""
    try:
        db = SessionLocal()
        user_repository = UserRepository(db)
        
        # Check if admin already exists
        admin_email = "admin@admin.com"
        existing_admin = user_repository.get_by_email(admin_email)
        
        if not existing_admin:
            logger.info("Creating first admin user...")
            
            # Create admin user
            admin = User(
                email=admin_email,
                hashed_password=get_password_hash("admin"),
                full_name="System Admin"
            )
            db.add(admin)
            
            # Create a default organization
            org = Organization(
                name="System Organization",
                db_connection_string="postgresql://eish:postgres@localhost:5432/system_org"
            )
            db.add(org)
            db.flush()  # Flush to get IDs
            
            # Create admin-organization relationship
            org_user = OrganizationUser(
                user_id=admin.id,
                organization_id=org.id,
                user_type="admin"
            )
            db.add(org_user)
            
            db.commit()
            logger.info(f"Created admin user: {admin_email}")
        else:
            logger.info("Admin user already exists")
            
    except Exception as e:
        logger.error(f"Error creating admin user: {str(e)}")
        raise e
    finally:
        db.close()

app.include_router(
    organization.router,
    tags=["organizations"]
)

app.include_router(
    admin_router,
    tags=["admin"]
)

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}

# Register routers
app.include_router(admin_router)


