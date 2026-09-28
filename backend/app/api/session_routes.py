from __future__ import annotations

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api")


@router.get("/status")
def api_status() -> dict[str, str]:
    return {"status": "online"}
