import asyncio
from http.client import NotConnected
import json
from channels.generic.websocket import AsyncWebsocketConsumer

#This works.
#But because of page reloading, you cant send a message to yourself
class notificationPl:
    def __init__(self):
        self.connections = {}

    async def addConnection(self, conn: AsyncWebsocketConsumer, cookie):
        if cookie == "":
            print("Null Cookie Found")
            conn.close()
        else:
            self.connections[conn] = int(cookie)
        # for debugging:
        #print(len(self.connections))

    async def removeConnection(self, conn):
        while conn in self.connections:
            del self.connections[conn]
        #for debugging:
        #print(len(self.connections))
   
   
    def sendAll(self, message):
        missed = asyncio.run(self._notifyAll(message))
        return missed
    def sendBroadcast(self, tokens, message):
        missed = asyncio.run(self._sendwithtimeout(tokens, message))
        return missed
    async def _notifyAll(self, message):
        # Schedule three calls *concurrently*:
        futures = await asyncio.gather(
            *(asyncio.wait_for( self._sender(i, message), timeout=3) for i in self.connections),
        return_exceptions=True)
        return True
    async def _sendwithtimeout(self,tokens, message):
        missed = []
        toSendTo = []
        for i in tokens:
            found = False
            for j in self.connections:
                if self.connections[j] == i:
                    found = True
                    toSendTo.append(j)
            if not(found):
                missed.append(i)

        # Schedule three calls *concurrently*:
        futures = await asyncio.gather(
            *(asyncio.wait_for( self._sender(i, message), timeout=3) for i in toSendTo),
        return_exceptions=True)
        for j in range(len(futures)):
            i = futures[j]
            if not(type(i) is int):
                missed.append(toSendTo[j])
        return missed

    async def _sender(self, conn, message):
        await conn.send(text_data=json.dumps({
            'type': 'domainmessage',
            'message': message
        }))
        return 0