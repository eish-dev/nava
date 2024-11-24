from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger
from app.db.session import get_db
from app.schemas import organization as org_schemas
from app.schemas import user as user_schemas
from app.services.organization import OrganizationService
from app.db.repositories.organization import OrganizationRepository
from app.api.deps import check_admin_access
from app.db.models.user import User

router = APIRouter(prefix="/api/v1/organization")

@router.post("/", response_model=org_schemas.OrganizationResponse)
def create_organization(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_access),
    org_in: org_schemas.OrganizationCreate,
    admin_in: user_schemas.UserCreate
):
    """Create new organization (admin access required)"""
    logger.info(f"Received request to create organization: {org_in.name}")
    org_repository = OrganizationRepository(db)
    org_service = OrganizationService(org_repository)
    
    try:
        org = org_service.create_organization_with_admin(org_in, admin_in)
        logger.info(f"Successfully created organization with ID: {org.id}")
        return org
    except Exception as e:
        logger.error(f"Failed to create organization: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{name}", response_model=org_schemas.OrganizationResponse)
def get_organization_by_name(
    name: str,
    db: Session = Depends(get_db)
):
    org_repository = OrganizationRepository(db)
    org_service = OrganizationService(org_repository)
    
    org = org_service.get_organization_by_name(name)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    return org 