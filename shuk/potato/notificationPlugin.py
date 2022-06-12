import asyncio
from http.client import NotConnected
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class notificationPl:
    def __init__(self):
        self.connections = {}

    def addConnection(self, conn: AsyncWebsocketConsumer, cookie):
        self.connections[cookie] = conn
        # for debugging:
        #print(len(self.connections))

    def removeConnection(self, conn):
        toremove = [k for k, v in self.connections.items() if v == conn]
        for key in toremove:
            del self.connections[key]
        # for debugging:
        #print(len(self.connections))

    def postBroadcast(self, tokens, message):
        notConnected = []
        for i in self.connections:
            if not(i in tokens):
                notConnected.append(i)
        asyncio.run(self.asyncsend(tokens, message))
        return notConnected

    async def asyncsend(self, tokens, message):
        clients = []
        for i in self.connections:
            if i in tokens:
                clients.append(self.connections[i])
        res = await asyncio.gather(*(self.send_with_timeout(i, message) for i in clients))
        return res
    async def send_with_timeout(self, conn, message):
        try:
            await asyncio.wait_for(self.sender(conn, message), timeout=3.0)
        except asyncio.TimeoutError:
            return "Aw %s" % message
    async def sender(self, conn, message):
        await conn.send(text_data=json.dumps({
            'type': 'domainmessage',
            'message': message
        }))
        return True
