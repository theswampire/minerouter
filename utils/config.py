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
