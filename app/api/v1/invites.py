from fastapi import APIRouter

router = APIRouter(prefix="/invites", tags=["invites"])


@router.post("/")
async def create_invite():
    pass


@router.post("/{token}/accept")
async def accept_invite(token: str):
    pass
