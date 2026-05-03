from fastapi import APIRouter
from fastapi import WebSocket
import json
from utils.connection_manager import ConnectionManager
from core.redis import redis_client
import asyncio
from service.trip_service import TripService


router_web_socket = APIRouter(prefix="/websocket")

manager = ConnectionManager()

@router_web_socket.websocket("/ws/{driver_id}/driver_id", )
async def driver(web_socket: WebSocket, driver_id: int):
    await manager.connect(web_socket)
    try:
        while True:
            data = await web_socket.receive_json()
            await redis_client.set(f"location:{driver_id}", json.dumps(data))
    except:
        manager.disconnect(web_socket)

@router_web_socket.websocket("/ws/passenger/{trip_id}")
async def pessenger(web_socket: WebSocket, trip_id: int):
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


            
        


    

