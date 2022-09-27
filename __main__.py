from tcpserver.server import MineRouterServer
from utils.config import Config, parse_args


def main():
    args = parse_args()
    print(args)

    Config(config={
        "upstream_config": {
            "127.0.0.1": ("127.0.0.1", 25569),
            "localhost": ("127.0.0.1", 25570),
            **{domain: tuple(addr) for domain, *addr in args.server}
        },
        'system_config': {
            "COMPLETE_PACKETS": False
        }
    })
    print(Config.config)

    with MineRouterServer(args.host, args.port) as mc:
        mc.serve_forever()


if __name__ == '__main__':
    main()
