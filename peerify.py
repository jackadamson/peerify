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
        print(self.color + "New Connection!")
        self.connections.add(self)

    def connectionLost(self, reason):
        print(self.color + "Connection Lost!")
        self.connections.discard(self)
        for connection in self.connections:
            reactor.callLater(0.1, connection.safeAbort)

    def dataReceived(self, data):
        print(self.color + "Data: {}".format(repr(data)))
        for connection in self.connections:
            if connection != self:
                connection.transport.write(data)


class PeerFactory(Factory):

    def __init__(self, port):
        self.connections = set()
        self.port = port

    def buildProtocol(self, addr):
        return Peer(self.connections, self.port)


if __name__ == '__main__':
    for iport in range(8110, 8140):
        reactor.listenTCP(iport, PeerFactory(iport))

    reactor.run()
