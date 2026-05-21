from fastapi import APIRouter

router = APIRouter(prefix="/members", tags=["members"])


@router.post("/")
async def add_member():
    pass


@router.delete("/{member_id}")
async def remove_member(member_id: int):
    pass


@router.patch("/{member_id}/role")
async def change_role(member_id: int):
    pass
