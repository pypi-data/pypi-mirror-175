from __future__ import annotations
from typing import Optional, TypeVar, Type

from aslabs.config import Config
from aslabs.dependencies import DependenciesABC, ResolverABC


T = TypeVar("T")


class ConfigBaseResolver(ResolverABC):
    def __init__(self, prefix: str, file_path: Optional[str] = None, dotenv_file: Optional[str] = None) -> None:
        self._config = Config()\
            .add_env_variables(prefix)
        if file_path:
            self._config.add_file(file_path)
        if dotenv_file:
            self._config.add_dotenv(dotenv_file)

    def __call__(self, deps: DependenciesABC) -> T:
        return self._config

    @property
    def resolved_type(self) -> Type[T]:
        return Config


class ConfigResolver(ResolverABC):
    def __init__(self, config_type: type[T], key: str):
        self._config_type = config_type
        self._key = key

    def __call__(self, deps: DependenciesABC) -> T:
        config = deps.get(Config)
        return config.resolve(self._config_type, self._key)

    @property
    def resolved_type(self) -> Type[T]:
        return self._config_type
