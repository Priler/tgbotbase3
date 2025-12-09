from pathlib import Path
from typing import Optional, Union

from fluent.runtime import FluentLocalization, FluentResourceLoader


def get_fluent_localization(
    locale: str = "en",
    locales_dir: Optional[Union[str, Path]] = None,
) -> FluentLocalization:
    """
    Load Fluent localization files.

    Args:
        locale: Locale code (e.g., 'en', 'ru')
        locales_dir: Path to localization directory

    Returns:
        Configured FluentLocalization instance

    Raises:
        FileNotFoundError: If localization directory or files not found
    """
    if locales_dir is None:
        locales_dir = Path(__file__).parent / "l10n"
    elif isinstance(locales_dir, str):
        locales_dir = Path(locales_dir)

    if not locales_dir.exists():
        raise FileNotFoundError(f"Localization directory not found: {locales_dir}")

    if not locales_dir.is_dir():
        raise NotADirectoryError(f"'{locales_dir}' is not a directory")

    locale_file = locales_dir / f"{locale}.ftl"
    if not locale_file.exists():
        locale_file = locales_dir / "locale.ftl"

    if not locale_file.exists():
        raise FileNotFoundError(
            f"No locale file found for '{locale}' in {locales_dir}"
        )

    loader = FluentResourceLoader(str(locale_file.absolute()))

    return FluentLocalization(
        locales=[locale],
        resource_ids=[str(locale_file.absolute())],
        resource_loader=loader,
    )
