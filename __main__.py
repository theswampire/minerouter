import socketserver
from tcpserver.tcphandler import ReverseProxyHandler

HOST, PORT = "127.0.0.1", 25565


def main(argv):
    with socketserver.TCPServer((HOST, PORT), ReverseProxyHandler) as server:
        server.serve_forever()


if __name__ == '__main__':
    import sys

    main(sys.argv[1:])
