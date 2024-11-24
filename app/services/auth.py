from datetime import timedelta
from fastapi import HTTPException, status
from loguru import logger
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.db.repositories.user import UserRepository
from app.core.constants import UserType

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate_user(self, email: str, password: str):
        logger.info(f"Attempting to authenticate user: {email}")
        
        user = self.user_repository.get_by_email(email)
        if not user:
            logger.warning(f"Authentication failed: User not found - {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Authentication failed: Invalid password - {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            user=user,
            expires_delta=access_token_expires
        )
        
        logger.info(f"User authenticated successfully: {email}")
        return {
            "access_token": access_token,
            "token_type": "bearer"
        } 

    def authenticate_admin(self, email: str, password: str):
        """Authenticate admin users"""
        logger.info(f"Attempting to authenticate admin: {email}")
        
        # Check if user exists
        user = self.user_repository.get_by_email(email)
        if not user:
            logger.warning(f"Admin authentication failed: User not found - {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Admin authentication failed: Invalid password - {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check admin status
        if not any(org_user.user_type == "admin" for org_user in user.organizations):
            logger.warning(f"Authentication failed: User is not an admin - {email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have admin privileges"
            )
        
        # Generate token - Pass the entire user object
        access_token = create_access_token(user=user)
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }