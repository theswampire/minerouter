from tcpserver.server import MineRouterServer
from utils.config import Config, parse_args, load_config_file, EmptyConfigData
from utils.logs import get_logger

log = get_logger(__name__)


def main():
    args = parse_args()

    cli_conf = {
        domain: tuple(addr) for domain, *addr in args.server
    } if args.server else EmptyConfigData["upstream_config"]

    Config(file_config=load_config_file(args.config), cli_config=cli_conf)
    log.debug(Config.instance)

    with MineRouterServer(args.host, args.port) as mc:
        mc.serve_forever()


if __name__ == '__main__':
    main()
