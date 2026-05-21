from fastapi import FastAPI
from app.api.v1 import auth, pools, transactions, invites, members

app = FastAPI(title="PoolPay", version="1.0.0")

app.include_router(auth.router, prefix="/api/v1")
app.include_router(pools.router, prefix="/api/v1")
app.include_router(transactions.router, prefix="/api/v1")
app.include_router(invites.router, prefix="/api/v1")
app.include_router(members.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
