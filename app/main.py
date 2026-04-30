from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.exceptions import BaseAppException
from routers.router_auth import router_auth
from routers.router_user import router_user




app = FastAPI(title="Uber")

@app.exception_handler(BaseAppException)
async def app_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

app.include_router(router_user)
app.include_router(router_auth)