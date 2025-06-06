import os
import sys
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['ADMIN_TOKEN'] = 'admintest'

from app.models import Base
from app.database import engine, SessionLocal
from app.auth import create_api_key
from app.routers.subdomains import router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def setup_module(module):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_subdomains_scan(monkeypatch):
    def fake_run(domain: str):
        return ["a." + domain, "b." + domain]

    monkeypatch.setattr("app.routers.subdomains.run_sublist3r", fake_run)
    with SessionLocal() as db:
        key = create_api_key(db, "tester")
    headers = {"Authorization": f"Bearer {key}"}
    response = client.post("/subdomains/scan?domain=example.com", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "domain": "example.com",
        "subdomains": ["a.example.com", "b.example.com"],
    }
