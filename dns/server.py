import SocketServer
import dnslib as dns # external library for parsing/building DNS wire-format packets

HOST = "localhost"
PORT = 53

class DomainNameQuery(object):
    """
    Encapsulation for the domain name query
    """

    def __init__(self, query):
        self._query = query

    def __str__(self):
        return "<{name}: {msg}>".format(name=self.__class__.__name__, msg=self.message)

    @property
    def message(self):
        return dns.DNSRecord.parse(self._query)

        
class DomainNameSystemServer(SocketServer.BaseRequestHandler):
    """
    Receives domain name lookup requests
    """

    def handle(self):
        """
        Return IP-address for requested domain
        """

        raw_query, socket = self.request
        query = DomainNameQuery(raw_query)
        print query
        socket.sendto("\x00", self.client_address)


if __name__ == "__main__":
    server = SocketServer.UDPServer((HOST, PORT), DomainNameSystemServer)
    server.serve_forever()