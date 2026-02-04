"""Authentication API endpoints."""

from datetime import datetime, timedelta, timezone
from typing import Optional
import hashlib

from fastapi import APIRouter, HTTPException, status, Form, Depends
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.config import get_settings
from src.database import get_session
from src.models.user import User, UserCreate, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    settings = get_settings()
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, settings.better_auth_secret, algorithm="HS256")
    return encoded_jwt


def hash_password(password: str) -> str:
    """Simple password hashing for development."""
    # For development, use SHA-256 with salt
    import secrets
    salt = secrets.token_hex(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}${pwdhash.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        salt, stored_hash = hashed_password.split('$')
        pwdhash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return pwdhash.hex() == stored_hash
    except:
        return False


@router.post("/register", response_model=dict)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    """Register a new user."""
    # Validate passwords match
    if user_data.password != user_data.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # Check if user already exists
    existing_user = await session.execute(
        select(User).where(User.email == user_data.email)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create user in database
    db_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    # Create a JWT token for the user
    token_data = {
        "sub": str(db_user.id),
        "email": user_data.email
    }
    access_token = create_access_token(data=token_data)

    # Prepare user response
    user_response = UserPublic(
        id=db_user.id,
        email=db_user.email,
        full_name=db_user.full_name,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at
    ).dict()

    return {
        "user": user_response,
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=dict)
async def login(email: str = Form(...), password: str = Form(...), session: AsyncSession = Depends(get_session)):
    """Authenticate a user and return a JWT token."""
    # Simple validation
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password required"
        )

    # Find user in database
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create a JWT token for the user
    token_data = {
        "sub": str(user.id),
        "email": user.email
    }
    access_token = create_access_token(data=token_data)

    # Prepare user response
    user_response = UserPublic(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        created_at=user.created_at,
        updated_at=user.updated_at
    ).dict()

    return {
        "user": user_response,
        "access_token": access_token,
        "token_type": "bearer"
    }
