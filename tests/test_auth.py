import os
import sys
import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Ensure database URL is set before importing app modules
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['ADMIN_TOKEN'] = 'admintest'

from app.models import Base
from app.database import engine, SessionLocal
from app.auth import create_api_key, get_current_key

# Create tables for test DB
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/protected")
def protected(api_key=Depends(get_current_key)):
    return {"owner": api_key.owner}

client = TestClient(app)


def setup_module(module):
    # Reset database state
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_get_current_key_missing_header():
    response = client.get("/protected")
    assert response.status_code == 401


def test_get_current_key_valid_header():
    with SessionLocal() as db:
        key = create_api_key(db, "tester")
    headers = {"Authorization": f"Bearer {key}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"owner": "tester"}

def test_get_current_key_invalid_token():
    headers = {"Authorization": "Bearer invalid"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401


def test_get_current_key_invalid_prefix():
    with SessionLocal() as db:
        key = create_api_key(db, "tester2")
    headers = {"Authorization": key}  # missing Bearer prefix
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
