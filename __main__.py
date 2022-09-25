from tcpserver.server import MineRouterServer
from utils.config import Config

HOST, PORT = "0.0.0.0", 25565


def main():
    Config(config={
        "upstream_config": {
            "127.0.0.1": ("127.0.0.1", 25569),
            "localhost": ("127.0.0.1", 25570),
        },
        'system_config': {
            "COMPLETE_PACKETS": False
        }
    })

    with MineRouterServer(HOST, PORT) as mc:
        mc.serve_forever()


if __name__ == '__main__':
    main()
