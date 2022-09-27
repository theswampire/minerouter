import argparse
from pathlib import Path
from typing import Dict, Tuple, Any, TypedDict


class Singleton:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class ConfigData(TypedDict):
    upstream_config: Dict[str, Tuple[str, int]]
    system_config: Dict[str, Any]


class Config(Singleton):
    config: ConfigData | None = None

    def __init__(self, config: ConfigData):
        Config.config = config

    @classmethod
    def get_addr(cls, *args, **kwargs) -> Any:
        if cls.config is None:
            raise ValueError("Config not initialized")
        return cls.config["upstream_config"].get(*args, **kwargs)

    @classmethod
    def get_system_conf(cls, *args, **kwargs) -> Any:
        if cls.config is None:
            raise ValueError("Config is not initialized")
        return cls.config['system_config'].get(*args, **kwargs)


def parse_args():
    parser = argparse.ArgumentParser(usage="Reverse proxy your Minecraft Servers")
    parser.add_argument("-H", "--host", default="0.0.0.0", type=str,
                        help="IP-Address to listen to, defaults to 0.0.0.0")
    parser.add_argument("-p", "--port", default=25565, type=int, help="Port to listen to, defaults to 25565")
    parser.add_argument("-c", "--config", default=Path("config.json"), type=Path,
                        help="Path to configuration file, defaults to ./config.json")
    parser.add_argument("-s", "--server", nargs=3, metavar=("DOMAIN", "IP", "PORT"), action="append", default=None,
                        type=ChooseType,
                        help="Define your upstream servers using the CLI: '-s <server-domain> <upstream-ip> "
                             "<upstream-port>'. ex: '-s mc2.example.com 10.0.8.2 25565'. Note: Overrides config-file")
    return parser.parse_args()


class ChooseType:
    def __new__(cls, *args, **kwargs):
        value = args[0]
        value: str
        if value.isdigit():
            return int(value)
        return value
