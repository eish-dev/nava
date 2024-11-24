from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from loguru import logger
from app.db.session import get_db
from app.core.security import decode_access_token
from app.db.repositories.user import UserRepository
from app.schemas.auth import TokenData
from app.schemas import organization as org_schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except Exception as e:
        logger.error(f"Token validation failed: {str(e)}")
        raise credentials_exception

    user_repository = UserRepository(db)
    user = user_repository.get_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user

def check_admin_access(current_user = Depends(get_current_user)):
    """Check if user has admin access"""
    if not any(org_user.user_type == "admin" for org_user in current_user.organizations):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have admin privileges"
        )
    return current_user 