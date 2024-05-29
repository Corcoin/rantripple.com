import asyncio
import websockets
import json

clients = {}

async def register(websocket, path):
    clients[websocket] = {"state": "connected"}
    print(f"{websocket.remote_address} connects.")
    await notify_users()

async def unregister(websocket):
    if websocket in clients:
        del clients[websocket]
        print(f"{websocket.remote_address} disconnects.")
        await notify_users()

async def notify_users():
    if clients:
        message = json.dumps({"type": "users", "count": len(clients)})
        await asyncio.wait([client.send(message) for client in clients])

async def handler(websocket, path):
    await register(websocket, path)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["type"] == "message":
                await asyncio.wait([client.send(message) for client in clients if client != websocket])
            elif data["type"] == "state_update":
                clients[websocket]["state"] = data["state"]
                print(f"{websocket.remote_address} state updated to {data['state']}")
    finally:
        await unregister(websocket)

if __name__ == "__main__":
    server = websockets.serve(handler, "localhost", 6789)

    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
