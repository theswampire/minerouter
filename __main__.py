from tcpserver.server import MineRouterServer2
from utils.config import Config

HOST, PORT = "127.0.0.1", 25565


def main():
    Config(config={
        "127.0.0.1": ("127.0.0.1", 25569),
        "localhost": ("127.0.0.1", 25570),
    })

    with MineRouterServer2(HOST, PORT) as mc:
        mc.serve_forever()


if __name__ == '__main__':
    main()
