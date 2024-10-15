from enum import StrEnum, auto
from functools import lru_cache
from os import environ
from tomllib import load
from typing import Type, TypeVar

from pydantic import BaseModel, SecretStr, field_validator

ConfigType = TypeVar("ConfigType", bound=BaseModel)


class LogRenderer(StrEnum):
    JSON = auto()
    CONSOLE = auto()


class BotConfig(BaseModel):
    token: SecretStr
    owners: list


class LogConfig(BaseModel):
    show_datetime: bool
    datetime_format: str
    show_debug_logs: bool
    time_in_utc: bool
    use_colors_in_console: bool
    renderer: LogRenderer

    @field_validator('renderer', mode="before")
    @classmethod
    def log_renderer_to_lower(cls, v: str):
        return v.lower()


class Config(BaseModel):
    bot: BotConfig


@lru_cache
def parse_config_file() -> dict:
    # Check if there's ENV variable that overrides config file path
    if environ.get('CONFIG_FILE_PATH') is not None:
        file_path = environ.get('CONFIG_FILE_PATH') # overriden config file name
    else:
        file_path = "config.toml" # default config file name

    if file_path is None:
        error = "Could not find settings file"
        raise ValueError(error)
    # Parse config as TOML
    with open(file_path, "rb") as file:
        config_data = load(file)
    return config_data


@lru_cache
def get_config(model: Type[ConfigType], root_key: str) -> ConfigType:
    config_dict = parse_config_file()
    if root_key not in config_dict:
        error = f"Key {root_key} not found"
        raise ValueError(error)
    return model.model_validate(config_dict[root_key])
