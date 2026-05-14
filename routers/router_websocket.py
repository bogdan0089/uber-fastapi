from fastapi import APIRouter
from fastapi import WebSocket
from utils.connection_manager import ConnectionManager
from core.redis import redis_client
import asyncio
from service.trip_service import TripService


router_web_socket = APIRouter(prefix="/websocket", tags=["WebSocket"])

manager = ConnectionManager()

@router_web_socket.websocket("/ws/driver/{driver_id}", )
async def driver(web_socket: WebSocket, driver_id: int):
    await manager.connect(web_socket)
    try:
        while True:
            data = await web_socket.receive_json()
            await redis_client.geoadd("drivers", [data["lon"], data["lat"], f"driver:{driver_id}"])
    except:
        manager.disconnect(web_socket)
        await redis_client.zrem(f"drivers", f"driver_id:{driver_id}")

@router_web_socket.websocket("/ws/passenger/{trip_id}")
async def passenger(web_socket: WebSocket, trip_id: int):
    await manager.connect(web_socket)
    trip = await TripService.get_trip(trip_id)
    driver_id = trip.driver_id
    try:
        while True:
            location = await redis_client.get(f"location:{driver_id}")
            if location:
                await manager.send_to(web_socket, location)
                await asyncio.sleep(2)
    except:
        manager.disconnect(web_socket)


            
        


    

