from fastapi import APIRouter

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/topup")
async def topup():
    pass


@router.post("/spend")
async def spend():
    pass


@router.get("/history")
async def history():
    pass
