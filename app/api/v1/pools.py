from fastapi import APIRouter

router = APIRouter(prefix="/pools", tags=["pools"])


@router.post("/")
async def create_pool():
    pass


@router.get("/{pool_id}")
async def get_pool(pool_id: int):
    pass


@router.delete("/{pool_id}")
async def delete_pool(pool_id: int):
    pass
