from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor, task
from typing import Set
from sty import fg, bg, ef, rs

color_list = [
    fg.red,
    fg.green,
    fg.blue,
    fg.yellow,
    fg.magenta,
    fg.cyan,
    fg.white,
    fg.li_cyan,
    fg.li_green,
    fg.li_magenta,
    fg.li_red
]

watchers = set()


class Peer(Protocol):
    connections: Set[Protocol]

    def __init__(self, connections, port):
        self.port = port
        self.color = color_list[port % 11]
        self.connections = connections

    def safeAbort(self):
        if self in self.connections:
            self.transport.abortConnection()

    def connectionMade(self):
        datarepr = self.color + "New Connection!"
        print(datarepr)
        for watcher in watchers:
            watcher.transport.write((datarepr+'\n').encode())
        self.connections.add(self)

    def connectionLost(self, reason):
        datarepr = self.color + "Connection Lost!"
        print(datarepr)
        for watcher in watchers:
            watcher.transport.write((datarepr+'\n').encode())
        self.connections.discard(self)
        for connection in self.connections:
            reactor.callLater(0.1, connection.safeAbort)

    def dataReceived(self, data):
        datarepr = self.color + "Data: {}".format(repr(data))
        print(datarepr)
        for watcher in watchers:
            watcher.transport.write((datarepr+'\n').encode())
        for connection in self.connections:
            if connection != self:
                connection.transport.write(data)


class PeerFactory(Factory):

    def __init__(self, port):
        self.connections = set()
        self.port = port

    def buildProtocol(self, addr):
        return Peer(self.connections, self.port)



class Watcher(Protocol):
    def connectionMade(self):
        print("New Watcher!")
        watchers.add(self)

    def connectionLost(self, reason):
        print("Watcher Lost!")
        watchers.discard(self)


class WatcherFactory(Factory):
    def buildProtocol(self, addr):
        return Watcher()


if __name__ == '__main__':
    reactor.listenTCP(8200, WatcherFactory())
    for iport in range(8110, 8140):
        reactor.listenTCP(iport, PeerFactory(iport))

    reactor.run()
