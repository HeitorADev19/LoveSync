from typing import Dict, List

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.core.security import decode_token
from app.crud import get_user
from app.db.session import AsyncSessionLocal

router = APIRouter()
connections: Dict[int, List[WebSocket]] = {}


async def get_user_from_token(token: str) -> AsyncSession:
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        return None

    async with AsyncSessionLocal() as db:
        return await get_user(db, user_id=user_id)


async def broadcast(couple_id: int, message: dict) -> None:
    for connection in connections.get(couple_id, []):
        await connection.send_json(message)


@router.websocket("/couple")
async def couple_room(websocket: WebSocket, token: str = Query(...)):
    user = await get_user_from_token(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    couple_id = user.couple_id
    await websocket.accept()
    connections.setdefault(couple_id, []).append(websocket)
    await broadcast(couple_id, {"event": "joined", "user": user.full_name})

    try:
        while True:
            data = await websocket.receive_text()
            await broadcast(couple_id, {"event": "message", "from": user.full_name, "text": data})
    except WebSocketDisconnect:
        connections[couple_id].remove(websocket)
        await broadcast(couple_id, {"event": "left", "user": user.full_name})
