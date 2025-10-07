"""
Authentication API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta

from ..core.database import get_db
from ..core.security import create_access_token, decode_access_token
from ..core.config import settings
from ..schemas.user import UserCreate, UserLogin, UserResponse, Token
from ..services.auth import auth_service
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    
    Args:
        user: User registration data
        db: Database session
        
    Returns:
        Created user data
    """
    return auth_service.create_user(db, user)


@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return JWT token
    
    Args:
        user: User login credentials
        db: Database session
        
    Returns:
        JWT access token
    """
    db_user = auth_service.authenticate_user(db, user.username, user.password)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user
    
    Args:
        credentials: HTTP authorization credentials with JWT token
        db: Database session
        
    Returns:
        Current user data
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    return auth_service.get_user_by_username(db, username)


async def get_current_user_dependency(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user
    Used in other routes that require authentication
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    return auth_service.get_user_by_username(db, username)
