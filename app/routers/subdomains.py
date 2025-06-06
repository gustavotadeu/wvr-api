from fastapi import APIRouter, Depends, HTTPException
from ..auth import get_current_key
from ..utils.sublist3r_runner import run_sublist3r

router = APIRouter(prefix="/subdomains", tags=["subdomains"])

@router.post("/scan")
def enumerate_subdomains(domain: str, api_key=Depends(get_current_key)):
    try:
        subdomains = run_sublist3r(domain)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"domain": domain, "subdomains": subdomains}
