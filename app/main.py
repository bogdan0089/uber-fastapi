from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.exceptions import BaseAppException
from routers.router_auth import router_auth
from routers.router_user import router_user
from routers.router_trip import router_trip
from routers.router_websocket import router_web_socket
from routers.router_rating import router_rating
from routers.router_admin import router_admin
from routers.router_payment import router_payment


app = FastAPI(title="Uber")

@app.exception_handler(BaseAppException)
async def app_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

app.include_router(router_user)
app.include_router(router_auth)
app.include_router(router_trip)
app.include_router(router_web_socket)
app.include_router(router_rating)
app.include_router(router_admin)