import argparse
import json
from pathlib import Path
from typing import Dict, Tuple, Any, TypedDict
from urllib.parse import urlparse


class Singleton:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


UpstreamConfig = Dict[str, Tuple[str, int]]


class ConfigData(TypedDict):
    upstream_config: UpstreamConfig
    system_config: Dict[str, Any]


class Config(Singleton):
    config: ConfigData | None = None

    def __init__(self, file_config: ConfigData, cli_config: UpstreamConfig):
        config = file_config
        config["upstream_config"] = {**file_config.get("upstream_config", {}), **cli_config}
        type(self).config = config

    @classmethod
    def get_addr(cls, key: Any, default: Any | None = None) -> Any:
        if cls.config is None:
            raise ValueError("Config not initialized")
        return cls.config["upstream_config"].get(key, default)

    @classmethod
    def get_system_conf(cls, key: Any, default: Any | None = None) -> Any:
        if cls.config is None:
            raise ValueError("Config is not initialized")
        if "system_config" not in cls.config:
            return default
        return cls.config['system_config'].get(key, default)

    def __str__(self):
        return f"Config({self.config})"

    def __repr__(self):
        return self.__str__()


EmptyConfigData: ConfigData = {"upstream_config": {}, "system_config": {}}


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
                             "<upstream-port>'. ex: '-s mc2.example.com 10.0.8.2 25565'. Note: Use it multiple times "
                             "to define more servers. Overrides config-file")
    return parser.parse_args()


class ChooseType:
    def __new__(cls, *args, **kwargs):
        value = args[0]
        value: str
        if value.isdigit():
            return int(value)
        return value


def load_config_file(path: Path) -> ConfigData:
    if not path.exists():
        return EmptyConfigData
    with open(path, "r", encoding="UTF-8") as f:
        data = json.load(f)

    if not data:
        return EmptyConfigData
    if "upstream_config" not in data:
        return EmptyConfigData

    data["upstream_config"] = {domain: _split_addr(addr) for domain, addr in data["upstream_config"].items()}

    return data


def _split_addr(addr: str) -> Tuple[str, int]:
    url = urlparse(f"//{addr}")
    return url.hostname, url.port or 25565

