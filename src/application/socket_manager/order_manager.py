from fastapi import WebSocket

class OrderManager:
    client_connection: dict[int, list[WebSocket]]

    def __init__(self):
        self.client_connection = {}

    async def connect(self, client_websocket: WebSocket, order_id: int):
        await client_websocket.accept()
        if order_id not in self.client_connection:
            self.client_connection[order_id] = []
        self.client_connection[order_id].append(client_websocket)

    def disconnect(self, client_websocket: WebSocket, order_id: int):
        if order_id in self.client_connection:
            self.client_connection[order_id].remove(client_websocket)
            if not self.client_connection[order_id]:
                del self.client_connection[order_id]

    async def broadcast(self, order_id: int, order_status: str):
        if order_id in self.client_connection:
            for connection in self.client_connection[order_id]:
                await connection.send_json({
                    "order_id": order_id,
                    "order_status": order_status
                })

order_manager = OrderManager()
