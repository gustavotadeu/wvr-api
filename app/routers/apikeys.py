from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..auth import create_api_key, get_db
from ..config import get_settings

router = APIRouter(prefix="/apikeys", tags=["apikeys"])


@router.post("/", status_code=201)
def generate_key(owner: str, admin_token: str, db: Session = Depends(get_db)):
    settings = get_settings()
    if admin_token != settings.admin_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin token")
    raw_key = create_api_key(db, owner)
    return {"api_key": raw_key}
