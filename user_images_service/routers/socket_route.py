from typing import List
from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder


socket_rout = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()

list_user_id_socket = []

@socket_rout.websocket("/ws/{user_google_id}")
async def websocket_endpoint(websocket: WebSocket, user_google_id:str, ):
    dict_info_websocket_client = {'user_google_id':user_google_id,'websocket_client':websocket}
    if (
        dict_info_websocket_client[
            'user_google_id'
            ] not in [
                user_id[
                    'user_google_id'
                    ] for user_id in list_user_id_socket
                ]
                ):
        list_user_id_socket.append(dict_info_websocket_client)
    print(list_user_id_socket)
    
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client # left the chat")

