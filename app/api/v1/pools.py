from fastapi import APIRouter,HTTPException,status, Depends
from app.core.dependencies import get_db, get_current_user
from app.schemas.pool import PoolCreateSchema, PoolUpdateSchema, PoolResponseSchema, PoolDetailResponseSchema
from app.services.wallet_service import WalletService
from sqlalchemy.orm import Session
router = APIRouter(prefix="/pools", tags=["pools"])
@router.post("/")
def create_pool(data:
PoolCreateSchema, db: Session = Depends(get_db), current_user= Depends(get_current_user)):
  service= WalletService(db)
  return service.create_pool(
    name=data.name,
    description= data.description,
    icon_url= data.icon_url,
    created_by= str(current_user.id)
  )
@router.get("/")
def get_my_pools(
  db: Session = Depends(get_db),
  current_user= Depends(get_current_user)
):
  service= WalletService(db)
  return service.get_pools_by_user