from datetime import datetime, timedelta
from typing import Optional, Dict
import bcrypt
from jose import jwt
from app.core.config import settings
from app.db.models.user import User

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode()
    )

def create_access_token(user: User, expires_delta: Optional[timedelta] = None) -> str:
    """Create access token for user"""
    # Get base token data
    token_data = {
        "sub": user.email,
        "user_id": user.id,
        # Get organization IDs where user is admin
        "admin_orgs": [
            org_user.organization_id 
            for org_user in user.organizations 
            if org_user.user_type == "admin"
        ]
    }
    
    # Add expiration
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    token_data.update({"exp": expire})
    
    # Create token
    return jwt.encode(
        token_data,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def decode_access_token(token: str) -> Dict:
    """Decode access token"""
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )