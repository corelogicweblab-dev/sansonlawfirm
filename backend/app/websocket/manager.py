import json
from typing import Any
from uuid import UUID

import redis.asyncio as aioredis

from app.core.config import get_settings

settings = get_settings()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list] = {}

    async def connect(self, user_id: str, websocket):
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: str, websocket):
        if user_id in self.active_connections:
            self.active_connections[user_id] = [
                ws for ws in self.active_connections[user_id] if ws != websocket
            ]

    async def send_to_user(self, user_id: str, message: dict[str, Any]):
        if user_id in self.active_connections:
            for ws in self.active_connections[user_id]:
                try:
                    await ws.send_json(message)
                except Exception:
                    pass


class RedisPubSub:
    CHANNEL = "sanson:realtime"

    def __init__(self):
        self.redis: aioredis.Redis | None = None

    async def get_redis(self) -> aioredis.Redis:
        if not self.redis:
            self.redis = aioredis.from_url(settings.redis_url, decode_responses=True)
        return self.redis

    async def publish(self, event: str, data: dict[str, Any], user_id: UUID | None = None):
        redis = await self.get_redis()
        payload = json.dumps({"event": event, "data": data, "user_id": str(user_id) if user_id else None})
        await redis.publish(self.CHANNEL, payload)

    async def subscribe(self, callback):
        redis = await self.get_redis()
        pubsub = redis.pubsub()
        await pubsub.subscribe(self.CHANNEL)
        async for message in pubsub.listen():
            if message["type"] == "message":
                await callback(json.loads(message["data"]))


manager = ConnectionManager()
pubsub = RedisPubSub()
