import os
import sys
from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['ADMIN_TOKEN'] = 'admintest'

from app.models import Base
from app.database import engine
from app.routers.apikeys import router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def setup_module(module):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_generate_key_success():
    response = client.post('/apikeys/?owner=alice&admin_token=admintest')
    assert response.status_code == 201
    data = response.json()
    assert 'api_key' in data and data['api_key']


def test_generate_key_invalid_admin_token():
    response = client.post('/apikeys/?owner=bob&admin_token=wrong')
    assert response.status_code == 401
