# import socketserver
# from tcpserver.tcphandler import ReverseProxyHandler
#
#
#
# def main(argv):
#     with socketserver.TCPServer((HOST, PORT), ReverseProxyHandler) as server:
#         server.serve_forever()
#
#
# if __name__ == '__main__':
#     import sys
#
#     main(sys.argv[1:])

from tcpserver.server import MineRouterServer2
from utils.config import Config

HOST, PORT = "127.0.0.1", 25565


def main():
    Config(config={
        "127.0.0.1": ("127.0.0.1", 25569),
        "localhost": ("127.0.0.1", 25570),
        "192.168.1.107": ("127.0.0.1", 25570),
    })

    with MineRouterServer2(HOST, PORT) as mc:
        mc.serve_forever()


if __name__ == '__main__':
    main()
