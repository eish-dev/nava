from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger
from app.db.session import get_db
from app.schemas.auth import TokenResponse, UserLogin
from app.services.auth import AuthService
from app.db.repositories.user import UserRepository

router = APIRouter(prefix="/api/v1/admin")

@router.post("/login", response_model=TokenResponse)
def admin_login(
    *,
    db: Session = Depends(get_db),
    user_in: UserLogin
):
    """Admin login endpoint"""
    logger.info(f"Admin login attempt for: {user_in.email}")
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)
    
    try:
        token = auth_service.authenticate_admin(user_in.email, user_in.password)
        logger.info(f"Admin login successful: {user_in.email}")
        return token
    except HTTPException as e:
        logger.error(f"Admin login failed: {e.detail}")
        raise e
    except Exception as e:
        error_msg = f"Unexpected error during admin login: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred during login"
        ) 