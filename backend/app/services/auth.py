"""
Authentication service for user operations
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.user import User
from ..schemas.user import UserCreate
from ..core.security import get_password_hash, verify_password


class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """Create a new user"""
        # Check if username exists
        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email exists
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password_hash(user.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """Authenticate user with username and password"""
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        return user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """Get user by username"""
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user


# Create service instance
auth_service = AuthService()
