import secrets
import hashlib
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import APIKey


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


def create_api_key(db: Session, owner: str) -> str:
    raw_key = secrets.token_urlsafe(32)
    key_hash = hash_key(raw_key)
    api_key = APIKey(key_hash=key_hash, owner=owner)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return raw_key


def verify_api_key(key: str, db: Session) -> APIKey:
    key_hash = hash_key(key)
    api_key = db.query(APIKey).filter_by(key_hash=key_hash, is_active=True).first()
    return api_key


def get_current_key(authorization: str = Header(None), db: Session = Depends(get_db)) -> APIKey:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    token = authorization.split(" ", 1)[1]
    api_key = verify_api_key(token, db)
    if not api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return api_key
