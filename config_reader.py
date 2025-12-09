from enum import StrEnum, auto
from functools import lru_cache
from os import environ
from pathlib import Path
from tomllib import load
from typing import Optional, Type, TypeVar

from pydantic import BaseModel, SecretStr, field_validator


ConfigType = TypeVar("ConfigType", bound=BaseModel)


class LogRenderer(StrEnum):
    JSON = auto()
    CONSOLE = auto()


class BotConfig(BaseModel):
    """Bot configuration."""
    token: SecretStr
    owners: list[int] = []

    @field_validator("owners", mode="before")
    @classmethod
    def parse_owners(cls, v):
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        return v


class LogConfig(BaseModel):
    """Logging configuration."""
    show_datetime: bool = True
    datetime_format: str = "%Y-%m-%d %H:%M:%S"
    show_debug_logs: bool = False
    time_in_utc: bool = False
    use_colors_in_console: bool = True
    renderer: LogRenderer = LogRenderer.CONSOLE

    @field_validator("renderer", mode="before")
    @classmethod
    def log_renderer_to_lower(cls, v: str) -> str:
        if isinstance(v, str):
            return v.lower()
        return v


class L10nConfig(BaseModel):
    """Localization configuration."""
    default_locale: str = "en"
    fallback_locale: str = "en"
    locales_path: str = "l10n"


class Config(BaseModel):
    """Root configuration model."""
    bot: BotConfig
    logs: LogConfig = LogConfig()
    localization: L10nConfig = L10nConfig()


def get_config_path() -> Path:
    """Get configuration file path from environment or default."""
    env_path = environ.get("CONFIG_FILE_PATH")
    if env_path:
        return Path(env_path)
    return Path("config.toml")


@lru_cache
def parse_config_file() -> dict:
    """Parse TOML configuration file."""
    file_path = get_config_path()

    if not file_path.exists():
        raise FileNotFoundError(f"Config file not found: {file_path}")

    with open(file_path, "rb") as file:
        return load(file)


@lru_cache
def get_config(model: Type[ConfigType], root_key: str) -> ConfigType:
    """
    Get typed configuration section.

    Args:
        model: Pydantic model class for validation
        root_key: Top-level key in config file

    Returns:
        Validated configuration object

    Raises:
        KeyError: If root_key not found in config
    """
    config_dict = parse_config_file()

    if root_key not in config_dict:
        raise KeyError(f"Configuration key '{root_key}' not found in config file")

    return model.model_validate(config_dict[root_key])


def get_env_or_config(
    env_var: str,
    config_model: Type[ConfigType],
    config_key: str,
    config_attr: str,
) -> Optional[str]:
    """
    Get value from environment variable or config file.

    Environment variables take precedence over config file values.
    """
    env_value = environ.get(env_var)
    if env_value is not None:
        return env_value

    try:
        config = get_config(model=config_model, root_key=config_key)
        return getattr(config, config_attr, None)
    except (KeyError, FileNotFoundError):
        return None
