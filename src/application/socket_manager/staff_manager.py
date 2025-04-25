from fastapi import WebSocket

class StaffManager:
    client_connections: dict[int, WebSocket]

    def __init__(self):
        self.client_connections = {}

    async def handshake_connection(self, client_websocket: WebSocket):
        await client_websocket.accept()

    async def connect(self, client_id: int, client_websocket: WebSocket):
        if client_id not in self.client_connections:
            self.client_connections[client_id] = client_websocket

    def disconnect(self, client_id: int):
        if client_id in self.client_connections:
            del self.client_connections[client_id]

    async def broadcast_new_order(self, order_id: int):
        for client_id, client_websocket in self.client_connections.items():
            await client_websocket.send_json({"order_id": order_id, "message": "Bạn có đơn hàng mới"})

staff_manager = StaffManager()
