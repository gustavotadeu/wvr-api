from fastapi import FastAPI
from .config import get_settings
from .database import engine
from .models import Base
from .routers import nmap, apikeys

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="WVR API")

app.include_router(apikeys.router, prefix=settings.api_v1_prefix)
app.include_router(nmap.router, prefix=settings.api_v1_prefix)
