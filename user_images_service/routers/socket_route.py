from typing import List
from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder


socket_rout = APIRouter()


class ConnectionManager:

    """
    Класс создания вебсокет соединений
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):

        """
        Подключение к Вебсокет соединению
        """

        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):

        """
        Отключение от Вебсокет соединения
        """

        self.active_connections.remove(websocket)

    async def send_personal_message(self, message, websocket: WebSocket):
        """
        Отправка данных  json через Вебсокет соединение
        """
        await websocket.send_json(message)

    async def broadcast(self, message):

        """
        Рассылка участникам соединеия что кто то отключился
        из участников от веб сокет соединения
        """

        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()

list_user_id_socket = []


async def add_websocket_id_in_list(websocket, user_google_id):

    """
    Функция добавляет данные вебсокет соединения в список,
    создана с целью того , что бы если клиент выйдет из браузера
    ,а потом снова зайдет ,не создавалось новое подключение а использовалось
    предыдущее
    """
    
    dict_info_websocket_client = {
        'user_google_id': user_google_id, 'websocket_client': websocket}
    if len(list_user_id_socket) != 0:
        for (ind, item) in enumerate(list_user_id_socket):
            if dict_info_websocket_client[
                'user_google_id'
                ] == item[
                    'user_google_id'
                    ]:
                del list_user_id_socket[ind]
            else:
                pass
        list_user_id_socket.append(dict_info_websocket_client)
    elif len(list_user_id_socket) == 0:
        list_user_id_socket.append(dict_info_websocket_client)

    print(list_user_id_socket)


@socket_rout.websocket("/ws/{user_google_id}")
async def websocket_endpoint(websocket: WebSocket, user_google_id: str, ):

    """
    Роут для подключения клиента к вебсокеткам
    """

    await add_websocket_id_in_list(websocket, user_google_id)
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
