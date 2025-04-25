from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ...infrastructure.config.security import websocket_verify_access_token
from ...infrastructure.utils.token_util import TokenClaims
from ...application.socket_manager.staff_manager import staff_manager

router = APIRouter(prefix="/ws", tags=["Staff"])

@router.websocket(path="/staff/order")
async def listen_new_order(client_websocket: WebSocket):
    await staff_manager.handshake_connection(client_websocket=client_websocket)
    claims: TokenClaims = await websocket_verify_access_token(client_websocket=client_websocket)
    await staff_manager.connect(client_id=claims.id, client_websocket=client_websocket)
    try:
        while True:
            await client_websocket.receive_json()
    except WebSocketDisconnect:
        staff_manager.disconnect(client_id=claims.id)
