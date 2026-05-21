from fastapi import Request
from fastapi.responses import JSONResponse


async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=404, content={"success": False, "message": str(exc)})


async def validation_error_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=422, content={"success": False, "message": str(exc)})
