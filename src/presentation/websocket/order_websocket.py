from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ...application.socket_manager.order_manager import order_manager


router = APIRouter(prefix="/ws", tags=["Order Websocket"])

@router.websocket(path="/order/{order_id}")
async def listen_order_status(client_websocket: WebSocket, order_id: int):
    await order_manager.connect(client_websocket=client_websocket, order_id=order_id)
    try:
        while True:
            await client_websocket.receive_json()
    except WebSocketDisconnect:
        order_manager.disconnect(client_websocket, order_id)
