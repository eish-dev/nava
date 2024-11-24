from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import TokenResponse, UserLogin
from app.services.auth import AuthService
from app.db.repositories.user import UserRepository

router = APIRouter(prefix="/api/v1/auth")

@router.post("/login", response_model=TokenResponse)
def login(
    *,
    db: Session = Depends(get_db),
    user_in: UserLogin
):
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)
    
    try:
        token = auth_service.authenticate_user(user_in.email, user_in.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    return token 