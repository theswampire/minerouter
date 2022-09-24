from typing import Dict, Tuple, Any


class Singleton:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Config(Singleton):
    config: Dict[str, Tuple[str, int]] | None = None

    def __init__(self, config: Dict[str, Tuple[str, int]]):
        Config.config = config

    @classmethod
    def get(cls, *args, **kwargs) -> Any:
        if cls.config is None:
            raise ValueError("Config not initialized")

        return cls.config.get(*args, **kwargs)
