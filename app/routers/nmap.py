from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..auth import get_current_key, get_db
from ..utils.nmap_runner import run_nmap
from ..models import NmapScan

router = APIRouter(prefix="/nmap", tags=["nmap"])


@router.post("/scan")
def scan(target: str, options: str = "", db: Session = Depends(get_db), api_key=Depends(get_current_key)):
    try:
        result = run_nmap(target, options)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    scan_entry = NmapScan(target=target, options=options, result=result)
    db.add(scan_entry)
    db.commit()
    db.refresh(scan_entry)
    return {"scan_id": scan_entry.id, "result": result}


@router.get("/scan/{scan_id}")
def get_scan(scan_id: int, db: Session = Depends(get_db), api_key=Depends(get_current_key)):
    scan_entry = db.query(NmapScan).filter_by(id=scan_id).first()
    if not scan_entry:
        raise HTTPException(status_code=404, detail="Scan not found")
    return {"scan_id": scan_entry.id, "target": scan_entry.target, "options": scan_entry.options, "result": scan_entry.result}
