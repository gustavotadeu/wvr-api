from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True, index=True)
    key_hash = Column(String, unique=True, index=True)
    owner = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class NmapScan(Base):
    __tablename__ = "nmap_scans"
    id = Column(Integer, primary_key=True, index=True)
    target = Column(String)
    options = Column(String)
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
